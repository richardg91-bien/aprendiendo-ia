import requests
import json

def test_aria():
    print("🧪 PRUEBA DE ARIA")
    
    try:
        # Probar status
        resp = requests.get("http://localhost:8000/api/status", timeout=3)
        print(f"✅ Status: {resp.json()}")
        
        # Probar diferentes preguntas
        preguntas = [
            "hola",
            "¿Qué has aprendido?",
            "¿Qué sabes sobre cloud computing?",
            "¿Tienes información sobre FPGAs?"
        ]
        
        for pregunta in preguntas:
            print(f"\n❓ {pregunta}")
            resp = requests.post("http://localhost:8000/api/chat", 
                               json={"message": pregunta}, 
                               timeout=5)
            
            if resp.status_code == 200:
                data = resp.json()
                response = data.get("response", "Sin respuesta")
                confidence = data.get("confidence", 0)
                advanced = data.get("advanced_mode", False)
                
                print(f"🤖 {response[:100]}{'...' if len(response) > 100 else ''}")
                print(f"📊 Confianza: {confidence:.0%} | Avanzado: {advanced}")
                
                if "Interesante. Me dijiste:" in response:
                    print("❌ RESPUESTA GENÉRICA")
                elif "conocimiento real" in response or "científica" in response:
                    print("✅ CONOCIMIENTO REAL")
                else:
                    print("🔍 OTRA RESPUESTA")
            else:
                print(f"❌ Error HTTP: {resp.status_code}")
    
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_aria()