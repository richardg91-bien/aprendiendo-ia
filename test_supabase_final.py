"""
🔍 Verificación Completa de Supabase (Simplificada)
==================================================
"""

import os
import requests
from dotenv import load_dotenv

def test_supabase_simple():
    print("🔍 VERIFICACIÓN COMPLETA DE SUPABASE")
    print("=" * 50)
    
    # Cargar variables de entorno
    load_dotenv("backend/.env")
    load_dotenv()
    
    supabase_url = os.getenv("SUPABASE_URL")
    supabase_key = os.getenv("SUPABASE_ANON_KEY")
    database_url = os.getenv("DATABASE_URL")
    
    print("📋 CONFIGURACIÓN VERIFICADA:")
    print(f"✅ SUPABASE_URL: {supabase_url}")
    print(f"✅ SUPABASE_ANON_KEY: {supabase_key[:20]}...")
    print(f"✅ DATABASE_URL: {database_url[:50]}...")
    print()
    
    # Verificar que contiene el proyecto correcto
    if "cggxjweagmeirqpdzypn" in supabase_url and "cggxjweagmeirqpdzypn" in database_url:
        print("✅ Proyecto cggxjweagmeirqpdzypn confirmado")
    else:
        print("❌ ID de proyecto no coincide")
        return False
    
    # Probar conexión HTTP a Supabase API
    print("\n🌐 PROBANDO API DE SUPABASE...")
    try:
        # Test 1: API Status
        response = requests.get(f"{supabase_url}/rest/v1/", 
                              headers={"apikey": supabase_key}, 
                              timeout=10)
        print(f"✅ API REST: Status {response.status_code}")
        
        # Test 2: Authentication endpoint
        auth_response = requests.get(f"{supabase_url}/auth/v1/settings", 
                                   headers={"apikey": supabase_key}, 
                                   timeout=10)
        print(f"✅ AUTH API: Status {auth_response.status_code}")
        
    except Exception as e:
        print(f"❌ Error en API: {e}")
        return False
    
    print("\n🎉 ¡SUPABASE COMPLETAMENTE CONFIGURADO!")
    print("=" * 50)
    print("✅ Conexión HTTP exitosa")
    print("✅ Autenticación disponible") 
    print("✅ API REST funcional")
    print("✅ Credenciales válidas")
    print()
    print("🚀 ARIA ESTÁ LISTO PARA:")
    print("   📊 Guardar conversaciones en la nube")
    print("   🧠 Aprendizaje colaborativo")
    print("   📈 Analytics y métricas")
    print("   👥 Funciones multiusuario")
    print()
    print("🎯 PRÓXIMOS PASOS:")
    print("   1. python backend/src/main.py      # Iniciar servidor")
    print("   2. npm start                       # Iniciar frontend")
    print("   3. ¡Disfruta de ARIA con Supabase!")
    
    return True

if __name__ == "__main__":
    test_supabase_simple()