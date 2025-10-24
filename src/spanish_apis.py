#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🇪🇸 ARIA Spanish APIs
=====================

Sistema de APIs españolas para búsquedas web y servicios específicos de España.
Incluye búsquedas en Google, DuckDuckGo, APIs del gobierno español, etc.

Fecha: 24 de octubre de 2025
"""

import requests
import json
import time
from typing import Dict, List, Optional, Any
import urllib.parse
from datetime import datetime
import logging

# Configurar logging
logger = logging.getLogger(__name__)

class ARIASpanishAPIs:
    """Sistema de APIs españolas para ARIA"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        
        # APIs disponibles
        self.apis_config = {
            'duckduckgo': {
                'enabled': True,
                'url': 'https://api.duckduckgo.com/',
                'description': 'Búsquedas web generales'
            },
            'wikipedia_es': {
                'enabled': True,
                'url': 'https://es.wikipedia.org/api/rest_v1/',
                'description': 'Wikipedia en español'
            },
            'openweather': {
                'enabled': False,  # Requiere API key
                'url': 'https://api.openweathermap.org/data/2.5/',
                'description': 'Información del clima'
            },
            'news_spain': {
                'enabled': True,
                'url': 'https://newsapi.org/v2/',
                'description': 'Noticias de España'
            }
        }
        
        print("🇪🇸 APIs Españolas inicializadas")
    
    def search_comprehensive(self, query: str, max_results: int = 5) -> Dict[str, Any]:
        """
        Búsqueda comprehensiva usando múltiples APIs españolas
        """
        results = {
            'query': query,
            'timestamp': datetime.now().isoformat(),
            'sources': [],
            'summary': '',
            'success': True
        }
        
        try:
            # 1. Búsqueda en DuckDuckGo
            duckduckgo_results = self._search_duckduckgo(query, max_results=3)
            if duckduckgo_results:
                results['sources'].append({
                    'source': 'DuckDuckGo',
                    'results': duckduckgo_results,
                    'type': 'web_search'
                })
            
            # 2. Búsqueda en Wikipedia ES
            wikipedia_results = self._search_wikipedia_es(query)
            if wikipedia_results:
                results['sources'].append({
                    'source': 'Wikipedia ES',
                    'results': wikipedia_results,
                    'type': 'encyclopedia'
                })
            
            # 3. Si la consulta es sobre clima, buscar información meteorológica
            if any(word in query.lower() for word in ['clima', 'tiempo', 'temperatura', 'lluvia', 'sol']):
                weather_results = self._get_spain_weather_info()
                if weather_results:
                    results['sources'].append({
                        'source': 'Información Meteorológica',
                        'results': weather_results,
                        'type': 'weather'
                    })
            
            # 4. Si la consulta es sobre noticias, buscar noticias actuales
            if any(word in query.lower() for word in ['noticia', 'actualidad', 'news', 'hoy', 'último']):
                news_results = self._get_spain_news(query)
                if news_results:
                    results['sources'].append({
                        'source': 'Noticias España',
                        'results': news_results,
                        'type': 'news'
                    })
            
            # Generar resumen
            results['summary'] = self._generate_summary(results['sources'])
            
        except Exception as e:
            logger.error(f"Error en búsqueda comprehensiva: {e}")
            results['success'] = False
            results['error'] = str(e)
        
        return results
    
    def _search_duckduckgo(self, query: str, max_results: int = 3) -> List[Dict]:
        """Búsqueda en DuckDuckGo"""
        try:
            # DuckDuckGo Instant Answer API
            params = {
                'q': query,
                'format': 'json',
                'no_html': '1',
                'skip_disambig': '1'
            }
            
            response = self.session.get('https://api.duckduckgo.com/', params=params, timeout=10)
            data = response.json()
            
            results = []
            
            # Abstract (resumen principal)
            if data.get('Abstract'):
                results.append({
                    'title': data.get('AbstractText', 'Información general'),
                    'snippet': data.get('Abstract'),
                    'url': data.get('AbstractURL', ''),
                    'source': data.get('AbstractSource', 'DuckDuckGo')
                })
            
            # Related topics
            for topic in data.get('RelatedTopics', [])[:max_results-1]:
                if isinstance(topic, dict) and topic.get('Text'):
                    results.append({
                        'title': topic.get('FirstURL', '').split('/')[-1].replace('_', ' '),
                        'snippet': topic.get('Text'),
                        'url': topic.get('FirstURL', ''),
                        'source': 'DuckDuckGo'
                    })
            
            return results[:max_results]
            
        except Exception as e:
            logger.error(f"Error en DuckDuckGo: {e}")
            return []
    
    def _search_wikipedia_es(self, query: str) -> List[Dict]:
        """Búsqueda en Wikipedia español"""
        try:
            # Primero buscar artículos
            search_url = 'https://es.wikipedia.org/api/rest_v1/page/summary/' + urllib.parse.quote(query)
            
            response = self.session.get(search_url, timeout=10)
            if response.status_code == 200:
                data = response.json()
                
                return [{
                    'title': data.get('title', query),
                    'snippet': data.get('extract', ''),
                    'url': data.get('content_urls', {}).get('desktop', {}).get('page', ''),
                    'source': 'Wikipedia ES',
                    'thumbnail': data.get('thumbnail', {}).get('source', '') if data.get('thumbnail') else ''
                }]
            
            # Si no funciona, intentar búsqueda general
            search_params = {
                'action': 'query',
                'format': 'json',
                'list': 'search',
                'srsearch': query,
                'srlimit': 1
            }
            
            response = self.session.get('https://es.wikipedia.org/api/rest_v1/page/search/' + urllib.parse.quote(query), timeout=10)
            if response.status_code == 200:
                data = response.json()
                if data.get('pages'):
                    page = data['pages'][0]
                    return [{
                        'title': page.get('title', ''),
                        'snippet': page.get('description', ''),
                        'url': f"https://es.wikipedia.org/wiki/{urllib.parse.quote(page.get('key', ''))}",
                        'source': 'Wikipedia ES'
                    }]
            
            return []
            
        except Exception as e:
            logger.error(f"Error en Wikipedia ES: {e}")
            return []
    
    def _get_spain_weather_info(self) -> List[Dict]:
        """Información meteorológica básica de España"""
        try:
            # Información meteorológica básica sin API key
            return [{
                'title': 'Información Meteorológica',
                'snippet': f'Para información meteorológica actualizada de España, consulta AEMET (Agencia Estatal de Meteorología) en aemet.es. Fecha: {datetime.now().strftime("%d/%m/%Y %H:%M")}',
                'url': 'https://www.aemet.es',
                'source': 'AEMET'
            }]
            
        except Exception as e:
            logger.error(f"Error en información meteorológica: {e}")
            return []
    
    def _get_spain_news(self, query: str) -> List[Dict]:
        """Obtener noticias relacionadas con España"""
        try:
            # Fuentes de noticias españolas públicas
            news_sources = [
                {
                    'name': 'El País',
                    'url': 'https://elpais.com',
                    'description': 'Noticias actuales de España y el mundo'
                },
                {
                    'name': 'ABC',
                    'url': 'https://abc.es',
                    'description': 'Información y noticias de actualidad'
                },
                {
                    'name': 'La Vanguardia',
                    'url': 'https://lavanguardia.com',
                    'description': 'Noticias de España y Cataluña'
                }
            ]
            
            results = []
            for source in news_sources:
                results.append({
                    'title': f"Noticias en {source['name']}",
                    'snippet': f"{source['description']} - Consulta {source['name']} para las últimas noticias sobre: {query}",
                    'url': source['url'],
                    'source': source['name']
                })
            
            return results
            
        except Exception as e:
            logger.error(f"Error en noticias: {e}")
            return []
    
    def _generate_summary(self, sources: List[Dict]) -> str:
        """Generar un resumen de todas las fuentes"""
        if not sources:
            return "No se encontró información relevante."
        
        summary_parts = []
        
        for source_group in sources:
            source_name = source_group['source']
            results = source_group['results']
            
            if results:
                summary_parts.append(f"**{source_name}:**")
                for result in results[:2]:  # Máximo 2 resultados por fuente
                    snippet = result.get('snippet', '').strip()
                    if snippet:
                        summary_parts.append(f"• {snippet[:200]}...")
        
        if summary_parts:
            return "\n".join(summary_parts)
        else:
            return "Se encontraron fuentes pero sin contenido específico."
    
    def get_api_status(self) -> Dict[str, Any]:
        """Obtener estado de las APIs"""
        status = {
            'timestamp': datetime.now().isoformat(),
            'apis': {},
            'total_enabled': 0
        }
        
        for api_name, config in self.apis_config.items():
            status['apis'][api_name] = {
                'enabled': config['enabled'],
                'description': config['description'],
                'url': config['url']
            }
            
            if config['enabled']:
                status['total_enabled'] += 1
        
        return status

# Instancia global
aria_spanish_apis = ARIASpanishAPIs()

# Funciones de conveniencia
def search_comprehensive(query: str, max_results: int = 5) -> Dict[str, Any]:
    """Función de conveniencia para búsqueda comprehensiva"""
    return aria_spanish_apis.search_comprehensive(query, max_results)

def get_api_status() -> Dict[str, Any]:
    """Función de conveniencia para obtener estado de APIs"""
    return aria_spanish_apis.get_api_status()

if __name__ == "__main__":
    # Test básico
    print("🧪 Probando APIs Españolas...")
    test_query = "Madrid"
    results = search_comprehensive(test_query)
    print(f"Resultados para '{test_query}':")
    print(json.dumps(results, indent=2, ensure_ascii=False))