#!/usr/bin/env python3
"""
Prueba directa de la API de ARIA para verificar conocimiento real
"""

import requests
import json
import time

def probar_aria_api(mensaje):
    """Envía un mensaje directamente a la API de ARIA"""
    url = "http://localhost:8000/api/chat"
    
    data = {
        "message": mensaje,
        "user_id": "test_user"
    }
    
    try:
        response = requests.post(url, json=data, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": f"Error de conexión: {e}"}
    except Exception as e:
        return {"error": str(e)}

def main():
    print("🧪 PRUEBA DIRECTA DE API ARIA")
    print("=" * 40)
    
    # Verificar que el servidor esté disponible
    try:
        test_response = requests.get("http://localhost:8000/api/status", timeout=5)
        print("✅ Servidor ARIA disponible")
    except:
        print("❌ Servidor ARIA no disponible")
        return
    
    # Preguntas específicas para probar
    preguntas = [
        "¿Qué has aprendido?",
        "¿Qué sabes sobre cloud computing?",
        "¿Tienes información sobre FPGAs?",
        "Cuéntame sobre seguridad en la nube"
    ]
    
    for i, pregunta in enumerate(preguntas, 1):
        print(f"\n🔍 PREGUNTA {i}: {pregunta}")
        print("-" * 40)
        
        resultado = probar_aria_api(pregunta)
        
        if "error" in resultado:
            print(f"❌ Error: {resultado['error']}")
            continue
            
        respuesta = resultado.get("response", "Sin respuesta")
        confianza = resultado.get("confidence", 0)
        
        print(f"🤖 RESPUESTA:")
        print(f"   {respuesta}")
        print(f"📊 Confianza: {confianza}%")
        
        # Análisis de la respuesta
        if "Interesante. Me dijiste:" in respuesta:
            print("❌ PROBLEMA: Respuesta genérica detectada")
        elif "Cloud FPGAs" in respuesta or "arxiv" in respuesta.lower() or "científica" in respuesta.lower():
            print("✅ ÉXITO: Conocimiento real detectado")
        elif "aprendido" in respuesta and "elementos" in respuesta:
            print("✅ ÉXITO: Resumen de aprendizaje real")
        else:
            print("🔍 Respuesta analizada - verificar contenido")
        
        time.sleep(1)
    
    print("\n" + "=" * 40)
    print("🏁 PRUEBA COMPLETADA")

if __name__ == "__main__":
    main()