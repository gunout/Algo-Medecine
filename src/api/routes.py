from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse  # ← AJOUT IMPORTANT
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import logging

from src.core.medical_predictions import AlgoVeriteMedical
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
    allow_origins=["*"],  # À restreindre en production
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

# Instances globales
algo_medical = AlgoVeriteMedical()

# Routes API
@app.get("/")
async def root():
    """Endpoint racine"""
    return {
        "message": "Algo Vérité Médical API",
        "version": "1.0.0",
        "status": "active"
    }

@app.get("/health")
async def health_check():
    """Health check de l'API"""
    return {
        "status": "healthy",
        "timestamp": "2024-01-01T00:00:00Z"  # Remplacer par datetime réel
    }

@app.post("/api/medical/analyze", response_model=MedicalAnalysisResponse)
async def analyze_patient(request: PatientAnalysisRequest):
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
        
        logger.info(f"Analyse terminée pour patient: {resultat['patient_id']}")
        
        return resultat
        
    except Exception as e:
        logger.error(f"Erreur lors de l'analyse: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erreur d'analyse: {str(e)}")

@app.get("/api/medical/patient/{patient_id}")
async def get_patient_analysis(patient_id: str):
    """
    Récupère l'analyse d'un patient précédemment analysé
    """
    try:
        if patient_id not in algo_medical.historique_patients:
            raise HTTPException(status_code=404, detail="Patient non trouvé")
        
        return algo_medical.historique_patients[patient_id]
        
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
async def analyze_cohort(patients: List[PatientAnalysisRequest]):
    """
    Analyse une cohorte de patients
    """
    try:
        patients_data = []
        for patient in patients:
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
    return {
        "patients_analyses": len(algo_medical.historique_patients),
        "algorithm_version": "1.0.0",
        "memory_usage": "OK",  # À implémenter avec psutil
        "database_status": "OK"
    }

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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=settings.API_HOST, port=settings.API_PORT)
