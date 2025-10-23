"""
Script directo para verificar la configuración de Supabase
"""
import os

print("🔍 VERIFICANDO CONFIGURACIÓN DE SUPABASE")
print("=" * 50)

# Leer directamente el archivo backend/.env
backend_env_path = "backend/.env"
if os.path.exists(backend_env_path):
    print(f"✅ Archivo {backend_env_path} encontrado")
    with open(backend_env_path, 'r') as f:
        content = f.read()
    
    if "cggxjweagmeirqpdzypn" in content:
        print("✅ ID de proyecto cggxjweagmeirqpdzypn encontrado en la configuración")
        print("\n📋 CONTENIDO DEL ARCHIVO:")
        print("-" * 30)
        print(content)
        print("-" * 30)
    else:
        print("❌ ID de proyecto cggxjweagmeirqpdzypn NO encontrado")
        print("\n📋 CONTENIDO ACTUAL:")
        print(content)
else:
    print(f"❌ Archivo {backend_env_path} no encontrado")

# Verificar también el .env principal
main_env_path = ".env"
if os.path.exists(main_env_path):
    print(f"\n📄 También verificando {main_env_path}...")
    with open(main_env_path, 'r') as f:
        content = f.read()
    
    if "cggxjweagmeirqpdzypn" in content:
        print("✅ ID de proyecto cggxjweagmeirqpdzypn encontrado en .env principal")
    else:
        print("❌ ID de proyecto cggxjweagmeirqpdzypn NO está en .env principal")

print("\n🎯 CONCLUSIÓN:")
print("El proyecto tiene referencias al ID cggxjweagmeirqpdzypn pero necesita:")
print("1. Configurar la contraseña real de la base de datos")
print("2. Obtener y configurar la SUPABASE_ANON_KEY")
print("3. Desde el dashboard: https://supabase.com/dashboard/project/cggxjweagmeirqpdzypn")