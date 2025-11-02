import pytest
import sys
import os

# Ajouter le chemin src
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.core.algo_verite import AlgoVerite
from src.core.medical_predictions import AlgoVeriteMedical
from src.core.pyramid_analysis import PyramidAnalyzer

class TestAlgoVerite:
    """Tests pour l'algorithme Vérité de base"""
    
    def test_analyser_sequence(self):
        """Test de l'analyse d'une séquence"""
        algo = AlgoVerite()
        sequence = [1, 2, 3, 4, 5]
        
        result = algo.analyser_sequence(sequence, "TestSequence")
        
        assert 'nom' in result
        assert 'pyramide' in result
        assert 'signatures' in result
        assert result['nom'] == "TestSequence"
        assert result['sequence_originale'] == sequence
    
    def test_pyramid_construction(self):
        """Test de la construction pyramidale"""
        algo = AlgoVerite()
        sequence = [1, 2, 3]
        
        result = algo.analyser_sequence(sequence, "Test")
        pyramid = result['pyramide']
        
        assert 'base' in pyramid
        assert 'superieure' in pyramid
        assert 'inferieure' in pyramid
        assert pyramid['base'] == sequence
    
    def test_signature_calculation(self):
        """Test du calcul des signatures"""
        algo = AlgoVerite()
        sequence = [10, 20, 30]
        
        result = algo.analyser_sequence(sequence, "Test")
        signatures = result['signatures']
        
        assert 'signature_racine' in signatures
        assert 'sommet_pyramidal' in signatures
        assert 'base_fondamentale' in signatures
        assert signatures['sommet_pyramidal'] > 0
    
    def test_integrity_verification(self):
        """Test de la vérification d'intégrité"""
        algo = AlgoVerite()
        sequence = [5, 10, 15]
        
        # Première analyse
        result1 = algo.analyser_sequence(sequence, "IntegrityTest")
        
        # Vérification
        verification = algo.verifier_integrite("IntegrityTest")
        
        assert verification['statut'] == 'INTÈGRE'
        assert verification['confiance'] == 1.0

class TestAlgoVeriteMedical:
    """Tests pour l'algorithme médical"""
    
    def test_patient_analysis(self):
        """Test de l'analyse d'un patient"""
        algo = AlgoVeriteMedical()
        patient_data = {
            'pathologie': 'GRIPPE',
            'symptomes': ['FIÈVRE', 'TOUX'],
            'profil': {
                'age': 30,
                'comorbidities': 0,
                'immunity_level': 0.8
            }
        }
        
        result = algo.analyser_patient(patient_data)
        
        assert 'patient_id' in result
        assert 'condition_actuelle' in result
        assert 'prediction_retablissement' in result
        assert 'traitements_recommandes' in result
    
    def test_condition_analysis(self):
        """Test de l'analyse de condition"""
        algo = AlgoVeriteMedical()
        patient_data = {
            'pathologie': 'GRIPPE',
            'symptomes': ['FIÈVRE', 'TOUX'],
            'profil': {'age': 30, 'comorbidities': 0}
        }
        
        condition = algo._analyser_condition_patient(patient_data)
        
        assert 'score_gravite' in condition
        assert 'resilience_patient' in condition
        assert 'harmonie_biologique' in condition
        assert 0 <= condition['score_gravite'] <= 1
    
    def test_treatment_recommendation(self):
        """Test de la recommandation de traitements"""
        algo = AlgoVeriteMedical()
        patient_data = {
            'pathologie': 'GRIPPE',
            'symptomes': ['FIÈVRE', 'TOUX'],
            'profil': {'age': 30, 'comorbidities': 0}
        }
        
        condition = algo._analyser_condition_patient(patient_data)
        treatments = algo._rechercher_traitements_optimaux(patient_data, condition)
        
        assert len(treatments) > 0
        assert 'nom' in treatments[0]
        assert 'score_global' in treatments[0]
        assert 0 <= treatments[0]['score_global'] <= 1

class TestPyramidAnalyzer:
    """Tests pour l'analyseur pyramidale"""
    
    def test_pyramid_analysis(self):
        """Test de l'analyse pyramidale"""
        analyzer = PyramidAnalyzer()
        base_sequence = [1, 2, 3, 4, 5]
        
        result = analyzer.analyze_pyramid_structure(base_sequence)
        
        assert 'pyramid' in result
        assert 'metrics' in result
        assert 'type' in result
        assert 'patterns' in result
    
    def test_metrics_calculation(self):
        """Test du calcul des métriques"""
        analyzer = PyramidAnalyzer()
        base_sequence = [10, 20, 30]
        
        result = analyzer.analyze_pyramid_structure(base_sequence)
        metrics = result['metrics']
        
        assert 'height' in metrics
        assert 'width' in metrics
        assert 'stability_score' in metrics
        assert 0 <= metrics['stability_score'] <= 1
    
    def test_pattern_detection(self):
        """Test de la détection de patterns"""
        analyzer = PyramidAnalyzer()
        
        # Test avec séquence arithmétique
        arithmetic_seq = [2, 4, 6, 8]
        result = analyzer.analyze_pyramid_structure(arithmetic_seq)
        
        assert 'patterns' in result
        # Une séquence arithmétique devrait être détectée

if __name__ == "__main__":
    pytest.main([__file__, "-v"])