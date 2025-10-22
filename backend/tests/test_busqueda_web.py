#!/usr/bin/env python3
"""
Script para probar específicamente la funcionalidad de búsqueda web
"""

import requests
import json
from time import sleep

def test_web_search():
    """Prueba la búsqueda web de ARIA"""
    base_url = "http://localhost:3000"
    
    print("🔍 Probando búsqueda web de ARIA")
    print("=" * 40)
    
    # Términos de búsqueda de prueba
    test_searches = [
        "inteligencia artificial",
        "programación Python",
        "machine learning",
        "desarrollo web",
        "bases de datos"
    ]
    
    for i, search_term in enumerate(test_searches, 1):
        print(f"\n🔍 Prueba {i}: Buscando '{search_term}'...")
        
        try:
            response = requests.post(
                f"{base_url}/api/buscar_web",
                json={"consulta": search_term},
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                
                if data.get('success'):
                    resultados = data.get('resultados', [])
                    total = data.get('total_resultados', 0)
                    
                    print(f"   ✅ Búsqueda exitosa: {total} resultados")
                    
                    for j, resultado in enumerate(resultados[:2], 1):  # Mostrar solo los primeros 2
                        titulo = resultado.get('titulo', 'Sin título')[:50]
                        fuente = resultado.get('fuente', 'Fuente desconocida')
                        url = resultado.get('url', 'Sin URL')
                        
                        print(f"   📄 {j}. {titulo}...")
                        print(f"      🔗 {url}")
                        print(f"      📰 Fuente: {fuente}")
                        
                else:
                    print(f"   ❌ Búsqueda falló: {data.get('error', 'Error desconocido')}")
                    
            else:
                print(f"   ❌ Error HTTP {response.status_code}")
                
        except requests.exceptions.Timeout:
            print(f"   ⏰ Timeout en la búsqueda")
        except requests.exceptions.ConnectionError:
            print(f"   🔌 Error de conexión - ¿Está el servidor corriendo?")
        except Exception as e:
            print(f"   ❌ Error inesperado: {e}")
        
        # Pausa breve entre búsquedas
        if i < len(test_searches):
            sleep(0.5)
    
    print(f"\n" + "=" * 40)
    print("🎯 Pruebas de búsqueda web completadas")
    print("💡 Prueba la búsqueda web en: http://localhost:3000")

if __name__ == "__main__":
    test_web_search()