"""
Configuración centralizada para ARIA
Sistema de Inteligencia Artificial - Proyecto Organizado
"""
import os
from pathlib import Path

# Rutas principales del proyecto
PROJECT_ROOT = Path(__file__).resolve().parent.parent
BACKEND_DIR = PROJECT_ROOT / "backend"
FRONTEND_DIR = PROJECT_ROOT / "frontend"
CONFIG_DIR = PROJECT_ROOT / "config"
DATA_DIR = PROJECT_ROOT / "data"
SCRIPTS_DIR = PROJECT_ROOT / "scripts"
DOCS_DIR = PROJECT_ROOT / "docs"
LEGACY_DIR = PROJECT_ROOT / "legacy"

# Configuración del servidor
class ServerConfig:
    """Configuración del servidor Flask"""
    DEBUG = os.getenv('DEBUG', 'True').lower() == 'true'
    HOST = os.getenv('HOST', '127.0.0.1')
    PORT = int(os.getenv('PORT', 8000))
    SECRET_KEY = os.getenv('SECRET_KEY', 'aria-dev-secret-key-2024')
    
    # Frontend
    STATIC_FOLDER = str(FRONTEND_DIR / "build")
    STATIC_URL_PATH = '/'
    
    # API
    API_VERSION = "2.0.0"
    API_PREFIX = "/api"

# Configuración de la base de datos
class DatabaseConfig:
    """Configuración de base de datos"""
    SUPABASE_URL = os.getenv('SUPABASE_URL')
    SUPABASE_KEY = os.getenv('SUPABASE_KEY')
    
    # SQLite local para desarrollo
    DATABASE_PATH = DATA_DIR / "aria_local.db"

# Configuración de IA
class AIConfig:
    """Configuración de IA y machine learning"""
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    MODEL_DIR = BACKEND_DIR / "modelo_neuronal"
    CONVERSATIONS_FILE = DATA_DIR / "conversations.json"
    LEARNING_DATA_FILE = DATA_DIR / "learning_data.json"

# Configuración de protección parental
class ParentalConfig:
    """Configuración de protección infantil"""
    SETTINGS_FILE = CONFIG_DIR / "parental_settings.json"
    SAFETY_LOG_FILE = DATA_DIR / "logs" / "safety_events.log"
    ENABLED = os.getenv('CHILD_PROTECTION', 'True').lower() == 'true'

# Configuración de logs
class LogConfig:
    """Configuración de logging"""
    LOG_DIR = DATA_DIR / "logs"
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    MAX_LOG_SIZE = 10 * 1024 * 1024  # 10MB
    BACKUP_COUNT = 5

# Configuración de desarrollo
class DevelopmentConfig:
    """Configuración específica para desarrollo"""
    AUTO_RELOAD = True
    TESTING = False
    DEBUG_TOOLBAR = True

# Configuración de producción
class ProductionConfig:
    """Configuración específica para producción"""
    AUTO_RELOAD = False
    TESTING = False
    DEBUG_TOOLBAR = False
    
    # Usar variables de entorno en producción
    HOST = '0.0.0.0'
    PORT = int(os.getenv('PORT', 8000))

# Configuración activa basada en el entorno
ENVIRONMENT = os.getenv('FLASK_ENV', 'development')

if ENVIRONMENT == 'production':
    active_config = ProductionConfig
else:
    active_config = DevelopmentConfig

# Exportar configuraciones
__all__ = [
    'PROJECT_ROOT',
    'ServerConfig', 
    'DatabaseConfig',
    'AIConfig',
    'ParentalConfig',
    'LogConfig',
    'active_config'
]