#!/usr/bin/env python3
"""
🧪 Test de Aprendizaje ARIA
============================

Script para probar si ARIA está realmente aprendiendo de Google/Internet.
"""

import requests
import json
import time

def test_learning():
    """Prueba el sistema de aprendizaje de ARIA"""
    
    print("🧪 PROBANDO SISTEMA DE APRENDIZAJE DE ARIA")
    print("=" * 50)
    
    base_url = "http://localhost:5000"
    
    # Temas de prueba
    topics = [
        {"tema": "inteligencia artificial 2024", "profundidad": "intermedio"},
        {"tema": "Python programming", "profundidad": "basico"},
        {"tema": "machine learning algorithms", "profundidad": "avanzado"}
    ]
    
    for i, topic in enumerate(topics, 1):
        print(f"\n🔍 Prueba {i}: Aprendiendo sobre '{topic['tema']}'...")
        print(f"   📊 Profundidad: {topic['profundidad']}")
        
        try:
            # Probar endpoint de aprendizaje
            response = requests.post(
                f"{base_url}/api/aprender",
                json=topic,
                timeout=15
            )
            
            if response.status_code == 200:
                data = response.json()
                
                if data.get('success'):
                    print(f"   ✅ Aprendizaje exitoso!")
                    print(f"   📚 Fuentes procesadas: {data.get('fuentes_procesadas', 0)}")
                    print(f"   🎯 Tipo: {data.get('tipo_busqueda', 'desconocido')}")
                    
                    resumen = data.get('resumen_aprendizaje', '')
                    if resumen:
                        print(f"   📖 Resumen: {resumen[:100]}...")
                    
                    # Si hay conocimiento web específico
                    if data.get('conocimiento_web'):
                        print(f"   🌐 Conocimiento web: {len(data['conocimiento_web'])} entradas")
                
                else:
                    print(f"   ❌ Aprendizaje falló: {data.get('error', 'Error desconocido')}")
                    
            else:
                print(f"   ❌ Error HTTP {response.status_code}")
                
        except requests.exceptions.Timeout:
            print(f"   ⏰ Timeout - el aprendizaje tomó demasiado tiempo")
        except requests.exceptions.ConnectionError:
            print(f"   🔌 Error de conexión - ¿Está el servidor corriendo?")
        except Exception as e:
            print(f"   ❌ Error inesperado: {e}")
        
        # Pausa entre pruebas
        if i < len(topics):
            time.sleep(2)
    
    print(f"\n" + "=" * 50)
    print("🎯 Pruebas de aprendizaje completadas")
    print("💡 Revisa los resultados arriba para ver si ARIA está aprendiendo realmente")

def test_web_search():
    """Prueba específicamente la búsqueda web"""
    
    print("\n🌐 PROBANDO BÚSQUEDA WEB DIRECTA")
    print("=" * 30)
    
    base_url = "http://localhost:5000"
    queries = ["artificial intelligence 2024", "Python tutorial", "machine learning"]
    
    for query in queries:
        print(f"\n🔍 Buscando: '{query}'...")
        
        try:
            response = requests.post(
                f"{base_url}/api/buscar_web",
                json={"query": query, "profundidad": 3},
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                
                if data.get('success'):
                    print(f"   ✅ Búsqueda exitosa")
                    print(f"   📊 Resultados: {data.get('resultados_encontrados', 0)}")
                    print(f"   🔍 Fuente: {data.get('fuente', 'desconocida')}")
                    
                    # Mostrar primer resultado si existe
                    resultados = data.get('resultados', [])
                    if resultados:
                        primer = resultados[0]
                        print(f"   📄 Primer resultado: {primer.get('titulo', 'Sin título')}")
                        print(f"   🌐 URL: {primer.get('url', 'Sin URL')}")
                        print(f"   📝 Tipo: {primer.get('tipo', 'desconocido')}")
                
                else:
                    print(f"   ❌ Búsqueda falló")
                    
            else:
                print(f"   ❌ Error HTTP {response.status_code}")
                
        except Exception as e:
            print(f"   ❌ Error: {e}")

if __name__ == "__main__":
    test_learning()
    test_web_search()