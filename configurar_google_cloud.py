#!/usr/bin/env python3
"""
⚙️ CONFIGURADOR DE GOOGLE CLOUD APIs
===================================

Script para ayudar a configurar Google Cloud APIs gratuitas en ARIA.
Guía paso a paso para obtener y configurar las claves de API.

Basado en la documentación oficial de Google Cloud.

Fecha: 22 de octubre de 2025
"""

import os
import sys
import json
import subprocess
from pathlib import Path

def print_header():
    """Imprime el encabezado del configurador"""
    print("🌐" + "="*60)
    print("   CONFIGURADOR DE GOOGLE CLOUD APIs PARA ARIA")
    print("="*62)
    print()

def check_current_configuration():
    """Verifica la configuración actual"""
    print("🔍 VERIFICANDO CONFIGURACIÓN ACTUAL...")
    print("-" * 40)
    
    # Verificar variables de entorno
    api_key = os.getenv('GOOGLE_CLOUD_API_KEY')
    project_id = os.getenv('GOOGLE_CLOUD_PROJECT')
    
    if api_key:
        print("✅ GOOGLE_CLOUD_API_KEY: Configurada")
        print(f"   Clave: {api_key[:10]}...{api_key[-4:] if len(api_key) > 14 else ''}")
    else:
        print("❌ GOOGLE_CLOUD_API_KEY: No configurada")
    
    if project_id:
        print(f"✅ GOOGLE_CLOUD_PROJECT: {project_id}")
    else:
        print("❌ GOOGLE_CLOUD_PROJECT: No configurado")
    
    # Verificar gcloud CLI
    try:
        result = subprocess.run(['gcloud', 'version'], 
                               capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print("✅ Google Cloud CLI: Instalado")
            
            # Verificar autenticación
            auth_result = subprocess.run(['gcloud', 'auth', 'list', '--filter=status:ACTIVE'], 
                                        capture_output=True, text=True, timeout=10)
            if auth_result.returncode == 0 and auth_result.stdout.strip():
                print("✅ Autenticación: Configurada")
            else:
                print("❌ Autenticación: No configurada")
        else:
            print("❌ Google Cloud CLI: No instalado")
    except (subprocess.TimeoutExpired, FileNotFoundError):
        print("❌ Google Cloud CLI: No encontrado")
    
    print()

def show_step_by_step_guide():
    """Muestra la guía paso a paso"""
    print("📋 GUÍA PASO A PASO PARA CONFIGURAR GOOGLE CLOUD")
    print("-" * 50)
    
    steps = [
        {
            'title': 'PASO 1: Instalar Google Cloud CLI',
            'description': [
                '1. Descargar desde: https://cloud.google.com/sdk/docs/install',
                '2. Ejecutar el instalador para Windows',
                '3. Reiniciar terminal después de la instalación',
                '4. Verificar con: gcloud version'
            ]
        },
        {
            'title': 'PASO 2: Crear/Configurar Proyecto',
            'description': [
                '1. Ir a: https://console.cloud.google.com/',
                '2. Crear nuevo proyecto o seleccionar existente',
                '3. Anotar el Project ID (lo necesitarás)',
                '4. Habilitar APIs necesarias:'
            ],
            'sub_items': [
                '   • Cloud Natural Language API',
                '   • Cloud Translation API',
                '   • (Ambas tienen niveles gratuitos generosos)'
            ]
        },
        {
            'title': 'PASO 3: Crear Clave de API',
            'description': [
                '1. En Google Cloud Console → APIs & Services → Credentials',
                '2. Hacer clic en "Create Credentials" → "API Key"',
                '3. Copiar la clave generada',
                '4. (Opcional) Restringir la clave a APIs específicas'
            ]
        },
        {
            'title': 'PASO 4: Configurar Autenticación Local',
            'description': [
                'Ejecutar estos comandos en terminal:',
                '',
                '# Autenticar con cuenta personal',
                'gcloud auth login',
                '',
                '# Configurar proyecto por defecto',
                'gcloud config set project TU_PROJECT_ID',
                '',
                '# Configurar credenciales por defecto',
                'gcloud auth application-default login'
            ]
        },
        {
            'title': 'PASO 5: Configurar Variables de Entorno',
            'description': [
                'En PowerShell (como administrador):',
                '',
                '# Configurar clave API',
                '$env:GOOGLE_CLOUD_API_KEY = "tu_clave_api_aqui"',
                '[Environment]::SetEnvironmentVariable("GOOGLE_CLOUD_API_KEY", "tu_clave_api", "User")',
                '',
                '# Configurar Project ID',
                '$env:GOOGLE_CLOUD_PROJECT = "tu_project_id"',
                '[Environment]::SetEnvironmentVariable("GOOGLE_CLOUD_PROJECT", "tu_project_id", "User")',
                '',
                '# Reiniciar terminal después'
            ]
        }
    ]
    
    for i, step in enumerate(steps, 1):
        print(f"\n🔸 {step['title']}")
        print("─" * len(step['title']))
        
        for desc in step['description']:
            print(f"   {desc}")
        
        if 'sub_items' in step:
            for sub_item in step['sub_items']:
                print(sub_item)
    
    print()

def show_limits_and_pricing():
    """Muestra límites del plan gratuito"""
    print("💰 LÍMITES DEL PLAN GRATUITO")
    print("-" * 30)
    
    limits = [
        {
            'api': 'Natural Language API',
            'free_tier': '5,000 unidades/mes',
            'what_counts': 'Cada documento analizado = 1 unidad',
            'pricing_after': '$1.00 por cada 1,000 unidades adicionales'
        },
        {
            'api': 'Translation API',
            'free_tier': '500,000 caracteres/mes',
            'what_counts': 'Caracteres de texto traducidos',
            'pricing_after': '$20 por cada 1M caracteres adicionales'
        }
    ]
    
    for limit in limits:
        print(f"📊 {limit['api']}:")
        print(f"   • Gratuito: {limit['free_tier']}")
        print(f"   • Qué cuenta: {limit['what_counts']}")
        print(f"   • Después: {limit['pricing_after']}")
        print()

def test_configuration():
    """Prueba la configuración actual"""
    print("🧪 PROBANDO CONFIGURACIÓN...")
    print("-" * 30)
    
    try:
        # Importar y probar módulo
        sys.path.append(os.path.join(os.path.dirname(__file__), 'backend', 'src'))
        from google_cloud_apis import google_cloud_apis
        
        # Obtener estado
        status = google_cloud_apis.get_usage_status()
        
        print(f"✅ Módulo importado correctamente")
        print(f"📊 API Key configurada: {status['api_key_configured']}")
        print(f"💾 Entradas en cache: {status['cache_entries']}")
        
        if status['api_key_configured']:
            print("\n🔍 Probando APIs...")
            
            # Prueba básica de análisis
            test_text = "Hello, this is a test for Google Cloud APIs integration."
            
            sentiment = google_cloud_apis.analyze_sentiment_advanced(test_text)
            if not sentiment.get('note'):
                print("✅ Natural Language API: Funcionando")
                print(f"   Sentimiento detectado: {sentiment.get('overall_sentiment', {}).get('label', 'N/A')}")
            else:
                print("❌ Natural Language API: No disponible")
            
            translation = google_cloud_apis.translate_text_google(test_text, target_lang='es')
            if not translation.get('note'):
                print("✅ Translation API: Funcionando")
                print(f"   Traducción: {translation.get('translated_text', 'N/A')[:50]}...")
            else:
                print("❌ Translation API: No disponible")
        else:
            print("\n⚠️ API Key no configurada - completar configuración primero")
            
    except ImportError as e:
        print(f"❌ Error importando módulo: {e}")
    except Exception as e:
        print(f"❌ Error en prueba: {e}")

def create_batch_configuration_script():
    """Crea un script batch para configurar variables fácilmente"""
    script_content = '''@echo off
echo ================================
echo   CONFIGURADOR DE VARIABLES
echo   Google Cloud APIs para ARIA
echo ================================
echo.

set /p API_KEY="Ingresa tu Google Cloud API Key: "
set /p PROJECT_ID="Ingresa tu Project ID: "

echo.
echo Configurando variables de entorno...

setx GOOGLE_CLOUD_API_KEY "%API_KEY%"
setx GOOGLE_CLOUD_PROJECT "%PROJECT_ID%"

echo.
echo ✅ Variables configuradas correctamente
echo ⚠️  Reinicia tu terminal para aplicar los cambios
echo.
pause
'''
    
    script_path = 'configurar_google_cloud.bat'
    
    try:
        with open(script_path, 'w', encoding='utf-8') as f:
            f.write(script_content)
        
        print(f"📝 Script de configuración creado: {script_path}")
        print("   Ejecuta este archivo para configurar variables fácilmente")
        
    except Exception as e:
        print(f"❌ Error creando script: {e}")

def main():
    """Función principal del configurador"""
    print_header()
    
    print("🎯 ESTE CONFIGURADOR TE AYUDARÁ A:")
    print("   • Verificar tu configuración actual")
    print("   • Obtener claves de API de Google Cloud")
    print("   • Configurar variables de entorno")
    print("   • Probar la integración")
    print()
    
    while True:
        print("📋 OPCIONES DISPONIBLES:")
        print("1. 🔍 Verificar configuración actual")
        print("2. 📖 Ver guía paso a paso")
        print("3. 💰 Ver límites del plan gratuito")
        print("4. 🧪 Probar configuración")
        print("5. 📝 Crear script de configuración")
        print("6. 🚪 Salir")
        print()
        
        try:
            choice = input("Selecciona una opción (1-6): ").strip()
            
            if choice == '1':
                print()
                check_current_configuration()
                
            elif choice == '2':
                print()
                show_step_by_step_guide()
                
            elif choice == '3':
                print()
                show_limits_and_pricing()
                
            elif choice == '4':
                print()
                test_configuration()
                print()
                
            elif choice == '5':
                print()
                create_batch_configuration_script()
                print()
                
            elif choice == '6':
                print("👋 ¡Hasta luego!")
                break
                
            else:
                print("❌ Opción inválida. Por favor selecciona 1-6.")
                
        except KeyboardInterrupt:
            print("\n👋 Configuración interrumpida por el usuario")
            break
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()