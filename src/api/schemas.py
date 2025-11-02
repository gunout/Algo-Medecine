from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from datetime import datetime
from enum import Enum

class HealthStatus(str, Enum):
    CRITICAL = "CRITIQUE"
    SERIOUS = "GRAVE"
    MODERATE = "MODÉRÉ"
    STABLE = "STABLE"
    EXCELLENT = "EXCELLENT"

class TreatmentStatus(str, Enum):
    RECOMMENDED = "RECOMMANDÉ"
    PRESCRIBED = "PRESCRIT"
    ADMINISTERED = "ADMINISTRÉ"
    COMPLETED = "TERMINÉ"

# Schémas de requête
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

class CohortAnalysisRequest(BaseModel):
    patients: List[PatientAnalysisRequest]

class FollowUpRequest(BaseModel):
    patient_id: str
    day_number: int
    health_status: str
    symptoms: List[str]
    notes: Optional[str] = ""

# Schémas de réponse
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
    evolution_predite: List[Dict[str, Any]]
    recommandations_specifiques: List[str]

class HealthConditionResponse(BaseModel):
    pyramide_sante: Dict[str, Any]
    score_gravite: float
    potentiel_retablissement: float
    resilience_patient: float
    harmonie_biologique: float
    etat_sante: str
    facteurs_aggravants: List[str]
    indicateurs_favorables: List[str]

class CarePlanResponse(BaseModel):
    traitement_principal: str
    protocole_applique: str
    duree_traitement_recommandee: int
    posologie_recommandee: str
    suivi_recommande: List[Dict[str, Any]]
    criteres_amelioration: List[str]
    actions_immediates: List[str]
    contingence: Dict[str, Any]
    recommandations_complementaires: List[str]

class MedicalAnalysisResponse(BaseModel):
    patient_id: str
    timestamp_analyse: str
    condition_actuelle: HealthConditionResponse
    traitements_recommandes: List[TreatmentResponse]
    prediction_retablissement: PredictionResponse
    plan_soins_personnalise: CarePlanResponse
    facteurs_pronostiques: Dict[str, Any]
    recommandations_suivi: List[str]
    score_confiance_global: float
    avertissements: List[str]

class PatientResponse(BaseModel):
    id: str
    data: Dict[str, Any]
    created_at: str
    updated_at: str

class AnalysisResponse(BaseModel):
    id: str
    patient_id: str
    analysis_data: Dict[str, Any]
    pyramid_structure: Dict[str, Any]
    predictions: Dict[str, Any]
    created_at: str

class FollowUpResponse(BaseModel):
    id: str
    patient_id: str
    day_number: int
    health_status: str
    symptoms: List[str]
    notes: str
    created_at: str

class StatisticsResponse(BaseModel):
    total_patients: int
    total_analyses: int
    common_pathologies: List[Dict[str, Any]]
    recent_analyses: List[Dict[str, Any]]
    database_size: str

class HealthCheckResponse(BaseModel):
    status: str
    timestamp: str
    database: str
    algorithm: str
    total_patients: int

class ErrorResponse(BaseModel):
    detail: str
    error_code: Optional[str] = None
    timestamp: str

# Schémas pour les réponses d'API
class APIResponse(BaseModel):
    success: bool
    message: str
    data: Optional[Dict[str, Any]] = None
    timestamp: str

    @classmethod
    def success_response(cls, message: str, data: Dict[str, Any] = None):
        return cls(
            success=True,
            message=message,
            data=data,
            timestamp=datetime.now().isoformat()
        )

    @classmethod
    def error_response(cls, message: str):
        return cls(
            success=False,
            message=message,
            timestamp=datetime.now().isoformat()
        )