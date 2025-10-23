#!/usr/bin/env python3
"""
🧪 PRUEBA RÁPIDA - GOOGLE CLOUD + ARIA
======================================

Prueba rápida para verificar la integración completa de Google Cloud APIs
con ARIA siguiendo la documentación oficial.

Verifica:
✅ Configuración de credenciales
✅ Application Default Credentials (ADC)
✅ APIs habilitadas
✅ Integración con sistema de aprendizaje de ARIA
✅ Respuestas mejoradas con Google Cloud

Fecha: 22 de octubre de 2025
"""

import sys
import os
import subprocess
import json
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend', 'src'))

def check_gcloud_setup():
    """Verifica configuración de gcloud CLI"""
    print("🔍 VERIFICANDO CONFIGURACIÓN DE GOOGLE CLOUD CLI")
    print("=" * 50)
    
    # Verificar instalación de gcloud
    try:
        result = subprocess.run(['gcloud', 'version'], 
                               capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            version_line = result.stdout.split('\n')[0]
            print(f"✅ gcloud CLI instalado: {version_line}")
        else:
            print("❌ gcloud CLI no encontrado")
            return False
    except (subprocess.TimeoutExpired, FileNotFoundError):
        print("❌ gcloud CLI no instalado")
        return False
    
    # Verificar autenticación
    try:
        auth_result = subprocess.run(['gcloud', 'auth', 'list', '--filter=status:ACTIVE'], 
                                   capture_output=True, text=True, timeout=10)
        if auth_result.returncode == 0 and auth_result.stdout.strip():
            print("✅ Usuario autenticado con gcloud")
        else:
            print("❌ Usuario no autenticado")
            print("💡 Ejecutar: gcloud auth login")
            return False
    except:
        print("❌ Error verificando autenticación")
        return False
    
    # Verificar proyecto configurado
    try:
        project_result = subprocess.run(['gcloud', 'config', 'get-value', 'project'], 
                                      capture_output=True, text=True, timeout=10)
        if project_result.returncode == 0 and project_result.stdout.strip():
            project_id = project_result.stdout.strip()
            print(f"✅ Proyecto configurado: {project_id}")
        else:
            print("❌ Proyecto no configurado")
            print("💡 Ejecutar: gcloud config set project TU_PROJECT_ID")
            return False
    except:
        print("❌ Error verificando proyecto")
        return False
    
    # Verificar Application Default Credentials
    adc_path = os.path.expanduser('~/.config/gcloud/application_default_credentials.json')
    if os.path.exists(adc_path):
        print("✅ Application Default Credentials configuradas")
    else:
        print("⚠️ ADC no configuradas")
        print("💡 Ejecutar: gcloud auth application-default login")
    
    return True

def check_environment_variables():
    """Verifica variables de entorno"""
    print("\n🌐 VERIFICANDO VARIABLES DE ENTORNO")
    print("=" * 40)
    
    api_key = os.getenv('GOOGLE_CLOUD_API_KEY')
    project_id = os.getenv('GOOGLE_CLOUD_PROJECT')
    
    if api_key:
        print(f"✅ GOOGLE_CLOUD_API_KEY: {api_key[:10]}...{api_key[-4:] if len(api_key) > 14 else ''}")
    else:
        print("❌ GOOGLE_CLOUD_API_KEY: No configurada")
    
    if project_id:
        print(f"✅ GOOGLE_CLOUD_PROJECT: {project_id}")
    else:
        print("❌ GOOGLE_CLOUD_PROJECT: No configurado")
    
    return bool(api_key or project_id)

def check_google_cloud_apis():
    """Verifica APIs habilitadas"""
    print("\n🔌 VERIFICANDO APIs HABILITADAS")
    print("=" * 35)
    
    required_apis = [
        'language.googleapis.com',
        'translate.googleapis.com',
        'serviceusage.googleapis.com'
    ]
    
    enabled_apis = 0
    
    for api in required_apis:
        try:
            result = subprocess.run(['gcloud', 'services', 'list', '--enabled', 
                                   '--filter', f'name:{api}'], 
                                  capture_output=True, text=True, timeout=15)
            
            if result.returncode == 0 and api in result.stdout:
                print(f"✅ {api}: Habilitada")
                enabled_apis += 1
            else:
                print(f"❌ {api}: No habilitada")
                print(f"💡 Ejecutar: gcloud services enable {api}")
                
        except Exception as e:
            print(f"⚠️ {api}: Error verificando - {e}")
    
    print(f"\n📊 APIs habilitadas: {enabled_apis}/{len(required_apis)}")
    return enabled_apis > 0

def test_google_cloud_integration():
    """Prueba integración con ARIA"""
    print("\n🧪 PROBANDO INTEGRACIÓN CON ARIA")
    print("=" * 35)
    
    try:
        from google_cloud_apis import google_cloud_apis
        print("✅ Módulo Google Cloud importado correctamente")
        
        # Obtener estado
        status = google_cloud_apis.get_usage_status()
        print(f"📊 API Key configurada: {status['api_key_configured']}")
        print(f"💾 Entradas en cache: {status['cache_entries']}")
        
        if status['api_key_configured']:
            # Probar análisis de sentimientos
            test_text = "ARIA with Google Cloud is working perfectly!"
            
            print(f"\n🔍 Probando análisis de sentimientos...")
            sentiment = google_cloud_apis.analyze_sentiment_advanced(test_text)
            
            if not sentiment.get('note'):
                score = sentiment.get('overall_sentiment', {}).get('score', 0)
                label = sentiment.get('overall_sentiment', {}).get('label', 'unknown')
                print(f"✅ Natural Language API funcional")
                print(f"   Texto: {test_text}")
                print(f"   Sentimiento: {label} (puntuación: {score:.2f})")
                
                # Probar traducción
                print(f"\n🔄 Probando traducción...")
                translation = google_cloud_apis.translate_text_google(test_text, target_lang='es')
                
                if not translation.get('note'):
                    translated_text = translation.get('translated_text', '')
                    print(f"✅ Translation API funcional")
                    print(f"   Original: {test_text}")
                    print(f"   Traducción: {translated_text}")
                    return True
                else:
                    print(f"❌ Translation API no disponible")
            else:
                print(f"❌ Natural Language API no disponible")
                print(f"   Nota: {sentiment.get('note', 'Error desconocido')}")
        else:
            print(f"⚠️ API Key no configurada - usando fallbacks")
            
        return False
        
    except ImportError as e:
        print(f"❌ Error importando módulo: {e}")
        return False
    except Exception as e:
        print(f"❌ Error en integración: {e}")
        return False

def test_aria_learning_with_google_cloud():
    """Prueba aprendizaje de ARIA con Google Cloud"""
    print("\n🧠 PROBANDO APRENDIZAJE DE ARIA CON GOOGLE CLOUD")
    print("=" * 50)
    
    try:
        from auto_learning_advanced import aria_advanced_learning
        print("✅ Sistema de aprendizaje de ARIA cargado")
        
        # Estado inicial
        initial_status = aria_advanced_learning.get_status()
        initial_count = initial_status.get('total_knowledge', 0)
        print(f"📚 Conocimiento inicial: {initial_count} elementos")
        
        # Intentar aprendizaje con Google Cloud
        print(f"\n🔍 Probando aprendizaje con Google Cloud APIs...")
        
        if hasattr(aria_advanced_learning, '_learn_from_google_cloud'):
            success = aria_advanced_learning._learn_from_google_cloud('artificial intelligence')
            
            if success:
                print("✅ Aprendizaje con Google Cloud exitoso")
                
                # Verificar nuevo conocimiento
                final_status = aria_advanced_learning.get_status()
                final_count = final_status.get('total_knowledge', 0)
                
                if final_count > initial_count:
                    print(f"📈 Conocimiento incrementado: {initial_count} → {final_count}")
                    return True
                else:
                    print("⚠️ No se detectó incremento en conocimiento")
            else:
                print("❌ Aprendizaje con Google Cloud falló")
        else:
            print("❌ Método _learn_from_google_cloud no disponible")
            
        return False
        
    except ImportError as e:
        print(f"❌ Error importando sistema de aprendizaje: {e}")
        return False
    except Exception as e:
        print(f"❌ Error en aprendizaje: {e}")
        return False

def show_next_steps():
    """Muestra próximos pasos según el estado"""
    print("\n📋 PRÓXIMOS PASOS RECOMENDADOS")
    print("=" * 35)
    
    # Verificar qué falta
    gcloud_ok = check_gcloud_setup()
    env_ok = check_environment_variables()
    
    if not gcloud_ok:
        print("🔧 CONFIGURACIÓN BÁSICA REQUERIDA:")
        print("   1. Instalar Google Cloud CLI")
        print("   2. Ejecutar configuración automática:")
        print("      python configuracion_google_cloud_automatica.py")
        print()
    
    elif not env_ok:
        print("🔑 CONFIGURAR CREDENCIALES:")
        print("   1. Crear clave API en Google Cloud Console")
        print("   2. Configurar variables de entorno")
        print("   3. O usar configurador automático:")
        print("      python configuracion_google_cloud_automatica.py")
        print()
    
    else:
        print("✅ CONFIGURACIÓN COMPLETA - SISTEMA LISTO")
        print("🚀 COMANDOS PARA PROBAR:")
        print("   • python prueba_respuestas_inteligentes.py")
        print("   • python aria_servidor_multilingue.py")
        print("   • python prueba_sistema_completo.py")
        print()

def main():
    """Función principal de verificación"""
    print("🧪 VERIFICACIÓN RÁPIDA DE GOOGLE CLOUD + ARIA")
    print("=" * 55)
    print("Verificando integración según documentación oficial de Google Cloud")
    print()
    
    results = {}
    
    try:
        # Verificaciones principales
        results['gcloud_setup'] = check_gcloud_setup()
        results['environment'] = check_environment_variables() 
        results['apis_enabled'] = check_google_cloud_apis()
        results['integration'] = test_google_cloud_integration()
        results['aria_learning'] = test_aria_learning_with_google_cloud()
        
        # Resumen final
        print("\n🎯 RESUMEN DE VERIFICACIÓN")
        print("=" * 30)
        
        total_checks = len(results)
        passed_checks = sum(1 for result in results.values() if result)
        
        for check, result in results.items():
            status = "✅ Correcto" if result else "❌ Pendiente"
            print(f"   {check.replace('_', ' ').title()}: {status}")
        
        print(f"\n📊 Estado general: {passed_checks}/{total_checks} verificaciones exitosas")
        
        if passed_checks >= 3:
            print("🎉 Sistema mayormente funcional")
        elif passed_checks >= 1:
            print("⚠️ Configuración parcial - revisar pendientes")
        else:
            print("❌ Configuración requerida")
        
        # Mostrar próximos pasos
        show_next_steps()
        
        return passed_checks >= 3
        
    except KeyboardInterrupt:
        print("\n⏹️ Verificación interrumpida por el usuario")
        return False
    except Exception as e:
        print(f"\n❌ Error durante verificación: {e}")
        return False

if __name__ == "__main__":
    main()