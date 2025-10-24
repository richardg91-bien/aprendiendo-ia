#!/usr/bin/env python3
"""
Script para simular completamente el flujo del servidor con Caracas
"""

import sys
import os
sys.path.append('src')

# Importar ARIA
from aria_servidor_superbase import ARIASuperServer

def test_full_flow():
    """Probar el flujo completo como si fuera una petición HTTP"""
    
    print("🔍 Inicializando ARIA...")
    aria = ARIASuperServer()
    
    print("\n🧪 Simulando petición HTTP completa...")
    
    # Simular el método process_message
    try:
        result = aria.process_message("caracas")
        print("\n✅ RESULTADO COMPLETO:")
        print(f"📱 Respuesta: {result['response'][:200]}...")
        print(f"🎯 Confianza: {result['confidence']}")
        print(f"🌍 Idioma: {result['language_detected']}")
        print(f"🧠 Aprendizaje: {result.get('learning_feedback', {}).get('new_concepts_learned', 0)} nuevos conceptos")
        
    except Exception as e:
        print(f"❌ ERROR: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_full_flow()