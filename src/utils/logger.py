import logging
import sys
from typing import Optional

def setup_logging(level: str = "INFO", log_file: Optional[str] = None):
    """Configure le système de logging"""
    
    log_level = getattr(logging, level.upper(), logging.INFO)
    
    # Formatter personnalisé
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Handler console
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    
    # Configuration root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)
    
    # Éviter les handlers multiples
    if not root_logger.handlers:
        root_logger.addHandler(console_handler)
    
    # Handler fichier si spécifié
    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)
        root_logger.addHandler(file_handler)
    
    # Logger spécifique pour l'application
    logger = logging.getLogger("algo_verite_medical")
    logger.setLevel(log_level)
    
    return logger

def get_logger(name: str) -> logging.Logger:
    """Retourne un logger avec le nom spécifié"""
    return logging.getLogger(f"algo_verite_medical.{name}")