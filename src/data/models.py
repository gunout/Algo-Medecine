from dataclasses import dataclass, asdict
from typing import List, Dict, Any, Optional
from datetime import datetime
from enum import Enum

class HealthStatus(Enum):
    CRITICAL = "CRITIQUE"
    SERIOUS = "GRAVE"
    MODERATE = "MODÉRÉ"
    STABLE = "STABLE"
    EXCELLENT = "EXCELLENT"

class TreatmentStatus(Enum):
    RECOMMENDED = "RECOMMANDÉ"
    PRESCRIBED = "PRESCRIT"
    ADMINISTERED = "ADMINISTRÉ"
    COMPLETED = "TERMINÉ"
    CANCELLED = "ANNULÉ"

@dataclass
class Patient:
    """Modèle de données pour un patient"""
    id: str
    first_name: str
    last_name: str
    age: int
    gender: str
    pathology: str
    symptoms: List[str]
    comorbidities: List[str]
    created_at: str
    updated_at: str
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Patient':
        return cls(**data)

@dataclass
class Treatment:
    """Modèle de données pour un traitement"""
    id: str
    patient_id: str
    name: str
    dosage: str
    frequency: str
    duration_days: int
    status: TreatmentStatus
    effectiveness_score: float
    start_date: str
    end_date: Optional[str] = None
    notes: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        data['status'] = self.status.value
        return data
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Treatment':
        data['status'] = TreatmentStatus(data['status'])
        return cls(**data)

@dataclass
class Analysis:
    """Modèle de données pour une analyse médicale"""
    id: str
    patient_id: str
    pyramid_structure: Dict[str, Any]
    health_metrics: Dict[str, float]
    predictions: Dict[str, Any]
    recommendations: List[str]
    confidence_score: float
    created_at: str
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Analysis':
        return cls(**data)

@dataclass
class FollowUp:
    """Modèle de données pour le suivi"""
    id: str
    patient_id: str
    day_number: int
    health_status: HealthStatus
    symptoms: List[str]
    treatment_adherence: float
    notes: str
    created_at: str
    
    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        data['health_status'] = self.health_status.value
        return data
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'FollowUp':
        data['health_status'] = HealthStatus(data['health_status'])
        return cls(**data)

@dataclass
class MedicalHistory:
    """Historique médical complet d'un patient"""
    patient: Patient
    analyses: List[Analysis]
    treatments: List[Treatment]
    follow_ups: List[FollowUp]
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'patient': self.patient.to_dict(),
            'analyses': [analysis.to_dict() for analysis in self.analyses],
            'treatments': [treatment.to_dict() for treatment in self.treatments],
            'follow_ups': [follow_up.to_dict() for follow_up in self.follow_ups]
        }