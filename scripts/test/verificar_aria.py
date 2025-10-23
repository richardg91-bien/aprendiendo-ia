"""
🔍 Verificación Final de ARIA
============================
"""

import requests
import time

def test_aria():
    print("🔍 VERIFICACIÓN FINAL DE ARIA")
    print("=" * 40)
    
    # Test 1: Frontend
    print("📱 Probando Frontend (Puerto 3000)...")
    try:
        response = requests.get("http://localhost:3000", timeout=5)
        if response.status_code == 200:
            print("✅ Frontend: FUNCIONANDO")
        else:
            print(f"⚠️  Frontend: Status {response.status_code}")
    except Exception as e:
        print(f"❌ Frontend: ERROR - {e}")
    
    # Test 2: Backend API Status
    print("\n🖥️  Probando Backend API (Puerto 8000)...")
    try:
        response = requests.get("http://localhost:8000/api/status", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print("✅ Backend API: FUNCIONANDO")
            print(f"   📊 Versión: {data.get('version', 'N/A')}")
            print(f"   🧠 Estado: {data.get('status', 'N/A')}")
        else:
            print(f"⚠️  Backend API: Status {response.status_code}")
    except Exception as e:
        print(f"❌ Backend API: ERROR - {e}")
    
    # Test 3: Chat Endpoint
    print("\n💬 Probando Chat...")
    try:
        response = requests.post("http://localhost:8000/api/chat", 
                               json={"message": "Hola ARIA"}, 
                               timeout=10)
        if response.status_code == 200:
            data = response.json()
            print("✅ Chat: FUNCIONANDO")
            print(f"   🤖 Respuesta: {data.get('response', 'N/A')[:50]}...")
        else:
            print(f"⚠️  Chat: Status {response.status_code}")
    except Exception as e:
        print(f"❌ Chat: ERROR - {e}")
    
    print("\n🎯 RESUMEN:")
    print("=" * 40)
    print("✅ Si todo muestra 'FUNCIONANDO', ARIA está listo")
    print("🌐 Accede a: http://localhost:3000")
    print("🔗 API Backend: http://localhost:8000")
    print("\n💡 Si hay errores, verifica que las ventanas del terminal estén abiertas")

if __name__ == "__main__":
    test_aria()