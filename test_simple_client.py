import requests

try:
    # Probar status
    resp = requests.get("http://localhost:8001/api/status", timeout=3)
    print(f"✅ Status: {resp.json()}")
    
    # Probar chat
    resp = requests.post("http://localhost:8001/api/chat", 
                        json={"message": "¿Qué has aprendido?"}, 
                        timeout=5)
    
    if resp.status_code == 200:
        data = resp.json()
        print(f"🤖 Respuesta: {data['response']}")
        print(f"📊 Confianza: {data['confidence']}")
    else:
        print(f"❌ Error: {resp.status_code}")
        
except Exception as e:
    print(f"❌ Error: {e}")