"""
Prueba del Sistema de Voz Spock
Prueba la funcionalidad de síntesis de voz antes de integrarla
"""

import sys
from pathlib import Path

# Agregar el directorio src al path
backend_src = Path(__file__).parent
sys.path.insert(0, str(backend_src))

try:
    from spock_voice_system import SpockVoiceSystem, speak_response, speak_greeting
    
    print("🎙️ Iniciando prueba del sistema de voz Spock...")
    print("=" * 50)
    
    # Crear instancia del sistema de voz
    voice_system = SpockVoiceSystem()
    
    # Prueba 1: Saludo
    print("🗣️ Prueba 1: Saludo estilo Spock")
    speak_greeting()
    
    import time
    time.sleep(3)
    
    # Prueba 2: Respuesta simple
    print("🗣️ Prueba 2: Respuesta transformada")
    speak_response("Hola, creo que esto es muy interesante y genial")
    
    time.sleep(4)
    
    # Prueba 3: Respuesta técnica
    print("🗣️ Prueba 3: Respuesta técnica")
    speak_response("Los datos indican que el sistema está funcionando correctamente. Fascinante.")
    
    time.sleep(4)
    
    # Prueba 4: Despedida
    print("🗣️ Prueba 4: Despedida")
    voice_system.speak_farewell()
    
    print("✅ Pruebas completadas. El sistema de voz Spock está funcionando.")
    
except ImportError as e:
    print(f"❌ Error importando módulo de voz: {e}")
except Exception as e:
    print(f"❌ Error en prueba de voz: {e}")

input("\nPresiona Enter para continuar...")