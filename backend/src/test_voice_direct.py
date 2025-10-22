"""
Test Rápido del Sistema de Voz SAPI
"""

import time

print("🔊 Probando sistema de voz directamente...")

try:
    from spock_voice_simple import SpockVoiceSystemSimple
    
    # Crear instancia del sistema de voz
    voice_system = SpockVoiceSystemSimple()
    
    print("✅ Sistema de voz SAPI inicializado correctamente")
    
    # Probar texto simple
    print("🗣️ Hablando: 'Hola, soy ARIA con voz del Sr. Spock'")
    voice_system.speak_async("Hola, soy ARIA con voz del Sr. Spock")
    
    # Esperar un momento para que complete
    time.sleep(3)
    print("✅ Primera prueba de voz completada")
    
    # Probar con transformación Spock
    print("🗣️ Hablando con transformación Spock...")
    voice_system.speak_async("¿Cómo estás? Espero que tengas un buen día.")
    
    # Esperar para que complete
    time.sleep(4)
    print("✅ Segunda prueba con transformación completada")
    
    print("\n🎯 Si escuchaste la voz, el sistema funciona correctamente!")
    print("🎯 Si no escuchaste nada, verifica:")
    print("   - Volumen del sistema activado")
    print("   - Altavoces/auriculares conectados")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()

input("\nPresiona Enter para continuar...")