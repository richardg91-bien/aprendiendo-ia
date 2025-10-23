#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🧪 Test del Servidor ARIA
Script para probar que el servidor esté funcionando
"""

import requests
import json
from datetime import datetime

def test_aria_server():
    """Prueba el servidor ARIA"""
    base_url = "http://localhost:8000"
    
    print("🧪 PROBANDO SERVIDOR ARIA")
    print("=" * 40)
    
    # Test 1: Estado del servidor
    print("\n🔍 Test 1: Estado del servidor...")
    try:
        response = requests.get(f"{base_url}/api/status", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print("✅ Servidor funcionando correctamente")
            print(f"   Estado: {data.get('status')}")
            print(f"   Modo: {data.get('mode', 'N/A')}")
            print(f"   Tiempo: {data.get('timestamp', 'N/A')[:19]}")
        else:
            print(f"❌ Error de estado: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ No se puede conectar al servidor")
        print("💡 Asegúrate de que el servidor esté ejecutándose en puerto 8000")
        return False
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        return False
    
    # Test 2: Chat básico
    print("\n💬 Test 2: Chat básico...")
    try:
        chat_data = {"message": "Hola ARIA, ¿cómo estás?"}
        response = requests.post(
            f"{base_url}/api/chat", 
            json=chat_data,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        if response.status_code == 200:
            data = response.json()
            print("✅ Chat funcionando")
            print(f"   Respuesta: {data.get('response', 'N/A')[:100]}...")
            print(f"   Conocimiento: {data.get('knowledge_learned', 0)}")
        else:
            print(f"❌ Error en chat: {response.status_code}")
            print(f"   Contenido: {response.text[:100]}")
    except Exception as e:
        print(f"❌ Error en chat: {e}")
    
    # Test 3: Conocimiento
    print("\n🧠 Test 3: Base de conocimiento...")
    try:
        response = requests.get(f"{base_url}/api/knowledge", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print("✅ Conocimiento accesible")
            print(f"   Total conocimiento: {data.get('total_knowledge', 0)}")
            print(f"   Conversaciones: {data.get('conversation_count', 0)}")
        else:
            print(f"❌ Error en conocimiento: {response.status_code}")
    except Exception as e:
        print(f"❌ Error en conocimiento: {e}")
    
    # Test 4: Página principal
    print("\n🏠 Test 4: Página principal...")
    try:
        response = requests.get(base_url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            print("✅ Página principal accesible")
            print(f"   Mensaje: {data.get('message', 'N/A')}")
        else:
            print(f"❌ Error en página principal: {response.status_code}")
    except Exception as e:
        print(f"❌ Error en página principal: {e}")
    
    print(f"\n🎯 RESUMEN:")
    print(f"   🌐 Servidor: http://localhost:8000")
    print(f"   📊 Estado: http://localhost:8000/api/status")
    print(f"   💬 Chat: POST http://localhost:8000/api/chat")
    print(f"   🧠 Conocimiento: http://localhost:8000/api/knowledge")
    
    return True

if __name__ == "__main__":
    try:
        test_aria_server()
    except KeyboardInterrupt:
        print("\n\n👋 Test interrumpido por el usuario")
    except Exception as e:
        print(f"\n❌ Error general: {e}")
        import traceback
        traceback.print_exc()