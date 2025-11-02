import pytest
import sys
import os
from fastapi.testclient import TestClient

# Ajouter le chemin src
sys.path.append(os.path.join(os.path.dirfile__, '..'))

from src.api.routes import app

client = TestClient(app)

class TestAPI:
    """Tests pour l'API"""
    
    def test_root_endpoint(self):
        """Test du endpoint racine"""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert data["message"] == "Algo Vérité Médical API"
    
    def test_health_check(self):
        """Test du health check"""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert "status" in data
        assert data["status"] in ["healthy", "unhealthy"]
    
    def test_patient_analysis(self):
        """Test de l'analyse d'un patient"""
        patient_data = {
            "pathologie": "GRIPPE",
            "symptomes": ["FIÈVRE", "TOUX"],
            "profil": {
                "age": 35,
                "comorbidities": 0,
                "immunity_level": 0.7
            }
        }
        
        response = client.post("/api/medical/analyze", json=patient_data)
        assert response.status_code == 200
        data = response.json()
        
        assert "patient_id" in data
        assert "prediction_retablissement" in data
        assert "traitements_recommandes" in data
    
    def test_invalid_patient_data(self):
        """Test avec des données patient invalides"""
        invalid_data = {
            "pathologie": "GRIPPE",
            # symptomes manquant
            "profil": {
                "age": 35
            }
        }
        
        response = client.post("/api/medical/analyze", json=invalid_data)
        # Doit retourner une erreur 422 (validation)
        assert response.status_code == 422
    
    def test_treatment_recommendation(self):
        """Test de la recommandation de traitements"""
        patient_data = {
            "pathologie": "GRIPPE",
            "symptomes": ["FIÈVRE", "TOUX"],
            "profil": {
                "age": 35,
                "comorbidities": 0,
                "immunity_level": 0.7
            }
        }
        
        response = client.post("/api/medical/treatment/recommend", json=patient_data)
        assert response.status_code == 200
        data = response.json()
        
        assert "traitements_recommandes" in data
        assert "condition_analyse" in data
    
    def test_system_status(self):
        """Test du statut du système"""
        response = client.get("/api/system/status")
        assert response.status_code == 200
        data = response.json()
        
        assert "patients_analyses" in data
        assert "algorithm_version" in data
    
    def test_nonexistent_endpoint(self):
        """Test d'un endpoint inexistant"""
        response = client.get("/api/nonexistent")
        assert response.status_code == 404

class TestDataEndpoints:
    """Tests pour les endpoints de données"""
    
    def test_patients_list(self):
        """Test de la liste des patients"""
        response = client.get("/api/patients")
        assert response.status_code == 200
        data = response.json()
        
        assert "patients" in data
        assert "total" in data
    
    def test_statistics(self):
        """Test des statistiques"""
        response = client.get("/api/statistics")
        assert response.status_code == 200
        data = response.json()
        
        assert "total_patients" in data
        assert "total_analyses" in data

if __name__ == "__main__":
    pytest.main([__file__, "-v"])