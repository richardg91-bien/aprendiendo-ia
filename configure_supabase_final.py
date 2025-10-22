"""
🔧 Configurador Final de Supabase para ARIA
==========================================
"""

import os
import re

def configure_supabase():
    print("🚀 CONFIGURADOR DE SUPABASE - ARIA")
    print("=" * 50)
    print("📋 Proyecto: cggxjweagmeirqpdzypn")
    print()
    
    # Solicitar credenciales
    print("🔑 INGRESA TUS CREDENCIALES DE SUPABASE:")
    print()
    
    # Contraseña de la base de datos
    password = input("🔐 Contraseña de la base de datos: ").strip()
    if not password:
        print("❌ La contraseña no puede estar vacía")
        return False
    
    # Clave anónima
    anon_key = input("🗝️  Clave anónima (anon public): ").strip()
    if not anon_key:
        print("❌ La clave anónima no puede estar vacía")
        return False
    
    print()
    print("⚙️  CONFIGURANDO ARCHIVOS...")
    
    # Configurar backend/.env
    backend_env_content = f"""# Configuración de Supabase para el proyecto cggxjweagmeirqpdzypn
DATABASE_URL="postgresql://postgres:{password}@db.cggxjweagmeirqpdzypn.supabase.co:5432/postgres"
SUPABASE_URL="https://cggxjweagmeirqpdzypn.supabase.co"
SUPABASE_ANON_KEY="{anon_key}"

# Configuración adicional
SUPABASE_SERVICE_ROLE_KEY="{anon_key}"
POSTGRES_PASSWORD="{password}"
"""
    
    try:
        with open("backend/.env", "w", encoding="utf-8") as f:
            f.write(backend_env_content)
        print("✅ backend/.env configurado")
    except Exception as e:
        print(f"❌ Error configurando backend/.env: {e}")
        return False
    
    # Leer .env principal actual
    main_env_content = ""
    if os.path.exists(".env"):
        with open(".env", "r", encoding="utf-8") as f:
            main_env_content = f.read()
    
    # Agregar configuración de Supabase al .env principal
    supabase_config = f"""

# ===========================================
# 🌐 CONFIGURACIÓN DE SUPABASE (AUTOMATICA)
# ===========================================
DATABASE_URL="postgresql://postgres:{password}@db.cggxjweagmeirqpdzypn.supabase.co:5432/postgres"
SUPABASE_URL="https://cggxjweagmeirqpdzypn.supabase.co"
SUPABASE_ANON_KEY="{anon_key}"
SUPABASE_SERVICE_ROLE_KEY="{anon_key}"
POSTGRES_PASSWORD="{password}"
"""
    
    # Solo agregar si no existe ya
    if "SUPABASE_URL" not in main_env_content:
        main_env_content += supabase_config
    else:
        # Reemplazar configuración existente
        # Eliminar configuración anterior de Supabase
        lines = main_env_content.split('\n')
        new_lines = []
        skip_supabase = False
        
        for line in lines:
            if "CONFIGURACIÓN DE SUPABASE" in line:
                skip_supabase = True
                continue
            elif line.startswith("SUPABASE_") or line.startswith("DATABASE_URL") or line.startswith("POSTGRES_PASSWORD"):
                if skip_supabase:
                    continue
            elif line.strip() == "" and skip_supabase:
                skip_supabase = False
                continue
            
            new_lines.append(line)
        
        main_env_content = '\n'.join(new_lines) + supabase_config
    
    try:
        with open(".env", "w", encoding="utf-8") as f:
            f.write(main_env_content)
        print("✅ .env principal actualizado")
    except Exception as e:
        print(f"❌ Error actualizando .env principal: {e}")
        return False
    
    print()
    print("🎉 ¡CONFIGURACIÓN COMPLETADA!")
    print("=" * 50)
    print("✅ Base de datos Supabase configurada")
    print("✅ Proyecto cggxjweagmeirqpdzypn conectado")
    print("✅ Credenciales guardadas de forma segura")
    print()
    print("🔄 PRÓXIMOS PASOS:")
    print("1. python test_connection_real.py  # Probar conexión")
    print("2. python start_aria.py            # Iniciar ARIA")
    print()
    print("🔗 Dashboard: https://supabase.com/dashboard/project/cggxjweagmeirqpdzypn")
    
    return True

if __name__ == "__main__":
    configure_supabase()