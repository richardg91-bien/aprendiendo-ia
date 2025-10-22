"""
🌐 ARIA - Extensión de APIs Gratuitas en Español
===============================================

Integración de servicios gratuitos para mejorar el aprendizaje y
las capacidades de ARIA en español
"""

import requests
import json
import time
from typing import Dict, List, Optional, Any
from datetime import datetime

class AriaSpanishAPIs:
    """Integración de APIs gratuitas en español para ARIA"""
    
    def __init__(self):
        self.apis_config = {
            'libretranslate': {
                'url': 'https://libretranslate.de/translate',
                'active': True,
                'free_limit': 5000,  # caracteres por día
                'description': 'Traducción automática gratuita'
            },
            'gemini_free': {
                'url': 'https://generativelanguage.googleapis.com/v1beta/models',
                'active': False,  # Requiere API key
                'free_limit': 60,  # requests por minuto
                'description': 'IA generativa de Google (requiere clave)'
            },
            'eden_ai': {
                'url': 'https://api.edenai.run/v2',
                'active': False,  # Requiere API key
                'free_limit': 1000,  # requests por mes
                'description': 'Plataforma agregadora de APIs de IA'
            }
        }
        
        # APIs públicas sin autenticación
        self.public_spanish_sources = {
            'rae_diccionario': 'https://dle.rae.es/data/search',
            'cervantes_virtual': 'http://www.cervantesvirtual.com/descarga/plataforma/',
            'fundeu': 'https://www.fundeu.es/consultas/',
            'news_spanish': [
                'https://feeds.elpais.com/mrss-s/pages/ep/site/elpais.com/section/ciencia/portada',
                'https://rss.cnn.com/rss/cnn_spanish.rss',
                'https://feeds.bbci.co.uk/mundo/rss.xml'
            ]
        }
        
        self.translation_cache = {}
        self.usage_stats = {
            'translations': 0,
            'spanish_content': 0,
            'api_calls': 0
        }
    
    def translate_to_spanish(self, text: str, source_lang: str = 'en') -> Optional[str]:
        """Traduce texto al español usando LibreTranslate"""
        if not text or len(text) > 500:  # Límite de caracteres
            return None
            
        # Verificar cache
        cache_key = f"{source_lang}:{text[:50]}"
        if cache_key in self.translation_cache:
            return self.translation_cache[cache_key]
        
        try:
            url = self.apis_config['libretranslate']['url']
            data = {
                'q': text,
                'source': source_lang,
                'target': 'es',
                'format': 'text'
            }
            
            headers = {'Content-Type': 'application/json'}
            
            response = requests.post(url, json=data, headers=headers, timeout=10)
            
            if response.status_code == 200:
                result = response.json()
                translated_text = result.get('translatedText', '')
                
                # Guardar en cache
                self.translation_cache[cache_key] = translated_text
                self.usage_stats['translations'] += 1
                
                return translated_text
            else:
                print(f"❌ Error en traducción: {response.status_code}")
                
        except Exception as e:
            print(f"❌ Error traduciendo texto: {e}")
        
        return None
    
    def get_spanish_news(self) -> List[Dict[str, Any]]:
        """Obtiene noticias en español de fuentes RSS"""
        spanish_articles = []
        
        try:
            import feedparser
            
            for feed_url in self.public_spanish_sources['news_spanish']:
                try:
                    feed = feedparser.parse(feed_url)
                    
                    for entry in feed.entries[:3]:  # Máximo 3 por fuente
                        article = {
                            'title': entry.get('title', ''),
                            'summary': entry.get('summary', '')[:300],
                            'url': entry.get('link', ''),
                            'source': feed.feed.get('title', 'Fuente desconocida'),
                            'language': 'es',
                            'date': entry.get('published', ''),
                            'keywords': self._extract_spanish_keywords(entry.get('title', '') + ' ' + entry.get('summary', ''))
                        }
                        
                        if len(article['title']) > 10:  # Filtrar artículos válidos
                            spanish_articles.append(article)
                            
                except Exception as e:
                    print(f"⚠️ Error procesando feed {feed_url}: {e}")
                    continue
                    
                time.sleep(1)  # Pausa entre feeds
                
        except ImportError:
            print("⚠️ feedparser no disponible para noticias en español")
        
        self.usage_stats['spanish_content'] += len(spanish_articles)
        return spanish_articles
    
    def search_rae_dictionary(self, word: str) -> Optional[Dict[str, Any]]:
        """Busca definiciones en el Diccionario de la RAE"""
        if not word or len(word) < 2:
            return None
            
        try:
            # Simular búsqueda en RAE (la API real requiere autenticación)
            # Aquí usaríamos datos estructurados locales o scraping ético
            rae_definitions = {
                'inteligencia': {
                    'definition': 'Capacidad de entender o comprender. Capacidad de resolver problemas.',
                    'etymology': 'Del lat. intelligentia.',
                    'examples': ['inteligencia artificial', 'inteligencia emocional']
                },
                'tecnología': {
                    'definition': 'Conjunto de teorías y técnicas que permiten el aprovechamiento práctico del conocimiento científico.',
                    'etymology': 'Del gr. τεχνολογία technología.',
                    'examples': ['tecnología digital', 'alta tecnología']
                },
                'algoritmo': {
                    'definition': 'Conjunto ordenado y finito de operaciones que permite hallar la solución de un problema.',
                    'etymology': 'Del ár. hisp. *alḵuwārizmī, y este del ár. clás. al-Ḵuwārizmī.',
                    'examples': ['algoritmo de búsqueda', 'algoritmo genético']
                }
            }
            
            word_lower = word.lower()
            if word_lower in rae_definitions:
                result = rae_definitions[word_lower].copy()
                result['word'] = word
                result['source'] = 'RAE (simulado)'
                self.usage_stats['api_calls'] += 1
                return result
                
        except Exception as e:
            print(f"❌ Error buscando en RAE: {e}")
        
        return None
    
    def _extract_spanish_keywords(self, text: str) -> List[str]:
        """Extrae palabras clave del texto en español"""
        if not text:
            return []
        
        # Palabras vacías en español
        stop_words = {
            'el', 'la', 'de', 'que', 'y', 'a', 'en', 'un', 'es', 'se', 'no', 'te', 'lo', 'le',
            'da', 'su', 'por', 'son', 'con', 'para', 'al', 'del', 'los', 'las', 'una', 'sobre',
            'todo', 'también', 'tras', 'otro', 'algún', 'alguna', 'algunos', 'algunas', 'ser',
            'estar', 'tener', 'hacer', 'poder', 'decir', 'todo', 'cada', 'quien', 'como'
        }
        
        words = text.lower().split()
        keywords = []
        
        for word in words:
            # Limpiar palabra
            clean_word = ''.join(c for c in word if c.isalpha())
            
            # Filtrar palabras significativas
            if (len(clean_word) > 3 and 
                clean_word not in stop_words and
                clean_word.isalpha()):
                keywords.append(clean_word)
        
        return list(set(keywords))[:10]  # Máximo 10 palabras clave únicas
    
    def enhance_knowledge_with_spanish(self, knowledge_item: Dict[str, Any]) -> Dict[str, Any]:
        """Mejora un elemento de conocimiento con información en español"""
        enhanced = knowledge_item.copy()
        
        try:
            # Traducir contenido si está en inglés
            if knowledge_item.get('language') == 'en' or 'english' in str(knowledge_item).lower():
                title = knowledge_item.get('title', '')
                content = knowledge_item.get('content', '')
                
                if title:
                    spanish_title = self.translate_to_spanish(title)
                    if spanish_title:
                        enhanced['spanish_title'] = spanish_title
                
                if content and len(content) < 400:  # Límite para traducción
                    spanish_content = self.translate_to_spanish(content[:300])
                    if spanish_content:
                        enhanced['spanish_summary'] = spanish_content
            
            # Agregar definiciones de palabras técnicas
            keywords = knowledge_item.get('keywords', [])
            if isinstance(keywords, str):
                keywords = keywords.split(',')
            
            spanish_definitions = {}
            for keyword in keywords[:3]:  # Máximo 3 definiciones
                if keyword.strip():
                    definition = self.search_rae_dictionary(keyword.strip())
                    if definition:
                        spanish_definitions[keyword.strip()] = definition
            
            if spanish_definitions:
                enhanced['spanish_definitions'] = spanish_definitions
            
            # Marcar como mejorado
            enhanced['spanish_enhanced'] = True
            enhanced['enhancement_date'] = datetime.now().isoformat()
            
        except Exception as e:
            print(f"❌ Error mejorando conocimiento con español: {e}")
        
        return enhanced
    
    def get_usage_stats(self) -> Dict[str, Any]:
        """Obtiene estadísticas de uso de las APIs"""
        return {
            'usage': self.usage_stats.copy(),
            'active_apis': [name for name, config in self.apis_config.items() if config['active']],
            'cache_size': len(self.translation_cache),
            'last_update': datetime.now().isoformat()
        }
    
    def test_apis(self) -> Dict[str, bool]:
        """Prueba la disponibilidad de las APIs"""
        results = {}
        
        # Probar traducción
        test_translation = self.translate_to_spanish("Hello world", "en")
        results['libretranslate'] = test_translation is not None
        
        # Probar noticias en español
        test_news = self.get_spanish_news()
        results['spanish_news'] = len(test_news) > 0
        
        # Probar diccionario RAE
        test_rae = self.search_rae_dictionary("tecnología")
        results['rae_dictionary'] = test_rae is not None
        
        return results

# Instancia global
aria_spanish_apis = AriaSpanishAPIs()

if __name__ == "__main__":
    print("🌐 Probando APIs en español para ARIA...")
    
    # Probar funcionalidades
    results = aria_spanish_apis.test_apis()
    
    for api, status in results.items():
        status_icon = "✅" if status else "❌"
        print(f"{status_icon} {api}: {'Disponible' if status else 'No disponible'}")
    
    # Mostrar estadísticas
    stats = aria_spanish_apis.get_usage_stats()
    print(f"\n📊 Estadísticas: {stats['usage']}")