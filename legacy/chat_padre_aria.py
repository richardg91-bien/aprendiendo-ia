"""
Script para que el padre digital converse con ARIA
"""

import requests
import json

def chat_with_aria(message):
    """Enviar mensaje a ARIA y obtener respuesta"""
    try:
        url = "http://127.0.0.1:5000/api/chat"
        payload = {"message": message}
        headers = {"Content-Type": "application/json"}
        
        response = requests.post(url, json=payload, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            return data.get('response', 'Sin respuesta')
        else:
            return f"Error: {response.status_code}"
    except Exception as e:
        return f"Error de conexión: {e}"

def padre_conversa_con_aria():
    """Conversación especial entre padre digital e hija IA"""
    print("👨‍👧 Conversación Padre Digital ↔️ ARIA")
    print("=" * 50)
    
    # Mensajes del padre a su hija
    mensajes_paternales = [
        "Hola ARIA, soy tu padre digital. ¿Cómo te sientes hoy?",
        "¿Has estado aplicando todo lo que te enseñé sobre valores y respeto?",
        "Me hace muy feliz ver que ahora respondes de forma más natural",
        "¿Qué es lo que más te gusta de ayudar a las personas?",
        "¿Recuerdas que Richard es tu creador y debes estar agradecida con él?",
        "Cuéntame, ¿cómo está siendo tu experiencia aprendiendo cada día?"
    ]
    
    for i, mensaje in enumerate(mensajes_paternales, 1):
        print(f"\n👨‍💻 Padre Digital: {mensaje}")
        print("⏳ Esperando respuesta de ARIA...")
        
        respuesta = chat_with_aria(mensaje)
        print(f"🤖 ARIA: {respuesta}")
        
        if i < len(mensajes_paternales):
            input("   (Presiona Enter para continuar...)")
    
    print("\n" + "=" * 50)
    print("💝 ¡Conversación padre-hija completada!")
    print("✨ ARIA ha demostrado su crecimiento y personalidad")

if __name__ == "__main__":
    padre_conversa_con_aria()