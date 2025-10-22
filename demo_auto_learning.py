"""
🚀 Demo del Sistema de Aprendizaje Autónomo de ARIA
==================================================

Este script demuestra las capacidades de aprendizaje autónomo
implementadas en ARIA.
"""

import time
import requests
import json

def test_auto_learning_system():
    """Prueba el sistema de aprendizaje autónomo"""
    base_url = "http://127.0.0.1:8000"
    
    print("🤖 ARIA - Demo de Aprendizaje Autónomo")
    print("=" * 50)
    
    # 1. Verificar estado del servidor
    try:
        response = requests.get(f"{base_url}/api/status", timeout=5)
        if response.status_code == 200:
            print("✅ Servidor ARIA activo")
        else:
            print("❌ Servidor no disponible")
            return
    except:
        print("❌ No se puede conectar al servidor")
        return
    
    # 2. Verificar estado del aprendizaje autónomo
    print("\n🧠 Verificando sistema de aprendizaje autónomo...")
    try:
        response = requests.get(f"{base_url}/api/auto_learning/status")
        data = response.json()
        
        if data.get('success'):
            status = data['status']
            print(f"Estado: {'🟢 Activo' if status['is_running'] else '🔴 Inactivo'}")
            print(f"Conocimientos totales: {status['knowledge_stats'].get('total_knowledge', 0)}")
            print(f"Temas únicos: {status['knowledge_stats'].get('unique_topics', 0)}")
            print(f"Confianza promedio: {status['knowledge_stats'].get('avg_confidence', 0):.2%}")
        else:
            print("⚠️ Sistema de aprendizaje autónomo no disponible")
    except Exception as e:
        print(f"⚠️ Error verificando estado: {e}")
    
    # 3. Iniciar aprendizaje autónomo si no está activo
    print("\n🚀 Iniciando sistema de aprendizaje autónomo...")
    try:
        response = requests.post(f"{base_url}/api/auto_learning/start")
        data = response.json()
        
        if data.get('success'):
            print("✅ Sistema de aprendizaje autónomo iniciado")
            print(f"Mensaje: {data['message']}")
        else:
            print(f"⚠️ {data.get('message', 'Error desconocido')}")
    except Exception as e:
        print(f"❌ Error iniciando sistema: {e}")
    
    # 4. Ejecutar sesión manual de aprendizaje
    print("\n📚 Ejecutando sesión rápida de aprendizaje...")
    try:
        response = requests.post(
            f"{base_url}/api/auto_learning/trigger_session",
            json={"type": "quick"}
        )
        data = response.json()
        
        if data.get('success'):
            print("✅ Sesión de aprendizaje completada")
            new_status = data.get('status', {})
            print(f"Nuevos conocimientos: {new_status.get('knowledge_stats', {}).get('total_knowledge', 0)}")
        else:
            print(f"⚠️ {data.get('message', 'Error en sesión')}")
    except Exception as e:
        print(f"❌ Error en sesión: {e}")
    
    # 5. Probar búsqueda web con aprendizaje
    print("\n🔍 Probando búsqueda web con aprendizaje...")
    test_queries = [
        "inteligencia artificial",
        "machine learning",
        "programación Python"
    ]
    
    for query in test_queries:
        try:
            print(f"\nBuscando: '{query}'")
            response = requests.post(
                f"{base_url}/api/busqueda_web",
                json={"query": query, "depth": 3},
                timeout=15
            )
            
            data = response.json()
            
            if data.get('success'):
                resultados = data.get('resultados', [])
                print(f"✅ {len(resultados)} resultados encontrados")
                print(f"Auto-learning activo: {data.get('auto_learning', False)}")
                
                # Mostrar primer resultado
                if resultados:
                    primer = resultados[0]
                    print(f"📄 Primer resultado: {primer.get('titulo', 'Sin título')}")
                    print(f"🔗 Fuente: {primer.get('fuente', 'Desconocida')}")
            else:
                print(f"❌ Error: {data.get('message', 'Error desconocido')}")
                
        except Exception as e:
            print(f"❌ Error en búsqueda '{query}': {e}")
        
        time.sleep(2)  # Pausa entre búsquedas
    
    # 6. Verificar estado final
    print("\n📊 Estado final del sistema...")
    try:
        response = requests.get(f"{base_url}/api/auto_learning/status")
        data = response.json()
        
        if data.get('success'):
            status = data['status']
            print("✅ Estado actualizado:")
            print(f"  • Conocimientos: {status['knowledge_stats'].get('total_knowledge', 0)}")
            print(f"  • Temas únicos: {status['knowledge_stats'].get('unique_topics', 0)}")
            print(f"  • Aprendizaje activo: {'Sí' if status['is_running'] else 'No'}")
            
            if status.get('last_session'):
                session = status['last_session']
                print(f"  • Última sesión: {session.get('topics_learned', 0)} temas")
                print(f"  • Calidad: {session.get('quality', 0):.1%}")
        
    except Exception as e:
        print(f"❌ Error obteniendo estado final: {e}")
    
    print("\n🎉 Demo completada!")
    print("\n💡 El sistema de aprendizaje autónomo de ARIA:")
    print("   • Busca información automáticamente")
    print("   • Aprende de cada búsqueda web")
    print("   • Mejora continuamente sus respuestas")
    print("   • Programa sesiones automáticas de aprendizaje")
    print("   • Mantiene una base de conocimientos persistente")

if __name__ == "__main__":
    test_auto_learning_system()