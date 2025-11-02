"""
Algo Vérité Médical - Système de recherche sanitaire et prédiction
"""

__version__ = "1.0.0"
__author__ = "Équipe Algo Vérité Médical"
__email__ = "contact@algo-verite-medical.com"

from src.core.algo_verite import AlgoVerite
from src.core.medical_predictions import AlgoVeriteMedical

__all__ = ["AlgoVerite", "AlgoVeriteMedical"]