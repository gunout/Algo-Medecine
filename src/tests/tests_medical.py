import pytest
import sys
import os

# Ajouter le chemin src
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.core.medical_predictions import AlgoVeriteMedical
from src.data.processors import DataProcessor

class TestMedicalPredictions:
    """Tests pour les prédictions médicales"""
    
    def setup_method(self):
        self.algo = AlgoVeriteMedical()
        self.processor = DataProcessor()
    
    def test_different_pathologies(self):
        """Test avec différentes pathologies"""
        test_cases = [
            {
                'pathologie': 'GRIPPE',
                'symptomes': ['FIÈVRE', 'TOUX', 'FATIGUE'],
                'profil': {'age': 25, 'comorbidities': 0}
            },
            {
                'pathologie': 'COVID', 
                'symptomes': ['FIÈVRE', 'TOUX', 'ANOSMIE'],
                'profil': {'age': 40, 'comorbidities': 1}
            },
            {
                'pathologie': 'BRONCHITE',
                'symptomes': ['TOUX', 'EXPECTORATION'],
                'profil': {'age': 55, 'comorbidities': 2}
            }
        ]
        
        for case in test_cases:
            result = self.algo.analyser_patient(case)
            
            # Vérifications de base
            assert 'patient_id' in result
            assert 'prediction_retablissement' in result
            assert 'traitements_recommandes' in result
            
            # Vérification des prédictions
            predictions = result['prediction_retablissement']
            assert predictions['duree_maladie_predite'] > 0
            assert 0 <= predictions['probabilite_succes'] <= 1
            assert 0 <= predictions['niveau_confiance'] <= 1
    
    def test_age_impact(self):
        """Test de l'impact de l'âge sur les prédictions"""
        young_patient = {
            'pathologie': 'GRIPPE',
            'symptomes': ['FIÈVRE', 'TOUX'],
            'profil': {'age': 20, 'comorbidities': 0}
        }
        
        senior_patient = {
            'pathologie': 'GRIPPE', 
            'symptomes': ['FIÈVRE', 'TOUX'],
            'profil': {'age': 70, 'comorbidities': 0}
        }
        
        young_result = self.algo.analyser_patient(young_patient)
        senior_result = self.algo.analyser_patient(senior_patient)
        
        # Le patient âgé devrait avoir une durée de maladie plus longue
        young_duration = young_result['prediction_retablissement']['duree_maladie_predite']
        senior_duration = senior_result['prediction_retablissement']['duree_maladie_predite']
        
        assert senior_duration >= young_duration
    
    def test_comorbidities_impact(self):
        """Test de l'impact des comorbidités"""
        healthy_patient = {
            'pathologie': 'GRIPPE',
            'symptomes': ['FIÈVRE', 'TOUX'],
            'profil': {'age': 40, 'comorbidities': 0}
        }
        
        comorbid_patient = {
            'pathologie': 'GRIPPE',
            'symptomes': ['FIÈVRE', 'TOUX'], 
            'profil': {'age': 40, 'comorbidities': 3}
        }
        
        healthy_result = self.algo.analyser_patient(healthy_patient)
        comorbid_result = self.algo.analyser_patient(comorbid_patient)
        
        # Le patient avec comorbidités devrait avoir une probabilité de succès plus faible
        healthy_prob = healthy_result['prediction_retablissement']['probabilite_succes']
        comorbid_prob = comorbid_result['prediction_retablissement']['probabilite_succes']
        
        assert comorbid_prob <= healthy_prob
    
    def test_symptom_severity_impact(self):
        """Test de l'impact de la sévérité des symptômes"""
        mild_case = {
            'pathologie': 'GRIPPE',
            'symptomes': ['FIÈVRE_LEGERE', 'TOUX'],
            'profil': {'age': 35, 'comorbidities': 0}
        }
        
        severe_case = {
            'pathologie': 'GRIPPE',
            'symptomes': ['FIÈVRE_ÉLEVÉE', 'DYSPNÉE_SEVERE'],
            'profil': {'age': 35, 'comorbidities': 0}
        }
        
        mild_result = self.algo.analyser_patient(mild_case)
        severe_result = self.algo.analyser_patient(severe_case)
        
        # Le cas sévère devrait avoir un score de gravité plus élevé
        mild_gravity = mild_result['condition_actuelle']['score_gravite']
        severe_gravity = severe_result['condition_actuelle']['score_gravite']
        
        assert severe_gravity > mild_gravity
    
    def test_treatment_relevance(self):
        """Test de la pertinence des traitements recommandés"""
        covid_patient = {
            'pathologie': 'COVID',
            'symptomes': ['FIÈVRE', 'TOUX', 'ANOSMIE'],
            'profil': {'age': 45, 'comorbidities': 1}
        }
        
        result = self.algo.analyser_patient(covid_patient)
        treatments = result['traitements_recommandes']
        
        # Vérifier qu'au moins un traitement est recommandé
        assert len(treatments) > 0
        
        # Vérifier la structure des traitements
        for treatment in treatments:
            assert 'nom' in treatment
            assert 'score_global' in treatment
            assert 'protocole' in treatment
            assert 0 <= treatment['score_global'] <= 1
    
    def test_cohort_analysis(self):
        """Test de l'analyse de cohorte"""
        patients = [
            {
                'pathologie': 'GRIPPE',
                'symptomes': ['FIÈVRE', 'TOUX'],
                'profil': {'age': 30, 'comorbidities': 0}
            },
            {
                'pathologie': 'GRIPPE',
                'symptomes': ['FIÈVRE', 'TOUX', 'FATIGUE'],
                'profil': {'age': 50, 'comorbidities': 1}
            }
        ]
        
        result = self.algo.analyser_cohorte(patients)
        
        assert 'cohorte_analyse' in result
        assert 'analyses_detaillees' in result
        assert 'recommandations_cohorte' in result
        
        cohort_stats = result['cohorte_analyse']
        assert cohort_stats['total_patients'] == 2
        assert cohort_stats['analyses_reussies'] == 2

class TestDataProcessing:
    """Tests pour le traitement des données"""
    
    def setup_method(self):
        self.processor = DataProcessor()
    
    def test_patient_data_processing(self):
        """Test du traitement des données patient"""
        raw_data = {
            'pathologie': 'GRIPPE',
            'symptomes': ['FIÈVRE', 'TOUX', 'FATIGUE'],
            'profil': {
                'age': 35,
                'comorbidities': 1,
                'immunity_level': 0.6
            }
        }
        
        processed = self.processor.process_patient_data(raw_data)
        
        assert 'demographics' in processed
        assert 'medical_info' in processed
        assert 'symptoms' in processed
        assert 'risk_factors' in processed
        
        # Vérifier les données démographiques
        demographics = processed['demographics']
        assert demographics['age'] == 35
        assert demographics['age_group'] == 'ADULTE'
    
    def test_risk_assessment(self):
        """Test de l'évaluation des risques"""
        high_risk_patient = {
            'pathologie': 'COVID',
            'symptomes': ['FIÈVRE_ÉLEVÉE', 'DYSPNÉE_SEVERE'],
            'profil': {
                'age': 75,
                'comorbidities': 3,
                'immunity_level': 0.3
            }
        }
        
        processed = self.processor.process_patient_data(high_risk_patient)
        risk_factors = processed['risk_factors']
        
        assert risk_factors['score'] > 0.5
        assert risk_factors['level'] == 'ÉLEVÉ'
        assert len(risk_factors['factors']) >= 3
    
    def test_pyramid_data_processing(self):
        """Test du traitement des données pyramidales"""
        pyramid_structure = {
            'base': [10, 20, 30],
            'superieure': [[30, 50], [80]],
            'inferieure': [[10, 10], [0]]
        }
        
        processed = self.processor.process_pyramid_data(pyramid_structure)
        
        assert 'base_metrics' in processed
        assert 'structural_metrics' in processed
        assert 'harmony_score' in processed
        
        # Vérifier les métriques de base
        base_metrics = processed['base_metrics']
        assert base_metrics['length'] == 3
        assert base_metrics['mean'] == 20.0

if __name__ == "__main__":
    pytest.main([__file__, "-v"])