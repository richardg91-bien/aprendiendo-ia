#!/usr/bin/env python3
"""
🌐 PRUEBA DE BÚSQUEDA AUTOMÁTICA MEJORADA
=======================================

Script para probar la nueva funcionalidad de búsqueda automática de ARIA
"""

import requests
import json
import time

def test_automatic_search():
    """Probar búsqueda automática con diferentes tipos de preguntas"""
    
    base_url = "http://localhost:5000/api/chat/futuristic"
    
    test_questions = [
        "que es el amor",
        "qué es la felicidad",
        "explica la inteligencia artificial",
        "háblame del universo",
        "dime sobre la amistad",
        "que es python",
        "define machine learning",
        "que es la vida",
        "explica la tecnología",
        "que es la consciencia"
    ]
    
    print("🌐 PROBANDO BÚSQUEDA AUTOMÁTICA DE ARIA")
    print("=" * 60)
    
    for i, question in enumerate(test_questions, 1):
        print(f"\n{i}. Pregunta: '{question}'")
        print("-" * 40)
        
        try:
            response = requests.post(base_url, json={
                'message': question,
                'emotion_context': 'neutral'
            }, timeout=15)
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    response_text = data['response']
                    
                    # Verificar si usó búsqueda automática
                    if "🌐" in response_text or "información actualizada" in response_text.lower():
                        print("   ✅ BÚSQUEDA AUTOMÁTICA ACTIVADA")
                    else:
                        print("   📚 Respuesta desde conocimiento base")
                    
                    # Mostrar respuesta truncada
                    if len(response_text) > 200:
                        print(f"   💬 ARIA: {response_text[:200]}...")
                    else:
                        print(f"   💬 ARIA: {response_text}")
                    
                    # Información emocional
                    emotion = data.get('emotion', 'No detectada')
                    print(f"   🎭 Emoción: {emotion}")
                    
                    # Confianza
                    confidence = data.get('confidence', 0)
                    print(f"   📊 Confianza: {confidence:.2f}")
                    
                else:
                    print(f"   ❌ Error: {data.get('error', 'Error desconocido')}")
            else:
                print(f"   ❌ Error HTTP: {response.status_code}")
                
        except requests.exceptions.ConnectionError:
            print(f"   ❌ No se puede conectar al servidor")
            break
        except requests.exceptions.Timeout:
            print(f"   ⏰ Timeout - búsqueda tomó demasiado tiempo")
        except Exception as e:
            print(f"   ❌ Error: {e}")
        
        # Pausa entre requests
        time.sleep(2)
    
    print("\n" + "=" * 60)
    print("✅ Prueba de búsqueda automática completada")

if __name__ == "__main__":
    test_automatic_search()