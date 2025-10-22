#!/usr/bin/env python3
"""
Prueba específica de la pregunta "¿Qué has aprendido?"
"""

import requests
import time

def probar_pregunta():
    print("🧪 PRUEBA ESPECÍFICA: '¿Qué has aprendido?'")
    print("=" * 50)
    
    # Esperar un poco para que el servidor esté listo
    print("⏳ Esperando servidor...")
    time.sleep(2)
    
    try:
        # Verificar estado
        print("📡 Verificando servidor...")
        resp = requests.get("http://localhost:8000/api/status", timeout=5)
        status = resp.json()
        print(f"✅ Servidor: {status['status']}")
        print(f"📚 Conocimiento: {status.get('knowledge_count', 0)} elementos")
        print(f"🧠 Sistema avanzado: {status.get('advanced', False)}")
        
        # La pregunta específica
        pregunta = "¿Qué has aprendido?"
        print(f"\n❓ Pregunta: {pregunta}")
        print("-" * 30)
        
        resp = requests.post("http://localhost:8000/api/chat", 
                           json={"message": pregunta}, 
                           timeout=10)
        
        if resp.status_code == 200:
            data = resp.json()
            response = data.get("response", "Sin respuesta")
            confidence = data.get("confidence", 0)
            knowledge_used = data.get("knowledge_used", False)
            
            print(f"🤖 RESPUESTA DE ARIA:")
            print(response)
            print(f"\n📊 Confianza: {confidence:.0%}")
            print(f"🧠 Usó conocimiento real: {'✅ SÍ' if knowledge_used else '❌ NO'}")
            
            # Análisis
            if "Interesante. Me dijiste:" in response:
                print("\n❌ PROBLEMA: Respuesta genérica detectada")
                print("🔧 El sistema no está accediendo al conocimiento real")
            elif "elementos de conocimiento" in response and "científico" in response:
                print("\n✅ ÉXITO: Respuesta con conocimiento real")
                print("🎉 El sistema está funcionando correctamente")
            else:
                print("\n🔍 RESPUESTA PROCESADA")
                print("📋 Verificar contenido manualmente")
        else:
            print(f"❌ Error HTTP: {resp.status_code}")
            
    except requests.exceptions.ConnectionError:
        print("❌ No se puede conectar al servidor")
        print("💡 Asegúrate de que aria_estable.py esté ejecutándose")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    probar_pregunta()