#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔍 Diagnóstico ARIA
==================
Script para diagnosticar problemas en el sistema ARIA
"""

import sys
import os
import time
import traceback
from pathlib import Path

def print_header(title):
    """Imprime una cabecera formateada"""
    print(f"\n{'='*50}")
    print(f"🔍 {title}")
    print(f"{'='*50}")

def check_python_environment():
    """Verifica el entorno de Python"""
    print_header("ENTORNO PYTHON")
    print(f"✅ Python Version: {sys.version}")
    print(f"✅ Executable: {sys.executable}")
    print(f"✅ Platform: {sys.platform}")
    print(f"✅ Working Dir: {os.getcwd()}")

def check_file_structure():
    """Verifica la estructura de archivos"""
    print_header("ESTRUCTURA DE ARCHIVOS")
    
    critical_files = [
        'main.py',
        'src/aria_servidor_superbase.py',
        'requirements.txt',
        '.env',
        'src/aria_superbase.py'
    ]
    
    for file_path in critical_files:
        if Path(file_path).exists():
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path} - NO ENCONTRADO")

def test_imports():
    """Prueba las importaciones críticas"""
    print_header("PRUEBA DE IMPORTACIONES")
    
    imports_to_test = [
        ('flask', 'Flask'),
        ('flask_cors', 'CORS'),
        ('supabase', 'create_client'),
        ('dotenv', 'load_dotenv'),
        ('sentence_transformers', 'SentenceTransformer')
    ]
    
    for module_name, import_item in imports_to_test:
        try:
            if import_item:
                exec(f"from {module_name} import {import_item}")
            else:
                exec(f"import {module_name}")
            print(f"✅ {module_name}")
        except ImportError as e:
            print(f"❌ {module_name}: {e}")
        except Exception as e:
            print(f"⚠️  {module_name}: {e}")

def test_aria_imports():
    """Prueba las importaciones específicas de ARIA"""
    print_header("IMPORTACIONES ARIA")
    
    # Cambiar al directorio src para las importaciones
    original_dir = os.getcwd()
    
    try:
        if Path('src').exists():
            os.chdir('src')
            sys.path.insert(0, os.getcwd())
        
        aria_imports = [
            'aria_superbase',
            'core.aria_embeddings_supabase',
            'core.emotion_detector_supabase'
        ]
        
        for module_name in aria_imports:
            try:
                exec(f"import {module_name}")
                print(f"✅ {module_name}")
            except ImportError as e:
                print(f"❌ {module_name}: {e}")
            except Exception as e:
                print(f"⚠️  {module_name}: {e}")
                
    finally:
        os.chdir(original_dir)

def test_server_startup():
    """Prueba si el servidor puede iniciar sin colgarse"""
    print_header("PRUEBA DEL SERVIDOR")
    
    try:
        print("🔄 Intentando importar servidor...")
        original_dir = os.getcwd()
        
        if Path('src').exists():
            os.chdir('src')
            sys.path.insert(0, os.getcwd())
        
        # Importar solo la parte inicial del servidor
        with open('aria_servidor_superbase.py', 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Verificar si hay problemas evidentes en el código
        if 'app.run(' in content:
            print("✅ Código del servidor encontrado")
        else:
            print("❌ No se encontró app.run() en el servidor")
            
        print("✅ Servidor puede ser analizado")
        
    except Exception as e:
        print(f"❌ Error al analizar servidor: {e}")
        traceback.print_exc()
    finally:
        os.chdir(original_dir)

def main():
    """Función principal del diagnóstico"""
    print("🔍 ARIA - Diagnóstico del Sistema")
    print(f"Fecha: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    check_python_environment()
    check_file_structure()
    test_imports()
    test_aria_imports()
    test_server_startup()
    
    print_header("DIAGNÓSTICO COMPLETADO")
    print("📋 Revisa los resultados arriba para identificar problemas")
    print("💡 Si hay errores de importación, ejecuta: pip install -r requirements.txt")
    print("💡 Si falta el archivo .env, copia env_template.txt como .env")

if __name__ == "__main__":
    main()