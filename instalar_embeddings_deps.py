#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔧 INSTALADOR DE DEPENDENCIAS PARA EMBEDDINGS
==============================================

Script para instalar todas las dependencias necesarias para el sistema
de embeddings con Supabase de ARIA.

Ejecutar: python instalar_embeddings_deps.py
"""

import subprocess
import sys
import os

def run_command(command):
    """Ejecutar comando y mostrar resultado"""
    print(f"🔄 Ejecutando: {command}")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Éxito: {command}")
            if result.stdout:
                print(f"   Output: {result.stdout.strip()}")
        else:
            print(f"❌ Error en: {command}")
            print(f"   Error: {result.stderr.strip()}")
        return result.returncode == 0
    except Exception as e:
        print(f"❌ Excepción ejecutando {command}: {e}")
        return False

def check_python_version():
    """Verificar versión de Python"""
    print("🐍 Verificando versión de Python...")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print(f"✅ Python {version.major}.{version.minor}.{version.micro} - Compatible")
        return True
    else:
        print(f"❌ Python {version.major}.{version.minor}.{version.micro} - Requiere Python 3.8+")
        return False

def install_dependencies():
    """Instalar dependencias necesarias"""
    print("\n📦 Instalando dependencias para embeddings...")
    
    # Lista de paquetes necesarios
    packages = [
        "sentence-transformers",  # Para embeddings locales
        "supabase",              # Cliente de Supabase
        "numpy",                 # Operaciones matemáticas
        "python-dotenv",         # Variables de entorno
        "psycopg2-binary",       # Cliente PostgreSQL
        "pgvector"               # Extensión de vectores (si es necesaria)
    ]
    
    success_count = 0
    
    for package in packages:
        print(f"\n📋 Instalando {package}...")
        if run_command(f"pip install {package}"):
            success_count += 1
        else:
            print(f"⚠️ Falló la instalación de {package}")
    
    print(f"\n🎯 Instalación completada: {success_count}/{len(packages)} paquetes exitosos")
    return success_count == len(packages)

def create_env_template():
    """Crear template de variables de entorno"""
    print("\n📄 Creando template de variables de entorno...")
    
    env_content = """# 🔑 CONFIGURACIÓN DE SUPABASE PARA EMBEDDINGS
# ============================================
# Obtén estos valores de tu panel de Supabase

# URL del proyecto Supabase
SUPABASE_URL=https://tu-proyecto.supabase.co

# API Key anónima de Supabase
SUPABASE_ANON_KEY=tu_anon_key_aqui

# API Key de servicio (opcional, para operaciones administrativas)
SUPABASE_SERVICE_KEY=tu_service_key_aqui

# 🗄️ CONFIGURACIÓN DE BASE DE DATOS (opcional)
DATABASE_URL=postgresql://postgres:tu_password@db.tu-proyecto.supabase.co:5432/postgres

# 🧠 CONFIGURACIÓN DE EMBEDDINGS
EMBEDDINGS_MODEL=all-MiniLM-L6-v2
EMBEDDINGS_DIMENSIONS=384
EMBEDDINGS_BATCH_SIZE=32

# 🎛️ CONFIGURACIÓN DE ARIA
ARIA_DEBUG=True
ARIA_LOG_LEVEL=INFO
"""
    
    try:
        with open('.env.embeddings', 'w', encoding='utf-8') as f:
            f.write(env_content)
        print("✅ Template creado: .env.embeddings")
        print("   📝 Edita este archivo con tus credenciales de Supabase")
        return True
    except Exception as e:
        print(f"❌ Error creando template: {e}")
        return False

def test_imports():
    """Probar que las importaciones funcionen"""
    print("\n🧪 Probando importaciones...")
    
    test_modules = [
        ("sentence_transformers", "SentenceTransformer"),
        ("supabase", "create_client"),
        ("numpy", "array"),
        ("dotenv", "load_dotenv"),
    ]
    
    success_count = 0
    
    for module, component in test_modules:
        try:
            exec(f"from {module} import {component}")
            print(f"✅ {module}.{component} - OK")
            success_count += 1
        except ImportError as e:
            print(f"❌ {module}.{component} - Error: {e}")
    
    print(f"\n🎯 Pruebas de importación: {success_count}/{len(test_modules)} exitosas")
    return success_count == len(test_modules)

def check_supabase_connection():
    """Verificar si se puede conectar a Supabase (opcional)"""
    print("\n🔗 Verificando configuración de Supabase...")
    
    # Buscar archivo .env
    env_files = ['.env', '.env.local', '.env.embeddings']
    found_env = False
    
    for env_file in env_files:
        if os.path.exists(env_file):
            print(f"✅ Encontrado archivo de configuración: {env_file}")
            found_env = True
            break
    
    if not found_env:
        print("⚠️ No se encontró archivo .env")
        print("   📝 Crea un archivo .env con tus credenciales de Supabase")
        return False
    
    # Intentar cargar variables de entorno
    try:
        from dotenv import load_dotenv
        load_dotenv()
        
        supabase_url = os.getenv('SUPABASE_URL')
        supabase_key = os.getenv('SUPABASE_ANON_KEY')
        
        if supabase_url and supabase_key:
            print(f"✅ Variables de entorno configuradas")
            print(f"   URL: {supabase_url}")
            print(f"   Key: {supabase_key[:20]}...")
            return True
        else:
            print("❌ Variables SUPABASE_URL o SUPABASE_ANON_KEY no encontradas")
            return False
            
    except Exception as e:
        print(f"❌ Error verificando configuración: {e}")
        return False

def main():
    """Función principal de instalación"""
    print("🚀 INSTALADOR DE EMBEDDINGS PARA ARIA")
    print("=" * 50)
    
    # Verificar Python
    if not check_python_version():
        print("❌ Versión de Python incompatible")
        return False
    
    # Instalar dependencias
    if not install_dependencies():
        print("❌ Error instalando dependencias")
        return False
    
    # Crear template de configuración
    create_env_template()
    
    # Probar importaciones
    if not test_imports():
        print("❌ Error en las importaciones")
        return False
    
    # Verificar configuración de Supabase
    check_supabase_connection()
    
    print("\n" + "=" * 50)
    print("🎉 INSTALACIÓN COMPLETADA")
    print("=" * 50)
    print("📋 Pasos siguientes:")
    print("1. 📝 Edita .env.embeddings con tus credenciales de Supabase")
    print("2. 🗄️ Ejecuta el esquema SQL en tu panel de Supabase:")
    print("   python -c \"print('Ejecuta: supabase_embeddings_schema.sql')\"")
    print("3. 🧪 Prueba el sistema:")
    print("   python aria_embeddings_supabase.py")
    print("4. 🚀 Inicia ARIA con embeddings:")
    print("   python aria_servidor_superbase.py")
    
    return True

if __name__ == "__main__":
    success = main()
    if not success:
        print("\n❌ Instalación falló. Revisa los errores arriba.")
        sys.exit(1)
    else:
        print("\n✅ Instalación exitosa.")
        sys.exit(0)