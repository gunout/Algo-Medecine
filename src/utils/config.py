from pydantic import BaseSettings
from typing import Optional
import os

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
    DATABASE_URL: str = "sqlite:///./algo_verite_medical.db"
    
    # Sécurité
    SECRET_KEY: str = "votre-cle-secrete-par-defaut-changez-en-production"
    JWT_ALGORITHM: str = "HS256"
    
    # Medical APIs
    CLINICAL_TRIALS_API_KEY: Optional[str] = None
    FDA_API_KEY: Optional[str] = None
    
    class Config:
        env_file = ".env"
        case_sensitive = True

def get_settings() -> Settings:
    """Retourne la configuration de l'application"""
    return Settings()