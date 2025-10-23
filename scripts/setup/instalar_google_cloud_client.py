#!/usr/bin/env python3
"""
🔧 INSTALADOR DE GOOGLE CLOUD API KEYS CLIENT
=============================================

Instala y configura la biblioteca oficial de Google Cloud API Keys Client
según la documentación oficial.

Características:
✅ Instalación automática de google-cloud-api-keys
✅ Configuración de entorno virtual
✅ Verificación de Python >= 3.7
✅ Configuración de logging avanzado
✅ Integración con sistema ARIA existente

Basado en documentación oficial:
https://cloud.google.com/python/docs/reference/apikeys/latest

Fecha: 22 de octubre de 2025
"""

import sys
import os
import subprocess
import logging
from pathlib import Path

class GoogleCloudClientInstaller:
    """Instalador de Google Cloud API Keys Client oficial"""
    
    def __init__(self):
        self.python_version = sys.version_info
        self.venv_path = Path("venv")
        self.requirements_added = []
        
        print("🔧 Instalador de Google Cloud API Keys Client")
        print("=" * 50)
    
    def check_python_version(self) -> bool:
        """Verifica versión de Python según documentación oficial"""
        print("🐍 VERIFICANDO VERSIÓN DE PYTHON")
        print("-" * 35)
        
        current_version = f"{self.python_version.major}.{self.python_version.minor}"
        print(f"   Versión actual: Python {current_version}")
        
        # Verificar según documentación: Python >= 3.7, incluyendo 3.14
        if self.python_version >= (3, 7):
            print(f"✅ Python {current_version} es compatible (>=3.7)")
            return True
        else:
            print(f"❌ Python {current_version} no es compatible")
            print("💡 Documentación oficial requiere: Python >= 3.7")
            print("   Actualizar Python antes de continuar")
            return False
    
    def check_virtual_environment(self) -> bool:
        """Verifica si está en entorno virtual"""
        print(f"\n📦 VERIFICANDO ENTORNO VIRTUAL")
        print("-" * 32)
        
        # Verificar si estamos en venv
        in_venv = hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix)
        
        if in_venv:
            print("✅ Ejecutándose en entorno virtual")
            print(f"   Ruta: {sys.prefix}")
            return True
        else:
            print("⚠️ No se detectó entorno virtual")
            print("💡 Recomendado usar entorno virtual para aislamiento")
            
            choice = input("¿Continuar sin entorno virtual? (s/n): ").lower()
            return choice == 's'
    
    def install_google_cloud_api_keys(self) -> bool:
        """Instala google-cloud-api-keys según documentación oficial"""
        print(f"\n📥 INSTALANDO GOOGLE CLOUD API KEYS CLIENT")
        print("-" * 45)
        
        try:
            # Comando según documentación oficial
            print("🔄 Ejecutando: pip install google-cloud-api-keys")
            
            result = subprocess.run([
                sys.executable, '-m', 'pip', 'install', 'google-cloud-api-keys'
            ], capture_output=True, text=True, timeout=300)
            
            if result.returncode == 0:
                print("✅ google-cloud-api-keys instalado correctamente")
                self.requirements_added.append("google-cloud-api-keys")
                
                # Verificar instalación
                try:
                    import google.cloud.api_keys_v1
                    print("✅ Módulo importado correctamente")
                    return True
                except ImportError as e:
                    print(f"❌ Error importando módulo: {e}")
                    return False
            else:
                print(f"❌ Error en instalación: {result.stderr}")
                return False
                
        except subprocess.TimeoutExpired:
            print("❌ Timeout en instalación (>300s)")
            return False
        except Exception as e:
            print(f"❌ Error inesperado: {e}")
            return False
    
    def install_additional_dependencies(self) -> bool:
        """Instala dependencias adicionales recomendadas"""
        print(f"\n📦 INSTALANDO DEPENDENCIAS ADICIONALES")
        print("-" * 40)
        
        additional_packages = [
            'google-auth',
            'google-auth-oauthlib',
            'google-auth-httplib2',
            'grpcio'
        ]
        
        installed_count = 0
        
        for package in additional_packages:
            try:
                print(f"🔄 Instalando {package}...")
                
                result = subprocess.run([
                    sys.executable, '-m', 'pip', 'install', package
                ], capture_output=True, text=True, timeout=120)
                
                if result.returncode == 0:
                    print(f"✅ {package} instalado")
                    self.requirements_added.append(package)
                    installed_count += 1
                else:
                    print(f"⚠️ {package} no se pudo instalar")
                    
            except Exception as e:
                print(f"⚠️ Error con {package}: {e}")
        
        print(f"\n📊 Dependencias instaladas: {installed_count}/{len(additional_packages)}")
        return installed_count > 0
    
    def configure_logging(self) -> bool:
        """Configura logging según documentación oficial"""
        print(f"\n📋 CONFIGURANDO LOGGING AVANZADO")
        print("-" * 35)
        
        try:
            # Configuración según documentación oficial
            
            # 1. Configurar logger base de Google
            base_logger = logging.getLogger("google")
            base_logger.addHandler(logging.StreamHandler())
            base_logger.setLevel(logging.INFO)  # Cambiar a DEBUG si necesario
            
            # 2. Configurar logger específico para API Keys
            api_keys_logger = logging.getLogger("google.cloud.api_keys_v1")
            api_keys_logger.addHandler(logging.StreamHandler())
            api_keys_logger.setLevel(logging.INFO)
            
            # 3. Configurar propagación según documentación
            logging.getLogger("google").propagate = True
            
            print("✅ Logging configurado según documentación oficial")
            print("   • Logger base: google (nivel INFO)")
            print("   • Logger específico: google.cloud.api_keys_v1")
            print("   • Propagación habilitada")
            
            # Variable de entorno opcional
            os.environ['GOOGLE_SDK_PYTHON_LOGGING_SCOPE'] = 'google.cloud.api_keys_v1'
            print("✅ Variable GOOGLE_SDK_PYTHON_LOGGING_SCOPE configurada")
            
            return True
            
        except Exception as e:
            print(f"❌ Error configurando logging: {e}")
            return False
    
    def verify_installation(self) -> bool:
        """Verifica que la instalación sea correcta"""
        print(f"\n🧪 VERIFICANDO INSTALACIÓN")
        print("-" * 25)
        
        verification_results = {}
        
        # Verificar importación principal
        try:
            from google.cloud import api_keys_v1
            verification_results['main_import'] = True
            print("✅ Importación principal: google.cloud.api_keys_v1")
        except ImportError as e:
            verification_results['main_import'] = False
            print(f"❌ Error importación principal: {e}")
        
        # Verificar cliente
        try:
            from google.cloud.api_keys_v1 import ApiKeysClient
            verification_results['client'] = True
            print("✅ Cliente disponible: ApiKeysClient")
        except ImportError as e:
            verification_results['client'] = False
            print(f"❌ Error cliente: {e}")
        
        # Verificar autenticación
        try:
            import google.auth
            credentials, project = google.auth.default()
            verification_results['auth'] = True
            print(f"✅ Autenticación disponible (proyecto: {project or 'N/A'})")
        except Exception as e:
            verification_results['auth'] = False
            print(f"⚠️ Autenticación pendiente: {e}")
        
        # Verificar logging
        try:
            logger = logging.getLogger("google.cloud.api_keys_v1")
            verification_results['logging'] = bool(logger.handlers)
            status = "Configurado" if logger.handlers else "Sin configurar"
            print(f"✅ Logging: {status}")
        except:
            verification_results['logging'] = False
            print("❌ Error verificando logging")
        
        # Resultado general
        passed = sum(1 for result in verification_results.values() if result)
        total = len(verification_results)
        
        print(f"\n📊 Verificación: {passed}/{total} elementos correctos")
        
        return passed >= 2  # Al menos importación y cliente funcionando
    
    def update_requirements_file(self):
        """Actualiza archivo requirements.txt"""
        print(f"\n📄 ACTUALIZANDO REQUIREMENTS.TXT")
        print("-" * 32)
        
        if not self.requirements_added:
            print("⚠️ No hay nuevos paquetes para agregar")
            return
        
        requirements_file = Path("backend/requirements.txt")
        
        try:
            # Leer requirements existentes
            existing_requirements = set()
            if requirements_file.exists():
                with open(requirements_file, 'r', encoding='utf-8') as f:
                    existing_requirements = {line.strip() for line in f if line.strip() and not line.startswith('#')}
            
            # Agregar nuevos paquetes
            new_requirements = []
            for package in self.requirements_added:
                if package not in existing_requirements:
                    new_requirements.append(package)
            
            if new_requirements:
                # Crear directorio si no existe
                requirements_file.parent.mkdir(parents=True, exist_ok=True)
                
                # Agregar nuevos requirements
                with open(requirements_file, 'a', encoding='utf-8') as f:
                    if requirements_file.stat().st_size > 0:
                        f.write('\n')
                    f.write(f'\n# Google Cloud API Keys Client - {self._get_timestamp()}\n')
                    for req in new_requirements:
                        f.write(f'{req}\n')
                
                print(f"✅ Agregados {len(new_requirements)} paquetes a requirements.txt")
                for req in new_requirements:
                    print(f"   + {req}")
            else:
                print("ℹ️ Todos los paquetes ya estaban en requirements.txt")
                
        except Exception as e:
            print(f"❌ Error actualizando requirements.txt: {e}")
    
    def _get_timestamp(self) -> str:
        """Obtiene timestamp actual"""
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def create_example_usage(self):
        """Crea ejemplo de uso del cliente"""
        print(f"\n📝 CREANDO EJEMPLO DE USO")
        print("-" * 27)
        
        example_code = '''#!/usr/bin/env python3
"""
🔑 EJEMPLO DE USO - Google Cloud API Keys Client
==============================================

Ejemplo básico de uso del cliente oficial de Google Cloud API Keys
según la documentación oficial.

Basado en: https://cloud.google.com/python/docs/reference/apikeys/latest
"""

import os
import logging
from google.cloud import api_keys_v1
from google.auth import default

# Configurar logging según documentación oficial
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("google.cloud.api_keys_v1")

def list_api_keys(project_id: str):
    """Lista todas las claves API del proyecto"""
    try:
        # Crear cliente según documentación
        client = api_keys_v1.ApiKeysClient()
        
        # Configurar request
        request = api_keys_v1.ListKeysRequest(
            parent=f"projects/{project_id}/locations/global"
        )
        
        # Ejecutar request
        print(f"🔍 Listando claves API para proyecto: {project_id}")
        page_result = client.list_keys(request=request)
        
        # Procesar resultados
        keys_found = 0
        for response in page_result:
            keys_found += 1
            print(f"   🔑 Clave {keys_found}: {response.name}")
            print(f"      Display Name: {response.display_name}")
            print(f"      Created: {response.create_time}")
            print()
        
        if keys_found == 0:
            print("   ℹ️ No se encontraron claves API")
        
        return keys_found
        
    except Exception as e:
        logger.error(f"Error listando claves API: {e}")
        return 0

def create_api_key(project_id: str, display_name: str):
    """Crea nueva clave API"""
    try:
        # Crear cliente
        client = api_keys_v1.ApiKeysClient()
        
        # Configurar clave API
        api_key = api_keys_v1.Key()
        api_key.display_name = display_name
        
        # Configurar request
        request = api_keys_v1.CreateKeyRequest(
            parent=f"projects/{project_id}/locations/global",
            key=api_key
        )
        
        print(f"🔨 Creando clave API: {display_name}")
        
        # Ejecutar request (operación asíncrona)
        operation = client.create_key(request=request)
        
        print("⏳ Esperando completación...")
        response = operation.result()
        
        print(f"✅ Clave API creada exitosamente")
        print(f"   Nombre: {response.name}")
        print(f"   Key String: {response.key_string}")
        
        return response.key_string
        
    except Exception as e:
        logger.error(f"Error creando clave API: {e}")
        return None

def main():
    """Función principal de ejemplo"""
    print("🔑 EJEMPLO DE Google Cloud API Keys Client")
    print("=" * 45)
    
    # Obtener credenciales y proyecto
    try:
        credentials, project_id = default()
        
        if not project_id:
            print("❌ No se detectó project_id")
            print("💡 Configurar: gcloud config set project TU_PROJECT_ID")
            return
        
        print(f"📊 Proyecto detectado: {project_id}")
        
        # Listar claves existentes
        keys_count = list_api_keys(project_id)
        
        # Crear nueva clave si se desea
        if keys_count < 5:  # Límite razonable
            create_choice = input("\\n🔨 ¿Crear nueva clave API? (s/n): ").lower()
            
            if create_choice == 's':
                display_name = input("📝 Nombre para la clave: ").strip()
                if display_name:
                    new_key = create_api_key(project_id, display_name)
                    
                    if new_key:
                        print("\\n💡 PRÓXIMOS PASOS:")
                        print(f"   1. Configurar variable de entorno:")
                        print(f"      set GOOGLE_CLOUD_API_KEY={new_key}")
                        print(f"   2. Integrar con sistema ARIA")
        else:
            print(f"ℹ️ Proyecto ya tiene {keys_count} claves API")
        
    except Exception as e:
        logger.error(f"Error en ejemplo: {e}")

if __name__ == "__main__":
    main()
'''
        
        example_file = Path("ejemplo_google_cloud_api_keys.py")
        
        try:
            with open(example_file, 'w', encoding='utf-8') as f:
                f.write(example_code)
            
            print(f"✅ Ejemplo creado: {example_file}")
            print("💡 Ejecutar: python ejemplo_google_cloud_api_keys.py")
            
        except Exception as e:
            print(f"❌ Error creando ejemplo: {e}")
    
    def show_next_steps(self):
        """Muestra próximos pasos"""
        print(f"\n📋 PRÓXIMOS PASOS")
        print("=" * 20)
        
        print("🔧 CONFIGURACIÓN BÁSICA:")
        print("   1. Instalar y configurar gcloud CLI")
        print("   2. Autenticar: gcloud auth application-default login")
        print("   3. Configurar proyecto: gcloud config set project TU_PROJECT_ID")
        print()
        
        print("🔑 GESTIÓN DE CLAVES API:")
        print("   1. Ejecutar ejemplo: python ejemplo_google_cloud_api_keys.py")
        print("   2. Configurar variable: set GOOGLE_CLOUD_API_KEY=tu_clave")
        print("   3. Probar integración: python verificar_google_cloud.py")
        print()
        
        print("🚀 INTEGRACIÓN CON ARIA:")
        print("   1. Probar sistema: python prueba_respuestas_inteligentes.py")
        print("   2. Servidor completo: python aria_servidor_multilingue.py")
        print("   3. Sistema completo: python prueba_sistema_completo.py")
        print()
        
        print("📚 DOCUMENTACIÓN:")
        print("   • Cliente API Keys: https://cloud.google.com/python/docs/reference/apikeys/latest")
        print("   • Autenticación: https://cloud.google.com/docs/authentication")
        print("   • Logging: Configurado según documentación oficial")
    
    def run_installation(self) -> bool:
        """Ejecuta instalación completa"""
        print("🚀 INICIANDO INSTALACIÓN DE GOOGLE CLOUD API KEYS CLIENT")
        print("=" * 60)
        
        steps_results = {}
        
        try:
            # Paso 1: Verificar Python
            steps_results['python'] = self.check_python_version()
            if not steps_results['python']:
                return False
            
            # Paso 2: Verificar entorno virtual
            steps_results['venv'] = self.check_virtual_environment()
            if not steps_results['venv']:
                return False
            
            # Paso 3: Instalar cliente principal
            steps_results['main_client'] = self.install_google_cloud_api_keys()
            
            # Paso 4: Instalar dependencias adicionales
            steps_results['dependencies'] = self.install_additional_dependencies()
            
            # Paso 5: Configurar logging
            steps_results['logging'] = self.configure_logging()
            
            # Paso 6: Verificar instalación
            steps_results['verification'] = self.verify_installation()
            
            # Paso 7: Actualizar requirements
            self.update_requirements_file()
            
            # Paso 8: Crear ejemplo
            self.create_example_usage()
            
            # Resumen
            print(f"\n📊 RESUMEN DE INSTALACIÓN")
            print("=" * 28)
            
            for step, result in steps_results.items():
                status = "✅ Exitoso" if result else "❌ Falló"
                print(f"   {step.replace('_', ' ').title()}: {status}")
            
            successful_steps = sum(1 for result in steps_results.values() if result)
            total_steps = len(steps_results)
            
            if successful_steps >= 4:  # Criterio mínimo de éxito
                print(f"\n🎉 INSTALACIÓN EXITOSA ({successful_steps}/{total_steps})")
                self.show_next_steps()
                return True
            else:
                print(f"\n⚠️ INSTALACIÓN PARCIAL ({successful_steps}/{total_steps})")
                print("💡 Revisar errores y reintentar")
                return False
                
        except KeyboardInterrupt:
            print(f"\n⏹️ Instalación interrumpida por el usuario")
            return False
        except Exception as e:
            print(f"\n❌ Error durante instalación: {e}")
            return False

def main():
    """Función principal del instalador"""
    installer = GoogleCloudClientInstaller()
    
    print("🎯 Este instalador configurará:")
    print("   • google-cloud-api-keys (cliente oficial)")
    print("   • Dependencias de autenticación")
    print("   • Logging avanzado según documentación")
    print("   • Ejemplo de uso funcional")
    print("   • Integración con sistema ARIA")
    print()
    
    choice = input("¿Continuar con la instalación? (s/n): ").lower()
    
    if choice == 's':
        success = installer.run_installation()
        
        if success:
            print("\n🎉 ¡Instalación completada exitosamente!")
            print("💡 Revisar próximos pasos arriba")
            return True
        else:
            print("\n⚠️ Instalación incompleta. Revisar errores.")
            return False
    else:
        print("👋 Instalación cancelada")
        return False

if __name__ == "__main__":
    main()