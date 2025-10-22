#!/usr/bin/env python3
"""
Prueba las respuestas de ARIA para verificar que use conocimiento real
vs respuestas genéricas
"""

import requests
import json
import time

def probar_aria(mensaje):
    """Envía un mensaje a ARIA y devuelve la respuesta"""
    url = "http://localhost:8000/api/chat"
    
    data = {
        "message": mensaje,
        "user_id": "test_user"
    }
    
    try:
        response = requests.post(url, json=data, timeout=10)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return {"error": str(e)}

def main():
    print("🧪 PROBANDO RESPUESTAS DE ARIA")
    print("=" * 50)
    
    # Preguntas para probar conocimiento
    preguntas = [
        "¿Qué has aprendido?",
        "¿Qué sabes sobre cloud computing?",
        "¿Tienes información sobre FPGAs?",
        "Cuéntame sobre seguridad en la nube",
        "¿Qué papers científicos conoces?"
    ]
    
    for i, pregunta in enumerate(preguntas, 1):
        print(f"\n🔍 Pregunta {i}: {pregunta}")
        print("-" * 30)
        
        resultado = probar_aria(pregunta)
        
        if "error" in resultado:
            print(f"❌ Error: {resultado['error']}")
        else:
            respuesta = resultado.get("response", "Sin respuesta")
            confianza = resultado.get("confidence", 0)
            
            print(f"🤖 Respuesta: {respuesta}")
            print(f"📊 Confianza: {confianza}%")
            
            # Verificar si es una respuesta genérica
            if "Interesante. Me dijiste:" in respuesta:
                print("⚠️  RESPUESTA GENÉRICA DETECTADA")
            elif "Cloud FPGAs" in respuesta or "arxiv" in respuesta.lower():
                print("✅ CONOCIMIENTO REAL DETECTADO")
            else:
                print("🔍 RESPUESTA ANALIZADA")
        
        time.sleep(1)  # Pausa entre preguntas
    
    print("\n" + "=" * 50)
    print("🏁 PRUEBA COMPLETADA")

if __name__ == "__main__":
    main()