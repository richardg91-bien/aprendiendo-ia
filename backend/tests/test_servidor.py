#!/usr/bin/env python3
"""
Script de prueba para verificar el funcionamiento del servidor integrado ARIA
"""

import requests
import json
from time import sleep

def test_api_endpoints():
    """Prueba todos los endpoints de la API"""
    base_url = "http://localhost:3000"
    
    print("🧪 Iniciando pruebas del servidor ARIA integrado")
    print("=" * 50)
    
    # Test 1: Estado del sistema
    try:
        print("📊 Probando /api/status...")
        response = requests.get(f"{base_url}/api/status")
        if response.status_code == 200:
            print("✅ Estado del sistema: OK")
            data = response.json()
            print(f"   Version: {data.get('version', 'N/A')}")
        else:
            print(f"❌ Error en estado: {response.status_code}")
    except Exception as e:
        print(f"❌ Error conectando: {e}")
    
    # Test 2: Información de red neuronal
    try:
        print("\n🧠 Probando /api/red_neuronal_info...")
        response = requests.get(f"{base_url}/api/red_neuronal_info")
        if response.status_code == 200:
            print("✅ Red neuronal: OK")
            data = response.json()
            print(f"   Accuracy: {data.get('accuracy', 'N/A')}%")
            print(f"   Parámetros: {data.get('parametros', 'N/A')}")
        else:
            print(f"❌ Error en red neuronal: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test 3: Chat
    try:
        print("\n💬 Probando /api/chat...")
        response = requests.post(f"{base_url}/api/chat", 
                               json={"mensaje": "Hola ARIA, ¿cómo estás?"})
        if response.status_code == 200:
            print("✅ Chat: OK")
            data = response.json()
            respuesta = data.get('respuesta', '')[:50] + "..."
            print(f"   Respuesta: {respuesta}")
        else:
            print(f"❌ Error en chat: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test 4: Búsqueda web
    try:
        print("\n🔍 Probando /api/buscar_web...")
        response = requests.post(f"{base_url}/api/buscar_web", 
                               json={"consulta": "inteligencia artificial"})
        if response.status_code == 200:
            print("✅ Búsqueda web: OK")
            data = response.json()
            total = data.get('total_resultados', 0)
            print(f"   Resultados encontrados: {total}")
        else:
            print(f"❌ Error en búsqueda: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test 5: Frontend
    try:
        print("\n🖥️  Probando frontend...")
        response = requests.get(f"{base_url}/")
        if response.status_code == 200:
            print("✅ Frontend: OK")
            content_type = response.headers.get('content-type', '')
            print(f"   Content-Type: {content_type}")
        else:
            print(f"❌ Error en frontend: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print("\n" + "=" * 50)
    print("🎉 Pruebas completadas")
    print("🌐 Accede a la aplicación en: http://localhost:3000")

if __name__ == "__main__":
    test_api_endpoints()