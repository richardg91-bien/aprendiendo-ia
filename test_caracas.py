#!/usr/bin/env python3
"""
Script de prueba para verificar la funcionalidad de Caracas en ARIA
"""

import sys
import os
sys.path.append('src')

# Importar ARIA
from aria_servidor_superbase import ARIASuperServer

def test_caracas():
    """Probar la detección de Caracas"""
    
    print("🔍 Inicializando ARIA...")
    aria = ARIASuperServer()
    
    print("\n🧪 Probando detección de entidades conocidas...")
    
    # Prueba 1: Caracas
    response = aria._detect_known_entities("caracas", "auto")
    print(f"\n1. Test 'caracas' -> {response[:100] if response else 'None'}...")
    
    # Prueba 2: Venezuela  
    response = aria._detect_known_entities("venezuela", "auto")
    print(f"\n2. Test 'venezuela' -> {response[:100] if response else 'None'}...")
    
    # Prueba 3: Palabra no conocida
    response = aria._detect_known_entities("randomword", "auto")
    print(f"\n3. Test 'randomword' -> {response}")
    
    print("\n🔍 Probando detección de idioma...")
    
    # Prueba 4: Detección de idioma
    lang = aria._detect_language("caracas")
    print(f"\n4. Idioma detectado para 'caracas': {lang}")
    
    lang = aria._detect_language("hola como estas")
    print(f"5. Idioma detectado para 'hola como estas': {lang}")
    
    lang = aria._detect_language("hello how are you")
    print(f"6. Idioma detectado para 'hello how are you': {lang}")
    
    print("\n✅ Pruebas completadas")

if __name__ == "__main__":
    test_caracas()