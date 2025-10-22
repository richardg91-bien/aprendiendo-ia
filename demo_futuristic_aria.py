"""
🚀 Demo del Sistema ARIA Futurista con Base de Datos en la Nube
============================================================

Este script demuestra todas las nuevas capacidades futuristas de ARIA:
- Base de datos en la nube
- Aprendizaje de otras IAs
- Sistema emocional con colores
- Interfaz futurista
"""

import time
import requests
import json
from datetime import datetime

def demo_futuristic_aria():
    """Demostración completa del sistema ARIA futurista"""
    
    print("🚀 ARIA FUTURISTIC SYSTEM DEMO")
    print("=" * 60)
    print("🤖 Asistente de IA del Futuro con Emociones y Aprendizaje en la Nube")
    print("=" * 60)
    
    base_url = "http://127.0.0.1:8000"
    
    # 1. Verificar conexión
    print("\n🔗 1. Verificando conexión con ARIA...")
    try:
        response = requests.get(f"{base_url}/api/status", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print("✅ ARIA está online y funcionando")
            print(f"   Versión: {data.get('version', 'N/A')}")
            print(f"   Estado: {data.get('status', 'N/A')}")
        else:
            print("❌ ARIA no está disponible")
            return
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        return
    
    # 2. Probar chat futurista
    print("\n💬 2. Probando chat futurista con emociones...")
    test_messages = [
        {"msg": "Hola ARIA, ¿cómo estás?", "expected_emotion": "neutral"},
        {"msg": "Quiero que aprendas sobre inteligencia artificial", "expected_emotion": "learning"},
        {"msg": "¡Excelente trabajo!", "expected_emotion": "happy"},
        {"msg": "Hay un problema con el sistema", "expected_emotion": "frustrated"}
    ]
    
    for i, test in enumerate(test_messages, 1):
        print(f"\n   Test {i}: {test['msg']}")
        try:
            response = requests.post(
                f"{base_url}/api/chat/futuristic",
                json={"message": test['msg']},
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                emotion = data.get('emotion', 'unknown')
                confidence = data.get('confidence', 0)
                
                # Mapeo de emociones a colores
                emotion_colors = {
                    'neutral': '🔵 Azul',
                    'learning': '🟢 Verde',
                    'happy': '🟡 Dorado',
                    'frustrated': '🔴 Rojo',
                    'thinking': '🟣 Púrpura'
                }
                
                color = emotion_colors.get(emotion, '⚪ Desconocido')
                
                print(f"   ✅ Respuesta: {data.get('response', '')[:80]}...")
                print(f"   🎭 Emoción: {emotion} ({color})")
                print(f"   📊 Confianza: {confidence:.1%}")
                
                if data.get('learned_something'):
                    print("   🧠 ARIA aprendió algo nuevo!")
                    
            else:
                print(f"   ❌ Error en respuesta: {response.status_code}")
                
        except Exception as e:
            print(f"   ❌ Error: {e}")
        
        time.sleep(1)
    
    # 3. Probar sistema de emociones
    print("\n🎭 3. Verificando sistema de emociones...")
    try:
        response = requests.get(f"{base_url}/api/cloud/emotions/recent")
        if response.status_code == 200:
            emotions = response.json()
            print(f"   ✅ {len(emotions)} emociones registradas")
            
            if emotions:
                print("   📊 Últimas emociones:")
                for emotion in emotions[:3]:
                    emo_type = emotion.get('emotion_type', 'unknown')
                    intensity = emotion.get('intensity', 0)
                    color = emotion.get('color_code', '#000000')
                    
                    print(f"      • {emo_type} ({intensity:.1%}) - Color: {color}")
            else:
                print("   ℹ️ No hay emociones registradas aún")
        else:
            print("   ⚠️ Sistema de emociones no disponible")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # 4. Probar estadísticas de la nube
    print("\n🌐 4. Verificando base de datos en la nube...")
    try:
        response = requests.get(f"{base_url}/api/cloud/stats")
        if response.status_code == 200:
            stats = response.json()
            print("   ✅ Estadísticas de la nube:")
            print(f"      📚 Conocimientos: {stats.get('knowledge_count', 0)}")
            print(f"      🤖 Fuentes IA: {stats.get('ai_sources', 0)}")
            print(f"      🎯 Confianza: {stats.get('confidence', 0):.1%}")
        else:
            print("   ⚠️ Estadísticas no disponibles")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # 5. Probar aprendizaje colaborativo
    print("\n🤖 5. Probando aprendizaje de otras IAs...")
    try:
        print("   🔄 Iniciando aprendizaje colaborativo...")
        response = requests.post(f"{base_url}/api/cloud/learn_from_ais", timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            print("   ✅ Aprendizaje colaborativo completado")
            print(f"      📖 Conocimientos aprendidos: {data.get('knowledge_learned', 0)}")
            print(f"      🌐 Fuentes consultadas: {data.get('sources', 0)}")
            print(f"      🎭 Emoción resultante: {data.get('emotion', 'neutral')}")
        else:
            print("   ⚠️ Aprendizaje colaborativo no disponible")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # 6. Probar búsqueda en la nube
    print("\n🔍 6. Probando búsqueda en conocimientos de la nube...")
    search_queries = ["inteligencia artificial", "machine learning", "python"]
    
    for query in search_queries:
        try:
            print(f"   🔍 Buscando: '{query}'")
            response = requests.post(
                f"{base_url}/api/cloud/search",
                json={"query": query, "limit": 3},
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                results = data.get('results', [])
                print(f"      ✅ {len(results)} resultados encontrados")
                
                for i, result in enumerate(results[:2], 1):
                    topic = result.get('topic', 'Sin título')
                    confidence = result.get('confidence_score', 0)
                    print(f"         {i}. {topic} (confianza: {confidence:.1%})")
            else:
                print(f"      ❌ Error en búsqueda: {response.status_code}")
                
        except Exception as e:
            print(f"      ❌ Error: {e}")
        
        time.sleep(0.5)
    
    # 7. Resumen final
    print(f"\n🎉 7. Resumen de la demostración")
    print("=" * 60)
    print("✅ FUNCIONALIDADES DEMOSTRADAS:")
    print("   🤖 Chat futurista con respuestas emocionales")
    print("   🎭 Sistema de emociones con colores visuales")
    print("   🌐 Base de datos en la nube operativa")
    print("   📊 Métricas y estadísticas en tiempo real")
    print("   🧠 Aprendizaje colaborativo de otras IAs")
    print("   🔍 Búsqueda inteligente en conocimientos")
    
    print("\n🌟 CARACTERÍSTICAS FUTURISTAS:")
    print("   🔵 Azul: Estado normal/interacción")
    print("   🟢 Verde: Aprendiendo conocimiento nuevo")
    print("   🔴 Rojo: Frustrada o con problemas")
    print("   🟡 Dorado: Feliz y satisfecha")
    print("   🟣 Púrpura: Pensando profundamente")
    
    print("\n🚀 INTERFAZ FUTURISTA:")
    print("   ✨ Efectos de partículas animadas")
    print("   🧠 Cerebro pulsante con emociones")
    print("   🎨 Colores que cambian según estado emocional")
    print("   📊 Métricas en tiempo real")
    print("   🌐 Panel de control de base de datos en la nube")
    
    print(f"\n🎯 ACCESO AL SISTEMA:")
    print(f"   🌐 Interfaz Web: http://127.0.0.1:8000")
    print(f"   🚀 Modo Futurista: Activado por defecto")
    print(f"   🖥️ Modo Clásico: Disponible como alternativa")
    
    print(f"\n💡 PRÓXIMOS PASOS:")
    print(f"   1. Configurar base de datos gratuita en Supabase")
    print(f"   2. Obtener APIs de Hugging Face para más IAs")
    print(f"   3. Personalizar colores emocionales")
    print(f"   4. Expandir conocimientos automáticamente")
    
    print(f"\n🎉 ¡ARIA DEL FUTURO ESTÁ LISTA!")
    print("=" * 60)

def show_cloud_setup_guide():
    """Muestra guía rápida de configuración de la nube"""
    print("\n📖 GUÍA RÁPIDA: CONFIGURAR BASE DE DATOS GRATUITA")
    print("-" * 50)
    print("1. 🌐 Ir a https://supabase.com")
    print("2. 📝 Crear cuenta gratuita")
    print("3. ➕ Crear nuevo proyecto")
    print("4. 🔑 Copiar URL y API Key")
    print("5. ⚙️ Configurar archivo .env:")
    print("   SUPABASE_URL=https://tu-proyecto.supabase.co")
    print("   SUPABASE_ANON_KEY=tu_clave_aqui")
    print("6. 🗃️ Ejecutar SQL para crear tablas (ver GUIA_BASE_DATOS_NUBE.md)")
    print("7. 🚀 Reiniciar ARIA para conectar a la nube")

if __name__ == "__main__":
    print("🚀 Iniciando demostración del sistema ARIA futurista...")
    time.sleep(2)
    
    demo_futuristic_aria()
    
    print("\n" + "=" * 60)
    show_cloud_setup_guide()
    print("=" * 60)
    
    print("\n🌟 ¡Gracias por probar ARIA del Futuro!")
    print("💖 Tu asistente de IA emocional está listo para evolucionar contigo")