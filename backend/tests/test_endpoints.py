#!/usr/bin/env python3
"""
Script de prueba para verificar todos los endpoints de ARIA
"""

import requests
import json
import time

BASE_URL = "http://localhost:5000"

def test_endpoint(endpoint, method="GET", data=None):
    """Prueba un endpoint específico"""
    try:
        url = f"{BASE_URL}{endpoint}"
        print(f"\n🔍 Probando {method} {endpoint}")
        
        if method == "GET":
            response = requests.get(url)
        elif method == "POST":
            response = requests.post(url, json=data)
        
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"   ✅ Respuesta exitosa")
            if 'success' in result:
                print(f"   Success: {result['success']}")
            if 'message' in result:
                print(f"   Message: {result['message']}")
            return True
        else:
            print(f"   ❌ Error: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"   ❌ Error de conexión: {e}")
        return False

def main():
    print("🚀 Iniciando pruebas de endpoints de ARIA")
    print("=" * 50)
    
    # Dar tiempo al servidor para iniciar
    time.sleep(2)
    
    tests = [
        # Test básico de estado
        ("/api/status", "GET"),
        
        # Test de endpoints disponibles
        ("/api/test_endpoints", "GET"),
        
        # Test de chat
        ("/api/chat", "POST", {"mensaje": "Hola ARIA, ¿cómo estás?"}),
        
        # Test de búsqueda web
        ("/api/buscar_web", "POST", {"consulta": "Python programming"}),
        
        # Test de información de red neuronal
        ("/api/red_neuronal_info", "GET"),
        
        # Test de entrenamiento
        ("/api/entrenar_red_neuronal", "POST", {"datos": "test training data"})
    ]
    
    results = []
    
    for test in tests:
        endpoint = test[0]
        method = test[1]
        data = test[2] if len(test) > 2 else None
        
        success = test_endpoint(endpoint, method, data)
        results.append((endpoint, success))
        
        # Pausa pequeña entre tests
        time.sleep(1)
    
    print("\n" + "=" * 50)
    print("📊 RESUMEN DE PRUEBAS")
    print("=" * 50)
    
    passed = 0
    total = len(results)
    
    for endpoint, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {endpoint}")
        if success:
            passed += 1
    
    print(f"\n🏆 Resultado: {passed}/{total} pruebas exitosas")
    
    if passed == total:
        print("🎉 ¡TODOS LOS ENDPOINTS FUNCIONAN CORRECTAMENTE!")
    else:
        print("⚠️  Algunos endpoints necesitan revisión")

if __name__ == "__main__":
    main()