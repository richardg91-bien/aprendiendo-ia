"""
🔍 Verificador de Configuración Actual de Supabase
================================================
"""

print("🔍 VERIFICANDO TU CONFIGURACIÓN ACTUAL DE SUPABASE")
print("=" * 60)

# Leer el archivo backend/.env
with open("backend/.env", "r") as f:
    content = f.read()

print("📄 CONFIGURACIÓN ENCONTRADA:")
print("-" * 30)
print(content)
print("-" * 30)

print("\n📋 ANÁLISIS:")

if "[$Yara25767]" in content:
    print("🔑 Contraseña detectada: [$Yara25767]")
    print("❓ ¿Es esta tu contraseña real de Supabase?")
    print()
    print("✅ Si [$Yara25767] es tu contraseña correcta:")
    print("   - Solo necesitas la SUPABASE_ANON_KEY")
    print("   - Ve a: https://supabase.com/dashboard/project/cggxjweagmeirqpdzypn/settings/api")
    print("   - Copia la 'anon public' key")
    print()
    print("❌ Si [$Yara25767] NO es tu contraseña:")
    print("   - Necesitas la contraseña real de la base de datos")
    print("   - Ve a: https://supabase.com/dashboard/project/cggxjweagmeirqpdzypn/settings/database")
    print("   - Busca 'Connection string' y copia la contraseña real")

if "[YOUR_SUPABASE_ANON_KEY]" in content:
    print("\n🗝️  ANON KEY pendiente:")
    print("   - Ve a: https://supabase.com/dashboard/project/cggxjweagmeirqpdzypn/settings/api")
    print("   - Copia la clave 'anon public'")

print("\n🎯 PRÓXIMO PASO:")
print("   Ejecuta: python configure_supabase_final.py")
print("   (Te permitirá actualizar solo lo que necesites)")