#!/usr/bin/env python3
"""
🌐 ARIA - Prueba de Capacidades Multilingües
==========================================

Prueba el sistema ARIA con conocimiento en español e inglés
"""

import sys
import os
import time

# Configurar rutas
sys.path.append(os.path.dirname(__file__))
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend', 'src'))

def probar_conocimiento_multilingue():
    print("🌐 ARIA - PRUEBA MULTILINGÜE")
    print("=" * 50)
    
    try:
        from auto_learning_advanced import aria_advanced_learning
        from spanish_apis import aria_spanish_apis
        
        print("✅ Módulos cargados correctamente")
        
        # Estado inicial
        status = aria_advanced_learning.get_status()
        print(f"📚 Conocimiento inicial: {status.get('total_knowledge', 0)} elementos")
        
        # Probar APIs en español
        print("\n🇪🇸 PROBANDO APIS EN ESPAÑOL:")
        spanish_tests = aria_spanish_apis.test_apis()
        for api, disponible in spanish_tests.items():
            status_icon = "✅" if disponible else "❌"
            print(f"   {status_icon} {api}")
        
        # Aprender contenido en español
        print("\n🧠 APRENDIENDO CONTENIDO EN ESPAÑOL:")
        temas_español = [
            'inteligencia artificial',
            'tecnología',
            'computación',
            'algoritmos'
        ]
        
        for tema in temas_español:
            print(f"   🔍 Explorando: {tema}")
            success = aria_advanced_learning._learn_from_spanish_sources(tema)
            if success:
                print(f"   ✅ Conocimiento adquirido sobre {tema}")
            else:
                print(f"   ⚠️ No se encontró información sobre {tema}")
            time.sleep(1)
        
        # Aprender contenido en inglés
        print("\n🇺🇸 APRENDIENDO CONTENIDO EN INGLÉS:")
        temas_ingles = [
            'machine learning',
            'cloud computing',
            'cybersecurity'
        ]
        
        for tema in temas_ingles:
            print(f"   🔍 Explorando: {tema}")
            success = aria_advanced_learning._learn_from_arxiv(tema)
            if success:
                print(f"   ✅ Conocimiento adquirido sobre {tema}")
            else:
                print(f"   ⚠️ No se encontró información sobre {tema}")
            time.sleep(1)
        
        # Estado final
        status_final = aria_advanced_learning.get_status()
        print(f"\n📊 RESUMEN FINAL:")
        print(f"   📚 Total conocimiento: {status_final.get('total_knowledge', 0)} elementos")
        print(f"   🏆 Temas principales: {list(status_final.get('top_topics', {}).keys())[:5]}")
        print(f"   📖 Fuentes principales: {list(status_final.get('top_sources', {}).keys())[:3]}")
        
        # Estadísticas de APIs en español
        stats_español = aria_spanish_apis.get_usage_stats()
        print(f"\n🌐 ESTADÍSTICAS ESPAÑOL:")
        print(f"   📰 Contenido español procesado: {stats_español['usage']['spanish_content']}")
        print(f"   🔤 Traducciones realizadas: {stats_español['usage']['translations']}")
        print(f"   📞 Llamadas a APIs: {stats_español['usage']['api_calls']}")
        
        # Buscar conocimiento específico
        print(f"\n🔍 PROBANDO BÚSQUEDA DE CONOCIMIENTO:")
        test_queries = [
            "inteligencia artificial",
            "machine learning", 
            "tecnología",
            "cloud computing"
        ]
        
        for query in test_queries:
            results = aria_advanced_learning.search_knowledge(query, limit=1)
            if results:
                result = results[0]
                print(f"   ✅ '{query}': {result['title'][:40]}... (confianza: {result['confidence_score']:.0%})")
            else:
                print(f"   ❌ '{query}': No encontrado")
        
        print("\n🎉 ¡PRUEBA MULTILINGÜE COMPLETADA!")
        print("ARIA ahora tiene conocimiento en español e inglés")
        
    except ImportError as e:
        print(f"❌ Error importando módulos: {e}")
    except Exception as e:
        print(f"❌ Error en la prueba: {e}")

if __name__ == "__main__":
    probar_conocimiento_multilingue()