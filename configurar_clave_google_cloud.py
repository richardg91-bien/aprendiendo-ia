#!/usr/bin/env python3
"""
🔧 CONFIGURADOR DE CLAVE API DE GOOGLE CLOUD PARA ARIA
====================================================

Configura automáticamente la clave API de Google Cloud proporcionada
para funcionar con todos los servicios ARIA.

Características:
✅ Configuración de variable de entorno
✅ Verificación de servicios habilitados
✅ Prueba de funcionalidad completa
✅ Configuración persistente

Clave API proporcionada: AIzaSyASWXk4RX29VhoL2ccwjz0-GtX-jMvCiYo

Fecha: 22 de octubre de 2025
"""

import os
import sys
import json
import requests
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional

class GoogleCloudAPIConfigurator:
    """Configurador de clave API de Google Cloud para ARIA"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.masked_key = f"{api_key[:8]}...{api_key[-4:]}"
        
        # Servicios que necesita ARIA
        self.required_services = {
            'translate.googleapis.com': 'Google Cloud Translation API',
            'language.googleapis.com': 'Google Cloud Natural Language API',
            'texttospeech.googleapis.com': 'Google Cloud Text-to-Speech API'
        }
        
        print("🔧 CONFIGURADOR DE CLAVE API GOOGLE CLOUD")
        print("=" * 45)
        print(f"🔑 Clave API: {self.masked_key}")
        print()
    
    def configure_environment_variable(self) -> bool:
        """Configura variable de entorno"""
        print("🌍 CONFIGURANDO VARIABLE DE ENTORNO")
        print("-" * 35)
        
        try:
            # Configurar variable de entorno actual
            os.environ['GOOGLE_CLOUD_API_KEY'] = self.api_key
            
            # Verificar configuración
            configured_key = os.getenv('GOOGLE_CLOUD_API_KEY')
            
            if configured_key == self.api_key:
                print(f"✅ Variable GOOGLE_CLOUD_API_KEY configurada")
                print(f"   Clave: {self.masked_key}")
                
                # Crear archivo .env para persistencia
                self._create_env_file()
                return True
            else:
                print("❌ Error configurando variable de entorno")
                return False
                
        except Exception as e:
            print(f"❌ Error: {e}")
            return False
    
    def _create_env_file(self):
        """Crea archivo .env para configuración persistente"""
        try:
            env_file = Path(".env")
            
            # Leer .env existente si existe
            existing_vars = {}
            if env_file.exists():
                with open(env_file, 'r', encoding='utf-8') as f:
                    for line in f:
                        if '=' in line and not line.strip().startswith('#'):
                            key, value = line.strip().split('=', 1)
                            existing_vars[key] = value
            
            # Actualizar con nueva clave
            existing_vars['GOOGLE_CLOUD_API_KEY'] = self.api_key
            
            # Escribir archivo .env actualizado
            with open(env_file, 'w', encoding='utf-8') as f:
                f.write(f"# Configuración ARIA - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                for key, value in existing_vars.items():
                    f.write(f"{key}={value}\n")
            
            print(f"✅ Archivo .env actualizado")
            
        except Exception as e:
            print(f"⚠️ Error creando .env: {e}")
    
    def test_api_key_validity(self) -> Dict:
        """Prueba validez básica de la clave API"""
        print(f"\n🧪 PROBANDO VALIDEZ DE CLAVE API")
        print("-" * 32)
        
        results = {
            'key_format_valid': False,
            'services_tested': {},
            'recommendations': []
        }
        
        # Verificar formato de clave
        if self.api_key.startswith('AIza') and len(self.api_key) == 39:
            results['key_format_valid'] = True
            print("✅ Formato de clave válido (39 caracteres, prefijo AIza)")
        else:
            print("❌ Formato de clave inválido")
            results['recommendations'].append("Verificar que la clave API sea correcta")
            return results
        
        # Probar cada servicio
        for service, description in self.required_services.items():
            print(f"\n🔍 Probando {description}:")
            
            try:
                test_result = self._test_service(service)
                results['services_tested'][service] = test_result
                
                if test_result['success']:
                    print(f"   ✅ {service}: Funcionando")
                else:
                    print(f"   ❌ {service}: {test_result.get('error', 'Error desconocido')}")
                    
                    if test_result.get('status_code') == 403:
                        results['recommendations'].append(f"Habilitar {description} en Google Cloud Console")
                    elif test_result.get('status_code') == 400:
                        results['recommendations'].append(f"Verificar configuración de {description}")
                        
            except Exception as e:
                print(f"   ❌ {service}: Error de conexión - {str(e)[:50]}...")
                results['services_tested'][service] = {
                    'success': False,
                    'error': str(e),
                    'status_code': None
                }
        
        return results
    
    def _test_service(self, service: str) -> Dict:
        """Prueba un servicio específico"""
        try:
            if service == 'translate.googleapis.com':
                return self._test_translation_api()
            elif service == 'language.googleapis.com':
                return self._test_natural_language_api()
            elif service == 'texttospeech.googleapis.com':
                return self._test_text_to_speech_api()
            else:
                return {'success': False, 'error': 'Servicio no implementado'}
                
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def _test_translation_api(self) -> Dict:
        """Prueba Translation API"""
        url = "https://translation.googleapis.com/language/translate/v2"
        
        params = {
            'key': self.api_key,
            'q': 'Hello world',
            'source': 'en',
            'target': 'es'
        }
        
        try:
            response = requests.post(url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if 'data' in data and 'translations' in data['data']:
                    return {
                        'success': True,
                        'response': data['data']['translations'][0]['translatedText']
                    }
            
            return {
                'success': False,
                'status_code': response.status_code,
                'error': f"HTTP {response.status_code}"
            }
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def _test_natural_language_api(self) -> Dict:
        """Prueba Natural Language API"""
        url = "https://language.googleapis.com/v1/documents:analyzeSentiment"
        
        headers = {'Content-Type': 'application/json'}
        params = {'key': self.api_key}
        
        data = {
            'document': {
                'content': 'I am happy',
                'type': 'PLAIN_TEXT'
            }
        }
        
        try:
            response = requests.post(url, headers=headers, params=params, 
                                   json=data, timeout=10)
            
            if response.status_code == 200:
                result = response.json()
                if 'documentSentiment' in result:
                    return {
                        'success': True,
                        'sentiment': result['documentSentiment']['magnitude']
                    }
            
            return {
                'success': False,
                'status_code': response.status_code,
                'error': f"HTTP {response.status_code}"
            }
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def _test_text_to_speech_api(self) -> Dict:
        """Prueba Text-to-Speech API"""
        url = "https://texttospeech.googleapis.com/v1/voices"
        
        params = {'key': self.api_key}
        
        try:
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if 'voices' in data:
                    return {
                        'success': True,
                        'voices_count': len(data['voices'])
                    }
            
            return {
                'success': False,
                'status_code': response.status_code,
                'error': f"HTTP {response.status_code}"
            }
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def integrate_with_aria(self) -> bool:
        """Integra la clave con el sistema ARIA"""
        print(f"\n🤖 INTEGRANDO CON SISTEMA ARIA")
        print("-" * 31)
        
        try:
            # Probar sistema ARIA
            sys.path.append('backend/src')
            
            # Importar APIs de Google Cloud de ARIA
            try:
                import google_cloud_apis
                print("✅ Módulo google_cloud_apis importado")
                
                # Probar funcionalidad
                from google_cloud_apis import GoogleCloudAPIs
                
                gcp = GoogleCloudAPIs()
                
                # Verificar que detecta la clave
                if hasattr(gcp, 'api_key') and gcp.api_key:
                    print(f"✅ ARIA detectó clave API: {gcp.api_key[:8]}...")
                    
                    # Probar análisis de sentimientos
                    try:
                        sentiment = gcp.analyze_sentiment_advanced("I am very happy today!")
                        print(f"✅ Análisis de sentimientos funcional")
                        return True
                    except Exception as e:
                        print(f"⚠️ Error en análisis: {str(e)[:40]}...")
                        return False
                else:
                    print("❌ ARIA no detectó la clave API")
                    return False
                    
            except ImportError as e:
                print(f"❌ Error importando google_cloud_apis: {e}")
                return False
                
        except Exception as e:
            print(f"❌ Error integrando con ARIA: {e}")
            return False
    
    def create_configuration_summary(self, test_results: Dict) -> Dict:
        """Crea resumen de configuración"""
        print(f"\n📋 GENERANDO RESUMEN DE CONFIGURACIÓN")
        print("-" * 37)
        
        # Calcular estado general
        services_working = sum(1 for result in test_results['services_tested'].values() 
                             if result.get('success', False))
        total_services = len(test_results['services_tested'])
        success_rate = (services_working / total_services) * 100 if total_services > 0 else 0
        
        # Determinar estado
        if success_rate >= 100:
            status = "🎉 COMPLETAMENTE FUNCIONAL"
        elif success_rate >= 66:
            status = "✅ MAYORMENTE FUNCIONAL"
        elif success_rate >= 33:
            status = "⚠️ PARCIALMENTE FUNCIONAL"
        else:
            status = "❌ NECESITA CONFIGURACIÓN"
        
        summary = {
            'timestamp': datetime.now().isoformat(),
            'api_key': self.masked_key,
            'status': status,
            'success_rate': success_rate,
            'services_working': services_working,
            'total_services': total_services,
            'services_status': test_results['services_tested'],
            'recommendations': test_results['recommendations']
        }
        
        # Mostrar resumen
        print(f"📊 ESTADO: {status}")
        print(f"📈 Servicios funcionando: {services_working}/{total_services} ({success_rate:.1f}%)")
        
        if test_results['recommendations']:
            print(f"\n💡 RECOMENDACIONES ({len(test_results['recommendations'])}):")
            for i, rec in enumerate(test_results['recommendations'], 1):
                print(f"   {i}. {rec}")
        
        # Guardar resumen
        self._save_configuration_summary(summary)
        
        return summary
    
    def _save_configuration_summary(self, summary: Dict):
        """Guarda resumen en archivo"""
        try:
            summary_file = Path(f"google_cloud_config_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
            
            with open(summary_file, 'w', encoding='utf-8') as f:
                json.dump(summary, f, indent=2, ensure_ascii=False, default=str)
            
            print(f"💾 Resumen guardado: {summary_file}")
            
        except Exception as e:
            print(f"⚠️ Error guardando resumen: {e}")
    
    def show_next_steps(self, summary: Dict):
        """Muestra próximos pasos según estado"""
        print(f"\n🚀 PRÓXIMOS PASOS")
        print("-" * 17)
        
        if summary['success_rate'] >= 100:
            print("🎉 ¡CONFIGURACIÓN COMPLETADA!")
            print("   1. Probar sistema ARIA completo:")
            print("      python aria_google_cloud_integration.py")
            print("   2. Ejecutar servidor ARIA:")
            print("      python backend/src/main_stable.py")
            print("   3. Probar funcionalidades avanzadas:")
            print("      python probar_apis_multilingues.py")
            
        elif summary['success_rate'] >= 33:
            print("⚙️ COMPLETAR CONFIGURACIÓN:")
            print("   1. Habilitar servicios faltantes en Google Cloud Console")
            print("   2. Verificar cuotas y límites de API")
            print("   3. Probar nuevamente: python configurar_clave_google_cloud.py")
            
        else:
            print("🔧 CONFIGURACIÓN INICIAL:")
            print("   1. Verificar clave API en Google Cloud Console")
            print("   2. Habilitar APIs necesarias:")
            for service, description in self.required_services.items():
                print(f"      • {description}")
            print("   3. Verificar configuración de facturación")
    
    def run_full_configuration(self) -> bool:
        """Ejecuta configuración completa"""
        print("🚀 INICIANDO CONFIGURACIÓN COMPLETA")
        print("=" * 37)
        
        success = True
        
        try:
            # Paso 1: Configurar variable de entorno
            if not self.configure_environment_variable():
                success = False
            
            # Paso 2: Probar validez de clave
            test_results = self.test_api_key_validity()
            
            # Paso 3: Integrar con ARIA
            aria_integration = self.integrate_with_aria()
            
            # Paso 4: Generar resumen
            summary = self.create_configuration_summary(test_results)
            
            # Paso 5: Mostrar próximos pasos
            self.show_next_steps(summary)
            
            print(f"\n" + "="*50)
            print(f"📋 CONFIGURACIÓN COMPLETADA")
            print(f"   Estado: {summary['status']}")
            print(f"   Servicios: {summary['services_working']}/{summary['total_services']}")
            print(f"   ARIA Integration: {'✅' if aria_integration else '❌'}")
            print("="*50)
            
            return summary['success_rate'] >= 66 and aria_integration
            
        except KeyboardInterrupt:
            print(f"\n⏹️ Configuración interrumpida por el usuario")
            return False
        except Exception as e:
            print(f"\n❌ Error durante configuración: {e}")
            return False

def main():
    """Función principal"""
    api_key = "AIzaSyASWXk4RX29VhoL2ccwjz0-GtX-jMvCiYo"
    
    print("🎯 Este configurador va a:")
    print("   • Configurar tu clave API de Google Cloud")
    print("   • Probar todos los servicios necesarios")
    print("   • Integrar con el sistema ARIA")
    print("   • Generar reporte de configuración")
    print()
    
    choice = input("¿Continuar con la configuración? (s/n): ").lower()
    
    if choice == 's':
        configurator = GoogleCloudAPIConfigurator(api_key)
        success = configurator.run_full_configuration()
        
        if success:
            print("\n🎉 ¡Configuración exitosa!")
            print("💡 Tu sistema ARIA ahora tiene acceso a Google Cloud APIs premium")
        else:
            print("\n⚠️ Configuración parcial completada")
            print("💡 Revisar recomendaciones arriba")
            
        return success
    else:
        print("👋 Configuración cancelada")
        return False

if __name__ == "__main__":
    main()