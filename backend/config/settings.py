"""
Configuración del Backend ARIA
"""
import os
from pathlib import Path

# Rutas del proyecto
BASE_DIR = Path(__file__).resolve().parent.parent
SRC_DIR = BASE_DIR / "src"
STATIC_DIR = BASE_DIR.parent / "frontend" / "build"

# Configuración del servidor
class Config:
    """Configuración base"""
    DEBUG = True
    HOST = '127.0.0.1'
    PORT = 5000
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'aria-dev-secret-key-2024'
    
    # CORS
    CORS_ORIGINS = ["http://localhost:3000", "http://127.0.0.1:3000"]
    
    # API
    API_VERSION = "2.0.0"
    API_PREFIX = "/api"
    
class DevelopmentConfig(Config):
    """Configuración de desarrollo"""
    DEBUG = True
    TESTING = False

class ProductionConfig(Config):
    """Configuración de producción"""
    DEBUG = False
    HOST = '0.0.0.0'
    SECRET_KEY = os.environ.get('SECRET_KEY')

class TestingConfig(Config):
    """Configuración para testing"""
    TESTING = True
    DEBUG = True

# Configuraciones disponibles
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}

# Google Cloud OAuth 2.0 Configuration - 2025-10-22
GOOGLE_OAUTH_CLIENT_ID = "209067283417-p7jrdl8hne7ck85iqtt50u02ak2p7gk8.apps.googleusercontent.com"
GOOGLE_CLOUD_API_KEY = "AIzaSyASWXk4RX29VhoL2ccwjz0-GtX-jMvCiYo"
GOOGLE_OAUTH_SCOPES = [
    "https://www.googleapis.com/auth/cloud-platform",
    "https://www.googleapis.com/auth/cloud-translation", 
    "https://www.googleapis.com/auth/cloud-language"
]
GOOGLE_OAUTH_REDIRECT_URI = "http://localhost:8080"
