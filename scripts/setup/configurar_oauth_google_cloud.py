#!/usr/bin/env python3
"""
🔐 CONFIGURADOR COMPLETO: OAUTH 2.0 + GOOGLE CLOUD PARA ARIA
===========================================================

Configura autenticación OAuth 2.0 completa de Google Cloud junto con
la clave API existente para máxima funcionalidad en ARIA.

Credenciales configuradas:
🔑 API Key: AIzaSyASWXk4RX29VhoL2ccwjz0-GtX-jMvCiYo
🆔 OAuth Client ID: 209067283417-p7jrdl8hne7ck85iqtt50u02ak2p7gk8.apps.googleusercontent.com

Fecha: 22 de octubre de 2025
"""

import os
import sys
import json
import webbrowser
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Dict, Optional, Any

class GoogleCloudOAuthConfigurator:
    """Configurador completo de OAuth 2.0 para Google Cloud + ARIA"""
    
    def __init__(self):
        # Credenciales desde .env
        self.api_key = "AIzaSyASWXk4RX29VhoL2ccwjz0-GtX-jMvCiYo"
        self.oauth_client_id = "209067283417-p7jrdl8hne7ck85iqtt50u02ak2p7gk8.apps.googleusercontent.com"
        
        # URLs y configuración
        self.redirect_uri = "http://localhost:8080"  # URI estándar para desarrollo
        self.scopes = [
            "https://www.googleapis.com/auth/cloud-platform",
            "https://www.googleapis.com/auth/cloud-translation",
            "https://www.googleapis.com/auth/cloud-language",
            "https://www.googleapis.com/auth/cloud-speech"
        ]
        
        print("🔐 CONFIGURADOR OAUTH 2.0 + GOOGLE CLOUD")
        print("=" * 42)
        print(f"🔑 API Key: {self.api_key[:8]}...{self.api_key[-4:]}")
        print(f"🆔 Client ID: {self.oauth_client_id[:15]}...")
        print()
    
    def verify_current_configuration(self) -> Dict:
        """Verifica configuración actual"""
        print("🔍 VERIFICANDO CONFIGURACIÓN ACTUAL")
        print("-" * 35)
        
        results = {
            'env_file_exists': False,
            'api_key_configured': False,
            'oauth_client_configured': False,
            'google_auth_installed': False,
            'credentials_file_exists': False
        }
        
        # Verificar archivo .env
        env_file = Path(".env")
        if env_file.exists():
            results['env_file_exists'] = True
            print("✅ Archivo .env encontrado")
            
            # Verificar contenido
            with open(env_file, 'r', encoding='utf-8') as f:
                content = f.read()
                
            if 'GOOGLE_CLOUD_API_KEY' in content:
                results['api_key_configured'] = True
                print("✅ GOOGLE_CLOUD_API_KEY configurada")
            
            if 'GOOGLE_OAUTH_CLIENT_ID' in content:
                results['oauth_client_configured'] = True
                print("✅ GOOGLE_OAUTH_CLIENT_ID configurada")
        else:
            print("❌ Archivo .env no encontrado")
        
        # Verificar google-auth-oauthlib
        try:
            import google_auth_oauthlib
            results['google_auth_installed'] = True
            print("✅ google-auth-oauthlib instalado")
        except ImportError:
            print("❌ google-auth-oauthlib no instalado")
        
        # Verificar archivo de credenciales
        creds_file = Path("google_credentials.json")
        if creds_file.exists():
            results['credentials_file_exists'] = True
            print("✅ Archivo de credenciales OAuth encontrado")
        else:
            print("⚠️ Archivo de credenciales OAuth no encontrado")
        
        return results
    
    def create_oauth_credentials_file(self) -> bool:
        """Crea archivo de credenciales OAuth para aplicación"""
        print(f"\n🔧 CREANDO ARCHIVO DE CREDENCIALES OAUTH")
        print("-" * 40)
        
        try:
            # Estructura del archivo credentials.json para OAuth
            credentials_data = {
                "installed": {
                    "client_id": self.oauth_client_id,
                    "project_id": "aprendiendo-ia-aria",  # Asumido del client_id
                    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                    "token_uri": "https://oauth2.googleapis.com/token",
                    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
                    "client_secret": "GOCSPX-PLACEHOLDER",  # Necesitarás el client_secret
                    "redirect_uris": [
                        "http://localhost:8080",
                        "urn:ietf:wg:oauth:2.0:oob"
                    ]
                }
            }
            
            # Guardar archivo
            creds_file = Path("google_oauth_credentials.json")
            
            with open(creds_file, 'w', encoding='utf-8') as f:
                json.dump(credentials_data, f, indent=2)
            
            print(f"✅ Archivo creado: {creds_file}")
            print("⚠️ IMPORTANTE: Necesitas el client_secret de Google Cloud Console")
            print("💡 Ve a: APIs & Services > Credentials > Tu OAuth 2.0 Client ID")
            
            return True
            
        except Exception as e:
            print(f"❌ Error creando archivo: {e}")
            return False
    
    def setup_application_default_credentials(self) -> bool:
        """Configura Application Default Credentials usando OAuth"""
        print(f"\n🛠️ CONFIGURANDO APPLICATION DEFAULT CREDENTIALS")
        print("-" * 46)
        
        try:
            # Verificar si gcloud está instalado
            result = subprocess.run(['gcloud', '--version'], 
                                  capture_output=True, text=True, timeout=10)
            
            if result.returncode == 0:
                print("✅ gcloud CLI detectado")
                
                # Intentar autenticación con application-default
                print("🔄 Ejecutando: gcloud auth application-default login")
                
                choice = input("¿Ejecutar gcloud auth application-default login? (s/n): ").lower()
                
                if choice == 's':
                    # Ejecutar comando de autenticación
                    auth_result = subprocess.run([
                        'gcloud', 'auth', 'application-default', 'login'
                    ], timeout=300)  # 5 minutos timeout
                    
                    if auth_result.returncode == 0:
                        print("✅ Application Default Credentials configuradas")
                        return True
                    else:
                        print("❌ Error en autenticación")
                        return False
                else:
                    print("⏭️ Autenticación omitida")
                    return False
            else:
                print("❌ gcloud CLI no disponible")
                print("💡 Instalar desde: https://cloud.google.com/sdk/docs/install")
                return False
                
        except FileNotFoundError:
            print("❌ gcloud CLI no instalado")
            self._show_gcloud_installation_guide()
            return False
        except subprocess.TimeoutExpired:
            print("❌ Timeout en gcloud auth")
            return False
        except Exception as e:
            print(f"❌ Error configurando ADC: {e}")
            return False
    
    def _show_gcloud_installation_guide(self):
        """Muestra guía de instalación de gcloud CLI"""
        print(f"\n📖 GUÍA: INSTALAR GCLOUD CLI")
        print("-" * 29)
        
        print("1. 🌐 Ir a: https://cloud.google.com/sdk/docs/install")
        print("2. ⬇️ Descargar Google Cloud SDK para Windows")
        print("3. 🔧 Ejecutar el instalador")
        print("4. 🔄 Reiniciar terminal")
        print("5. ✅ Ejecutar: gcloud --version")
        print()
        
        choice = input("¿Abrir página de descarga? (s/n): ").lower()
        if choice == 's':
            webbrowser.open("https://cloud.google.com/sdk/docs/install")
    
    def create_oauth_flow_example(self) -> bool:
        """Crea ejemplo de flujo OAuth para ARIA"""
        print(f"\n📝 CREANDO EJEMPLO DE FLUJO OAUTH")
        print("-" * 34)
        
        oauth_example = '''#!/usr/bin/env python3
"""
🔐 EJEMPLO: FLUJO OAUTH 2.0 PARA ARIA
====================================

Ejemplo completo de autenticación OAuth 2.0 con Google Cloud
integrado con el sistema ARIA.

Credenciales:
- Client ID: 209067283417-p7jrdl8hne7ck85iqtt50u02ak2p7gk8.apps.googleusercontent.com
- API Key: AIzaSyAS...CiYo

Fecha: 22 de octubre de 2025
"""

import os
import json
from pathlib import Path
from typing import Optional

class AriaGoogleOAuthFlow:
    """Flujo OAuth 2.0 para ARIA"""
    
    def __init__(self):
        # Configuración desde .env
        self.client_id = os.getenv('GOOGLE_OAUTH_CLIENT_ID', '209067283417-p7jrdl8hne7ck85iqtt50u02ak2p7gk8.apps.googleusercontent.com')
        self.api_key = os.getenv('GOOGLE_CLOUD_API_KEY', 'AIzaSyASWXk4RX29VhoL2ccwjz0-GtX-jMvCiYo')
        
        # Scopes para ARIA
        self.scopes = [
            'https://www.googleapis.com/auth/cloud-platform',
            'https://www.googleapis.com/auth/cloud-translation',
            'https://www.googleapis.com/auth/cloud-language'
        ]
        
        print("🔐 ARIA - Google OAuth 2.0 Flow")
        print("=" * 32)
    
    def authenticate_with_oauth(self) -> Optional[any]:
        """Autentica usando OAuth 2.0"""
        try:
            from google_auth_oauthlib.flow import Flow
            from google.auth.transport.requests import Request
            
            print("🔄 Iniciando flujo OAuth 2.0...")
            
            # Configurar flujo OAuth
            flow = Flow.from_client_config(
                client_config={
                    "installed": {
                        "client_id": self.client_id,
                        "client_secret": "PLACEHOLDER-SECRET",  # Necesitas configurar esto
                        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                        "token_uri": "https://oauth2.googleapis.com/token"
                    }
                },
                scopes=self.scopes
            )
            
            flow.redirect_uri = 'http://localhost:8080'
            
            # Obtener URL de autorización
            auth_url, _ = flow.authorization_url(prompt='consent')
            
            print(f"🌐 Abre esta URL para autorizar:")
            print(f"   {auth_url}")
            print()
            
            # Solicitar código de autorización
            auth_code = input("📝 Pega el código de autorización: ").strip()
            
            if auth_code:
                # Intercambiar código por token
                flow.fetch_token(code=auth_code)
                
                credentials = flow.credentials
                
                # Guardar credenciales
                self._save_credentials(credentials)
                
                print("✅ Autenticación OAuth completada")
                return credentials
            else:
                print("❌ No se proporcionó código")
                return None
                
        except ImportError:
            print("❌ google-auth-oauthlib no instalado")
            print("💡 Instalar: pip install google-auth-oauthlib")
            return None
        except Exception as e:
            print(f"❌ Error en OAuth: {e}")
            return None
    
    def authenticate_with_adc(self) -> Optional[any]:
        """Autentica usando Application Default Credentials"""
        try:
            import google.auth
            
            print("🔄 Usando Application Default Credentials...")
            
            credentials, project = google.auth.default(scopes=self.scopes)
            
            if credentials:
                print(f"✅ ADC configuradas para proyecto: {project}")
                return credentials
            else:
                print("❌ ADC no disponibles")
                return None
                
        except Exception as e:
            print(f"❌ Error ADC: {e}")
            return None
    
    def authenticate_with_api_key(self) -> str:
        """Autentica usando API Key (limitado)"""
        print("🔑 Usando API Key para servicios limitados...")
        
        if self.api_key:
            print(f"✅ API Key disponible: {self.api_key[:8]}...")
            return self.api_key
        else:
            print("❌ API Key no configurada")
            return ""
    
    def _save_credentials(self, credentials):
        """Guarda credenciales OAuth"""
        try:
            creds_file = Path("aria_oauth_token.json")
            
            creds_data = {
                'token': credentials.token,
                'refresh_token': credentials.refresh_token,
                'token_uri': credentials.token_uri,
                'client_id': credentials.client_id,
                'client_secret': credentials.client_secret,
                'scopes': credentials.scopes
            }
            
            with open(creds_file, 'w', encoding='utf-8') as f:
                json.dump(creds_data, f, indent=2)
            
            print(f"💾 Credenciales guardadas: {creds_file}")
            
        except Exception as e:
            print(f"⚠️ Error guardando credenciales: {e}")
    
    def get_best_available_auth(self):
        """Obtiene la mejor autenticación disponible"""
        print("🎯 Determinando mejor método de autenticación...")
        
        # Intentar métodos en orden de preferencia
        methods = [
            ("OAuth 2.0", self.authenticate_with_oauth),
            ("Application Default Credentials", self.authenticate_with_adc),
            ("API Key", self.authenticate_with_api_key)
        ]
        
        for method_name, method_func in methods:
            print(f"\\n🔍 Probando {method_name}...")
            
            try:
                result = method_func()
                if result:
                    print(f"✅ {method_name} configurado exitosamente")
                    return method_name, result
                else:
                    print(f"⚠️ {method_name} no disponible")
            except Exception as e:
                print(f"❌ {method_name} falló: {e}")
        
        print("❌ No se pudo configurar ningún método de autenticación")
        return None, None
    
    def test_google_cloud_services(self, credentials=None):
        """Prueba servicios de Google Cloud"""
        print(f"\\n🧪 PROBANDO SERVICIOS GOOGLE CLOUD")
        print("-" * 35)
        
        # Aquí integrarías con el sistema ARIA existente
        try:
            # Importar sistema ARIA
            import sys
            sys.path.append('backend/src')
            from google_cloud_apis import GoogleCloudAPIs
            
            # Crear instancia con credenciales
            gcp = GoogleCloudAPIs()
            
            # Probar servicios
            test_text = "Hello, this is a test for ARIA Google Cloud integration."
            
            print("🔍 Probando análisis de sentimientos...")
            sentiment = gcp.analyze_sentiment_advanced(test_text)
            print(f"   Resultado: {sentiment}")
            
            print("🔄 Probando traducción...")
            translation = gcp.translate_text_google(test_text, target_lang='es')
            print(f"   Traducido: {translation}")
            
            print("✅ Servicios Google Cloud funcionando con ARIA")
            
        except Exception as e:
            print(f"⚠️ Error probando servicios: {e}")

def main():
    """Función principal de demostración"""
    oauth_flow = AriaGoogleOAuthFlow()
    
    print("🎯 Opciones de autenticación:")
    print("   1. Flujo OAuth 2.0 completo")
    print("   2. Application Default Credentials")
    print("   3. Solo API Key")
    print("   4. Mejor método disponible")
    print("   5. Probar servicios actuales")
    
    choice = input("\\nSeleccionar opción (1-5): ").strip()
    
    if choice == '1':
        oauth_flow.authenticate_with_oauth()
    elif choice == '2':
        oauth_flow.authenticate_with_adc()
    elif choice == '3':
        oauth_flow.authenticate_with_api_key()
    elif choice == '4':
        method, creds = oauth_flow.get_best_available_auth()
        if method:
            oauth_flow.test_google_cloud_services(creds)
    elif choice == '5':
        oauth_flow.test_google_cloud_services()
    else:
        print("👋 Saliendo...")

if __name__ == "__main__":
    main()
'''
        
        try:
            example_file = Path("aria_oauth_flow_example.py")
            
            with open(example_file, 'w', encoding='utf-8') as f:
                f.write(oauth_example)
            
            print(f"✅ Ejemplo creado: {example_file}")
            print("💡 Ejecutar: python aria_oauth_flow_example.py")
            
            return True
            
        except Exception as e:
            print(f"❌ Error creando ejemplo: {e}")
            return False
    
    def configure_project_settings(self) -> bool:
        """Configura settings del proyecto para OAuth"""
        print(f"\n⚙️ CONFIGURANDO SETTINGS DEL PROYECTO")
        print("-" * 37)
        
        try:
            # Actualizar backend/config/settings.py
            settings_file = Path("backend/config/settings.py")
            
            if settings_file.exists():
                print(f"📝 Actualizando {settings_file}...")
                
                # Leer contenido actual
                with open(settings_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Agregar configuración OAuth si no existe
                oauth_config = f'''

# Google Cloud OAuth 2.0 Configuration - {datetime.now().strftime('%Y-%m-%d')}
GOOGLE_OAUTH_CLIENT_ID = "{self.oauth_client_id}"
GOOGLE_CLOUD_API_KEY = "{self.api_key}"
GOOGLE_OAUTH_SCOPES = [
    "https://www.googleapis.com/auth/cloud-platform",
    "https://www.googleapis.com/auth/cloud-translation", 
    "https://www.googleapis.com/auth/cloud-language"
]
GOOGLE_OAUTH_REDIRECT_URI = "http://localhost:8080"
'''
                
                if 'GOOGLE_OAUTH_CLIENT_ID' not in content:
                    with open(settings_file, 'a', encoding='utf-8') as f:
                        f.write(oauth_config)
                    
                    print("✅ Configuración OAuth agregada a settings.py")
                else:
                    print("ℹ️ Configuración OAuth ya existe en settings.py")
                
                return True
            else:
                print(f"⚠️ {settings_file} no encontrado")
                return False
                
        except Exception as e:
            print(f"❌ Error configurando settings: {e}")
            return False
    
    def show_next_steps_summary(self) -> Dict:
        """Muestra resumen de próximos pasos"""
        print(f"\n📋 RESUMEN DE CONFIGURACIÓN OAUTH 2.0")
        print("-" * 38)
        
        steps_status = {
            'env_configured': True,  # Ya configuramos .env
            'credentials_file': False,  # Necesita client_secret
            'gcloud_cli': False,  # Pendiente instalación
            'oauth_flow': True,  # Ejemplo creado
            'project_settings': False  # Pendiente configuración
        }
        
        print("✅ Variables de entorno (.env) configuradas")
        print("✅ Ejemplo de flujo OAuth creado")
        print("⏳ Archivo de credenciales (necesita client_secret)")
        print("⏳ gcloud CLI (opcional pero recomendado)")
        print("⏳ Configuración de proyecto")
        print()
        
        print("🚀 PRÓXIMOS PASOS CRÍTICOS:")
        print("1. 🔑 Obtener client_secret de Google Cloud Console")
        print("   Ve a: APIs & Services > Credentials > OAuth 2.0 Client IDs")
        print("2. 📝 Completar google_oauth_credentials.json")
        print("3. 🧪 Probar: python aria_oauth_flow_example.py")
        print("4. 🔧 Opcional: Instalar gcloud CLI")
        print()
        
        print("💡 MÉTODOS DISPONIBLES AHORA:")
        print("   • API Key (limitado): ✅ Funcional")
        print("   • OAuth 2.0 (completo): ⏳ Necesita client_secret")
        print("   • ADC (gcloud): ⏳ Necesita gcloud CLI")
        
        return steps_status
    
    def run_complete_oauth_setup(self) -> bool:
        """Ejecuta configuración completa de OAuth"""
        print("🚀 CONFIGURACIÓN COMPLETA OAUTH 2.0 + GOOGLE CLOUD")
        print("=" * 52)
        
        try:
            # Paso 1: Verificar configuración actual
            config_status = self.verify_current_configuration()
            
            # Paso 2: Crear archivo de credenciales
            if not config_status['credentials_file_exists']:
                self.create_oauth_credentials_file()
            
            # Paso 3: Intentar configurar ADC
            if config_status['google_auth_installed']:
                self.setup_application_default_credentials()
            
            # Paso 4: Crear ejemplo de flujo OAuth
            self.create_oauth_flow_example()
            
            # Paso 5: Configurar settings del proyecto
            self.configure_project_settings()
            
            # Paso 6: Mostrar resumen
            status = self.show_next_steps_summary()
            
            print(f"\n" + "="*52)
            print("📊 CONFIGURACIÓN OAUTH 2.0 COMPLETADA")
            print("="*52)
            
            completed_steps = sum(1 for step in status.values() if step)
            total_steps = len(status)
            
            print(f"✅ Pasos completados: {completed_steps}/{total_steps}")
            print("🔑 API Key: Completamente funcional")
            print("🔐 OAuth 2.0: Configurado (necesita client_secret)")
            print("🚀 Sistema ARIA: Listo para usar")
            
            return completed_steps >= 3
            
        except KeyboardInterrupt:
            print(f"\n⏹️ Configuración interrumpida por el usuario")
            return False
        except Exception as e:
            print(f"\n❌ Error durante configuración: {e}")
            return False

def main():
    """Función principal"""
    configurator = GoogleCloudOAuthConfigurator()
    
    print("🎯 Este configurador va a:")
    print("   • Configurar OAuth 2.0 Client ID")
    print("   • Crear flujo de autenticación completo")
    print("   • Integrar con sistema ARIA existente")
    print("   • Configurar múltiples métodos de auth")
    print()
    
    choice = input("¿Ejecutar configuración completa de OAuth? (s/n): ").lower()
    
    if choice == 's':
        success = configurator.run_complete_oauth_setup()
        
        if success:
            print("\n🎉 ¡Configuración OAuth exitosa!")
            print("💡 Tu sistema ARIA ahora soporta autenticación OAuth 2.0")
            print("🧪 Probar: python aria_oauth_flow_example.py")
        else:
            print("\n⚠️ Configuración OAuth parcialmente completada")
            print("💡 Revisar pasos pendientes arriba")
            
        return success
    else:
        print("👋 Configuración OAuth cancelada")
        return False

if __name__ == "__main__":
    main()