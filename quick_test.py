#!/usr/bin/env python3
"""
🚀 PRUEBA RÁPIDA DE BÚSQUEDA WEB
===============================

Script simple para probar búsqueda web sin interferir con el servidor.
"""

import requests
import json

def quick_test():
    """Prueba rápida y simple"""
    print("🔍 Probando búsqueda web de ARIA...")
    
    try:
        # Usar requests con timeout corto para evitar bloqueos
        response = requests.post(
            "http://localhost:5000/api/buscar_web",
            json={"query": "artificial intelligence", "profundidad": 2},
            timeout=5  # Solo 5 segundos
        )
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Respuesta exitosa!")
            print(f"Fuente: {data.get('fuente', 'N/A')}")
            print(f"Éxito: {data.get('success', False)}")
            
            resultados = data.get('resultados', [])
            if resultados and len(resultados) > 0:
                primer = resultados[0]
                print(f"Primer resultado - Tipo: {primer.get('tipo', 'N/A')}")
                print(f"URL: {primer.get('url', 'N/A')[:50]}...")
        else:
            print(f"❌ Error: {response.status_code}")
            
    except requests.exceptions.Timeout:
        print("⏰ Timeout (posible búsqueda real en curso)")
    except requests.exceptions.ConnectionError:
        print("🔌 Servidor no disponible")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    quick_test()