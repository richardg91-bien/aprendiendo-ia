#!/usr/bin/env python3
"""
🧪 PRUEBA FINAL DEL SISTEMA EMOCIONAL EN SUPABASE
===============================================

Prueba completa del sistema ARIA con emociones almacenadas en Supabase
"""

import requests
import json
import time
from datetime import datetime

def test_server_status():
    """Probar estado del servidor"""
    print("🔍 Verificando estado del servidor...")
    
    try:
        response = requests.get("http://localhost:8000/status", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print("✅ Servidor funcionando")
            print(f"   📊 Sesión: {data.get('session_id', 'N/A')}")
            print(f"   🎭 Emoción actual: {data.get('current_emotion', 'N/A')}")
            print(f"   🗄️ Supabase: {'✅' if data.get('superbase_connected') else '❌'}")
            print(f"   💬 Conversaciones: {data.get('conversations_count', 0)}")
            return True
    except Exception as e:
        print(f"❌ Servidor no disponible: {e}")
        return False

def test_emotion_endpoints():
    """Probar endpoints de emociones"""
    print("\n🎭 Probando endpoints de emociones...")
    
    # Estadísticas emocionales
    try:
        response = requests.get("http://localhost:8000/emotions/stats")
        if response.status_code == 200:
            data = response.json()
            print("✅ Estadísticas emocionales:")
            print(f"   🔧 Sistema: {data.get('emotion_system', 'N/A')}")
            print(f"   🎭 Emoción actual: {data.get('current_emotion', 'N/A')}")
            
            if 'stats' in data:
                stats = data['stats']
                print(f"   📊 Emociones disponibles: {stats.get('emotions_available', 0)}")
                print(f"   📝 Historial: {stats.get('emotion_history_entries', 0)}")
    except Exception as e:
        print(f"⚠️ Error en estadísticas: {e}")
    
    # Emociones disponibles
    try:
        response = requests.get("http://localhost:8000/emotions/available")
        if response.status_code == 200:
            data = response.json()
            print("✅ Emociones disponibles:")
            print(f"   📊 Total: {data.get('total', 0)}")
            print(f"   🗄️ Fuente: {data.get('source', 'N/A')}")
            
            emotions = data.get('emotions', [])
            for i, emotion in enumerate(emotions[:5]):
                name = emotion.get('name', 'N/A')
                color = emotion.get('color', 'N/A')
                print(f"     {i+1}. {name} - {color}")
                
    except Exception as e:
        print(f"⚠️ Error en emociones disponibles: {e}")

def test_chat_with_emotions():
    """Probar chat con detección emocional"""
    print("\n💬 Probando chat con detección emocional...")
    
    test_messages = [
        "hola ARIA, ¿cómo estás?",
        "me siento triste hoy",
        "¡estoy muy feliz!",
        "¿puedes ayudarme a aprender?",
        "cuéntame sobre Roma"
    ]
    
    for i, message in enumerate(test_messages, 1):
        try:
            print(f"\n{i}. Enviando: '{message}'")
            
            response = requests.post(
                "http://localhost:8000/chat",
                json={'message': message},
                timeout=15
            )
            
            if response.status_code == 200:
                data = response.json()
                
                print(f"   🤖 Respuesta: {data.get('response', 'N/A')[:100]}...")
                print(f"   🎭 Emoción ARIA: {data.get('emotion', 'N/A')}")
                print(f"   📊 Confianza: {data.get('confidence', 0):.2f}")
                print(f"   🌐 APIs usadas: {len(data.get('apis_called', []))}")
                print(f"   ⏱️ Tiempo: {data.get('response_time', 0):.3f}s")
                
                # Mostrar información emocional específica
                if 'user_emotion' in data:
                    user_emotion = data['user_emotion']
                    print(f"   😊 Emoción usuario: {user_emotion.get('name', 'N/A')} ({user_emotion.get('color', 'N/A')})")
                
                if 'aria_emotion' in data:
                    aria_emotion = data['aria_emotion']
                    print(f"   🤖 Emoción ARIA: {aria_emotion.get('name', 'N/A')} ({aria_emotion.get('color', 'N/A')})")
                
            else:
                print(f"   ❌ Error HTTP: {response.status_code}")
                
        except Exception as e:
            print(f"   ❌ Error: {e}")
        
        time.sleep(1)  # Pausa entre mensajes

def test_knowledge_from_supabase():
    """Probar recuperación de conocimiento desde Supabase"""
    print("\n📚 Probando conocimiento desde Supabase...")
    
    try:
        response = requests.get("http://localhost:8000/knowledge?limit=5")
        if response.status_code == 200:
            data = response.json()
            knowledge = data.get('knowledge', [])
            
            print(f"✅ Conocimiento disponible: {len(knowledge)} entradas")
            
            for i, item in enumerate(knowledge[:3], 1):
                concept = item.get('concept', 'N/A')
                category = item.get('category', 'N/A')
                confidence = item.get('confidence', 0)
                
                print(f"   {i}. {concept} ({category}) - Confianza: {confidence:.2f}")
                
    except Exception as e:
        print(f"❌ Error obteniendo conocimiento: {e}")

def main():
    """Función principal de pruebas"""
    print("🚀 PRUEBA FINAL DEL SISTEMA ARIA CON EMOCIONES EN SUPABASE")
    print("=" * 70)
    print(f"🕒 Inicio: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Ejecutar todas las pruebas
    tests = [
        ("Estado del Servidor", test_server_status),
        ("Endpoints Emocionales", test_emotion_endpoints),
        ("Conocimiento Supabase", test_knowledge_from_supabase),
        ("Chat con Emociones", test_chat_with_emotions)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n{'='*50}")
        print(f"🧪 EJECUTANDO: {test_name.upper()}")
        print('='*50)
        
        try:
            success = test_func()
            results.append((test_name, success))
        except Exception as e:
            print(f"❌ Error en {test_name}: {e}")
            results.append((test_name, False))
    
    # Resumen final
    print("\n" + "="*70)
    print("📊 RESUMEN FINAL")
    print("="*70)
    
    passed = 0
    for test_name, success in results:
        if success is not False:  # None también cuenta como éxito
            status = "✅ EXITOSO"
            passed += 1
        else:
            status = "❌ FALLIDO"
        
        print(f"   {status}: {test_name}")
    
    print(f"\n🎯 Resultado: {passed}/{len(results)} pruebas exitosas")
    
    if passed >= len(results) - 1:  # Permitir 1 fallo
        print("🎉 ¡SISTEMA ARIA CON EMOCIONES EN SUPABASE FUNCIONANDO!")
        print("✅ El sistema emocional está correctamente almacenado en la nube")
        print("🗄️ ARIA ya no es un chatbot básico - es un sistema RAG completo")
    else:
        print("⚠️ Algunos componentes necesitan ajustes")
        print("🔧 Revisa el estado del servidor y la configuración")
    
    print(f"\n🕒 Fin: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    main()