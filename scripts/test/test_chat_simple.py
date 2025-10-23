#!/usr/bin/env python3
"""
Script simple para probar la API de chat sin iniciar servidor
"""

import requests
import json
import time

def test_chat():
    url = "http://localhost:8000/api/chat"
    
    preguntas = [
        "¿Qué has aprendido?",
        "¿Qué sabes sobre cloud computing?", 
        "¿Tienes información sobre FPGAs?",
        "Cuéntame sobre seguridad en la nube"
    ]
    
    print("🧪 PRUEBA RÁPIDA DE CHAT")
    print("=" * 30)
    
    for pregunta in preguntas:
        print(f"\n❓ {pregunta}")
        
        try:
            response = requests.post(url, json={"message": pregunta}, timeout=5)
            if response.status_code == 200:
                data = response.json()
                respuesta = data.get("response", "Sin respuesta")
                confianza = data.get("confidence", 0)
                
                print(f"🤖 {respuesta[:200]}{'...' if len(respuesta) > 200 else ''}")
                print(f"📊 Confianza: {confianza}%")
                
                if "Interesante. Me dijiste:" in respuesta:
                    print("❌ GENÉRICA")
                elif "Cloud FPGAs" in respuesta or "científica" in respuesta:
                    print("✅ CONOCIMIENTO REAL")
                elif "aprendido" in respuesta and "elementos" in respuesta:
                    print("✅ RESUMEN REAL")
                    
            else:
                print(f"❌ Error HTTP: {response.status_code}")
                
        except Exception as e:
            print(f"❌ Error: {e}")
            
        time.sleep(0.5)

if __name__ == "__main__":
    test_chat()