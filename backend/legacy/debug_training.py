import requests
import json
import traceback

def test_training_endpoint():
    """Prueba específica para el endpoint de entrenamiento"""
    try:
        print("🧠 Probando endpoint de entrenamiento neural...")
        
        url = "http://localhost:5000/api/entrenar_red_neuronal"
        payload = {"epochs": 10}
        headers = {"Content-Type": "application/json"}
        
        print(f"URL: {url}")
        print(f"Payload: {payload}")
        
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        
        print(f"Status Code: {response.status_code}")
        print(f"Response Headers: {dict(response.headers)}")
        
        if response.text:
            try:
                data = response.json()
                print(f"Response JSON: {json.dumps(data, indent=2)}")
            except:
                print(f"Response Text: {response.text}")
        
        return response.status_code == 200
        
    except requests.exceptions.ConnectionError:
        print("❌ No se puede conectar al servidor")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🔍 Debug del Entrenamiento Neural")
    print("=" * 40)
    test_training_endpoint()