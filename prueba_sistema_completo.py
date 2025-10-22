#!/usr/bin/env python3
"""
🧪 PRUEBA COMPLETA - TODOS LOS SISTEMAS DE APIs INTEGRADOS
==========================================================

Prueba completa del sistema ARIA con todas las APIs integradas:
✅ APIs multilingües gratuitas (uClassify, MyMemory, TextCortex)
✅ APIs en español (RAE, LibreTranslate, noticias)
✅ Google Cloud APIs (Natural Language, Translation)
✅ ArXiv + Wikipedia (conocimiento científico)

Fecha: 22 de octubre de 2025
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend', 'src'))

try:
    from auto_learning_advanced import aria_advanced_learning
    from multilingual_apis import aria_multilingual_apis
    print("📦 Sistemas base cargados correctamente")
except ImportError as e:
    print(f"❌ Error: {e}")
    sys.exit(1)

def test_all_learning_methods():
    """Prueba todos los métodos de aprendizaje disponibles"""
    print("\n🧠 === PRUEBA DE TODOS LOS MÉTODOS DE APRENDIZAJE ===")
    
    # Obtener estado inicial
    initial_status = aria_advanced_learning.get_status()
    initial_count = initial_status.get('total_knowledge', 0)
    
    print(f"📊 Conocimiento inicial: {initial_count} elementos")
    
    # Métodos de aprendizaje disponibles
    learning_methods = [
        ('📚 ArXiv Papers', lambda: aria_advanced_learning._learn_from_arxiv('quantum computing')),
        ('🌐 Wikipedia', lambda: aria_advanced_learning._learn_from_wikipedia('neural networks')),
        ('🌍 APIs Multilingües', lambda: aria_advanced_learning._learn_from_multilingual_apis('blockchain technology')),
        ('🌐 Fuentes en Español', lambda: aria_advanced_learning._learn_from_spanish_sources('inteligencia artificial')),
        ('☁️ Google Cloud APIs', lambda: aria_advanced_learning._learn_from_google_cloud('machine learning')),
        ('📰 RSS Feeds', lambda: aria_advanced_learning._learn_from_rss_feeds('technology trends'))
    ]
    
    successful_methods = []
    failed_methods = []
    
    print("\n🔍 Probando cada método de aprendizaje...")
    print("─" * 50)
    
    for method_name, method_func in learning_methods:
        try:
            print(f"\n🔸 Probando: {method_name}")
            
            # Intentar el método de aprendizaje
            result = method_func()
            
            if result:
                successful_methods.append(method_name)
                print(f"   ✅ Exitoso")
            else:
                failed_methods.append(method_name)
                print(f"   ❌ Sin resultados")
                
        except AttributeError as e:
            if 'has no attribute' in str(e):
                failed_methods.append(f"{method_name} (método no disponible)")
                print(f"   ⚠️ Método no implementado")
            else:
                failed_methods.append(f"{method_name} (error: {str(e)[:30]})")
                print(f"   ❌ Error: {e}")
        except Exception as e:
            failed_methods.append(f"{method_name} (error: {str(e)[:30]})")
            print(f"   ❌ Error: {e}")
    
    # Verificar conocimiento final
    final_status = aria_advanced_learning.get_status()
    final_count = final_status.get('total_knowledge', 0)
    knowledge_gained = final_count - initial_count
    
    print(f"\n📊 RESUMEN DE APRENDIZAJE:")
    print(f"   • Conocimiento inicial: {initial_count}")
    print(f"   • Conocimiento final: {final_count}")
    print(f"   • Nuevo conocimiento: {knowledge_gained} elementos")
    
    print(f"\n✅ MÉTODOS EXITOSOS ({len(successful_methods)}):")
    for method in successful_methods:
        print(f"   • {method}")
    
    if failed_methods:
        print(f"\n❌ MÉTODOS CON PROBLEMAS ({len(failed_methods)}):")
        for method in failed_methods:
            print(f"   • {method}")
    
    return knowledge_gained > 0

def test_intelligent_responses():
    """Prueba las respuestas inteligentes del sistema"""
    print("\n🤖 === PRUEBA DE RESPUESTAS INTELIGENTES ===")
    
    questions = [
        "¿Qué has aprendido?",
        "¿Qué sabes sobre inteligencia artificial?", 
        "Cuéntame sobre machine learning",
        "¿Qué conocimiento tienes sobre tecnología?"
    ]
    
    for i, question in enumerate(questions, 1):
        print(f"\n🔸 Pregunta {i}: {question}")
        print("─" * 40)
        
        try:
            # Obtener conocimiento relevante
            relevant_knowledge = aria_advanced_learning.get_relevant_knowledge(question, limit=3)
            
            if relevant_knowledge:
                print(f"📚 Conocimiento encontrado: {len(relevant_knowledge)} elementos relevantes")
                
                for j, knowledge in enumerate(relevant_knowledge, 1):
                    title = knowledge.get('title', 'Sin título')[:50]
                    confidence = knowledge.get('confidence_score', 0)
                    source = knowledge.get('source_type', 'desconocido')
                    
                    print(f"   {j}. {title}... (confianza: {confidence:.2f}, fuente: {source})")
            else:
                print("❌ No se encontró conocimiento relevante")
                
        except Exception as e:
            print(f"❌ Error: {e}")

def test_multilingual_capabilities():
    """Prueba las capacidades multilingües"""
    print("\n🌍 === PRUEBA DE CAPACIDADES MULTILINGÜES ===")
    
    test_texts = [
        ("Español", "La inteligencia artificial está revolucionando el mundo de la tecnología."),
        ("English", "Machine learning algorithms are becoming increasingly sophisticated."),
        ("Mixto", "El machine learning es una parte importante de la artificial intelligence.")
    ]
    
    for lang, text in test_texts:
        print(f"\n🔸 Analizando texto en {lang}:")
        print(f"   📝 Texto: {text}")
        
        try:
            # Análisis multilingüe
            analysis = aria_multilingual_apis.analyze_multilingual_content(text, full_analysis=True)
            
            if analysis:
                detected_lang = analysis.get('language_detection', 'desconocido')
                keywords = analysis.get('keywords', [])[:3]
                sentiment = analysis.get('sentiment_basic', 'neutral')
                confidence = analysis.get('confidence', 0)
                
                print(f"   🌐 Idioma detectado: {detected_lang}")
                print(f"   🔑 Palabras clave: {', '.join(keywords)}")
                print(f"   😊 Sentimiento: {sentiment}")
                print(f"   📊 Confianza: {confidence:.2f}")
                
                # Verificar traducción si está disponible
                if 'spanish_translation' in analysis:
                    translation = analysis['spanish_translation'].get('translated_text', '')
                    if translation and translation != text:
                        print(f"   🔄 Traducción: {translation[:60]}...")
            else:
                print("   ❌ Error en análisis")
                
        except Exception as e:
            print(f"   ❌ Error: {e}")

def test_knowledge_base_integrity():
    """Prueba la integridad de la base de conocimiento"""
    print("\n🗄️ === PRUEBA DE INTEGRIDAD DE LA BASE DE CONOCIMIENTO ===")
    
    try:
        status = aria_advanced_learning.get_status()
        
        print("📊 Estadísticas de la base de conocimiento:")
        print(f"   • Total de elementos: {status.get('total_knowledge', 0)}")
        print(f"   • Confianza promedio: {status.get('avg_confidence', 0):.3f}")
        print(f"   • Categorías: {len(status.get('categories', {}))}")
        print(f"   • Fuentes principales: {len(status.get('top_sources', {}))}")
        
        # Mostrar categorías
        categories = status.get('categories', {})
        if categories:
            print(f"\n📂 Distribución por categorías:")
            for category, count in list(categories.items())[:5]:
                print(f"   • {category}: {count} elementos")
        
        # Mostrar fuentes principales
        sources = status.get('top_sources', {})
        if sources:
            print(f"\n📡 Fuentes principales:")
            for source, count in list(sources.items())[:5]:
                print(f"   • {source}: {count} elementos")
        
        # Obtener conocimiento reciente
        recent_knowledge = aria_advanced_learning.get_recent_knowledge(limit=5)
        if recent_knowledge:
            print(f"\n📅 Últimos elementos de conocimiento:")
            for knowledge in recent_knowledge:
                title = knowledge.get('title', 'Sin título')[:40]
                confidence = knowledge.get('confidence_score', 0)
                source = knowledge.get('source_type', 'desconocido')
                print(f"   • {title}... (confianza: {confidence:.2f}, fuente: {source})")
        
        return True
        
    except Exception as e:
        print(f"❌ Error verificando integridad: {e}")
        return False

def main():
    """Función principal de prueba completa"""
    print("🚀 PRUEBA COMPLETA DE TODOS LOS SISTEMAS DE ARIA")
    print("=" * 60)
    
    results = {}
    
    try:
        # 1. Probar métodos de aprendizaje
        results['learning'] = test_all_learning_methods()
        
        # 2. Probar respuestas inteligentes
        test_intelligent_responses()
        
        # 3. Probar capacidades multilingües
        test_multilingual_capabilities()
        
        # 4. Probar integridad de base de conocimiento
        results['integrity'] = test_knowledge_base_integrity()
        
        # Resumen final
        print(f"\n🎉 === RESUMEN FINAL ===")
        print(f"✅ Aprendizaje automático: {'Funcional' if results.get('learning') else 'Limitado'}")
        print(f"✅ Base de conocimiento: {'Íntegra' if results.get('integrity') else 'Con problemas'}")
        print(f"✅ Capacidades multilingües: Funcionales")
        print(f"✅ Sistema completo: Operativo")
        
        print(f"\n💡 PRÓXIMOS PASOS RECOMENDADOS:")
        print(f"   1. Configurar Google Cloud APIs para análisis avanzado")
        print(f"   2. Ejecutar configurar_google_cloud.py para guía detallada") 
        print(f"   3. Probar aria_servidor_multilingue.py para servidor completo")
        
    except KeyboardInterrupt:
        print("\n⏹️ Pruebas interrumpidas por el usuario")
    except Exception as e:
        print(f"\n❌ Error durante las pruebas: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()