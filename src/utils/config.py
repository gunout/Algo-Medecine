from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    """Configuration de l'application"""
    
    # Environnement
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    LOG_LEVEL: str = "INFO"
    
    # API
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    
    # Base de données
    DATABASE_URL: Optional[str] = "sqlite:///./algo_verite_medical.db"
    
    # Sécurité
    SECRET_KEY: str = "votre-cle-secrete-par-defaut-changez-en-production"
    
    # Variables optionnelles (pour éviter les erreurs)
    PYTHONPATH: Optional[str] = None
    REDIS_URL: Optional[str] = None
    JWT_ALGORITHM: Optional[str] = None
    CLINICAL_TRIALS_API_KEY: Optional[str] = None
    FDA_API_KEY: Optional[str] = None
    OPENFDA_API_KEY: Optional[str] = None
    ELASTICSEARCH_URL: Optional[str] = None
    
    class Config:
        env_file = ".env"
        extra = "ignore"  # ← IMPORTANT: ignore les variables supplémentaires

def get_settings() -> Settings:
    """Retourne la configuration de l'application"""
    return Settings()
