#!/usr/bin/env python3
"""
Script de prueba del endpoint de entrenamiento neural de ARIA
"""

import requests
import json
import sys
import time

def wait_for_server(url, max_attempts=10):
    """Espera a que el servidor esté disponible"""
    for i in range(max_attempts):
        try:
            response = requests.get(f"{url}/api/status", timeout=2)
            if response.status_code == 200:
                return True
        except:
            pass
        time.sleep(1)
    return False

def test_neural_training():
    """Prueba específica del entrenamiento neural"""
    base_url = "http://localhost:5000"
    
    print("🧠 Probando Entrenamiento Neural de ARIA")
    print("=" * 50)
    
    # Verificar que el servidor esté disponible
    print("🔍 Verificando conexión al servidor...")
    if not wait_for_server(base_url, 5):
        print("❌ Servidor no disponible en http://localhost:5000")
        print("   Asegúrate de que ARIA esté ejecutándose")
        return False
    
    print("✅ Servidor disponible")
    
    # Probar el endpoint de entrenamiento
    try:
        print("\n🚀 Enviando solicitud de entrenamiento...")
        
        payload = {
            "epochs": 25
        }
        
        response = requests.post(
            f"{base_url}/api/entrenar_red_neuronal",
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=15
        )
        
        print(f"📊 Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            if data.get("success"):
                print("✅ Entrenamiento EXITOSO!")
                print(f"   📈 Precisión inicial: {data.get('accuracy_inicial', 'N/A')}%")
                print(f"   🎯 Precisión final: {data.get('accuracy_final', 'N/A')}%")
                print(f"   📉 Loss final: {data.get('loss_final', 'N/A')}")
                print(f"   🔄 Epochs: {data.get('epochs_completados', 'N/A')}")
                print(f"   ⏱️ Tiempo: {data.get('tiempo_entrenamiento', 'N/A')}")
                return True
            else:
                print(f"❌ Entrenamiento falló: {data.get('message', 'Error desconocido')}")
                return False
        else:
            print(f"❌ Error HTTP {response.status_code}")
            try:
                error_data = response.json()
                print(f"   Mensaje: {error_data.get('message', 'Sin mensaje')}")
            except:
                print(f"   Respuesta: {response.text[:200]}")
            return False
            
    except requests.exceptions.Timeout:
        print("❌ Timeout - El entrenamiento tardó demasiado")
        return False
    except requests.exceptions.ConnectionError:
        print("❌ Error de conexión - Servidor no disponible")
        return False
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        return False

if __name__ == "__main__":
    success = test_neural_training()
    sys.exit(0 if success else 1)