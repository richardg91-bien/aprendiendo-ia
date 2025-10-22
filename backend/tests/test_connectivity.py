#!/usr/bin/env python3
"""
Test rápido de conectividad para ARIA
"""

import requests
import sys

def test_connectivity():
    """Prueba rápida de conectividad"""
    print("🔍 Probando conectividad con ARIA...")
    
    try:
        # Test 1: Página principal
        print("📄 Probando página principal...")
        response = requests.get("http://localhost:3000", timeout=5)
        if response.status_code == 200:
            print("   ✅ Página principal: OK")
        else:
            print(f"   ❌ Página principal: {response.status_code}")
            
        # Test 2: API Status
        print("📊 Probando API status...")
        response = requests.get("http://localhost:3000/api/status", timeout=5)
        if response.status_code == 200:
            print("   ✅ API status: OK")
            data = response.json()
            print(f"   📋 Versión: {data.get('version', 'N/A')}")
        else:
            print(f"   ❌ API status: {response.status_code}")
            
        # Test 3: Búsqueda web
        print("🔍 Probando búsqueda web...")
        response = requests.post(
            "http://localhost:3000/api/buscar_web",
            json={"consulta": "test"},
            timeout=5
        )
        if response.status_code == 200:
            print("   ✅ Búsqueda web: OK")
            data = response.json()
            total = data.get('total_resultados', 0)
            print(f"   📈 Resultados: {total}")
        else:
            print(f"   ❌ Búsqueda web: {response.status_code}")
            
        print("\n🎉 Tests completados")
        return True
        
    except requests.exceptions.ConnectionError:
        print("❌ Error: No se puede conectar al servidor")
        print("💡 Verifica que el servidor esté corriendo en localhost:3000")
        return False
    except requests.exceptions.Timeout:
        print("❌ Error: Timeout en la conexión")
        return False
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        return False

if __name__ == "__main__":
    success = test_connectivity()
    sys.exit(0 if success else 1)