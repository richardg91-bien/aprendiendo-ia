#!/usr/bin/env python3
"""
🔐 CONFIGURACIÓN AUTOMÁTICA DE GOOGLE CLOUD PARA ARIA
====================================================

Implementación automática basada en la documentación oficial de Google Cloud.
Configura autenticación, permisos y APIs siguiendo las mejores prácticas.

Basado en la documentación oficial:
- https://cloud.google.com/docs/authentication/application-default-credentials
- Roles: serviceusage.apiKeysAdmin, serviceusage.serviceUsageViewer
- Políticas de organización para vinculación de cuentas de servicio

Fecha: 22 de octubre de 2025
"""

import os
import sys
import subprocess
import json
import time
from pathlib import Path
from typing import Dict, List, Optional

class GoogleCloudSetupAutomator:
    """Automatizador de configuración de Google Cloud para ARIA"""
    
    def __init__(self):
        self.gcloud_installed = False
        self.authenticated = False
        self.project_configured = False
        self.apis_enabled = False
        self.credentials_configured = False
        
        # APIs requeridas para ARIA
        self.required_apis = [
            'language.googleapis.com',      # Natural Language API
            'translate.googleapis.com',     # Translation API
            'serviceusage.googleapis.com'   # Service Usage API
        ]
        
        # Roles requeridos según documentación oficial
        self.required_roles = [
            'roles/serviceusage.apiKeysAdmin',
            'roles/serviceusage.serviceUsageViewer'
        ]
        
        self.setup_log = []
        print("🔐 Configurador automático de Google Cloud iniciado")
    
    def log_step(self, message: str, success: bool = True):
        """Registra paso de configuración"""
        icon = "✅" if success else "❌"
        log_entry = f"{icon} {message}"
        print(log_entry)
        self.setup_log.append(log_entry)
    
    def check_gcloud_cli(self) -> bool:
        """Verifica si gcloud CLI está instalado"""
        try:
            result = subprocess.run(['gcloud', 'version'], 
                                  capture_output=True, text=True, timeout=10)
            
            if result.returncode == 0:
                self.gcloud_installed = True
                version_info = result.stdout.split('\n')[0]
                self.log_step(f"Google Cloud CLI detectado: {version_info}")
                return True
            else:
                self.log_step("Google Cloud CLI no encontrado", False)
                return False
                
        except (subprocess.TimeoutExpired, FileNotFoundError):
            self.log_step("Google Cloud CLI no instalado", False)
            return False
    
    def install_gcloud_cli_guide(self):
        """Muestra guía para instalar gcloud CLI"""
        print("\n📥 INSTALACIÓN DE GOOGLE CLOUD CLI")
        print("-" * 40)
        print("1. 🌐 Descargar desde: https://cloud.google.com/sdk/docs/install")
        print("2. 💻 Ejecutar el instalador para Windows")
        print("3. 🔄 Reiniciar terminal después de la instalación")
        print("4. ✅ Verificar con: gcloud version")
        print()
        
        choice = input("¿Has instalado gcloud CLI? (s/n): ").lower()
        if choice == 's':
            return self.check_gcloud_cli()
        return False
    
    def authenticate_gcloud(self) -> bool:
        """Autentica con Google Cloud según documentación oficial"""
        try:
            print("\n🔐 CONFIGURANDO AUTENTICACIÓN...")
            print("-" * 35)
            
            # Paso 1: Autenticación básica del usuario
            print("🔑 Paso 1: Autenticación de usuario")
            print("   Ejecutando: gcloud auth login")
            
            auth_result = subprocess.run(['gcloud', 'auth', 'login'], 
                                       timeout=120)
            
            if auth_result.returncode != 0:
                self.log_step("Error en autenticación de usuario", False)
                return False
            
            self.log_step("Usuario autenticado correctamente")
            
            # Paso 2: Configurar Application Default Credentials (ADC)
            print("\n🔑 Paso 2: Configurando Application Default Credentials")
            print("   Ejecutando: gcloud auth application-default login")
            
            adc_result = subprocess.run(['gcloud', 'auth', 'application-default', 'login'], 
                                      timeout=120)
            
            if adc_result.returncode == 0:
                self.log_step("Application Default Credentials configuradas")
                self.authenticated = True
                self.credentials_configured = True
                return True
            else:
                self.log_step("Error configurando ADC", False)
                return False
                
        except subprocess.TimeoutExpired:
            self.log_step("Timeout en autenticación", False)
            return False
        except Exception as e:
            self.log_step(f"Error en autenticación: {e}", False)
            return False
    
    def configure_project(self) -> bool:
        """Configura proyecto de Google Cloud"""
        try:
            # Listar proyectos disponibles
            print("\n📋 CONFIGURACIÓN DE PROYECTO")
            print("-" * 30)
            
            projects_result = subprocess.run(['gcloud', 'projects', 'list'], 
                                           capture_output=True, text=True, timeout=15)
            
            if projects_result.returncode == 0:
                print("📁 Proyectos disponibles:")
                print(projects_result.stdout)
                
                project_id = input("\n🔍 Ingresa el PROJECT_ID a usar (o presiona Enter para crear nuevo): ").strip()
                
                if not project_id:
                    return self.create_new_project()
                
                # Configurar proyecto seleccionado
                config_result = subprocess.run(['gcloud', 'config', 'set', 'project', project_id], 
                                             capture_output=True, text=True, timeout=10)
                
                if config_result.returncode == 0:
                    self.log_step(f"Proyecto configurado: {project_id}")
                    
                    # Configurar variable de entorno
                    os.environ['GOOGLE_CLOUD_PROJECT'] = project_id
                    self.set_environment_variable('GOOGLE_CLOUD_PROJECT', project_id)
                    
                    self.project_configured = True
                    return True
                else:
                    self.log_step(f"Error configurando proyecto: {config_result.stderr}", False)
                    return False
            else:
                self.log_step("Error listando proyectos", False)
                return False
                
        except Exception as e:
            self.log_step(f"Error en configuración de proyecto: {e}", False)
            return False
    
    def create_new_project(self) -> bool:
        """Crea nuevo proyecto de Google Cloud"""
        try:
            project_id = input("🆕 Ingresa un ID para el nuevo proyecto (formato: aria-project-12345): ").strip()
            
            if not project_id:
                self.log_step("ID de proyecto vacío", False)
                return False
            
            # Crear proyecto
            create_result = subprocess.run(['gcloud', 'projects', 'create', project_id], 
                                         capture_output=True, text=True, timeout=30)
            
            if create_result.returncode == 0:
                self.log_step(f"Proyecto creado: {project_id}")
                
                # Configurar como proyecto activo
                subprocess.run(['gcloud', 'config', 'set', 'project', project_id], timeout=10)
                
                os.environ['GOOGLE_CLOUD_PROJECT'] = project_id
                self.set_environment_variable('GOOGLE_CLOUD_PROJECT', project_id)
                
                self.project_configured = True
                return True
            else:
                self.log_step(f"Error creando proyecto: {create_result.stderr}", False)
                return False
                
        except Exception as e:
            self.log_step(f"Error creando proyecto: {e}", False)
            return False
    
    def enable_required_apis(self) -> bool:
        """Habilita APIs requeridas para ARIA"""
        try:
            print("\n🔌 HABILITANDO APIs REQUERIDAS...")
            print("-" * 35)
            
            apis_enabled = 0
            
            for api in self.required_apis:
                print(f"🔄 Habilitando {api}...")
                
                enable_result = subprocess.run(['gcloud', 'services', 'enable', api], 
                                             capture_output=True, text=True, timeout=30)
                
                if enable_result.returncode == 0:
                    self.log_step(f"API habilitada: {api}")
                    apis_enabled += 1
                else:
                    self.log_step(f"Error habilitando {api}: {enable_result.stderr}", False)
            
            if apis_enabled == len(self.required_apis):
                self.apis_enabled = True
                self.log_step(f"Todas las APIs habilitadas ({apis_enabled}/{len(self.required_apis)})")
                return True
            else:
                self.log_step(f"APIs parcialmente habilitadas ({apis_enabled}/{len(self.required_apis)})", False)
                return apis_enabled > 0
                
        except Exception as e:
            self.log_step(f"Error habilitando APIs: {e}", False)
            return False
    
    def create_api_key(self) -> Optional[str]:
        """Crea clave API siguiendo mejores prácticas"""
        try:
            print("\n🔑 CREANDO CLAVE API...")
            print("-" * 25)
            
            # Crear clave API con restricciones
            api_key_name = f"aria-api-key-{int(time.time())}"
            
            create_key_result = subprocess.run([
                'gcloud', 'alpha', 'services', 'api-keys', 'create',
                '--display-name', api_key_name,
                '--api-target', 'service=language.googleapis.com',
                '--api-target', 'service=translate.googleapis.com'
            ], capture_output=True, text=True, timeout=30)
            
            if create_key_result.returncode == 0:
                # Extraer la clave del output
                output_lines = create_key_result.stdout.split('\n')
                api_key = None
                
                for line in output_lines:
                    if 'keyString:' in line:
                        api_key = line.split('keyString:')[1].strip()
                        break
                
                if api_key:
                    self.log_step(f"Clave API creada: {api_key[:10]}...{api_key[-4:]}")
                    
                    # Configurar variable de entorno
                    os.environ['GOOGLE_CLOUD_API_KEY'] = api_key
                    self.set_environment_variable('GOOGLE_CLOUD_API_KEY', api_key)
                    
                    return api_key
                else:
                    self.log_step("Error extrayendo clave API", False)
                    return None
            else:
                # Método alternativo: crear clave básica
                return self.create_basic_api_key()
                
        except Exception as e:
            self.log_step(f"Error creando clave API: {e}", False)
            return None
    
    def create_basic_api_key(self) -> Optional[str]:
        """Método alternativo para crear clave API básica"""
        print("\n🔄 Intentando método alternativo para clave API...")
        print("   💡 Ve a: https://console.cloud.google.com/apis/credentials")
        print("   📝 Haz clic en 'Create Credentials' → 'API Key'")
        print("   📋 Copia la clave generada")
        
        api_key = input("\n🔑 Pega tu clave API aquí: ").strip()
        
        if api_key and len(api_key) > 20:
            os.environ['GOOGLE_CLOUD_API_KEY'] = api_key
            self.set_environment_variable('GOOGLE_CLOUD_API_KEY', api_key)
            self.log_step(f"Clave API configurada manualmente: {api_key[:10]}...{api_key[-4:]}")
            return api_key
        else:
            self.log_step("Clave API inválida", False)
            return None
    
    def set_environment_variable(self, var_name: str, var_value: str):
        """Configura variable de entorno permanente en Windows"""
        try:
            # Usar setx para configuración permanente
            subprocess.run(['setx', var_name, var_value], 
                          capture_output=True, timeout=10)
            self.log_step(f"Variable de entorno configurada: {var_name}")
            
        except Exception as e:
            self.log_step(f"Error configurando variable {var_name}: {e}", False)
    
    def verify_setup(self) -> bool:
        """Verifica que la configuración esté completa"""
        print("\n🧪 VERIFICANDO CONFIGURACIÓN...")
        print("-" * 30)
        
        verification_results = {}
        
        # Verificar autenticación
        try:
            auth_check = subprocess.run(['gcloud', 'auth', 'list', '--filter=status:ACTIVE'], 
                                      capture_output=True, text=True, timeout=10)
            verification_results['auth'] = auth_check.returncode == 0 and auth_check.stdout.strip()
        except:
            verification_results['auth'] = False
        
        # Verificar proyecto
        try:
            project_check = subprocess.run(['gcloud', 'config', 'get-value', 'project'], 
                                         capture_output=True, text=True, timeout=10)
            verification_results['project'] = project_check.returncode == 0 and project_check.stdout.strip()
        except:
            verification_results['project'] = False
        
        # Verificar APIs
        try:
            for api in self.required_apis:
                api_check = subprocess.run(['gcloud', 'services', 'list', '--enabled', 
                                          '--filter', f'name:{api}'], 
                                         capture_output=True, text=True, timeout=10)
                verification_results[f'api_{api}'] = api in api_check.stdout
        except:
            verification_results.update({f'api_{api}': False for api in self.required_apis})
        
        # Verificar variables de entorno
        verification_results['env_project'] = bool(os.getenv('GOOGLE_CLOUD_PROJECT'))
        verification_results['env_api_key'] = bool(os.getenv('GOOGLE_CLOUD_API_KEY'))
        
        # Mostrar resultados
        for check, result in verification_results.items():
            self.log_step(f"{check}: {'Configurado' if result else 'Pendiente'}", result)
        
        # Determinar éxito general
        critical_checks = ['auth', 'project', 'env_api_key']
        success = all(verification_results.get(check, False) for check in critical_checks)
        
        return success
    
    def test_apis(self) -> bool:
        """Prueba las APIs configuradas con ARIA"""
        try:
            print("\n🧪 PROBANDO INTEGRACIÓN CON ARIA...")
            print("-" * 35)
            
            # Importar y probar sistema de ARIA
            sys.path.append(os.path.join(os.path.dirname(__file__), 'backend', 'src'))
            from google_cloud_apis import google_cloud_apis
            
            # Probar análisis de sentimientos
            test_text = "Google Cloud integration with ARIA is working perfectly!"
            sentiment_result = google_cloud_apis.analyze_sentiment_advanced(test_text)
            
            if not sentiment_result.get('note'):  # Si no hay nota de error
                self.log_step("Natural Language API: Funcional")
                
                # Probar traducción
                translation_result = google_cloud_apis.translate_text_google(test_text, target_lang='es')
                
                if not translation_result.get('note'):
                    self.log_step("Translation API: Funcional")
                    self.log_step(f"Traducción de prueba: {translation_result.get('translated_text', '')[:50]}...")
                    return True
                else:
                    self.log_step("Translation API: Error", False)
            else:
                self.log_step("Natural Language API: Error", False)
            
            return False
            
        except ImportError:
            self.log_step("Error: Módulo ARIA no encontrado", False)
            return False
        except Exception as e:
            self.log_step(f"Error probando APIs: {e}", False)
            return False
    
    def generate_setup_summary(self):
        """Genera resumen de configuración"""
        print("\n📋 RESUMEN DE CONFIGURACIÓN")
        print("=" * 40)
        
        for log_entry in self.setup_log:
            print(log_entry)
        
        print(f"\n📊 Estado final:")
        print(f"   • gcloud CLI: {'✅' if self.gcloud_installed else '❌'}")
        print(f"   • Autenticación: {'✅' if self.authenticated else '❌'}")
        print(f"   • Proyecto: {'✅' if self.project_configured else '❌'}")
        print(f"   • APIs habilitadas: {'✅' if self.apis_enabled else '❌'}")
        print(f"   • Credenciales: {'✅' if self.credentials_configured else '❌'}")
        
        if all([self.gcloud_installed, self.authenticated, self.project_configured]):
            print(f"\n🎉 ¡Configuración completada exitosamente!")
            print(f"💡 Próximos pasos:")
            print(f"   1. Reiniciar terminal para aplicar variables de entorno")
            print(f"   2. Ejecutar: python prueba_respuestas_inteligentes.py")
            print(f"   3. Probar: python aria_servidor_multilingue.py")
        else:
            print(f"\n⚠️ Configuración incompleta. Revisar pasos fallidos.")
    
    def run_full_setup(self) -> bool:
        """Ejecuta configuración completa automatizada"""
        print("🚀 INICIANDO CONFIGURACIÓN AUTOMÁTICA DE GOOGLE CLOUD")
        print("=" * 60)
        
        # Paso 1: Verificar gcloud CLI
        if not self.check_gcloud_cli():
            if not self.install_gcloud_cli_guide():
                return False
        
        # Paso 2: Autenticación
        if not self.authenticate_gcloud():
            return False
        
        # Paso 3: Configurar proyecto
        if not self.configure_project():
            return False
        
        # Paso 4: Habilitar APIs
        if not self.enable_required_apis():
            return False
        
        # Paso 5: Crear clave API
        if not self.create_api_key():
            return False
        
        # Paso 6: Verificar configuración
        setup_success = self.verify_setup()
        
        # Paso 7: Probar integración con ARIA
        if setup_success:
            self.test_apis()
        
        # Paso 8: Generar resumen
        self.generate_setup_summary()
        
        return setup_success

def main():
    """Función principal del configurador automático"""
    try:
        configurator = GoogleCloudSetupAutomator()
        
        print("🎯 Este configurador automatizará:")
        print("   • Instalación/verificación de gcloud CLI")
        print("   • Autenticación con Google Cloud")
        print("   • Configuración de proyecto")
        print("   • Habilitación de APIs requeridas")
        print("   • Creación de claves API")
        print("   • Configuración de variables de entorno")
        print("   • Pruebas de integración con ARIA")
        print()
        
        choice = input("¿Continuar con la configuración automática? (s/n): ").lower()
        
        if choice == 's':
            success = configurator.run_full_setup()
            
            if success:
                print("\n🎉 ¡Configuración completada exitosamente!")
                return True
            else:
                print("\n⚠️ Configuración incompleta. Revisar errores arriba.")
                return False
        else:
            print("👋 Configuración cancelada por el usuario")
            return False
            
    except KeyboardInterrupt:
        print("\n⏹️ Configuración interrumpida por el usuario")
        return False
    except Exception as e:
        print(f"\n❌ Error durante la configuración: {e}")
        return False

if __name__ == "__main__":
    main()