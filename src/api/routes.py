from fastapi import FastAPI, HTTPException, Depends, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import logging
import json
from datetime import datetime

from src.core.medical_predictions import AlgoVeriteMedical
from src.data.database import DatabaseManager
from src.data.processors import DataProcessor, MedicalDataEncoder
from src.utils.config import get_settings
from src.utils.logger import get_logger

# Configuration
settings = get_settings()
logger = get_logger("api")

# Application FastAPI
app = FastAPI(
    title="Algo Vérité Médical API",
    description="Système de recherche sanitaire et prédiction de rétablissement",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Modèles de données
class SymptomModel(BaseModel):
    nom: str
    intensite: Optional[str] = "MODEREE"

class PatientProfileModel(BaseModel):
    age: int
    age_group: Optional[str] = None
    comorbidities: int = 0
    immunity_level: float = 0.7
    poids: Optional[float] = None
    taille: Optional[float] = None

class PatientAnalysisRequest(BaseModel):
    id: Optional[str] = None
    pathologie: str
    symptomes: List[str]
    profil: PatientProfileModel

class TreatmentResponse(BaseModel):
    nom: str
    protocole: str
    efficacite_base: float
    compatibilite_personnalisee: float
    score_global: float
    delai_action_attendu: int
    indications: List[str]

class PredictionResponse(BaseModel):
    duree_maladie_predite: int
    date_retablissement_predite: str
    probabilite_succes: float
    niveau_confiance: float
    facteurs_favorables: List[str]
    risques_identifies: List[str]

class MedicalAnalysisResponse(BaseModel):
    patient_id: str
    timestamp_analyse: str
    condition_actuelle: Dict[str, Any]
    traitements_recommandes: List[TreatmentResponse]
    prediction_retablissement: PredictionResponse
    plan_soins_personnalise: Dict[str, Any]
    score_confiance_global: float

class CohortAnalysisRequest(BaseModel):
    patients: List[PatientAnalysisRequest]

class FollowUpRequest(BaseModel):
    patient_id: str
    day_number: int
    health_status: str
    symptoms: List[str]
    notes: Optional[str] = ""

# Instances globales
algo_medical = AlgoVeriteMedical()
db_manager = DatabaseManager()
data_processor = DataProcessor()

# Routes API
@app.get("/")
async def root():
    """Endpoint racine"""
    return {
        "message": "Algo Vérité Médical API",
        "version": "1.0.0",
        "status": "active",
        "timestamp": datetime.now().isoformat()
    }

@app.get("/health")
async def health_check():
    """Health check de l'API"""
    try:
        # Test de la base de données
        stats = db_manager.get_statistics()
        
        # Test de l'algorithme
        test_patient = {
            'pathologie': 'GRIPPE',
            'symptomes': ['FIÈVRE', 'TOUX'],
            'profil': {'age': 35, 'comorbidities': 0}
        }
        test_result = algo_medical.analyser_patient(test_patient)
        
        return {
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "database": "connected",
            "algorithm": "operational",
            "total_patients": stats.get('total_patients', 0)
        }
        
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return {
            "status": "unhealthy",
            "timestamp": datetime.now().isoformat(),
            "error": str(e)
        }

@app.post("/api/medical/analyze", response_model=MedicalAnalysisResponse)
async def analyze_patient(request: PatientAnalysisRequest, background_tasks: BackgroundTasks = None):
    """
    Analyse un patient et prédit son rétablissement
    """
    try:
        logger.info(f"Analyse du patient pour pathologie: {request.pathologie}")
        
        # Conversion des données
        patient_data = {
            "id": request.id,
            "pathologie": request.pathologie,
            "symptomes": request.symptomes,
            "profil": request.profil.dict()
        }
        
        # Analyse avec l'algorithme
        resultat = algo_medical.analyser_patient(patient_data)
        
        # Sauvegarde en base de données (en arrière-plan si possible)
        if background_tasks:
            background_tasks.add_task(save_analysis_to_db, patient_data, resultat)
        else:
            save_analysis_to_db(patient_data, resultat)
        
        logger.info(f"Analyse terminée pour patient: {resultat['patient_id']}")
        
        return resultat
        
    except Exception as e:
        logger.error(f"Erreur lors de l'analyse: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erreur d'analyse: {str(e)}")

def save_analysis_to_db(patient_data: Dict, analysis_result: Dict):
    """Sauvegarde l'analyse en base de données"""
    try:
        patient_id = db_manager.save_patient(patient_data)
        db_manager.save_analysis(patient_id, analysis_result)
    except Exception as e:
        logger.error(f"Erreur lors de la sauvegarde en base: {e}")

@app.get("/api/medical/patient/{patient_id}")
async def get_patient_analysis(patient_id: str):
    """
    Récupère l'analyse d'un patient précédemment analysé
    """
    try:
        # Chercher d'abord dans l'historique en mémoire
        if patient_id in algo_medical.historique_patients:
            return algo_medical.historique_patients[patient_id]
        
        # Sinon chercher en base de données
        patient_data = db_manager.get_patient(patient_id)
        if not patient_data:
            raise HTTPException(status_code=404, detail="Patient non trouvé")
        
        analyses = db_manager.get_patient_analyses(patient_id)
        if not analyses:
            raise HTTPException(status_code=404, detail="Aucune analyse trouvée pour ce patient")
        
        # Retourner la dernière analyse
        latest_analysis = analyses[0]
        return {
            'patient_id': patient_id,
            'patient_data': patient_data['data'],
            'analysis': latest_analysis['analysis_data'],
            'timestamp': latest_analysis['created_at']
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erreur lors de la récupération: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erreur de récupération: {str(e)}")

@app.post("/api/medical/treatment/recommend")
async def recommend_treatments(request: PatientAnalysisRequest):
    """
    Recommande des traitements sans analyse complète
    """
    try:
        patient_data = {
            "pathologie": request.pathologie,
            "symptomes": request.symptomes,
            "profil": request.profil.dict()
        }
        
        # Analyse condition seulement
        analyse_sante = algo_medical._analyser_condition_patient(patient_data)
        traitements = algo_medical._rechercher_traitements_optimaux(patient_data, analyse_sante)
        
        return {
            "pathologie": request.pathologie,
            "traitements_recommandes": traitements,
            "condition_analyse": {
                "score_gravite": analyse_sante["score_gravite"],
                "etat_sante": analyse_sante["etat_sante"].label
            }
        }
        
    except Exception as e:
        logger.error(f"Erreur lors de la recommandation: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erreur de recommandation: {str(e)}")

@app.post("/api/medical/cohort/analyze")
async def analyze_cohort(request: CohortAnalysisRequest):
    """
    Analyse une cohorte de patients
    """
    try:
        patients_data = []
        for patient in request.patients:
            patients_data.append({
                "id": patient.id,
                "pathologie": patient.pathologie,
                "symptomes": patient.symptomes,
                "profil": patient.profil.dict()
            })
        
        resultat = algo_medical.analyser_cohorte(patients_data)
        
        return resultat
        
    except Exception as e:
        logger.error(f"Erreur lors de l'analyse de cohorte: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erreur d'analyse de cohorte: {str(e)}")

@app.get("/api/system/status")
async def system_status():
    """
    Statut du système et métriques
    """
    stats = db_manager.get_statistics()
    
    return {
        "patients_analyses": len(algo_medical.historique_patients),
        "database_patients": stats.get('total_patients', 0),
        "database_analyses": stats.get('total_analyses', 0),
        "algorithm_version": "1.0.0",
        "memory_usage": "OK",
        "database_status": "OK",
        "common_pathologies": stats.get('common_pathologies', [])
    }

@app.get("/api/patients")
async def list_patients(limit: int = 50, offset: int = 0):
    """
    Liste tous les patients
    """
    try:
        patients = db_manager.get_all_patients(limit=limit)
        return {
            "patients": patients[offset:offset+limit],
            "total": len(patients),
            "limit": limit,
            "offset": offset
        }
    except Exception as e:
        logger.error(f"Erreur lors de la liste des patients: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/follow-up")
async def add_follow_up(request: FollowUpRequest):
    """
    Ajoute une entrée de suivi pour un patient
    """
    try:
        db_manager.add_follow_up(
            patient_id=request.patient_id,
            day_number=request.day_number,
            health_status=request.health_status,
            symptoms=request.symptoms,
            notes=request.notes or ""
        )
        
        return {"status": "success", "message": "Suivi ajouté avec succès"}
        
    except Exception as e:
        logger.error(f"Erreur lors de l'ajout du suivi: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/follow-up/{patient_id}")
async def get_patient_follow_ups(patient_id: str):
    """
    Récupère le suivi d'un patient
    """
    try:
        follow_ups = db_manager.get_patient_follow_ups(patient_id)
        return {
            "patient_id": patient_id,
            "follow_ups": follow_ups,
            "total_entries": len(follow_ups)
        }
    except Exception as e:
        logger.error(f"Erreur lors de la récupération du suivi: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/statistics")
async def get_statistics():
    """
    Récupère les statistiques globales
    """
    try:
        stats = db_manager.get_statistics()
        return stats
    except Exception as e:
        logger.error(f"Erreur lors de la récupération des statistiques: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/export/data")
async def export_data():
    """
    Exporte les données au format JSON
    """
    try:
        export_path = f"export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        db_manager.export_data(export_path)
        
        return FileResponse(
            path=export_path,
            filename=export_path,
            media_type='application/json'
        )
    except Exception as e:
        logger.error(f"Erreur lors de l'export: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Gestion des erreurs
@app.exception_handler(500)
async def internal_server_error_handler(request, exc):
    logger.error(f"Erreur interne du serveur: {exc}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Erreur interne du serveur"}
    )

@app.exception_handler(404)
async def not_found_handler(request, exc):
    return JSONResponse(
        status_code=404,
        content={"detail": "Ressource non trouvée"}
    )

@app.exception_handler(422)
async def validation_error_handler(request, exc):
    return JSONResponse(
        status_code=422,
        content={"detail": "Données de requête invalides"}
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=settings.API_HOST, port=settings.API_PORT)