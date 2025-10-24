#!/usr/bin/env python3
"""
🔍 Prueba Rápida de Búsqueda Web Real
===================================
"""

import requests
import json

def test_single_search():
    """Prueba una sola búsqueda web para verificar si es real"""
    
    print("🌐 PROBANDO BÚSQUEDA WEB REAL EN ARIA")
    print("=" * 40)
    
    try:
        print("🔍 Realizando búsqueda: 'artificial intelligence'...")
        
        response = requests.post(
            "http://localhost:5000/api/buscar_web",
            json={"query": "artificial intelligence", "profundidad": 2},
            timeout=20
        )
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Respuesta recibida!")
            print(f"📊 Status: {data.get('success')}")
            print(f"🔍 Fuente: {data.get('fuente', 'No especificada')}")
            print(f"📈 Resultados: {data.get('resultados_encontrados', 0)}")
            
            # Ver primer resultado
            resultados = data.get('resultados', [])
            if resultados:
                primer = resultados[0]
                print(f"\n📄 PRIMER RESULTADO:")
                print(f"   📝 Título: {primer.get('titulo', 'Sin título')}")
                print(f"   🌐 URL: {primer.get('url', 'Sin URL')}")
                print(f"   📰 Tipo: {primer.get('tipo', 'desconocido')}")
                print(f"   🎯 Fuente: {primer.get('fuente', 'desconocida')}")
                
                # Esto nos dirá si es búsqueda real o simulada
                if 'tipo' in primer:
                    if primer['tipo'] == 'resultado_real':
                        print("\n🎉 ¡BÚSQUEDA WEB REAL FUNCIONANDO!")
                    else:
                        print("\n⚠️ Usando búsqueda simulada")
                
            print(f"\n📖 Resumen: {data.get('resumen', 'Sin resumen')[:200]}...")
            
        else:
            print(f"❌ Error HTTP: {response.status_code}")
            
    except requests.exceptions.Timeout:
        print("⏰ Timeout - la búsqueda tardó demasiado")
    except requests.exceptions.ConnectionError:
        print("🔌 Error de conexión - servidor no disponible")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_single_search()