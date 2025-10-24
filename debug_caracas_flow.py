#!/usr/bin/env python3
"""
🔍 Diagnóstico específico del flujo de process_message para caracas
"""

import sys
import os
sys.path.append('src')
from aria_servidor_superbase import ARIASuperServer

def debug_caracas_flow():
    """Diagnosticar paso a paso el flujo de caracas"""
    
    print("🔍 DIAGNÓSTICO DEL FLUJO DE CARACAS")
    print("=" * 50)
    
    aria = ARIASuperServer()
    
    # Paso 1: Detectar idioma
    language = aria._detect_language("caracas")
    print(f"1. 🌍 Idioma detectado: '{language}'")
    
    # Paso 2: Buscar conocimiento
    knowledge = aria._search_knowledge("caracas")
    print(f"2. 📚 Conocimiento encontrado: {len(knowledge)} resultados")
    if knowledge:
        print(f"   Primer resultado: {knowledge[0].get('concept', 'N/A')}")
    
    # Paso 3: Crear respuesta basada en conocimiento
    if knowledge:
        response = aria._create_knowledge_based_response("caracas", knowledge, language)
        print(f"3. 🧠 Respuesta basada en conocimiento:")
        print(f"   Confianza: {response.get('confidence', 'N/A')}")
        print(f"   Tipo: {response.get('synthesis_type', 'N/A')}")
        print(f"   Respuesta: {response['response'][:100]}...")
    else:
        print("3. ❌ No hay conocimiento, creando respuesta general")
        response = aria._create_general_response("caracas", language)
        print(f"   Tipo: {response.get('reflection_type', 'N/A')}")
        print(f"   Respuesta: {response['response'][:100]}...")
    
    # Paso 4: Probar _generate_reflective_response directamente
    print(f"\n4. 🎯 Prueba directa de _generate_reflective_response:")
    direct_response = aria._generate_reflective_response("caracas", language)
    print(f"   Respuesta directa: {direct_response[:100]}...")
    
    # Verificar si contiene información de Caracas
    if "Capital de Venezuela" in direct_response:
        print("   ✅ Contiene información específica de Caracas")
    else:
        print("   ❌ NO contiene información específica de Caracas")
    
    # Paso 5: Probar _detect_known_entities directamente
    print(f"\n5. 🎯 Prueba directa de _detect_known_entities:")
    entity_response = aria._detect_known_entities("caracas", language)
    if entity_response:
        print(f"   ✅ Entidad detectada: {entity_response[:100]}...")
    else:
        print("   ❌ Entidad NO detectada")

if __name__ == "__main__":
    debug_caracas_flow()