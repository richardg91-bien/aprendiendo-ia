#!/usr/bin/env python3
"""
Script para probar específicamente la detección de entidades en el flujo completo
"""

import sys
import os
sys.path.append('src')

# Importar ARIA
from aria_servidor_superbase import ARIASuperServer

def test_entity_detection_flow():
    """Probar el flujo de detección de entidades específicamente"""
    
    print("🔍 Inicializando ARIA...")
    aria = ARIASuperServer()
    
    print("\n🧪 Probando detección directa...")
    
    # Prueba directa de _detect_known_entities
    direct_result = aria._detect_known_entities("caracas", "auto")
    print(f"📍 Detección directa: {direct_result is not None}")
    if direct_result:
        print(f"📄 Resultado directo: {direct_result[:100]}...")
    
    # Prueba de _generate_reflective_response
    print("\n🧪 Probando _generate_reflective_response...")
    reflective_result = aria._generate_reflective_response("caracas", "auto")
    print(f"🤔 Respuesta reflexiva: {reflective_result[:100]}...")
    
    # Verificar si la respuesta reflexiva contiene información de Caracas
    if "Capital de Venezuela" in reflective_result:
        print("✅ La información de Caracas está en la respuesta reflexiva")
    else:
        print("❌ La información de Caracas NO está en la respuesta reflexiva")
    
    print(f"\n🎭 Respuesta completa:")
    print(reflective_result)

if __name__ == "__main__":
    test_entity_detection_flow()