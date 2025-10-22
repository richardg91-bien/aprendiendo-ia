import requests
import json

def test_simple_connection():
    """Prueba simple de conexión a ARIA"""
    try:
        print("🔍 Probando conexión básica a ARIA...")
        
        # Probar endpoint de status
        response = requests.get("http://localhost:5000/api/status", timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            print("✅ ARIA está funcionando correctamente!")
            print(f"   Mensaje: {data.get('message', 'N/A')}")
            print(f"   Servicios: {len(data.get('servicios', {}))}")
            return True
        else:
            print(f"❌ Error: Status code {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ No se puede conectar a ARIA (¿Está el servidor ejecutándose?)")
        return False
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        return False

if __name__ == "__main__":
    print("🤖 Test Simple de ARIA")
    print("=" * 30)
    test_simple_connection()