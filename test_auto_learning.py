"""
🔍 Verificador específico del Aprendizaje Autónomo
================================================
"""

import requests
import json

def test_auto_learning():
    print("🔍 VERIFICANDO APRENDIZAJE AUTÓNOMO")
    print("=" * 50)
    
    base_url = "http://localhost:8000"
    
    # Test 1: Status del aprendizaje
    print("1. 📊 Probando status del aprendizaje...")
    try:
        response = requests.get(f"{base_url}/api/auto_learning/status", timeout=5)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Respuesta: {json.dumps(data, indent=2)}")
        else:
            print(f"   ❌ Error: {response.text}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    print()
    
    # Test 2: Intentar iniciar aprendizaje
    print("2. 🚀 Probando iniciar aprendizaje...")
    try:
        response = requests.post(f"{base_url}/api/auto_learning/start", timeout=5)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Respuesta: {json.dumps(data, indent=2)}")
        else:
            print(f"   ❌ Error: {response.text}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    print()
    
    # Test 3: Probar sesión manual
    print("3. 🧠 Probando sesión manual...")
    try:
        response = requests.post(f"{base_url}/api/auto_learning/trigger_session", 
                               json={"type": "quick"}, timeout=10)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Respuesta: {json.dumps(data, indent=2)}")
        else:
            print(f"   ❌ Error: {response.text}")
    except Exception as e:
        print(f"   ❌ Error: {e}")

if __name__ == "__main__":
    test_auto_learning()