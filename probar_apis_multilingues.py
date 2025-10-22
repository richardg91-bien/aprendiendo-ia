#!/usr/bin/env python3
"""
🧪 PRUEBA DE APIS MULTILINGÜES GRATUITAS
======================================

Script para probar las nuevas APIs multilingües integradas en ARIA.
Prueba el sistema completo de análisis y aprendizaje.

Fecha: 22 de octubre de 2025
"""

import sys
import os
import time
import json

# Agregar el directorio src al path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend', 'src'))

try:
    from multilingual_apis import aria_multilingual_apis
    from auto_learning_advanced import aria_advanced_learning
    
    print("📦 Módulos importados correctamente")
except ImportError as e:
    print(f"❌ Error importando módulos: {e}")
    sys.exit(1)

def test_multilingual_apis():
    """Prueba las APIs multilingües individualmente"""
    print("\n🌐 === PRUEBA DE APIs MULTILINGÜES ===")
    
    # Texto de prueba en español
    test_text_es = """
    La inteligencia artificial está revolucionando el mundo. 
    Es una tecnología fascinante que permite a las máquinas aprender y tomar decisiones.
    """
    
    # Texto de prueba en inglés
    test_text_en = """
    Machine learning is a subset of artificial intelligence that enables computers 
    to learn and make decisions from data without explicit programming.
    """
    
    print("🔍 Probando análisis multilingüe...")
    
    # Análisis del texto en español
    print("\n📝 Analizando texto en español:")
    result_es = aria_multilingual_apis.analyze_multilingual_content(test_text_es, full_analysis=True)
    
    print(f"   • Idioma detectado: {result_es.get('language_detection')}")
    print(f"   • Palabras clave: {result_es.get('keywords')[:5]}")
    print(f"   • Sentimiento: {result_es.get('sentiment_basic')}")
    print(f"   • Confianza: {result_es.get('confidence', 0):.2f}")
    
    # Análisis del texto en inglés
    print("\n📝 Analizando texto en inglés:")
    result_en = aria_multilingual_apis.analyze_multilingual_content(test_text_en, full_analysis=True)
    
    print(f"   • Idioma detectado: {result_en.get('language_detection')}")
    print(f"   • Palabras clave: {result_en.get('keywords')[:5]}")
    print(f"   • Sentimiento: {result_en.get('sentiment_basic')}")
    print(f"   • Confianza: {result_en.get('confidence', 0):.2f}")
    
    # Prueba de traducción
    if result_en.get('language_detection') == 'en':
        print("\n🔄 Probando traducción...")
        translation = aria_multilingual_apis.translate_text_free(test_text_en, target_lang="es")
        if not translation.get('error'):
            print(f"   • Texto original: {test_text_en[:50]}...")
            print(f"   • Traducción: {translation.get('translated_text', '')[:50]}...")
            print(f"   • Confianza: {translation.get('confidence', 0):.2f}")
    
    return True

def test_advanced_learning_system():
    """Prueba el sistema de aprendizaje avanzado con APIs multilingües"""
    print("\n🧠 === PRUEBA DEL SISTEMA DE APRENDIZAJE AVANZADO ===")
    
    # Verificar estado inicial
    status_before = aria_advanced_learning.get_status()
    print(f"📊 Conocimiento inicial: {status_before.get('total_knowledge', 0)} elementos")
    
    # Probar aprendizaje con APIs multilingües
    topics_to_learn = [
        "artificial intelligence",
        "machine learning", 
        "cloud computing"
    ]
    
    successful_learnings = 0
    
    for topic in topics_to_learn:
        print(f"\n🔍 Probando aprendizaje sobre: '{topic}'")
        try:
            # Usar el método de APIs multilingües directamente
            success = aria_advanced_learning._learn_from_multilingual_apis(topic)
            if success:
                successful_learnings += 1
                print(f"   ✅ Aprendizaje exitoso sobre '{topic}'")
            else:
                print(f"   ❌ No se pudo aprender sobre '{topic}'")
        except Exception as e:
            print(f"   ❌ Error aprendiendo sobre '{topic}': {e}")
        
        # Pequeña pausa entre aprendizajes
        time.sleep(1)
    
    # Verificar estado final
    status_after = aria_advanced_learning.get_status()
    new_knowledge_count = status_after.get('total_knowledge', 0)
    knowledge_gained = new_knowledge_count - status_before.get('total_knowledge', 0)
    
    print(f"\n📊 Resultado del aprendizaje:")
    print(f"   • Conocimiento inicial: {status_before.get('total_knowledge', 0)}")
    print(f"   • Conocimiento final: {new_knowledge_count}")
    print(f"   • Nuevo conocimiento: {knowledge_gained} elementos")
    print(f"   • Temas aprendidos exitosamente: {successful_learnings}/{len(topics_to_learn)}")
    
    return knowledge_gained > 0

def test_knowledge_retrieval():
    """Prueba la recuperación de conocimiento para responder preguntas"""
    print("\n🔍 === PRUEBA DE RECUPERACIÓN DE CONOCIMIENTO ===")
    
    questions = [
        "¿Qué has aprendido?",
        "¿Qué sabes sobre inteligencia artificial?",
        "Cuéntame sobre machine learning"
    ]
    
    for question in questions:
        print(f"\n❓ Pregunta: {question}")
        
        try:
            # Simular recuperación de conocimiento
            relevant_knowledge = aria_advanced_learning.get_relevant_knowledge(question, limit=3)
            
            if relevant_knowledge:
                print(f"   📚 Conocimiento encontrado: {len(relevant_knowledge)} elementos")
                for i, knowledge in enumerate(relevant_knowledge, 1):
                    title = knowledge.get('title', 'Sin título')[:50]
                    confidence = knowledge.get('confidence_score', 0)
                    print(f"   {i}. {title}... (confianza: {confidence:.2f})")
            else:
                print("   ❌ No se encontró conocimiento relevante")
                
        except Exception as e:
            print(f"   ❌ Error recuperando conocimiento: {e}")

def test_api_status():
    """Prueba el estado de las APIs"""
    print("\n🌐 === ESTADO DE LAS APIs ===")
    
    try:
        api_status = aria_multilingual_apis.get_api_status()
        
        print(f"📊 Estado general: {api_status.get('overall_status', 'unknown')}")
        print(f"🔢 APIs disponibles: {api_status.get('total_apis_available', 0)}")
        print(f"💾 Entradas en cache: {api_status.get('cache_entries', 0)}")
        
        print("\n🔧 Estado individual de APIs:")
        for api_name, status in api_status.get('apis_tested', {}).items():
            status_icon = "✅" if status else "❌"
            print(f"   {status_icon} {api_name}: {'Disponible' if status else 'No disponible'}")
            
    except Exception as e:
        print(f"❌ Error verificando estado de APIs: {e}")

def main():
    """Función principal de prueba"""
    print("🚀 INICIANDO PRUEBAS DEL SISTEMA MULTILINGÜE DE ARIA")
    print("=" * 60)
    
    try:
        # Prueba 1: APIs multilingües individuales
        test_multilingual_apis()
        
        # Prueba 2: Sistema de aprendizaje avanzado
        test_advanced_learning_system()
        
        # Prueba 3: Recuperación de conocimiento
        test_knowledge_retrieval()
        
        # Prueba 4: Estado de las APIs
        test_api_status()
        
        print("\n🎉 === PRUEBAS COMPLETADAS ===")
        print("✅ Todas las pruebas del sistema multilingüe ejecutadas")
        
    except KeyboardInterrupt:
        print("\n⏹️ Pruebas interrumpidas por el usuario")
    except Exception as e:
        print(f"\n❌ Error durante las pruebas: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()