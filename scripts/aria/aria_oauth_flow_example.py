#!/usr/bin/env python3
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
            print(f"\n🔍 Probando {method_name}...")
            
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
        print(f"\n🧪 PROBANDO SERVICIOS GOOGLE CLOUD")
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
    
    choice = input("\nSeleccionar opción (1-5): ").strip()
    
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
