"""
🔍 Probador de Conexión Real a Supabase
======================================
"""

import os
import sys
from dotenv import load_dotenv

def test_supabase_connection():
    print("🔍 PROBANDO CONEXIÓN A SUPABASE")
    print("=" * 50)
    
    # Cargar variables de entorno
    load_dotenv("backend/.env")
    load_dotenv()
    
    database_url = os.getenv("DATABASE_URL")
    supabase_url = os.getenv("SUPABASE_URL")
    supabase_key = os.getenv("SUPABASE_ANON_KEY")
    
    print("📋 VERIFICANDO CONFIGURACIÓN:")
    
    if not database_url:
        print("❌ DATABASE_URL no encontrada")
        return False
    
    if not supabase_url:
        print("❌ SUPABASE_URL no encontrada")
        return False
        
    if not supabase_key:
        print("❌ SUPABASE_ANON_KEY no encontrada")
        return False
    
    print("✅ Todas las variables de entorno encontradas")
    print()
    
    # Verificar que las credenciales no sean placeholders
    if "[YOUR_PASSWORD]" in database_url or "[YOUR_SUPABASE_ANON_KEY]" in supabase_key:
        print("⚠️  CREDENCIALES INCOMPLETAS")
        print("   Las credenciales contienen placeholders")
        print("   Ejecuta: python configure_supabase_final.py")
        return False
    
    print("✅ Credenciales configuradas")
    print()
    
    # Probar conexión HTTP a Supabase API
    print("🌐 PROBANDO CONEXIÓN HTTP...")
    try:
        import requests
        response = requests.get(f"{supabase_url}/rest/v1/", 
                              headers={"apikey": supabase_key}, 
                              timeout=10)
        if response.status_code in [200, 401, 404]:  # 401/404 son esperados sin autenticación completa
            print(f"✅ Conexión HTTP exitosa (Status: {response.status_code})")
        else:
            print(f"⚠️  Respuesta inesperada: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"❌ Error de conexión HTTP: {e}")
        return False
    except ImportError:
        print("⚠️  requests no disponible, instalando...")
        import subprocess
        subprocess.check_call([sys.executable, "-m", "pip", "install", "requests"])
        print("✅ requests instalado, vuelve a ejecutar el script")
        return False
    
    print()
    
    # Probar conexión a PostgreSQL
    print("🗄️  PROBANDO CONEXIÓN A BASE DE DATOS...")
    try:
        import psycopg
        
        # Extraer componentes de la URL
        conn = psycopg.connect(database_url)
        cursor = conn.cursor()
        
        # Ejecutar una consulta simple
        cursor.execute("SELECT version();")
        db_version = cursor.fetchone()[0]
        
        print("✅ Conexión a PostgreSQL exitosa")
        print(f"📊 Versión de la base de datos: {db_version[:50]}...")
        
        cursor.close()
        conn.close()
        
    except ImportError:
        print("⚠️  psycopg no disponible")
        print("   Ejecuta: pip install psycopg[binary]")
        return False
    except Exception as e:
        print(f"❌ Error de conexión a PostgreSQL: {e}")
        print("   Verifica que la contraseña sea correcta")
        return False
    
    print()
    print("🎉 ¡CONEXIÓN EXITOSA!")
    print("=" * 50)
    print("✅ Supabase completamente configurado")
    print("✅ Base de datos accesible")
    print("✅ ARIA listo para usar la base de datos")
    print()
    print("🚀 Ahora puedes iniciar ARIA:")
    print("   python start_aria.py")
    
    return True

if __name__ == "__main__":
    test_supabase_connection()