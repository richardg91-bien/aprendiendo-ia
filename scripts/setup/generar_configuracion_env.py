#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🚀 Generador de Configuración .env - ARIA
Script para generar automáticamente archivos .env desde plantillas
"""

import os
import sys
from pathlib import Path
import shutil
from typing import Dict, List

class EnvGenerator:
    def __init__(self):
        self.base_path = Path(__file__).parent.parent.parent
        self.templates = {
            'development': {
                'PORT': '8000',
                'HOST': 'localhost',
                'DEBUG': 'true',
                'NODE_ENV': 'development',
                'ARIA_VOICE_ENABLED': 'true',
                'ARIA_LEARNING_MODE': 'advanced',
                'ARIA_LANGUAGE': 'es',
                'PARENTAL_CONTROLS': 'true',
                'CONTENT_FILTER': 'strict',
                'MAX_SESSION_TIME': '60',
                'FRONTEND_URL': 'http://localhost:3000',
                'BACKEND_URL': 'http://localhost:8000',
                'API_BASE_URL': 'http://localhost:8000/api'
            },
            'production': {
                'PORT': '80',
                'HOST': '0.0.0.0',
                'DEBUG': 'false',
                'NODE_ENV': 'production',
                'ARIA_VOICE_ENABLED': 'true',
                'ARIA_LEARNING_MODE': 'standard',
                'ARIA_LANGUAGE': 'es',
                'PARENTAL_CONTROLS': 'true',
                'CONTENT_FILTER': 'strict',
                'MAX_SESSION_TIME': '120',
                'FRONTEND_URL': 'https://yourdomain.com',
                'BACKEND_URL': 'https://api.yourdomain.com',
                'API_BASE_URL': 'https://api.yourdomain.com/api'
            }
        }
    
    def show_menu(self):
        """Muestra el menú de opciones"""
        print("\n" + "="*60)
        print("🚀 GENERADOR DE CONFIGURACIÓN .env - ARIA")
        print("="*60)
        print("\n📋 OPCIONES DISPONIBLES:")
        print("\n1. 🔧 Generar .env para DESARROLLO")
        print("2. 🌐 Generar .env para PRODUCCIÓN")
        print("3. 📄 Crear .env desde .env.example")
        print("4. 🔍 Verificar configuración actual")
        print("5. 📝 Generar plantilla .env.example")
        print("6. 🔄 Restaurar desde respaldo")
        print("\n0. ❌ Salir")
        print("-" * 60)
    
    def backup_existing_env(self) -> bool:
        """Hace respaldo del .env existente"""
        env_file = self.base_path / '.env'
        if env_file.exists():
            backup_file = self.base_path / '.env.backup'
            try:
                shutil.copy2(env_file, backup_file)
                print(f"✅ Respaldo creado: {backup_file}")
                return True
            except Exception as e:
                print(f"❌ Error creando respaldo: {e}")
                return False
        return True
    
    def generate_env_development(self):
        """Genera .env para desarrollo"""
        print("\n🔧 Generando configuración para DESARROLLO...")
        
        if not self.backup_existing_env():
            return
        
        env_content = self._generate_env_content('development')
        env_content += self._get_user_input_for_sensitive_vars()
        
        env_file = self.base_path / '.env'
        try:
            with open(env_file, 'w', encoding='utf-8') as f:
                f.write(env_content)
            print(f"✅ Archivo .env para desarrollo creado: {env_file}")
            print("\n🔍 Recuerda configurar las variables sensibles:")
            print("  - SUPABASE_URL")
            print("  - SUPABASE_ANON_KEY")
            print("  - GOOGLE_CLOUD_PROJECT_ID")
            print("  - OPENAI_API_KEY")
        except Exception as e:
            print(f"❌ Error creando .env: {e}")
    
    def generate_env_production(self):
        """Genera .env para producción"""
        print("\n🌐 Generando configuración para PRODUCCIÓN...")
        print("⚠️ ADVERTENCIA: Configuración de producción requiere datos reales")
        
        confirm = input("\n¿Continuar? (s/N): ").lower()
        if confirm != 's':
            print("❌ Operación cancelada")
            return
        
        if not self.backup_existing_env():
            return
        
        env_content = self._generate_env_content('production')
        env_content += self._get_user_input_for_sensitive_vars(production=True)
        
        env_file = self.base_path / '.env'
        try:
            with open(env_file, 'w', encoding='utf-8') as f:
                f.write(env_content)
            print(f"✅ Archivo .env para producción creado: {env_file}")
            print("\n🛡️ IMPORTANTE: Verificar todas las configuraciones antes del despliegue")
        except Exception as e:
            print(f"❌ Error creando .env: {e}")
    
    def create_from_example(self):
        """Crea .env desde .env.example"""
        print("\n📄 Creando .env desde .env.example...")
        
        example_file = self.base_path / '.env.example'
        if not example_file.exists():
            print("❌ Archivo .env.example no encontrado")
            print("💡 Generando .env.example primero...")
            self.generate_example_template()
            return
        
        if not self.backup_existing_env():
            return
        
        env_file = self.base_path / '.env'
        try:
            shutil.copy2(example_file, env_file)
            print(f"✅ Archivo .env creado desde plantilla: {env_file}")
            print("\n📝 Ahora edita .env y completa las variables necesarias:")
            print(f"  notepad {env_file}")
        except Exception as e:
            print(f"❌ Error copiando plantilla: {e}")
    
    def verify_current_config(self):
        """Verifica la configuración actual"""
        print("\n🔍 Verificando configuración actual...")
        
        # Ejecutar el verificador de configuración
        verifier_script = self.base_path / 'scripts' / 'test' / 'verificar_configuracion_env.py'
        if verifier_script.exists():
            try:
                import subprocess
                result = subprocess.run([sys.executable, str(verifier_script)], 
                                      capture_output=True, text=True)
                print(result.stdout)
                if result.stderr:
                    print("Errores:", result.stderr)
            except Exception as e:
                print(f"❌ Error ejecutando verificador: {e}")
        else:
            print("❌ Script verificador no encontrado")
    
    def generate_example_template(self):
        """Genera plantilla .env.example"""
        print("\n📝 Generando plantilla .env.example...")
        
        example_content = self._generate_example_template()
        example_file = self.base_path / '.env.example'
        
        try:
            with open(example_file, 'w', encoding='utf-8') as f:
                f.write(example_content)
            print(f"✅ Plantilla .env.example creada: {example_file}")
        except Exception as e:
            print(f"❌ Error creando plantilla: {e}")
    
    def restore_from_backup(self):
        """Restaura .env desde respaldo"""
        print("\n🔄 Restaurando desde respaldo...")
        
        backup_file = self.base_path / '.env.backup'
        if not backup_file.exists():
            print("❌ No se encontró archivo de respaldo")
            return
        
        env_file = self.base_path / '.env'
        try:
            shutil.copy2(backup_file, env_file)
            print(f"✅ Configuración restaurada desde: {backup_file}")
        except Exception as e:
            print(f"❌ Error restaurando respaldo: {e}")
    
    def _generate_env_content(self, environment: str) -> str:
        """Genera el contenido del archivo .env"""
        template = self.templates.get(environment, self.templates['development'])
        
        content = f"""# ===========================================
# CONFIGURACIÓN DE VARIABLES DE ENTORNO - ARIA
# Entorno: {environment.upper()}
# Generado automáticamente el: {Path(__file__).stat().st_mtime}
# ===========================================

"""
        
        # Configuración del servidor
        content += "# Configuración del Servidor\n"
        for key in ['PORT', 'HOST', 'DEBUG', 'NODE_ENV']:
            if key in template:
                content += f"{key}={template[key]}\n"
        content += "\n"
        
        # Configuración de ARIA
        content += "# Configuración de ARIA\n"
        aria_keys = ['ARIA_VOICE_ENABLED', 'ARIA_LEARNING_MODE', 'ARIA_LANGUAGE']
        for key in aria_keys:
            if key in template:
                content += f"{key}={template[key]}\n"
        content += "\n"
        
        # Configuración de seguridad
        content += "# Configuración de Seguridad\n"
        security_keys = ['PARENTAL_CONTROLS', 'CONTENT_FILTER', 'MAX_SESSION_TIME']
        for key in security_keys:
            if key in template:
                content += f"{key}={template[key]}\n"
        content += "\n"
        
        # URLs de servicio
        content += "# URLs de Servicio\n"
        url_keys = ['FRONTEND_URL', 'BACKEND_URL', 'API_BASE_URL']
        for key in url_keys:
            if key in template:
                content += f"{key}={template[key]}\n"
        content += "\n"
        
        return content
    
    def _get_user_input_for_sensitive_vars(self, production: bool = False) -> str:
        """Solicita al usuario las variables sensibles"""
        content = "# Variables Sensibles (COMPLETAR MANUALMENTE)\n"
        
        sensitive_vars = {
            'SUPABASE_URL': 'URL de Supabase (https://your-project.supabase.co)',
            'SUPABASE_ANON_KEY': 'Clave anónima de Supabase',
            'SUPABASE_SERVICE_ROLE_KEY': 'Clave de servicio de Supabase (opcional)',
            'GOOGLE_CLOUD_PROJECT_ID': 'ID del proyecto de Google Cloud',
            'GOOGLE_APPLICATION_CREDENTIALS': 'config/google_oauth_credentials.json',
            'OPENAI_API_KEY': 'Clave de API de OpenAI (opcional)',
        }
        
        for var, description in sensitive_vars.items():
            if production:
                content += f"{var}=# COMPLETAR: {description}\n"
            else:
                content += f"{var}=# {description}\n"
        
        content += "\n"
        return content
    
    def _generate_example_template(self) -> str:
        """Genera contenido para .env.example"""
        content = """# ===========================================
# PLANTILLA DE VARIABLES DE ENTORNO - ARIA
# Copia este archivo como .env y completa las variables
# ===========================================

# Configuración del Servidor
PORT=8000
HOST=localhost
DEBUG=true
NODE_ENV=development

# Base de Datos (Supabase)
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_ANON_KEY=your_anon_key_here
SUPABASE_SERVICE_ROLE_KEY=your_service_role_key_here

# Google Cloud
GOOGLE_CLOUD_PROJECT_ID=your_project_id
GOOGLE_APPLICATION_CREDENTIALS=config/google_oauth_credentials.json
GOOGLE_CLOUD_REGION=us-central1

# APIs de IA
OPENAI_API_KEY=your_openai_api_key_here

# APIs Multilingües
TRANSLATION_API_KEY=your_translation_api_key
SPEECH_API_KEY=your_speech_api_key

# Configuración de ARIA
ARIA_VOICE_ENABLED=true
ARIA_LEARNING_MODE=advanced
ARIA_LANGUAGE=es

# Configuración de Seguridad
PARENTAL_CONTROLS=true
CONTENT_FILTER=strict
MAX_SESSION_TIME=60

# URLs de Servicio
FRONTEND_URL=http://localhost:3000
BACKEND_URL=http://localhost:8000
API_BASE_URL=http://localhost:8000/api

# Variables Opcionales
EXTERNAL_API_KEY=your_external_api_key
EXTERNAL_API_URL=https://api.example.com
"""
        return content
    
    def run(self):
        """Ejecuta el generador principal"""
        while True:
            try:
                self.show_menu()
                choice = input("\n🎯 Selecciona una opción (0-6): ").strip()
                
                if choice == "0":
                    print("\n👋 ¡Hasta luego!")
                    break
                elif choice == "1":
                    self.generate_env_development()
                elif choice == "2":
                    self.generate_env_production()
                elif choice == "3":
                    self.create_from_example()
                elif choice == "4":
                    self.verify_current_config()
                elif choice == "5":
                    self.generate_example_template()
                elif choice == "6":
                    self.restore_from_backup()
                else:
                    print("❌ Opción no válida. Intenta de nuevo.")
                
                input("\n⏸️ Presiona Enter para continuar...")
                
            except KeyboardInterrupt:
                print("\n\n👋 ¡Hasta luego!")
                break
            except Exception as e:
                print(f"❌ Error inesperado: {e}")

def main():
    """Función principal"""
    generator = EnvGenerator()
    generator.run()

if __name__ == "__main__":
    main()