
### 6. `main.py`
```python
#!/usr/bin/env python3
"""
Point d'entrée principal de l'application Algo Vérité Médical
"""

import uvicorn
from src.utils.config import get_settings
from src.utils.logger import setup_logging

def main():
    """Fonction principale pour démarrer l'application"""
    
    # Configuration
    settings = get_settings()
    setup_logging(level=settings.LOG_LEVEL)
    
    print(f"""
╔═══════════════════════════════════════╗
║        ALGO VÉRITÉ MÉDICAL           ║
║      Système Prédictif Sanitaire     ║
║               v1.0.0                 ║
╚═══════════════════════════════════════╝

Environnement: {settings.ENVIRONMENT}
API: http://{settings.API_HOST}:{settings.API_PORT}
Documentation: http://{settings.API_HOST}:{settings.API_PORT}/docs
    """)
    
    # Démarrage du serveur
    uvicorn.run(
        "src.api.routes:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=settings.DEBUG,
        log_level=settings.LOG_LEVEL.lower()
    )

if __name__ == "__main__":
    main()