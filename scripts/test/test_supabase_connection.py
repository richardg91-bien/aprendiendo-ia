"""
Script de prueba para verificar conexión a Supabase
"""
import os
from dotenv import load_dotenv

# Cargar variables de entorno desde backend/.env
backend_env_path = os.path.join("backend", ".env")
load_dotenv(backend_env_path)

# También cargar el .env principal
load_dotenv()

# Verificar configuración
database_url = os.getenv("DATABASE_URL")
supabase_url = os.getenv("SUPABASE_URL") 
supabase_key = os.getenv("SUPABASE_ANON_KEY")

print("🔍 VERIFICANDO CONFIGURACIÓN DE SUPABASE")
print("=" * 50)

if database_url:
    print(f"✅ DATABASE_URL encontrada")
    if "cggxjweagmeirqpdzypn" in database_url:
        print("✅ Proyecto cggxjweagmeirqpdzypn detectado en DATABASE_URL")
    else:
        print("❌ El proyecto cggxjweagmeirqpdzypn NO está en DATABASE_URL")
    print(f"📋 URL: {database_url[:50]}...")
else:
    print("❌ DATABASE_URL no encontrada")

if supabase_url:
    print(f"✅ SUPABASE_URL encontrada")
    if "cggxjweagmeirqpdzypn" in supabase_url:
        print("✅ Proyecto cggxjweagmeirqpdzypn detectado en SUPABASE_URL")
    else:
        print("❌ El proyecto cggxjweagmeirqpdzypn NO está en SUPABASE_URL")
    print(f"📋 URL: {supabase_url}")
else:
    print("❌ SUPABASE_URL no encontrada")

if supabase_key:
    print(f"✅ SUPABASE_ANON_KEY encontrada")
    print(f"📋 Key: {supabase_key[:20]}...")
else:
    print("❌ SUPABASE_ANON_KEY no encontrada")

print("\n🎯 RESUMEN:")
if database_url and "cggxjweagmeirqpdzypn" in database_url:
    print("✅ SÍ - El proyecto está configurado para el proyecto cggxjweagmeirqpdzypn")
    print("🔗 Dashboard: https://supabase.com/dashboard/project/cggxjweagmeirqpdzypn")
    print("\n⚠️  IMPORTANTE:")
    print("   - Necesitas reemplazar [YOUR_PASSWORD] con tu contraseña real de Supabase")
    print("   - Necesitas reemplazar [YOUR_SUPABASE_ANON_KEY] con tu clave anónima real")
    print("   - Ve al dashboard de Supabase para obtener estas credenciales")
else:
    print("❌ NO - El proyecto NO está conectado al proyecto cggxjweagmeirqpdzypn")