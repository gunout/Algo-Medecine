import pytest
from src.core.algo_verite import AlgoVerite
from src.core.medical_predictions import AlgoVeriteMedical

class TestAlgoVerite:
    def test_analyser_mot(self):
        algo = AlgoVerite()
        resultat = algo.analyser_mot("TEST")
        
        assert 'mot' in resultat
        assert resultat['mot'] == "TEST"
        assert 'pyramide' in resultat
        assert 'signatures' in resultat
        
    def test_verifier_integrite(self):
        algo = AlgoVerite()
        algo.analyser_mot("TEST")
        verification = algo.verifier_integrite("TEST")
        
        assert 'statut' in verification
        assert verification['statut'] in ['INTÈGRE', 'CORROMPU']

class TestAlgoVeriteMedical:
    def test_analyser_patient(self):
        algo_medical = AlgoVeriteMedical()
        patient_data = {
            'id': 'TEST001',
            'pathologie': 'GRIPPE',
            'symptomes': ['FIÈVRE', 'TOUX'],
            'profil': {'age_group': 'ADULTE', 'comorbidities': 0}
        }
        
        resultat = algo_medical.analyser_patient(patient_data)
        
        assert 'patient_id' in resultat
        assert 'prediction_retablissement' in resultat
        assert 'traitements_recommandes' in resultat