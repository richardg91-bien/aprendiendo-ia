import requests
import json

def test_simple():
    print("🧪 PRUEBA SIMPLE")
    
    try:
        # Probar status
        resp = requests.get("http://localhost:8000/api/status", timeout=3)
        print(f"✅ Status: {resp.status_code}")
        
        # Probar chat
        chat_data = {"message": "¿Qué has aprendido?"}
        resp = requests.post("http://localhost:8000/api/chat", json=chat_data, timeout=5)
        
        if resp.status_code == 200:
            data = resp.json()
            response = data.get("response", "Sin respuesta")
            confidence = data.get("confidence", 0)
            
            print(f"🤖 Respuesta: {response[:100]}...")
            print(f"📊 Confianza: {confidence}%")
            
            if "Interesante. Me dijiste:" in response:
                print("❌ RESPUESTA GENÉRICA")
            elif "elementos de conocimiento" in response or "científica" in response:
                print("✅ CONOCIMIENTO REAL")
            else:
                print("🔍 RESPUESTA DIFERENTE")
        else:
            print(f"❌ Error HTTP: {resp.status_code}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_simple()