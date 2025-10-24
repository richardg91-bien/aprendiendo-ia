#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🧠 Test de Respuestas Originales de ARIA
========================================

Script para probar el nuevo sistema de respuestas originales que genera
conclusiones propias en lugar de copiar información externa.

Uso:
    python test_respuestas_originales.py
"""

import requests
import json
import time
from datetime import datetime

# Configuración
ARIA_URL = "http://localhost:8000"

def test_aria_connection():
    """Probar conexión con ARIA"""
    try:
        response = requests.get(f"{ARIA_URL}/status", timeout=5)
        return response.status_code == 200
    except:
        return False

def send_test_question(question, description=""):
    """Enviar pregunta de prueba y analizar la respuesta"""
    try:
        print(f"\n{'='*80}")
        print(f"🧠 PREGUNTA: {question}")
        print(f"📋 Tipo: {description}")
        print(f"{'='*80}")
        
        response = requests.post(f"{ARIA_URL}/chat", 
                               json={"message": question})
        
        if response.status_code == 200:
            data = response.json()
            answer = data.get('response', 'Sin respuesta')
            
            print(f"🤖 RESPUESTA DE ARIA:")
            print(f"{answer}")
            print()
            
            # Análisis de la respuesta
            print(f"📊 ANÁLISIS DE ORIGINALIDAD:")
            
            # Verificar indicadores de originalidad
            original_indicators = [
                "mi análisis", "mi perspectiva", "mi reflexión", "mi conclusión",
                "considero que", "en mi opinión", "creo que", "desde mi punto de vista",
                "mi experiencia", "mi comprensión", "mi enfoque", "mi recomendación"
            ]
            
            copy_indicators = [
                "según", "de acuerdo a", "basándome en fuentes", "extraído de",
                "copiado de", "tomado de", "según estudios", "investigaciones muestran"
            ]
            
            original_count = sum(1 for indicator in original_indicators if indicator in answer.lower())
            copy_count = sum(1 for indicator in copy_indicators if indicator in answer.lower())
            
            print(f"   ✅ Indicadores de originalidad: {original_count}")
            print(f"   ❌ Indicadores de copia: {copy_count}")
            
            # Verificar estructura de respuesta original
            has_reflection = any(word in answer.lower() for word in ["reflexión", "reflection", "análisis", "analysis"])
            has_personal_view = any(word in answer.lower() for word in ["mi", "my", "creo", "believe", "considero", "consider"])
            has_structured_thinking = "💭" in answer or "🧠" in answer or "🔍" in answer
            
            print(f"   🧠 Contiene reflexión: {'✅' if has_reflection else '❌'}")
            print(f"   👤 Perspectiva personal: {'✅' if has_personal_view else '❌'}")
            print(f"   🏗️ Pensamiento estructurado: {'✅' if has_structured_thinking else '❌'}")
            
            # Verificar información técnica del sistema
            confidence = data.get('confidence', 0)
            original_analysis = data.get('original_analysis', False)
            synthesis_type = data.get('synthesis_type', 'N/A')
            
            print(f"   📈 Confianza: {confidence:.2f}")
            print(f"   🎯 Análisis original: {'✅' if original_analysis else '❌'}")
            print(f"   🔬 Tipo de síntesis: {synthesis_type}")
            
            # Puntuación de originalidad
            originality_score = (original_count * 10) + (40 if has_reflection else 0) + \
                              (30 if has_personal_view else 0) + (20 if has_structured_thinking else 0) - \
                              (copy_count * 15)
            
            print(f"   🌟 Puntuación de originalidad: {max(0, originality_score)}/100")
            
            return True
        else:
            print(f"❌ Error: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    """Función principal"""
    print("🧠 ARIA - Test de Respuestas Originales vs Copias")
    print("=" * 60)
    print("🎯 Objetivo: Verificar que ARIA genera conclusiones propias")
    print("📝 Método: Analizar respuestas por indicadores de originalidad")
    print()
    
    # Verificar conexión
    if not test_aria_connection():
        print("❌ Error: No se puede conectar con ARIA")
        print("💡 Ejecuta primero: cd src && python aria_servidor_superbase.py")
        return
    
    print("✅ Conexión establecida con ARIA")
    
    # Preguntas de prueba diseñadas para verificar originalidad
    test_questions = [
        {
            "question": "¿Qué es la inteligencia artificial?",
            "type": "Pregunta de definición",
            "expected": "Síntesis original con reflexión personal"
        },
        {
            "question": "¿Cómo funciona el machine learning?",
            "type": "Pregunta explicativa",
            "expected": "Explicación basada en análisis propio"
        },
        {
            "question": "¿Cuál es la diferencia entre Python y JavaScript?",
            "type": "Pregunta comparativa",
            "expected": "Comparación analítica original"
        },
        {
            "question": "¿Cómo puedo aprender programación?",
            "type": "Pregunta procedimental",
            "expected": "Guía metodológica personal"
        },
        {
            "question": "¿Qué opinas sobre el desarrollo web moderno?",
            "type": "Pregunta de opinión",
            "expected": "Reflexión profunda y perspectiva personal"
        },
        {
            "question": "Explícame sobre bases de datos",
            "type": "Pregunta general",
            "expected": "Análisis multidimensional original"
        },
        {
            "question": "¿Cómo optimizar el rendimiento de una aplicación?",
            "type": "Pregunta técnica",
            "expected": "Marco metodológico personal"
        },
        {
            "question": "¿Qué es el blockchain?",
            "type": "Pregunta conceptual",
            "expected": "Síntesis conceptual con perspectiva propia"
        }
    ]
    
    print(f"🎯 Realizando {len(test_questions)} pruebas de originalidad...")
    print()
    
    successful_tests = 0
    total_originality_score = 0
    
    for i, test in enumerate(test_questions, 1):
        print(f"\n{'🧪 TEST ' + str(i):=^80}")
        success = send_test_question(test["question"], test["type"])
        
        if success:
            successful_tests += 1
        
        # Pausa entre tests
        if i < len(test_questions):
            time.sleep(2)
    
    # Resumen final
    print(f"\n{'📊 RESUMEN FINAL':=^80}")
    print(f"✅ Tests exitosos: {successful_tests}/{len(test_questions)}")
    print(f"📈 Tasa de éxito: {(successful_tests/len(test_questions)*100):.1f}%")
    print()
    
    print("🎯 CRITERIOS DE ORIGINALIDAD EVALUADOS:")
    print("   • Uso de perspectiva personal ('mi análisis', 'mi perspectiva')")
    print("   • Ausencia de indicadores de copia ('según fuentes', 'extraído de')")
    print("   • Presencia de reflexión estructurada")
    print("   • Pensamiento analítico propio")
    print("   • Conclusiones sintéticas originales")
    print()
    
    print("💡 RESULTADOS ESPERADOS:")
    print("   ✅ Respuestas con alto contenido reflexivo")
    print("   ✅ Análisis original sin copia textual")
    print("   ✅ Perspectivas personales de ARIA")
    print("   ✅ Síntesis conceptual propia")
    print("   ✅ Conclusiones originales estructuradas")
    print()
    
    print("🚀 ¡Test de originalidad completado!")
    print("🌐 Puedes seguir probando en: http://localhost:8000")

if __name__ == "__main__":
    main()