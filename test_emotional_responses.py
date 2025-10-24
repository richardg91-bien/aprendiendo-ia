#!/usr/bin/env python3
"""
🎭 PRUEBA DE RESPUESTAS EMOCIONALES MEJORADAS
===========================================

Script para probar las nuevas respuestas emocionales de ARIA
"""

import requests
import json
import time

def test_emotional_responses():
    """Probar diferentes tipos de preguntas emocionales"""
    
    base_url = "http://localhost:5000/api/chat/futuristic"
    
    test_messages = [
        "como te sientes",
        "cómo te sientes ARIA",
        "how do you feel",
        "¿estás bien?",
        "te sientes bien",
        "cual es tu estado emocional",
        "hola como estas",
    ]
    
    print("🎭 PROBANDO RESPUESTAS EMOCIONALES DE ARIA")
    print("=" * 50)
    
    for i, message in enumerate(test_messages, 1):
        print(f"\n{i}. Mensaje: '{message}'")
        
        try:
            response = requests.post(base_url, json={
                'message': message,
                'emotion_context': 'neutral'
            }, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    print(f"   ✅ ARIA: {data['response'][:100]}...")
                    print(f"   🎭 Emoción: {data.get('emotion', 'No detectada')}")
                    
                    # Información de emociones detectadas
                    if data.get('aria_emotion'):
                        aria_emotion = data['aria_emotion']
                        print(f"   🤖 Emoción ARIA: {aria_emotion.get('emotion_name', 'No especificada')}")
                        print(f"   🎨 Color: {aria_emotion.get('color', 'No especificado')}")
                else:
                    print(f"   ❌ Error: {data.get('error', 'Error desconocido')}")
            else:
                print(f"   ❌ Error HTTP: {response.status_code}")
                
        except requests.exceptions.ConnectionError:
            print(f"   ❌ No se puede conectar al servidor")
            break
        except Exception as e:
            print(f"   ❌ Error: {e}")
        
        # Pausa entre requests
        time.sleep(1)
    
    print("\n" + "=" * 50)
    print("✅ Prueba completada")

if __name__ == "__main__":
    test_emotional_responses()