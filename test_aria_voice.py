"""
Prueba independiente del sistema de voz ARIA
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend', 'src'))

def test_aria_voice():
    print("🔊 Iniciando prueba del sistema de voz ARIA...")
    
    try:
        from voice_system import voice_system
        
        if voice_system is None:
            print("❌ Sistema de voz no disponible")
            return False
        
        print("✅ Sistema de voz cargado")
        print(f"Voces disponibles: {voice_system.get_voice_info()['total_voices']}")
        print(f"Voz actual: {voice_system.get_voice_info()['current_voice']}")
        
        # Prueba con PowerShell
        print("🔊 Probando síntesis de voz...")
        result = voice_system.speak_with_powershell("¡Hola! Soy ARIA. Mi sistema de voz está funcionando perfectamente.")
        
        if result:
            print("✅ ¡Síntesis de voz exitosa!")
            return True
        else:
            print("❌ Error en síntesis de voz")
            return False
            
    except Exception as e:
        print(f"❌ Error en prueba de voz: {e}")
        return False

if __name__ == "__main__":
    test_aria_voice()