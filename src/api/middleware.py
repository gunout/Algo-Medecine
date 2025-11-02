import time
import logging
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp

logger = logging.getLogger(__name__)

class LoggingMiddleware(BaseHTTPMiddleware):
    """Middleware de logging des requêtes"""
    
    def __init__(self, app: ASGIApp):
        super().__init__(app)
    
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        
        # Log de la requête entrante
        logger.info(f"Requête entrante: {request.method} {request.url}")
        
        # Traitement de la requête
        response = await call_next(request)
        
        # Calcul du temps de traitement
        process_time = time.time() - start_time
        
        # Log de la réponse
        logger.info(
            f"Réponse: {request.method} {request.url} "
            f"Status: {response.status_code} "
            f"Temps: {process_time:.3f}s"
        )
        
        # Ajouter le temps de traitement dans les headers
        response.headers["X-Process-Time"] = str(process_time)
        
        return response

class SecurityMiddleware(BaseHTTPMiddleware):
    """Middleware de sécurité"""
    
    def __init__(self, app: ASGIApp):
        super().__init__(app)
    
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        
        # Headers de sécurité
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        
        # CORS headers supplémentaires
        if "Origin" in request.headers:
            response.headers["Access-Control-Allow-Origin"] = "*"
            response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
            response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
        
        return response

class ErrorHandlingMiddleware(BaseHTTPMiddleware):
    """Middleware de gestion des erreurs"""
    
    def __init__(self, app: ASGIApp):
        super().__init__(app)
    
    async def dispatch(self, request: Request, call_next):
        try:
            response = await call_next(request)
            return response
            
        except Exception as exc:
            logger.error(f"Erreur non gérée: {exc}", exc_info=True)
            
            # Retourner une réponse d'erreur standardisée
            from fastapi.responses import JSONResponse
            return JSONResponse(
                status_code=500,
                content={
                    "detail": "Erreur interne du serveur",
                    "error_code": "INTERNAL_SERVER_ERROR",
                    "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ")
                }
            )