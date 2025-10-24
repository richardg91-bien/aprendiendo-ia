#!/usr/bin/env python3
"""
🎭 PRUEBA DE EDENAI PARA ARIA
============================

Script para probar la integración de EdenAI con el sistema de emociones
"""

import os
from dotenv import load_dotenv
load_dotenv()

# Importar nuestro detector
from emotion_detector import init_emotion_detector, detect_user_emotion, detect_aria_emotion

def test_edenai():
    """Prueba EdenAI con diferentes textos"""
    
    # Obtener API key
    api_key = os.environ.get('EDENAI_API_KEY')
    
    if not api_key:
        print("❌ No se encontró EDENAI_API_KEY")
        return
    
    print(f"🔑 API Key encontrada: {api_key[:20]}...")
    
    # Inicializar detector
    try:
        init_emotion_detector(api_key)
        print("✅ Detector de emociones inicializado")
    except Exception as e:
        print(f"❌ Error inicializando detector: {e}")
        return
    
    # Textos de prueba
    test_texts = [
        "¡Estoy muy feliz hoy!",
        "Me siento triste y melancólico",
        "¡Qué emocionante! No puedo esperar",
        "Estoy confundido, no entiendo nada",
        "Me da mucho miedo este examen",
        "¡Excelente trabajo, ARIA!",
        "No funciona nada, qué frustante",
        "Hola, ¿cómo estás?"
    ]
    
    print("\n🎭 PRUEBAS DE DETECCIÓN DE EMOCIONES:")
    print("=" * 50)
    
    for i, text in enumerate(test_texts, 1):
        print(f"\n{i}. Texto: '{text}'")
        
        try:
            # Detectar emoción del usuario
            result = detect_user_emotion(text)
            
            if result['success']:
                print(f"   🎭 Emoción: {result['emotion_name']}")
                print(f"   🎨 Color: {result['color']}")
                print(f"   📊 Confianza: {result['confidence']:.2f}")
                print(f"   🔧 Proveedor: {result['provider']}")
            else:
                print(f"   ❌ Error en detección")
                
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    print("\n" + "=" * 50)
    print("✅ Prueba completada")

if __name__ == "__main__":
    test_edenai()