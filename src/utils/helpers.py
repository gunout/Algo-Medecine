import hashlib
from typing import Any, Dict
from datetime import datetime

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