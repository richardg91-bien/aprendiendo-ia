#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🤖 ARIA - Sistema de IA Personal
===================================
Launcher principal con configuración automática y detección de errores

Ejecuta desde: python main.py
"""

import os
import sys
import subprocess
import logging
from pathlib import Path

def setup_logging():
    """Configura el sistema de logging"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler('data/logs/aria_startup.log', encoding='utf-8')
        ]
    )
    return logging.getLogger(__name__)

def check_python_version():
    """Verifica que la versión de Python sea compatible"""
    if sys.version_info < (3, 8):
        print("❌ ERROR: Se requiere Python 3.8 o superior")
        print(f"   Versión actual: {sys.version}")
        return False
    return True

def check_env_file():
    """Verifica que exista el archivo .env"""
    env_path = Path('.env')
    if not env_path.exists():
        print("⚠️  ARCHIVO .env NO ENCONTRADO")
        print("\n📋 INSTRUCCIONES:")
        print("1. Copia 'env_template.txt' como '.env'")
        print("2. Configura tus valores de Supabase")
        print("3. Ejecuta nuevamente el programa")
        return False
    return True

def install_dependencies():
    """Instala las dependencias si no están presentes"""
    try:
        import flask
        import supabase
        import sentence_transformers
        print("✅ Dependencias principales encontradas")
        return True
    except ImportError as e:
        print(f"⚠️  Instalando dependencias faltantes...")
        try:
            subprocess.check_call([
                sys.executable, "-m", "pip", "install", "-r", "requirements.txt"
            ])
            print("✅ Dependencias instaladas correctamente")
            return True
        except subprocess.CalledProcessError:
            print(f"❌ Error al instalar dependencias: {e}")
            return False

def check_database_setup():
    """Verifica si la base de datos está configurada"""
    try:
        # Cargar variables de entorno
        from dotenv import load_dotenv
        load_dotenv()
        
        # Verificar variables de entorno necesarias
        import os
        supabase_url = os.getenv('SUPABASE_URL')
        supabase_key = os.getenv('SUPABASE_ANON_KEY') or os.getenv('SUPABASE_KEY')
        
        if not supabase_url or not supabase_key:
            print("⚠️  Variables de entorno de Supabase no encontradas")
            return False
        
        print("✅ Variables de entorno de Supabase encontradas")
        
        # Intentar conexión básica con Supabase
        try:
            from supabase import create_client
            supabase = create_client(supabase_url, supabase_key)
            
            # Test básico de conexión
            response = supabase.table('aria_knowledge').select('*').limit(1).execute()
            print("✅ Conexión a Supabase exitosa")
            return True
        except Exception as db_error:
            print(f"⚠️  Error de conexión con Supabase: {db_error}")
            print("   La base de datos puede necesitar configuración inicial")
            return True  # Permitir continuar, se configurará automáticamente
            
    except Exception as e:
        print(f"⚠️  Error general: {e}")
        return True  # Permitir continuar

def start_aria_server():
    """Inicia el servidor principal de ARIA"""
    try:
        # Cambiar al directorio src y ejecutar el servidor
        original_dir = os.getcwd()
        os.chdir('src')
        
        # Agregar src al path para las importaciones
        sys.path.insert(0, os.getcwd())
        
        print("\n🚀 INICIANDO SERVIDOR ARIA...")
        print("📍 URL: http://localhost:8000")
        print("🛑 Presiona Ctrl+C para detener")
        print("-" * 50)
        
        # Importar y ejecutar el servidor
        import aria_servidor_superbase
        
    except KeyboardInterrupt:
        print("\n\n👋 ARIA detenido por el usuario")
    except ImportError as e:
        print(f"\n❌ Error al importar el servidor: {e}")
        print("   Verifica que todos los archivos estén en su lugar")
        return False
    except Exception as e:
        print(f"\n❌ Error al iniciar ARIA: {e}")
        return False
    finally:
        # Volver al directorio raíz
        os.chdir(original_dir)
        # Limpiar el path
        if os.path.join(original_dir, 'src') in sys.path:
            sys.path.remove(os.path.join(original_dir, 'src'))
    
    return True

def main():
    """Función principal del launcher"""
    print("🤖 ARIA - Sistema de IA Personal")
    print("=" * 35)
    
    # Configurar logging
    logger = setup_logging()
    
    # Verificar si hay argumentos de línea de comandos
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        print("🧪 Modo de prueba activado")
        print("   Ejecutando servidor básico...")
        try:
            subprocess.run([sys.executable, "test_servidor.py"])
            return True
        except Exception as e:
            print(f"❌ Error en modo prueba: {e}")
            return False
    
    # Verificaciones previas
    if not check_python_version():
        return False
    
    if not check_env_file():
        return False
    
    if not install_dependencies():
        return False
    
    if not check_database_setup():
        return False
    
    # Iniciar servidor
    return start_aria_server()

if __name__ == "__main__":
    success = main()
    if not success:
        print("\n❌ ARIA no pudo iniciarse correctamente")
        input("Presiona Enter para salir...")
        sys.exit(1)