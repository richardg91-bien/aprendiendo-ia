#!/usr/bin/env python3
"""
📋 VERIFICACIÓN COMPLETA: GOOGLE CLOUD API KEYS CLIENT + ARIA
============================================================

Verifica la instalación y configuración completa del cliente oficial
de Google Cloud API Keys integrado con el sistema ARIA.

Incluye:
✅ Verificación de google-cloud-api-keys
✅ Estado de autenticación y credenciales
✅ Integración con sistema ARIA existente
✅ Pruebas de funcionalidad
✅ Diagnóstico de problemas comunes

Basado en documentación oficial de Google Cloud
Fecha: 22 de octubre de 2025
"""

import sys
import os
import subprocess
import json
import logging
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional

# Configurar logging básico
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

class GoogleCloudAriaVerificator:
    """Verificador completo de Google Cloud + ARIA"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.verification_results = {}
        self.recommendations = []
        
        print("🔍 VERIFICADOR GOOGLE CLOUD API KEYS CLIENT + ARIA")
        print("=" * 55)
        print(f"Iniciado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()
    
    def verify_python_environment(self) -> Dict:
        """Verifica entorno Python y dependencias"""
        print("🐍 VERIFICANDO ENTORNO PYTHON")
        print("-" * 32)
        
        results = {
            'python_version': None,
            'virtual_env': False,
            'pip_available': False,
            'packages_installed': {}
        }
        
        # Verificar versión de Python
        python_version = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
        results['python_version'] = python_version
        
        print(f"   Python: {python_version}")
        
        if sys.version_info >= (3, 7):
            print("   ✅ Versión compatible (>=3.7)")
        else:
            print("   ❌ Versión no compatible (requiere >=3.7)")
            self.recommendations.append("Actualizar Python a versión 3.7 o superior")
        
        # Verificar entorno virtual
        in_venv = hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix)
        results['virtual_env'] = in_venv
        
        if in_venv:
            print(f"   ✅ Entorno virtual activo: {sys.prefix}")
        else:
            print("   ⚠️ No se detectó entorno virtual")
            self.recommendations.append("Usar entorno virtual para aislamiento de dependencias")
        
        # Verificar pip
        try:
            import pip
            results['pip_available'] = True
            print("   ✅ pip disponible")
        except ImportError:
            results['pip_available'] = False
            print("   ❌ pip no disponible")
        
        # Verificar paquetes instalados
        packages_to_check = [
            'google-cloud-api-keys',
            'google-auth',
            'google-auth-oauthlib',
            'google-auth-httplib2',
            'grpcio',
            'requests'
        ]
        
        print("   📦 Paquetes Google Cloud:")
        for package in packages_to_check:
            try:
                result = subprocess.run([
                    sys.executable, '-m', 'pip', 'show', package
                ], capture_output=True, text=True, timeout=10)
                
                if result.returncode == 0:
                    # Extraer versión
                    for line in result.stdout.split('\n'):
                        if line.startswith('Version:'):
                            version = line.split(':', 1)[1].strip()
                            results['packages_installed'][package] = version
                            print(f"      ✅ {package}: {version}")
                            break
                    else:
                        results['packages_installed'][package] = "installed"
                        print(f"      ✅ {package}: instalado")
                else:
                    results['packages_installed'][package] = None
                    print(f"      ❌ {package}: no instalado")
                    
            except Exception as e:
                results['packages_installed'][package] = None
                print(f"      ⚠️ {package}: error verificando")
        
        return results
    
    def verify_google_cloud_client(self) -> Dict:
        """Verifica cliente de Google Cloud API Keys"""
        print(f"\n🔑 VERIFICANDO GOOGLE CLOUD API KEYS CLIENT")
        print("-" * 45)
        
        results = {
            'import_methods': {},
            'client_available': False,
            'auth_available': False,
            'credentials_configured': False
        }
        
        # Probar diferentes métodos de importación
        import_methods = [
            ('google.cloud.apikeys_v1', 'from google.cloud import apikeys_v1'),
            ('google.cloud.api_keys.v1', 'from google.cloud.api_keys import v1'),
            ('google.cloud.api_keys_v1', 'from google.cloud import api_keys_v1')
        ]
        
        print("   📥 Métodos de importación:")
        
        for module_name, import_statement in import_methods:
            try:
                exec(import_statement)
                results['import_methods'][module_name] = True
                print(f"      ✅ {module_name}: disponible")
            except ImportError as e:
                results['import_methods'][module_name] = False
                print(f"      ❌ {module_name}: {str(e)[:50]}...")
        
        # Verificar si algún método de importación funcionó
        if any(results['import_methods'].values()):
            results['client_available'] = True
            print("   ✅ Cliente API Keys disponible")
        else:
            print("   ❌ Cliente API Keys no disponible")
            self.recommendations.append("Verificar instalación: pip install google-cloud-api-keys")
        
        # Verificar autenticación
        print("   🔐 Autenticación:")
        try:
            import google.auth
            credentials, project = google.auth.default()
            
            results['auth_available'] = True
            print("      ✅ Módulo google.auth disponible")
            
            if credentials:
                results['credentials_configured'] = True
                print(f"      ✅ Credenciales configuradas")
                print(f"      📊 Proyecto: {project or 'No detectado'}")
            else:
                print("      ⚠️ Credenciales no configuradas")
                self.recommendations.append("Configurar credenciales: gcloud auth application-default login")
                
        except ImportError:
            results['auth_available'] = False
            print("      ❌ google.auth no disponible")
        except Exception as e:
            print(f"      ⚠️ Error en autenticación: {str(e)[:50]}...")
            self.recommendations.append("Configurar credenciales de Google Cloud")
        
        return results
    
    def verify_aria_integration(self) -> Dict:
        """Verifica integración con sistema ARIA"""
        print(f"\n🤖 VERIFICANDO INTEGRACIÓN CON ARIA")
        print("-" * 36)
        
        results = {
            'auto_learning_available': False,
            'config_files_found': [],
            'google_cloud_apis_available': False,
            'multilingual_apis_available': False
        }
        
        # Verificar sistema de aprendizaje avanzado
        print("   🧠 Sistema de aprendizaje:")
        try:
            sys.path.append('backend/src')
            from auto_learning_advanced import aria_advanced_learning
            
            results['auto_learning_available'] = True
            print("      ✅ auto_learning_advanced disponible")
            
            # Probar status
            try:
                status = aria_advanced_learning.get_status()
                knowledge_count = status.get('total_knowledge', 0)
                confidence = status.get('confidence', 0)
                
                print(f"      📊 Conocimiento: {knowledge_count} elementos")
                print(f"      📈 Confianza: {confidence:.1f}%")
                
            except Exception as e:
                print(f"      ⚠️ Error obteniendo status: {str(e)[:30]}...")
                
        except ImportError:
            print("      ❌ auto_learning_advanced no disponible")
            self.recommendations.append("Verificar ruta del sistema de aprendizaje ARIA")
        
        # Verificar archivos de configuración
        print("   ⚙️ Archivos de configuración:")
        config_files = [
            'config/settings.py',
            'backend/config/settings.py', 
            'backend/src/google_cloud_apis.py',
            'aria_google_cloud_integration.py'
        ]
        
        for config_file in config_files:
            if Path(config_file).exists():
                results['config_files_found'].append(config_file)
                print(f"      ✅ {config_file}")
            else:
                print(f"      ❌ {config_file}")
        
        # Verificar APIs de Google Cloud
        print("   ☁️ APIs de Google Cloud:")
        try:
            sys.path.append('backend/src')
            import google_cloud_apis
            
            results['google_cloud_apis_available'] = True
            print("      ✅ google_cloud_apis.py disponible")
            
        except ImportError:
            print("      ❌ google_cloud_apis.py no disponible")
        
        # Verificar APIs multilingües
        print("   🌐 APIs multilingües:")
        try:
            import multilingual_apis_free
            results['multilingual_apis_available'] = True
            print("      ✅ multilingual_apis_free disponible")
            
        except ImportError:
            print("      ❌ multilingual_apis_free no disponible")
        
        return results
    
    def verify_gcloud_cli(self) -> Dict:
        """Verifica gcloud CLI y configuración"""
        print(f"\n⚡ VERIFICANDO GCLOUD CLI")
        print("-" * 25)
        
        results = {
            'gcloud_installed': False,
            'gcloud_version': None,
            'authenticated': False,
            'project_configured': False,
            'current_project': None
        }
        
        # Verificar instalación de gcloud
        try:
            result = subprocess.run(['gcloud', '--version'], 
                                  capture_output=True, text=True, timeout=10)
            
            if result.returncode == 0:
                results['gcloud_installed'] = True
                # Extraer versión
                for line in result.stdout.split('\n'):
                    if 'Google Cloud SDK' in line:
                        results['gcloud_version'] = line.strip()
                        print(f"   ✅ gcloud CLI instalado: {line.strip()}")
                        break
                
                # Verificar autenticación
                try:
                    auth_result = subprocess.run(['gcloud', 'auth', 'list'], 
                                               capture_output=True, text=True, timeout=10)
                    
                    if auth_result.returncode == 0 and 'ACTIVE' in auth_result.stdout:
                        results['authenticated'] = True
                        print("   ✅ Usuario autenticado")
                    else:
                        print("   ⚠️ Usuario no autenticado")
                        self.recommendations.append("Autenticar con: gcloud auth login")
                        
                except Exception:
                    print("   ⚠️ No se pudo verificar autenticación")
                
                # Verificar proyecto configurado
                try:
                    project_result = subprocess.run(['gcloud', 'config', 'get-value', 'project'], 
                                                  capture_output=True, text=True, timeout=10)
                    
                    if project_result.returncode == 0 and project_result.stdout.strip():
                        project = project_result.stdout.strip()
                        if project != '(unset)':
                            results['project_configured'] = True
                            results['current_project'] = project
                            print(f"   ✅ Proyecto configurado: {project}")
                        else:
                            print("   ⚠️ Proyecto no configurado")
                            self.recommendations.append("Configurar proyecto: gcloud config set project TU_PROJECT_ID")
                    else:
                        print("   ⚠️ No se pudo obtener proyecto")
                        
                except Exception:
                    print("   ⚠️ Error verificando proyecto")
            else:
                print("   ❌ gcloud CLI no responde correctamente")
                
        except FileNotFoundError:
            results['gcloud_installed'] = False
            print("   ❌ gcloud CLI no instalado")
            self.recommendations.append("Instalar gcloud CLI: https://cloud.google.com/sdk/docs/install")
        except subprocess.TimeoutExpired:
            print("   ❌ gcloud CLI timeout")
        except Exception as e:
            print(f"   ❌ Error verificando gcloud: {str(e)[:30]}...")
        
        return results
    
    def run_integration_tests(self) -> Dict:
        """Ejecuta pruebas de integración"""
        print(f"\n🧪 EJECUTANDO PRUEBAS DE INTEGRACIÓN")
        print("-" * 37)
        
        results = {
            'aria_google_cloud_test': False,
            'example_execution': False,
            'config_creation': False
        }
        
        # Prueba 1: Importar integración ARIA Google Cloud
        print("   🔗 Prueba integración ARIA-Google Cloud:")
        try:
            from aria_google_cloud_integration import aria_google_cloud
            results['aria_google_cloud_test'] = True
            print("      ✅ Integración importada exitosamente")
            
            # Probar obtener estado
            try:
                status = aria_google_cloud.get_enhanced_services_status()
                google_available = status.get('google_cloud', {}).get('available', False)
                aria_available = status.get('aria_integration', {}).get('learning_system', False)
                
                print(f"      📊 Google Cloud: {'✅' if google_available else '❌'}")
                print(f"      📊 ARIA Learning: {'✅' if aria_available else '❌'}")
                
            except Exception as e:
                print(f"      ⚠️ Error obteniendo estado: {str(e)[:30]}...")
                
        except ImportError as e:
            print(f"      ❌ Error importando: {str(e)[:50]}...")
        
        # Prueba 2: Ejecutar ejemplo
        print("   📄 Prueba ejemplo de uso:")
        if Path("ejemplo_google_cloud_api_keys.py").exists():
            print("      ✅ Archivo de ejemplo encontrado")
            results['example_execution'] = True
            
            # Intentar verificar sintaxis
            try:
                with open("ejemplo_google_cloud_api_keys.py", 'r', encoding='utf-8') as f:
                    content = f.read()
                
                compile(content, "ejemplo_google_cloud_api_keys.py", 'exec')
                print("      ✅ Sintaxis del ejemplo válida")
                
            except SyntaxError as e:
                print(f"      ⚠️ Error sintaxis: {str(e)[:30]}...")
            except Exception as e:
                print(f"      ⚠️ Error verificando ejemplo: {str(e)[:30]}...")
        else:
            print("      ❌ Archivo de ejemplo no encontrado")
        
        # Prueba 3: Verificar configuraciones creadas
        print("   ⚙️ Prueba archivos de configuración:")
        config_files = [
            "backend/requirements.txt",
            "aria_google_cloud_integration.py",
            "instalar_google_cloud_client.py"
        ]
        
        files_found = 0
        for config_file in config_files:
            if Path(config_file).exists():
                files_found += 1
                print(f"      ✅ {config_file}")
            else:
                print(f"      ❌ {config_file}")
        
        if files_found >= 2:
            results['config_creation'] = True
        
        return results
    
    def generate_report(self) -> Dict:
        """Genera reporte completo de verificación"""
        print(f"\n📊 GENERANDO REPORTE COMPLETO")
        print("-" * 30)
        
        # Ejecutar todas las verificaciones
        verification_data = {
            'timestamp': datetime.now().isoformat(),
            'python_env': self.verify_python_environment(),
            'google_cloud_client': self.verify_google_cloud_client(),
            'aria_integration': self.verify_aria_integration(),
            'gcloud_cli': self.verify_gcloud_cli(),
            'integration_tests': self.run_integration_tests()
        }
        
        # Calcular puntuación general
        scores = []
        
        # Python Environment (20%)
        python_score = 0
        if verification_data['python_env']['python_version']:
            python_score += 25
        if verification_data['python_env']['virtual_env']:
            python_score += 25
        google_packages = len([p for p in verification_data['python_env']['packages_installed'].values() if p])
        python_score += min(50, google_packages * 8)  # Máximo 50 por paquetes
        scores.append(('Python Environment', python_score, 20))
        
        # Google Cloud Client (25%)
        client_score = 0
        if any(verification_data['google_cloud_client']['import_methods'].values()):
            client_score += 50
        if verification_data['google_cloud_client']['auth_available']:
            client_score += 30
        if verification_data['google_cloud_client']['credentials_configured']:
            client_score += 20
        scores.append(('Google Cloud Client', client_score, 25))
        
        # ARIA Integration (25%)
        aria_score = 0
        if verification_data['aria_integration']['auto_learning_available']:
            aria_score += 40
        aria_score += len(verification_data['aria_integration']['config_files_found']) * 15
        if verification_data['aria_integration']['google_cloud_apis_available']:
            aria_score += 30
        scores.append(('ARIA Integration', min(100, aria_score), 25))
        
        # gcloud CLI (15%)
        gcloud_score = 0
        if verification_data['gcloud_cli']['gcloud_installed']:
            gcloud_score += 40
        if verification_data['gcloud_cli']['authenticated']:
            gcloud_score += 30
        if verification_data['gcloud_cli']['project_configured']:
            gcloud_score += 30
        scores.append(('gcloud CLI', gcloud_score, 15))
        
        # Integration Tests (15%)
        tests_score = 0
        test_results = verification_data['integration_tests']
        if test_results['aria_google_cloud_test']:
            tests_score += 40
        if test_results['example_execution']:
            tests_score += 30
        if test_results['config_creation']:
            tests_score += 30
        scores.append(('Integration Tests', tests_score, 15))
        
        # Calcular puntuación final
        final_score = sum(score * weight / 100 for _, score, weight in scores)
        
        # Determinar estado general
        if final_score >= 80:
            status = "🎉 EXCELENTE"
            color = "Verde"
        elif final_score >= 60:
            status = "✅ BUENO"
            color = "Amarillo"
        elif final_score >= 40:
            status = "⚠️ PARCIAL"
            color = "Naranja"
        else:
            status = "❌ NECESITA TRABAJO"
            color = "Rojo"
        
        report = {
            'verification_data': verification_data,
            'scores': scores,
            'final_score': final_score,
            'status': status,
            'color': color,
            'recommendations': self.recommendations
        }
        
        return report
    
    def print_report(self, report: Dict):
        """Imprime reporte formateado"""
        print(f"\n" + "="*60)
        print(f"📋 REPORTE FINAL DE VERIFICACIÓN")
        print(f"="*60)
        
        # Estado general
        print(f"🎯 ESTADO GENERAL: {report['status']}")
        print(f"📊 PUNTUACIÓN: {report['final_score']:.1f}/100")
        print()
        
        # Desglose por categorías
        print(f"📈 DESGLOSE POR CATEGORÍAS:")
        for category, score, weight in report['scores']:
            bar_length = 20
            filled_length = int(bar_length * score / 100)
            bar = '█' * filled_length + '░' * (bar_length - filled_length)
            print(f"   {category:<20} {bar} {score:>3.0f}% (peso {weight}%)")
        
        print()
        
        # Recomendaciones
        if report['recommendations']:
            print(f"💡 RECOMENDACIONES ({len(report['recommendations'])}):")
            for i, rec in enumerate(report['recommendations'], 1):
                print(f"   {i}. {rec}")
            print()
        
        # Próximos pasos
        print(f"🚀 PRÓXIMOS PASOS SUGERIDOS:")
        if report['final_score'] < 40:
            print("   1. Instalar dependencias faltantes")
            print("   2. Configurar gcloud CLI")
            print("   3. Verificar integración ARIA")
        elif report['final_score'] < 60:
            print("   1. Completar configuración de Google Cloud")
            print("   2. Probar ejemplos de uso")
            print("   3. Configurar proyecto y credenciales")
        elif report['final_score'] < 80:
            print("   1. Optimizar configuración existente")
            print("   2. Probar todas las funcionalidades")
            print("   3. Documentar configuración personalizada")
        else:
            print("   1. ¡Sistema listo para producción!")
            print("   2. Explorar funcionalidades avanzadas")
            print("   3. Implementar monitoreo y logging")
        
        print(f"\n📚 DOCUMENTACIÓN:")
        print(f"   • Google Cloud API Keys: https://cloud.google.com/python/docs/reference/apikeys/latest")
        print(f"   • Autenticación: https://cloud.google.com/docs/authentication")
        print(f"   • ARIA Integration: aria_google_cloud_integration.py")
        
        print(f"\n⏰ Reporte generado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*60)
    
    def save_report(self, report: Dict):
        """Guarda reporte en archivo JSON"""
        try:
            report_file = Path(f"google_cloud_verification_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
            
            with open(report_file, 'w', encoding='utf-8') as f:
                json.dump(report, f, indent=2, ensure_ascii=False, default=str)
            
            print(f"💾 Reporte guardado: {report_file}")
            
        except Exception as e:
            print(f"❌ Error guardando reporte: {e}")

def main():
    """Función principal de verificación"""
    verificator = GoogleCloudAriaVerificator()
    
    print("🎯 Este verificador analiza:")
    print("   • Entorno Python y dependencias")
    print("   • Cliente Google Cloud API Keys")
    print("   • Integración con sistema ARIA")
    print("   • Configuración de gcloud CLI")
    print("   • Pruebas de funcionalidad")
    print()
    
    choice = input("¿Ejecutar verificación completa? (s/n): ").lower()
    
    if choice == 's':
        # Generar y mostrar reporte
        report = verificator.generate_report()
        verificator.print_report(report)
        
        # Opción de guardar
        save_choice = input("\n💾 ¿Guardar reporte en archivo JSON? (s/n): ").lower()
        if save_choice == 's':
            verificator.save_report(report)
        
        print(f"\n🎉 ¡Verificación completada!")
        return True
    else:
        print("👋 Verificación cancelada")
        return False

if __name__ == "__main__":
    main()