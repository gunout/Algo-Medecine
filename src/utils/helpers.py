import hashlib
from typing import Any, Dict, List
from datetime import datetime
import numpy as np

def generate_hash(data: str) -> str:
    """Génère un hash SHA-256 d'une chaîne de données"""
    return hashlib.sha256(data.encode()).hexdigest()

def safe_divide(numerator: float, denominator: float, default: float = 0.0) -> float:
    """Division sécurisée avec valeur par défaut si dénominateur nul"""
    if denominator == 0:
        return default
    return numerator / denominator

def normalize_value(value: float, min_val: float, max_val: float) -> float:
    """Normalise une valeur entre 0 et 1"""
    if max_val == min_val:
        return 0.5
    return (value - min_val) / (max_val - min_val)

def timestamp() -> str:
    """Retourne un timestamp formaté"""
    return datetime.now().isoformat()

def deep_merge(dict1: Dict, dict2: Dict) -> Dict:
    """Fusion récursive de deux dictionnaires"""
    result = dict1.copy()
    for key, value in dict2.items():
        if (key in result and isinstance(result[key], dict) 
            and isinstance(value, dict)):
            result[key] = deep_merge(result[key], value)
        else:
            result[key] = value
    return result

def calculate_percentage(part: float, total: float) -> float:
    """Calcule un pourcentage sécurisé"""
    if total == 0:
        return 0.0
    return (part / total) * 100

def format_duration(days: int) -> str:
    """Formate une durée en jours en texte lisible"""
    if days == 1:
        return "1 jour"
    elif days < 7:
        return f"{days} jours"
    elif days < 30:
        weeks = days // 7
        return f"{weeks} semaine{'s' if weeks > 1 else ''}"
    else:
        months = days // 30
        return f"{months} mois"

def validate_patient_data(data: Dict[str, Any]) -> List[str]:
    """Valide les données d'un patient et retourne les erreurs"""
    errors = []
    
    if 'pathologie' not in data or not data['pathologie']:
        errors.append("La pathologie est requise")
    
    if 'symptomes' not in data or not data['symptomes']:
        errors.append("Au moins un symptôme est requis")
    
    if 'profil' not in data:
        errors.append("Le profil patient est requis")
    else:
        profil = data['profil']
        if 'age' not in profil or profil['age'] <= 0:
            errors.append("L'âge doit être un nombre positif")
        if 'comorbidities' not in profil or profil['comorbidities'] < 0:
            errors.append("Le nombre de comorbidités ne peut pas être négatif")
    
    return errors

def calculate_age_group(age: int) -> str:
    """Calcule le groupe d'âge"""
    if age < 18:
        return "PÉDIATRIQUE"
    elif age < 65:
        return "ADULTE"
    else:
        return "SÉNIOR"

def generate_patient_id() -> str:
    """Génère un ID patient unique"""
    return f"PAT_{datetime.now().strftime('%Y%m%d%H%M%S')}_{hashlib.md5(str(datetime.now().timestamp()).encode()).hexdigest()[:6]}"

def safe_json_serialize(obj: Any) -> Any:
    """Sérialise un objet en JSON de façon sécurisée"""
    if isinstance(obj, (np.integer, np.floating)):
        return float(obj)
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
    elif hasattr(obj, '__dict__'):
        return obj.__dict__
    else:
        return str(obj)