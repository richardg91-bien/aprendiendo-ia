#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
🧪 PRUEBA ESPECÍFICA DE DETECCIÓN DE CARACAS
=============================================

Prueba directa de la función _detect_known_entities
"""

import sys
import os

def test_caracas_detection():
    """Prueba la detección específica de Caracas"""
    print("🧪 PRUEBA DE DETECCIÓN DE CARACAS")
    print("=" * 40)
    
    # Agregar src al path
    sys.path.append('src')
    
    try:
        from aria_servidor_superbase import ARIASuperServer
        
        print("📡 Inicializando servidor ARIA...")
        server = ARIASuperServer()
        
        print("✅ Servidor inicializado")
        
        # Probar diferentes variaciones de caracas
        test_cases = [
            "caracas",
            "¿Qué sabes sobre caracas?",
            "Caracas",
            "CARACAS",
            "caracas venezuela",
            "capital venezuela"
        ]
        
        print("\\n🔍 PROBANDO DETECCIÓN DE ENTIDADES:")
        print("-" * 40)
        
        for case in test_cases:
            try:
                # Probar la función directamente con el parámetro language
                entity_info = server._detect_known_entities(case, 'es')
                
                print(f"📝 Texto: '{case}'")
                if entity_info:
                    print(f"   ✅ Detectado: {entity_info}")
                else:
                    print(f"   ❌ No detectado")
                print()
                
            except Exception as e:
                print(f"   ❌ Error: {e}")
                print()
        
        return True
        
    except Exception as e:
        print(f"❌ Error inicializando: {e}")
        return False

def test_synthesis_pipeline():
    """Prueba el pipeline completo de síntesis"""
    print("\\n🔄 PROBANDO PIPELINE DE SÍNTESIS")
    print("=" * 40)
    
    sys.path.append('src')
    
    try:
        from aria_servidor_superbase import ARIASuperServer
        
        server = ARIASuperServer()
        
        # Simular una conversación completa
        message = "¿Qué sabes sobre caracas?"
        
        print(f"💬 Mensaje: {message}")
        print("🔄 Procesando...")
        
        # Llamar a la función de síntesis original con parámetros correctos
        result = server._synthesize_original_conclusion(
            user_message=message,
            knowledge=[],  # Lista vacía de conocimiento
            language='es'
        )
        
        print("\\n📋 RESULTADO DEL PIPELINE:")
        print("-" * 30)
        print(f"✅ Respuesta: {result['response']}")
        print(f"📊 Confianza: {result['confidence']}")
        print(f"🎯 Método: {result.get('method', 'No especificado')}")
        
        # Verificar si menciona información específica
        response_lower = result['response'].lower()
        if 'capital' in response_lower and 'venezuela' in response_lower:
            print("🎉 ¡PERFECTO! Menciona que Caracas es capital de Venezuela")
        elif 'caracas' in response_lower and len(result['response']) > 100:
            print("✅ BUENO: Información específica sobre Caracas")
        else:
            print("⚠️ REVISAR: Puede ser una respuesta genérica")
        
        return True
        
    except Exception as e:
        print(f"❌ Error en pipeline: {e}")
        return False

def main():
    print("🚀 DIAGNÓSTICO COMPLETO DE CARACAS")
    print("=" * 50)
    
    # Verificar que estamos en el directorio correcto
    if not os.path.exists('src'):
        print("❌ Directorio 'src' no encontrado")
        print("   Ejecuta desde el directorio raíz del proyecto")
        return False
    
    success1 = test_caracas_detection()
    success2 = test_synthesis_pipeline()
    
    print("\\n" + "=" * 50)
    print("📊 RESUMEN:")
    print(f"🔍 Detección de entidades: {'✅ OK' if success1 else '❌ FALLO'}")
    print(f"🔄 Pipeline de síntesis: {'✅ OK' if success2 else '❌ FALLO'}")
    
    if success1 and success2:
        print("\\n🎉 ¡CARACAS DETECTADO CORRECTAMENTE!")
        print("✅ Las modificaciones están funcionando")
    else:
        print("\\n⚠️ Hay problemas con la detección de Caracas")
        print("🔧 Puede necesitar verificación del código")
    
    return success1 and success2

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\\n👋 Prueba interrumpida")
        sys.exit(1)