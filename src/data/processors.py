import json
import pandas as pd
import numpy as np
from typing import Dict, List, Any, Optional
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class DataProcessor:
    """
    Processeur de données médicales
    """
    
    def __init__(self):
        self.encoders = {}
    
    def process_patient_data(self, raw_data: Dict[str, Any]) -> Dict[str, Any]:
        """Traite les données brutes d'un patient"""
        try:
            processed = {
                'id': raw_data.get('id', f"PAT_{datetime.now().strftime('%Y%m%d%H%M%S')}"),
                'demographics': self._extract_demographics(raw_data),
                'medical_info': self._extract_medical_info(raw_data),
                'symptoms': self._process_symptoms(raw_data.get('symptomes', [])),
                'risk_factors': self._assess_risk_factors(raw_data),
                'processed_at': datetime.now().isoformat()
            }
            
            return processed
            
        except Exception as e:
            logger.error(f"Erreur lors du traitement des données patient: {e}")
            raise
    
    def _extract_demographics(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Extrait les données démographiques"""
        profil = data.get('profil', {})
        return {
            'age': profil.get('age', 0),
            'age_group': self._get_age_group(profil.get('age', 0)),
            'comorbidities_count': profil.get('comorbidities', 0),
            'immunity_level': profil.get('immunity_level', 0.7)
        }
    
    def _get_age_group(self, age: int) -> str:
        """Détermine le groupe d'âge"""
        if age <= 25:
            return 'JEUNE'
        elif age <= 60:
            return 'ADULTE'
        else:
            return 'SENIOR'
    
    def _extract_medical_info(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Extrait les informations médicales"""
        return {
            'pathology': data.get('pathologie', ''),
            'symptom_count': len(data.get('symptomes', [])),
            'severity_indicators': self._extract_severity_indicators(data.get('symptomes', []))
        }
    
    def _extract_severity_indicators(self, symptoms: List[str]) -> List[str]:
        """Extrait les indicateurs de sévérité"""
        severe_indicators = []
        severe_symptoms = {'DYSPNÉE_SEVERE', 'FIÈVRE_ÉLEVÉE', 'DOULEUR_THORACIQUE'}
        
        for symptom in symptoms:
            if symptom in severe_symptoms:
                severe_indicators.append(symptom)
        
        return severe_indicators
    
    def _process_symptoms(self, symptoms: List[str]) -> Dict[str, Any]:
        """Traite la liste des symptômes"""
        symptom_categories = {
            'respiratory': ['TOUX', 'DYSPNÉE', 'EXPECTORATION'],
            'fever': ['FIÈVRE', 'FIÈVRE_ÉLEVÉE', 'FIÈVRE_LEGERE'],
            'pain': ['DOULEURS_MUSCULAIRES', 'CEPHALÉE', 'DOULEUR_THORACIQUE'],
            'general': ['FATIGUE', 'ANOSMIE', 'NAUSÉE']
        }
        
        categorized = {category: [] for category in symptom_categories.keys()}
        
        for symptom in symptoms:
            for category, category_symptoms in symptom_categories.items():
                if symptom in category_symptoms:
                    categorized[category].append(symptom)
                    break
        
        return {
            'all_symptoms': symptoms,
            'categorized_symptoms': categorized,
            'symptom_diversity_score': self._calculate_symptom_diversity(symptoms),
            'severity_score': self._calculate_symptom_severity(symptoms)
        }
    
    def _calculate_symptom_diversity(self, symptoms: List[str]) -> float:
        """Calcule le score de diversité des symptômes"""
        if not symptoms:
            return 0.0
        
        categories_represented = sum(1 for category_symptoms in self._process_symptoms(symptoms)['categorized_symptoms'].values() if category_symptoms)
        total_categories = 4  # respiratory, fever, pain, general
        
        return categories_represented / total_categories
    
    def _calculate_symptom_severity(self, symptoms: List[str]) -> float:
        """Calcule le score de sévérité des symptômes"""
        severity_weights = {
            'FIÈVRE_LEGERE': 0.3,
            'TOUX': 0.3,
            'FATIGUE': 0.2,
            'FIÈVRE': 0.5,
            'DYSPNÉE': 0.7,
            'FIÈVRE_ÉLEVÉE': 0.8,
            'DYSPNÉE_SEVERE': 0.9,
            'DOULEUR_THORACIQUE': 0.8
        }
        
        if not symptoms:
            return 0.0
        
        total_severity = sum(severity_weights.get(symptom, 0.3) for symptom in symptoms)
        return min(total_severity / len(symptoms), 1.0)
    
    def _assess_risk_factors(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Évalue les facteurs de risque"""
        profil = data.get('profil', {})
        age = profil.get('age', 0)
        comorbidities = profil.get('comorbidities', 0)
        immunity = profil.get('immunity_level', 0.7)
        
        risk_factors = []
        risk_score = 0.0
        
        # Facteur âge
        if age >= 65:
            risk_factors.append("Âge avancé")
            risk_score += 0.3
        elif age <= 12:
            risk_factors.append("Âge pédiatrique")
            risk_score += 0.2
        
        # Facteur comorbidités
        if comorbidities >= 3:
            risk_factors.append("Multiples comorbidités")
            risk_score += 0.4
        elif comorbidities >= 1:
            risk_factors.append("Comorbidités présentes")
            risk_score += 0.2
        
        # Facteur immunité
        if immunity <= 0.4:
            risk_factors.append("Immunodépression")
            risk_score += 0.3
        
        # Symptômes sévères
        severe_symptoms = self._extract_severity_indicators(data.get('symptomes', []))
        if severe_symptoms:
            risk_factors.append("Symptômes sévères présents")
            risk_score += 0.3
        
        return {
            'factors': risk_factors,
            'score': min(risk_score, 1.0),
            'level': self._get_risk_level(risk_score)
        }
    
    def _get_risk_level(self, score: float) -> str:
        """Détermine le niveau de risque"""
        if score >= 0.7:
            return "ÉLEVÉ"
        elif score >= 0.4:
            return "MODÉRÉ"
        else:
            return "FAIBLE"
    
    def process_pyramid_data(self, pyramid_structure: Dict[str, Any]) -> Dict[str, Any]:
        """Traite les données de la pyramide"""
        try:
            base = pyramid_structure.get('base', [])
            upper = pyramid_structure.get('superieure', [])
            lower = pyramid_structure.get('inferieure', [])
            
            return {
                'base_metrics': self._analyze_base(base),
                'upper_metrics': self._analyze_levels(upper, "upper"),
                'lower_metrics': self._analyze_levels(lower, "lower"),
                'structural_metrics': self._calculate_structural_metrics(pyramid_structure),
                'harmony_score': self._calculate_harmony_score(pyramid_structure)
            }
            
        except Exception as e:
            logger.error(f"Erreur lors du traitement des données pyramidales: {e}")
            raise
    
    def _analyze_base(self, base: List[int]) -> Dict[str, Any]:
        """Analyse la base de la pyramide"""
        if not base:
            return {}
        
        return {
            'length': len(base),
            'mean': float(np.mean(base)),
            'std': float(np.std(base)),
            'min': min(base),
            'max': max(base),
            'sum': sum(base),
            'entropy': self._calculate_entropy(base)
        }
    
    def _analyze_levels(self, levels: List[List[int]], level_type: str) -> Dict[str, Any]:
        """Analyse les niveaux de la pyramide"""
        if not levels:
            return {}
        
        all_values = [value for level in levels for value in level]
        
        return {
            'level_count': len(levels),
            'total_values': len(all_values),
            'mean_values_per_level': len(all_values) / len(levels) if levels else 0,
            'overall_mean': float(np.mean(all_values)) if all_values else 0,
            'overall_std': float(np.std(all_values)) if all_values else 0,
            'convergence_speed': self._calculate_convergence_speed(levels, level_type)
        }
    
    def _calculate_entropy(self, sequence: List[int]) -> float:
        """Calcule l'entropie d'une séquence"""
        if not sequence:
            return 0.0
        
        # Normaliser la séquence
        seq_array = np.array(sequence, dtype=float)
        if np.sum(seq_array) == 0:
            return 0.0
        
        probabilities = seq_array / np.sum(seq_array)
        probabilities = probabilities[probabilities > 0]  # Éviter log(0)
        
        return float(-np.sum(probabilities * np.log(probabilities)))
    
    def _calculate_convergence_speed(self, levels: List[List[int]], level_type: str) -> float:
        """Calcule la vitesse de convergence"""
        if not levels:
            return 0.0
        
        if level_type == "upper":
            # Pour la partie supérieure, on regarde comment les valeurs augmentent
            level_sizes = [len(level) for level in levels]
            return 1.0 - (min(level_sizes) / max(level_sizes)) if max(level_sizes) > 0 else 0.0
        else:
            # Pour la partie inférieure, on regarde comment les valeurs convergent
            final_level = levels[-1]
            if len(final_level) == 1:
                return 1.0  # Convergence parfaite
            else:
                variation = np.std(final_level) / (np.mean(final_level) if np.mean(final_level) != 0 else 1)
                return max(0, 1 - variation)
    
    def _calculate_structural_metrics(self, pyramid: Dict[str, Any]) -> Dict[str, Any]:
        """Calcule les métriques structurelles"""
        upper_levels = len(pyramid.get('superieure', []))
        lower_levels = len(pyramid.get('inferieure', []))
        base_length = len(pyramid.get('base', []))
        
        symmetry = 1.0 - (abs(upper_levels - lower_levels) / max(upper_levels, lower_levels, 1))
        balance = upper_levels / (upper_levels + lower_levels) if (upper_levels + lower_levels) > 0 else 0.5
        
        return {
            'symmetry_score': symmetry,
            'balance_ratio': balance,
            'total_levels': upper_levels + lower_levels,
            'structure_complexity': (upper_levels + lower_levels) / base_length if base_length > 0 else 0
        }
    
    def _calculate_harmony_score(self, pyramid: Dict[str, Any]) -> float:
        """Calcule le score d'harmonie global"""
        structural_metrics = self._calculate_structural_metrics(pyramid)
        
        scores = [
            structural_metrics['symmetry_score'],
            self._calculate_base_harmony(pyramid.get('base', [])),
            self._calculate_level_harmony(pyramid)
        ]
        
        return float(np.mean([s for s in scores if s is not None]))
    
    def _calculate_base_harmony(self, base: List[int]) -> float:
        """Calcule l'harmonie de la base"""
        if len(base) < 2:
            return 0.5
        
        # Vérifier les progressions arithmétiques ou géométriques
        differences = [base[i] - base[i-1] for i in range(1, len(base))]
        if len(set(differences)) == 1:
            return 0.9  # Progression arithmétique parfaite
        
        ratios = [base[i] / base[i-1] for i in range(1, len(base)) if base[i-1] != 0]
        if ratios and len(set(round(r, 1) for r in ratios)) == 1:
            return 0.8  # Progression géométrique
        
        return 0.5  # Aucun pattern détecté
    
    def _calculate_level_harmony(self, pyramid: Dict[str, Any]) -> float:
        """Calcule l'harmonie entre les niveaux"""
        upper = pyramid.get('superieure', [])
        lower = pyramid.get('inferieure', [])
        
        if not upper or not lower:
            return 0.5
        
        # Comparer le sommet de la partie supérieure et la base de la partie inférieure
        upper_top = upper[0][0] if upper[0] else 0
        lower_base = lower[-1][0] if lower[-1] else 0
        
        if upper_top == 0 or lower_base == 0:
            return 0.5
        
        ratio = min(upper_top, lower_base) / max(upper_top, lower_base)
        # Plus proche de 1, meilleure l'harmonie
        return 1.0 - abs(ratio - 1.0)

class MedicalDataEncoder:
    """
    Encodeur de données médicales pour la sérialisation
    """
    
    @staticmethod
    def encode_patient_for_storage(patient_data: Dict[str, Any]) -> str:
        """Encode les données patient pour le stockage"""
        try:
            # Nettoyer et structurer les données
            encoded = {
                'metadata': {
                    'version': '1.0',
                    'encoded_at': datetime.now().isoformat(),
                    'data_type': 'patient'
                },
                'patient': MedicalDataEncoder._clean_patient_data(patient_data)
            }
            
            return json.dumps(encoded, ensure_ascii=False)
            
        except Exception as e:
            logger.error(f"Erreur lors de l'encodage des données patient: {e}")
            raise
    
    @staticmethod
    def decode_patient_from_storage(encoded_data: str) -> Dict[str, Any]:
        """Décode les données patient depuis le stockage"""
        try:
            data = json.loads(encoded_data)
            return data.get('patient', {})
        except Exception as e:
            logger.error(f"Erreur lors du décodage des données patient: {e}")
            return {}
    
    @staticmethod
    def _clean_patient_data(data: Dict[str, Any]) -> Dict[str, Any]:
        """Nettoie et structure les données patient"""
        cleaned = data.copy()
        
        # Standardiser les champs
        if 'profil' in cleaned:
            cleaned['profile'] = cleaned.pop('profil')
        
        if 'symptomes' in cleaned:
            cleaned['symptoms'] = [s.upper() for s in cleaned.pop('symptomes')]
        
        # Ajouter des métadonnées
        cleaned['processed_at'] = datetime.now().isoformat()
        cleaned['data_version'] = '1.0'
        
        return cleaned
    
    @staticmethod
    def encode_analysis_for_api(analysis_data: Dict[str, Any]) -> Dict[str, Any]:
        """Encode les données d'analyse pour l'API"""
        try:
            # Structure standardisée pour l'API
            encoded = {
                'analysis_id': analysis_data.get('patient_id', 'UNKNOWN'),
                'timestamp': analysis_data.get('timestamp_analyse', datetime.now().isoformat()),
                'health_assessment': MedicalDataEncoder._extract_health_assessment(analysis_data),
                'predictions': MedicalDataEncoder._extract_predictions(analysis_data),
                'recommendations': MedicalDataEncoder._extract_recommendations(analysis_data),
                'confidence_metrics': MedicalDataEncoder._extract_confidence_metrics(analysis_data)
            }
            
            return encoded
            
        except Exception as e:
            logger.error(f"Erreur lors de l'encodage pour l'API: {e}")
            return {}
    
    @staticmethod
    def _extract_health_assessment(analysis_data: Dict[str, Any]) -> Dict[str, Any]:
        """Extrait l'évaluation de santé"""
        condition = analysis_data.get('condition_actuelle', {})
        return {
            'severity_score': condition.get('score_gravite', 0.5),
            'recovery_potential': condition.get('potentiel_retablissement', 0.5),
            'resilience': condition.get('resilience_patient', 0.5),
            'biological_harmony': condition.get('harmonie_biologique', 0.5),
            'health_status': getattr(condition.get('etat_sante'), 'label', 'INCONNU')
        }
    
    @staticmethod
    def _extract_predictions(analysis_data: Dict[str, Any]) -> Dict[str, Any]:
        """Extrait les prédictions"""
        predictions = analysis_data.get('prediction_retablissement', {})
        return {
            'illness_duration_days': predictions.get('duree_maladie_predite', 7),
            'recovery_date': predictions.get('date_retablissement_predite', ''),
            'success_probability': predictions.get('probabilite_succes', 0.5),
            'confidence_level': predictions.get('niveau_confiance', 0.5)
        }
    
    @staticmethod
    def _extract_recommendations(analysis_data: Dict[str, Any]) -> Dict[str, Any]:
        """Extrait les recommandations"""
        treatments = analysis_data.get('traitements_recommandes', [])
        care_plan = analysis_data.get('plan_soins_personnalise', {})
        
        return {
            'treatments': [
                {
                    'name': t.get('nom', ''),
                    'score': t.get('score_global', 0),
                    'protocol': t.get('protocole', '')
                } for t in treatments
            ],
            'care_plan': {
                'main_treatment': care_plan.get('traitement_principal', ''),
                'duration_days': care_plan.get('duree_traitement_recommandee', 7),
                'immediate_actions': care_plan.get('actions_immediates', [])
            }
        }
    
    @staticmethod
    def _extract_confidence_metrics(analysis_data: Dict[str, Any]) -> Dict[str, Any]:
        """Extrait les métriques de confiance"""
        return {
            'global_confidence': analysis_data.get('score_confiance_global', 0.5),
            'factors_count': len(analysis_data.get('prediction_retablissement', {}).get('facteurs_favorables', [])),
            'risks_count': len(analysis_data.get('prediction_retablissement', {}).get('risques_identifies', [])),
            'warnings_count': len(analysis_data.get('avertissements', []))
        }