#!/usr/bin/env python3
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
            create_choice = input("\n🔨 ¿Crear nueva clave API? (s/n): ").lower()
            
            if create_choice == 's':
                display_name = input("📝 Nombre para la clave: ").strip()
                if display_name:
                    new_key = create_api_key(project_id, display_name)
                    
                    if new_key:
                        print("\n💡 PRÓXIMOS PASOS:")
                        print(f"   1. Configurar variable de entorno:")
                        print(f"      set GOOGLE_CLOUD_API_KEY={new_key}")
                        print(f"   2. Integrar con sistema ARIA")
        else:
            print(f"ℹ️ Proyecto ya tiene {keys_count} claves API")
        
    except Exception as e:
        logger.error(f"Error en ejemplo: {e}")

if __name__ == "__main__":
    main()
