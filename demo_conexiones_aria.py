"""
🔗 ARIA - DEMOSTRACIÓN EN VIVO DE CONEXIONES
==========================================

Este script hace una demostración real de cómo ARIA se conecta a fuentes externas
"""

import requests
import feedparser
import json
from urllib.parse import quote
from datetime import datetime

def demo_wikipedia_connection():
    """Demuestra conexión real a Wikipedia"""
    print("=" * 60)
    print("🌐 DEMOSTRACIÓN EN VIVO: CONEXIÓN A WIKIPEDIA")
    print("=" * 60)
    
    topic = "artificial intelligence"
    print(f"🎯 Buscando información sobre: '{topic}'")
    
    # Construir URL como lo hace ARIA
    search_url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{quote(topic)}"
    print(f"🔗 URL construida: {search_url}")
    
    try:
        print("\n📡 Enviando petición HTTP...")
        response = requests.get(search_url, timeout=10)
        
        print(f"📊 Código de respuesta: {response.status_code}")
        print(f"📏 Tamaño de respuesta: {len(response.content)} bytes")
        
        if response.status_code == 200:
            data = response.json()
            
            print("\n✅ DATOS EXTRAÍDOS:")
            print(f"   📰 Título: {data.get('title', 'N/A')}")
            print(f"   📄 Extracto: {data.get('extract', 'N/A')[:150]}...")
            print(f"   🔗 URL: {data.get('content_urls', {}).get('desktop', {}).get('page', 'N/A')}")
            
            # Simular guardado como lo hace ARIA
            knowledge_item = {
                'topic': topic,
                'title': data.get('title', topic),
                'content': data.get('extract', ''),
                'source_type': 'wikipedia',
                'source_url': data.get('content_urls', {}).get('desktop', {}).get('page', ''),
                'confidence_score': 0.9,
                'timestamp': datetime.now().isoformat()
            }
            
            print("\n💾 ESTRUCTURA DE DATOS COMO ARIA LA GUARDA:")
            print(json.dumps(knowledge_item, indent=2, ensure_ascii=False))
            
            return True
        else:
            print(f"❌ Error HTTP: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        return False

def demo_rss_connection():
    """Demuestra conexión real a RSS feeds"""
    print("\n" + "=" * 60)
    print("📰 DEMOSTRACIÓN EN VIVO: CONEXIÓN A RSS FEEDS")
    print("=" * 60)
    
    feed_url = "https://feeds.feedburner.com/TechCrunch"
    print(f"📡 Conectando a: {feed_url}")
    
    try:
        print("\n📡 Parseando RSS feed...")
        feed = feedparser.parse(feed_url)
        
        print(f"📊 Título del feed: {feed.feed.get('title', 'N/A')}")
        print(f"📈 Artículos encontrados: {len(feed.entries)}")
        
        if feed.entries:
            print("\n📰 ÚLTIMOS 3 ARTÍCULOS:")
            
            for i, entry in enumerate(feed.entries[:3]):
                print(f"\n   {i+1}. 📰 {entry.get('title', 'Sin título')}")
                print(f"      📅 Fecha: {entry.get('published', 'N/A')}")
                print(f"      🔗 URL: {entry.get('link', 'N/A')}")
                print(f"      📄 Resumen: {entry.get('summary', 'N/A')[:100]}...")
            
            # Simular selección por relevancia como ARIA
            topic = "artificial intelligence"
            print(f"\n🎯 Buscando artículos relevantes a '{topic}':")
            
            relevant_articles = []
            topic_words = topic.lower().split()
            
            for entry in feed.entries[:10]:
                title = entry.get('title', '').lower()
                summary = entry.get('summary', '').lower()
                
                relevance = 0
                for word in topic_words:
                    if word in title:
                        relevance += 2
                    if word in summary:
                        relevance += 1
                
                if relevance > 0:
                    relevant_articles.append((entry, relevance))
            
            if relevant_articles:
                # Ordenar por relevancia
                relevant_articles.sort(key=lambda x: x[1], reverse=True)
                best_article, relevance_score = relevant_articles[0]
                
                print(f"\n✅ ARTÍCULO MÁS RELEVANTE (puntuación: {relevance_score}):")
                print(f"   📰 {best_article.get('title', 'N/A')}")
                print(f"   🔗 {best_article.get('link', 'N/A')}")
                
                # Como ARIA lo guardaría
                knowledge_item = {
                    'topic': topic,
                    'title': best_article.get('title', ''),
                    'content': best_article.get('summary', '')[:500],
                    'source_type': 'rss_news',
                    'source_url': best_article.get('link', ''),
                    'relevance_score': min(relevance_score / 5.0, 1.0),
                    'confidence_score': 0.7,
                    'timestamp': datetime.now().isoformat()
                }
                
                print("\n💾 COMO ARIA LO GUARDARÍA:")
                print(json.dumps(knowledge_item, indent=2, ensure_ascii=False))
                
                return True
            else:
                print(f"⚠️ No se encontraron artículos relevantes a '{topic}'")
                return False
        else:
            print("❌ No se encontraron artículos en el feed")
            return False
            
    except Exception as e:
        print(f"❌ Error parseando RSS: {e}")
        return False

def demo_arxiv_connection():
    """Demuestra conexión real a ArXiv"""
    print("\n" + "=" * 60)
    print("🔬 DEMOSTRACIÓN EN VIVO: CONEXIÓN A ARXIV")
    print("=" * 60)
    
    topic = "machine learning"
    query = f"all:{quote(topic)}"
    url = f"http://export.arxiv.org/api/query?search_query={query}&start=0&max_results=3"
    
    print(f"🎯 Buscando papers sobre: '{topic}'")
    print(f"🔗 URL: {url}")
    
    try:
        print("\n📡 Consultando ArXiv...")
        response = requests.get(url, timeout=15)
        
        print(f"📊 Código de respuesta: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ Respuesta recibida, parseando XML...")
            
            # ArXiv devuelve XML, simular el parsing
            import xml.etree.ElementTree as ET
            root = ET.fromstring(response.content)
            
            # Namespace para ArXiv
            ns = {'atom': 'http://www.w3.org/2005/Atom'}
            entries = root.findall('atom:entry', ns)
            
            print(f"📚 Papers encontrados: {len(entries)}")
            
            if entries:
                print("\n📖 PRIMEROS 3 PAPERS:")
                
                for i, entry in enumerate(entries[:3]):
                    title = entry.find('atom:title', ns)
                    summary = entry.find('atom:summary', ns)
                    link = entry.find('atom:id', ns)
                    published = entry.find('atom:published', ns)
                    
                    if title is not None:
                        print(f"\n   {i+1}. 📖 {title.text.strip()}")
                        if published is not None:
                            print(f"      📅 Publicado: {published.text}")
                        if link is not None:
                            print(f"      🔗 URL: {link.text}")
                        if summary is not None:
                            print(f"      📄 Resumen: {summary.text.strip()[:150]}...")
                
                # Simular como ARIA guardaría el primer paper
                first_entry = entries[0]
                title = first_entry.find('atom:title', ns)
                summary = first_entry.find('atom:summary', ns)
                link = first_entry.find('atom:id', ns)
                
                if title is not None and summary is not None:
                    knowledge_item = {
                        'topic': topic,
                        'title': title.text.strip(),
                        'content': summary.text.strip()[:1000],
                        'source_type': 'arxiv',
                        'source_url': link.text if link is not None else '',
                        'confidence_score': 0.95,
                        'relevance_score': 0.9,
                        'category': 'scientific_paper',
                        'timestamp': datetime.now().isoformat()
                    }
                    
                    print("\n💾 COMO ARIA GUARDARÍA EL PRIMER PAPER:")
                    print(json.dumps(knowledge_item, indent=2, ensure_ascii=False))
                    
                    return True
            else:
                print("❌ No se encontraron papers")
                return False
        else:
            print(f"❌ Error HTTP: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error consultando ArXiv: {e}")
        return False

def mostrar_flujo_completo():
    """Muestra el flujo completo de aprendizaje"""
    print("\n" + "=" * 60)
    print("🔄 FLUJO COMPLETO DE APRENDIZAJE DE ARIA")
    print("=" * 60)
    
    print("\n1️⃣ INICIO DEL CICLO")
    print("   🎲 ARIA selecciona tema aleatorio: 'quantum computing'")
    print("   🎯 Elige fuente aleatoria: Wikipedia")
    
    print("\n2️⃣ CONSTRUCCIÓN DE PETICIÓN")
    print("   🔤 Codifica tema: quantum%20computing")
    print("   🔗 URL: https://en.wikipedia.org/api/rest_v1/page/summary/quantum%20computing")
    
    print("\n3️⃣ PETICIÓN HTTP")
    print("   📡 requests.get(url, timeout=10)")
    print("   ⏱️ Espera máximo 10 segundos")
    
    print("\n4️⃣ PROCESAMIENTO")
    print("   📄 Parsea JSON de respuesta")
    print("   🔍 Extrae palabras clave")
    print("   📊 Calcula puntuación de confianza")
    
    print("\n5️⃣ ALMACENAMIENTO")
    print("   💾 Guarda en SQLite: data/aria_advanced_learning.db")
    print("   🏷️ Etiqueta con metadatos")
    
    print("\n6️⃣ ESTADÍSTICAS")
    print("   📈 Incrementa contadores")
    print("   📊 Actualiza métricas de éxito")
    
    print("\n7️⃣ PAUSA Y REPETICIÓN")
    print("   ⏱️ Espera 30-120 segundos")
    print("   🔁 Vuelve al paso 1 con nuevo tema")
    
    print("\n✨ RESULTADO: Conocimiento real y actualizado almacenado!")

def main():
    """Función principal de demostración"""
    print("🚀 ARIA - DEMOSTRACIÓN EN VIVO DE CONEXIONES A FUENTES EXTERNAS")
    print("=" * 80)
    print("📅 Fecha de demostración:", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    print("\n⚠️ IMPORTANTE: Esta demostración usa las MISMAS técnicas que ARIA")
    print("📡 Se conecta a internet en tiempo real")
    print("🔍 Extrae información real de fuentes públicas")
    print("💾 Muestra cómo se almacenaría la información")
    
    resultados = []
    
    # Probar cada conexión
    resultados.append(("Wikipedia", demo_wikipedia_connection()))
    resultados.append(("RSS Feeds", demo_rss_connection()))
    resultados.append(("ArXiv", demo_arxiv_connection()))
    
    # Mostrar flujo
    mostrar_flujo_completo()
    
    # Resumen final
    print("\n" + "=" * 60)
    print("📊 RESUMEN DE DEMOSTRACIONES")
    print("=" * 60)
    
    exitosas = 0
    for fuente, resultado in resultados:
        status = "✅ EXITOSA" if resultado else "❌ FALLÓ"
        print(f"{status:<12} {fuente}")
        if resultado:
            exitosas += 1
    
    print(f"\n🎯 Resultado: {exitosas}/{len(resultados)} conexiones exitosas")
    
    if exitosas > 0:
        print("\n🎉 ¡DEMOSTRACIÓN EXITOSA!")
        print("✅ ARIA puede conectarse realmente a internet")
        print("✅ Extrae información de fuentes verificadas")
        print("✅ Procesa datos en tiempo real")
        print("✅ Almacena conocimiento estructurado")
        print("\n🚀 ¡No es simulación - es conocimiento REAL!")
    else:
        print("\n⚠️ Algunas conexiones fallaron")
        print("💡 Posibles causas: problemas de red, APIs temporalmente no disponibles")
        print("🔧 ARIA está configurado para manejar estos errores automáticamente")

if __name__ == "__main__":
    main()