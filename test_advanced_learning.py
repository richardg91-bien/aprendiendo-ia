"""
🧪 ARIA - Prueba del Sistema de Aprendizaje Avanzado
==================================================

Script para verificar que todas las mejoras funcionan correctamente
"""

import sys
import os
import time
import asyncio

# Agregar path del backend
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend', 'src'))

def test_basic_imports():
    """Prueba las importaciones básicas"""
    print("🔍 Probando importaciones...")
    
    try:
        import requests
        print("✅ requests - OK")
    except ImportError as e:
        print(f"❌ requests - Error: {e}")
    
    try:
        import feedparser
        print("✅ feedparser - OK")
    except ImportError as e:
        print(f"❌ feedparser - Error: {e}")
    
    try:
        from backend.src.auto_learning_advanced import AriaAdvancedLearning
        print("✅ AriaAdvancedLearning - OK")
        return True
    except ImportError as e:
        print(f"❌ AriaAdvancedLearning - Error: {e}")
        return False

def test_advanced_learning():
    """Prueba el sistema de aprendizaje avanzado"""
    print("\n🚀 Probando Sistema de Aprendizaje Avanzado...")
    
    try:
        from backend.src.auto_learning_advanced import AriaAdvancedLearning
        
        # Crear instancia
        aria = AriaAdvancedLearning()
        print("✅ Instancia creada correctamente")
        
        # Probar capacidades
        print("\n📊 Capacidades del sistema:")
        print(f"   🔹 Temas de aprendizaje: {len(aria.learning_topics)}")
        print(f"   🔹 Fuentes RSS: {len(aria.rss_feeds)}")
        print(f"   🔹 APIs disponibles: {len(aria.knowledge_sources)}")
        
        # Obtener estado inicial
        status = aria.get_status()
        print(f"\n📈 Estado inicial:")
        print(f"   🔹 Ejecutándose: {status['running']}")
        print(f"   🔹 Conocimiento total: {status['total_knowledge']}")
        print(f"   🔹 Capacidades avanzadas: {status['learning_capabilities']}")
        
        # Probar búsqueda
        print("\n🔍 Probando búsqueda de conocimiento...")
        results = aria.search_knowledge("artificial intelligence", limit=3)
        print(f"   🔹 Resultados encontrados: {len(results)}")
        
        # Probar una sesión rápida de aprendizaje
        print("\n🧠 Iniciando sesión de prueba...")
        start_result = aria.start_learning()
        print(f"   🔹 Inicio: {start_result}")
        
        # Esperar un poco para que aprenda algo
        print("   ⏳ Esperando 30 segundos para que el sistema aprenda...")
        time.sleep(30)
        
        # Verificar nuevo estado
        new_status = aria.get_status()
        print(f"\n📊 Estado después de aprendizaje:")
        print(f"   🔹 Conocimiento total: {new_status['total_knowledge']}")
        print(f"   🔹 Estadísticas: {new_status.get('statistics', {})}")
        
        # Detener aprendizaje
        stop_result = aria.stop_learning()
        print(f"   🔹 Detención: {stop_result}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error en prueba avanzada: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_wikipedia_api():
    """Prueba específica de la API de Wikipedia"""
    print("\n🌐 Probando acceso a Wikipedia...")
    
    try:
        import requests
        from urllib.parse import quote
        
        # Probar Wikipedia API
        topic = "artificial intelligence"
        url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{quote(topic)}"
        
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Wikipedia API - OK")
            print(f"   🔹 Título: {data.get('title', 'N/A')}")
            print(f"   🔹 Extracto: {data.get('extract', 'N/A')[:100]}...")
            return True
        else:
            print(f"❌ Wikipedia API - Error HTTP {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Wikipedia API - Error: {e}")
        return False

def test_rss_feeds():
    """Prueba lectura de feeds RSS"""
    print("\n📰 Probando feeds RSS...")
    
    try:
        import feedparser
        
        # Probar feed de TechCrunch
        feed_url = "https://feeds.feedburner.com/TechCrunch"
        
        print(f"   📡 Accediendo a: {feed_url}")
        feed = feedparser.parse(feed_url)
        
        if feed.entries:
            print(f"✅ RSS Feed - OK")
            print(f"   🔹 Artículos encontrados: {len(feed.entries)}")
            print(f"   🔹 Primer artículo: {feed.entries[0].get('title', 'N/A')[:80]}...")
            return True
        else:
            print(f"❌ RSS Feed - No se encontraron entradas")
            return False
            
    except Exception as e:
        print(f"❌ RSS Feed - Error: {e}")
        return False

def test_database_creation():
    """Prueba creación de base de datos"""
    print("\n💾 Probando creación de base de datos...")
    
    try:
        from backend.src.auto_learning_advanced import AriaAdvancedLearning
        
        aria = AriaAdvancedLearning()
        
        # Verificar que la base de datos se creó
        if os.path.exists(aria.db_path):
            print(f"✅ Base de datos creada en: {aria.db_path}")
            
            # Verificar tamaño
            size = os.path.getsize(aria.db_path)
            print(f"   🔹 Tamaño: {size} bytes")
            
            return True
        else:
            print(f"❌ Base de datos no encontrada en: {aria.db_path}")
            return False
            
    except Exception as e:
        print(f"❌ Error creando base de datos: {e}")
        return False

def main():
    """Función principal de pruebas"""
    print("=" * 60)
    print("🧪 ARIA - PRUEBAS DEL SISTEMA DE APRENDIZAJE AVANZADO")
    print("=" * 60)
    
    tests = [
        ("Importaciones Básicas", test_basic_imports),
        ("Creación de Base de Datos", test_database_creation),
        ("API de Wikipedia", test_wikipedia_api),
        ("Feeds RSS", test_rss_feeds),
        ("Sistema Avanzado Completo", test_advanced_learning),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ Error crítico en {test_name}: {e}")
            results.append((test_name, False))
    
    # Resumen final
    print("\n" + "="*60)
    print("📋 RESUMEN DE PRUEBAS")
    print("="*60)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASÓ" if result else "❌ FALLÓ"
        print(f"{status:<10} {test_name}")
        if result:
            passed += 1
    
    print(f"\n🎯 Resultado: {passed}/{total} pruebas pasaron")
    
    if passed == total:
        print("🎉 ¡Todas las pruebas pasaron! El sistema avanzado está listo.")
    elif passed > total // 2:
        print("⚠️ La mayoría de pruebas pasaron. Sistema parcialmente funcional.")
    else:
        print("🚨 Múltiples fallos. Revisar configuración del sistema.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    
    if success:
        print("\n🚀 Sistema listo para superar las limitaciones actuales!")
        print("\n✨ NUEVAS CAPACIDADES DISPONIBLES:")
        print("   🌐 Acceso a internet en tiempo real")
        print("   📚 Lectura de fuentes externas (Wikipedia, ArXiv, RSS)")
        print("   🔍 Análisis de contenido web")
        print("   📊 Puntuación de relevancia y confianza")
        print("   📈 Estadísticas de aprendizaje en tiempo real")
        print("   🎯 Conocimiento basado en fuentes verificadas")
    else:
        print("\n⚠️ Algunas funcionalidades pueden no estar disponibles.")
        print("   💡 Sugerencia: Instalar dependencias faltantes")
        print("   🔧 Comando: pip install feedparser beautifulsoup4 lxml requests")