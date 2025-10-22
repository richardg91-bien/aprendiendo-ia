"""
🌐 ARIA - Integración con Google Cloud APIs Gratuitas
===================================================

Integración del sistema ARIA con Google Cloud Natural Language API
y otros servicios gratuitos de Google Cloud para mejorar capacidades multilingües.

Características:
✅ Google Cloud Natural Language API (5,000 unidades/mes gratis)
✅ Google Cloud Translation API (500,000 caracteres/mes gratis)
✅ Análisis de sentimientos avanzado
✅ Detección de entidades y clasificación
✅ Configuración segura con credenciales locales

Fecha: 22 de octubre de 2025
"""

import os
import json
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime
import requests

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class GoogleCloudAPIsIntegration:
    """Integración con Google Cloud APIs gratuitas para ARIA"""
    
    def __init__(self):
        self.project_id = os.getenv('GOOGLE_CLOUD_PROJECT', '')
        self.api_key = os.getenv('GOOGLE_CLOUD_API_KEY', '')
        
        # URLs base para las APIs
        self.natural_language_url = "https://language.googleapis.com/v1/documents"
        self.translation_url = "https://translation.googleapis.com/language/translate/v2"
        
        # Cache para optimizar llamadas
        self.cache = {}
        self.cache_ttl = 3600  # 1 hora
        
        # Contadores para límites gratuitos
        self.daily_usage = {
            'natural_language': 0,
            'translation': 0,
            'sentiment_analysis': 0
        }
        
        # Límites de plan gratuito
        self.free_limits = {
            'natural_language': 5000,  # unidades por mes
            'translation': 500000,     # caracteres por mes
            'sentiment_analysis': 5000  # unidades por mes
        }
        
        self._verify_credentials()
        print("🌐 Google Cloud APIs inicializadas")
    
    def _verify_adc_credentials(self):
        """Verifica Application Default Credentials"""
        try:
            # Verificar si ADC están configuradas
            adc_path = os.path.expanduser('~/.config/gcloud/application_default_credentials.json')
            
            if os.path.exists(adc_path):
                logger.info("✅ Application Default Credentials encontradas")
                return True
            else:
                logger.info("⚠️ ADC no configuradas - usar gcloud auth application-default login")
                return False
                
        except Exception as e:
            logger.warning(f"⚠️ Error verificando ADC: {e}")
            return False
    
    def _verify_credentials(self):
        """Verifica si las credenciales están configuradas"""
        if not self.api_key:
            logger.warning("⚠️ GOOGLE_CLOUD_API_KEY no configurada")
            logger.info("💡 Para configurar Google Cloud APIs automáticamente:")
            logger.info("   Ejecutar: python configuracion_google_cloud_automatica.py")
            logger.info("   O manualmente:")
            logger.info("   1. Instalar gcloud CLI")
            logger.info("   2. Ejecutar: gcloud auth application-default login")
            logger.info("   3. Crear clave API en Google Cloud Console")
            logger.info("   4. Configurar: set GOOGLE_CLOUD_API_KEY=tu_clave")
        else:
            logger.info("✅ Credenciales de Google Cloud detectadas")
            self._verify_adc_credentials()
    
    def analyze_sentiment_advanced(self, text: str, language: str = 'auto') -> Dict:
        """
        Análisis avanzado de sentimientos usando Google Cloud Natural Language API
        
        Args:
            text: Texto a analizar
            language: Código de idioma (auto, es, en)
            
        Returns:
            Dict con análisis detallado de sentimientos
        """
        if not self.api_key:
            return self._fallback_sentiment_analysis(text)
        
        cache_key = f"sentiment_gc_{hash(text)}"
        cached = self._get_cached_result(cache_key)
        if cached:
            return cached
        
        try:
            # Preparar solicitud para Google Cloud Natural Language
            url = f"{self.natural_language_url}:analyzeSentiment"
            
            payload = {
                "document": {
                    "type": "PLAIN_TEXT",
                    "content": text[:1000],  # Limitar para plan gratuito
                    "language": language if language != 'auto' else None
                },
                "encodingType": "UTF8"
            }
            
            headers = {
                'Content-Type': 'application/json',
                'X-goog-api-key': self.api_key
            }
            
            response = requests.post(url, json=payload, headers=headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                # Procesar respuesta de Google Cloud
                document_sentiment = data.get('documentSentiment', {})
                sentences = data.get('sentences', [])
                
                result = {
                    'api': 'Google Cloud Natural Language',
                    'overall_sentiment': {
                        'score': document_sentiment.get('score', 0),
                        'magnitude': document_sentiment.get('magnitude', 0),
                        'label': self._classify_sentiment_score(document_sentiment.get('score', 0))
                    },
                    'sentence_analysis': [
                        {
                            'text': sent.get('text', {}).get('content', ''),
                            'sentiment': sent.get('sentiment', {}),
                            'score': sent.get('sentiment', {}).get('score', 0),
                            'magnitude': sent.get('sentiment', {}).get('magnitude', 0)
                        }
                        for sent in sentences[:3]  # Primeras 3 oraciones
                    ],
                    'confidence': min(document_sentiment.get('magnitude', 0), 1.0),
                    'language_detected': data.get('language', language),
                    'processing_time': datetime.now().isoformat(),
                    'characters_processed': len(text)
                }
                
                self._set_cached_result(cache_key, result)
                self.daily_usage['sentiment_analysis'] += 1
                
                logger.info(f"✅ Google Cloud: Análisis de sentimientos completado")
                return result
            else:
                logger.error(f"❌ Google Cloud API error: {response.status_code}")
                return self._fallback_sentiment_analysis(text)
                
        except Exception as e:
            logger.error(f"❌ Error en Google Cloud Natural Language: {e}")
            return self._fallback_sentiment_analysis(text)
    
    def translate_text_google(self, text: str, target_lang: str = 'es', source_lang: str = 'auto') -> Dict:
        """
        Traducción usando Google Cloud Translation API
        
        Args:
            text: Texto a traducir
            target_lang: Idioma destino (es, en, fr, etc.)
            source_lang: Idioma origen (auto para detección)
            
        Returns:
            Dict con resultado de traducción
        """
        if not self.api_key:
            return self._fallback_translation(text, target_lang)
        
        cache_key = f"translate_gc_{source_lang}_{target_lang}_{hash(text)}"
        cached = self._get_cached_result(cache_key)
        if cached:
            return cached
        
        try:
            # Verificar límite de caracteres
            if len(text) > 5000:  # Limitar para plan gratuito
                text = text[:5000] + "..."
            
            url = self.translation_url
            
            params = {
                'key': self.api_key,
                'q': text,
                'target': target_lang,
                'format': 'text'
            }
            
            if source_lang != 'auto':
                params['source'] = source_lang
            
            response = requests.post(url, data=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                translations = data.get('data', {}).get('translations', [])
                
                if translations:
                    translation = translations[0]
                    
                    result = {
                        'api': 'Google Cloud Translation',
                        'original_text': text,
                        'translated_text': translation.get('translatedText', text),
                        'detected_source_language': translation.get('detectedSourceLanguage', source_lang),
                        'target_language': target_lang,
                        'confidence': 0.95,  # Google Cloud tiene alta confiabilidad
                        'characters_processed': len(text),
                        'timestamp': datetime.now().isoformat()
                    }
                    
                    self._set_cached_result(cache_key, result)
                    self.daily_usage['translation'] += len(text)
                    
                    logger.info(f"✅ Google Translate: '{text[:30]}...' → {target_lang}")
                    return result
            
            logger.error(f"❌ Google Translation API error: {response.status_code}")
            return self._fallback_translation(text, target_lang)
            
        except Exception as e:
            logger.error(f"❌ Error en Google Cloud Translation: {e}")
            return self._fallback_translation(text, target_lang)
    
    def analyze_entities_and_classify(self, text: str, language: str = 'auto') -> Dict:
        """
        Análisis de entidades y clasificación usando Google Cloud Natural Language
        
        Args:
            text: Texto a analizar
            language: Código de idioma
            
        Returns:
            Dict con entidades identificadas y clasificación
        """
        if not self.api_key:
            return self._fallback_entity_analysis(text)
        
        cache_key = f"entities_gc_{hash(text)}"
        cached = self._get_cached_result(cache_key)
        if cached:
            return cached
        
        try:
            # Análisis de entidades
            entities_url = f"{self.natural_language_url}:analyzeEntities"
            
            payload = {
                "document": {
                    "type": "PLAIN_TEXT",
                    "content": text[:1000],
                    "language": language if language != 'auto' else None
                },
                "encodingType": "UTF8"
            }
            
            headers = {
                'Content-Type': 'application/json',
                'X-goog-api-key': self.api_key
            }
            
            response = requests.post(entities_url, json=payload, headers=headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                entities = data.get('entities', [])
                
                # También intentar clasificación de contenido
                classification_result = self._classify_content_google(text, language)
                
                result = {
                    'api': 'Google Cloud Natural Language',
                    'entities': [
                        {
                            'name': entity.get('name', ''),
                            'type': entity.get('type', 'UNKNOWN'),
                            'salience': entity.get('salience', 0),
                            'wikipedia_url': entity.get('metadata', {}).get('wikipedia_url', ''),
                            'mid': entity.get('metadata', {}).get('mid', '')
                        }
                        for entity in entities[:10]  # Top 10 entidades
                    ],
                    'classification': classification_result,
                    'language_detected': data.get('language', language),
                    'entity_count': len(entities),
                    'confidence': 0.9,
                    'timestamp': datetime.now().isoformat()
                }
                
                self._set_cached_result(cache_key, result)
                self.daily_usage['natural_language'] += 1
                
                logger.info(f"✅ Google Cloud: {len(entities)} entidades identificadas")
                return result
            
            return self._fallback_entity_analysis(text)
            
        except Exception as e:
            logger.error(f"❌ Error en análisis de entidades: {e}")
            return self._fallback_entity_analysis(text)
    
    def _classify_content_google(self, text: str, language: str) -> Dict:
        """Clasificación de contenido usando Google Cloud"""
        try:
            classify_url = f"{self.natural_language_url}:classifyText"
            
            payload = {
                "document": {
                    "type": "PLAIN_TEXT",
                    "content": text,
                    "language": language if language != 'auto' else None
                }
            }
            
            headers = {
                'Content-Type': 'application/json',
                'X-goog-api-key': self.api_key
            }
            
            response = requests.post(classify_url, json=payload, headers=headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                categories = data.get('categories', [])
                
                return {
                    'categories': [
                        {
                            'name': cat.get('name', ''),
                            'confidence': cat.get('confidence', 0)
                        }
                        for cat in categories[:5]
                    ],
                    'primary_category': categories[0].get('name', 'General') if categories else 'General'
                }
            
        except Exception:
            pass
        
        return {
            'categories': [],
            'primary_category': 'General'
        }
    
    # Métodos auxiliares
    
    def _classify_sentiment_score(self, score: float) -> str:
        """Clasifica puntuación de sentimiento en etiqueta"""
        if score >= 0.25:
            return 'positive'
        elif score <= -0.25:
            return 'negative'
        else:
            return 'neutral'
    
    def _get_cached_result(self, key: str) -> Optional[Any]:
        """Obtiene resultado desde cache"""
        if key in self.cache:
            data, timestamp = self.cache[key]
            if (datetime.now().timestamp() - timestamp) < self.cache_ttl:
                return data
        return None
    
    def _set_cached_result(self, key: str, data: Any):
        """Guarda resultado en cache"""
        self.cache[key] = (data, datetime.now().timestamp())
    
    def _fallback_sentiment_analysis(self, text: str) -> Dict:
        """Análisis de sentimientos de respaldo"""
        return {
            'api': 'Fallback Sentiment',
            'overall_sentiment': {
                'score': 0.0,
                'magnitude': 0.5,
                'label': 'neutral'
            },
            'sentence_analysis': [],
            'confidence': 0.6,
            'note': 'Usando análisis básico - configurar Google Cloud API para análisis avanzado'
        }
    
    def _fallback_translation(self, text: str, target_lang: str) -> Dict:
        """Traducción de respaldo"""
        return {
            'api': 'Fallback Translation',
            'original_text': text,
            'translated_text': text,
            'target_language': target_lang,
            'confidence': 0.5,
            'note': 'Sin traducción - configurar Google Cloud API'
        }
    
    def _fallback_entity_analysis(self, text: str) -> Dict:
        """Análisis de entidades de respaldo"""
        return {
            'api': 'Fallback Entity Analysis',
            'entities': [],
            'classification': {'categories': [], 'primary_category': 'General'},
            'confidence': 0.5,
            'note': 'Análisis básico - configurar Google Cloud API para análisis avanzado'
        }
    
    def get_usage_status(self) -> Dict:
        """Obtiene estado de uso de las APIs"""
        return {
            'daily_usage': self.daily_usage.copy(),
            'free_limits': self.free_limits.copy(),
            'usage_percentage': {
                service: (used / limit * 100) 
                for service, (used, limit) in zip(
                    self.daily_usage.keys(),
                    [(self.daily_usage[k], self.free_limits[k]) for k in self.daily_usage.keys()]
                )
            },
            'api_key_configured': bool(self.api_key),
            'cache_entries': len(self.cache),
            'timestamp': datetime.now().isoformat()
        }

# Instancia global
google_cloud_apis = GoogleCloudAPIsIntegration()

if __name__ == "__main__":
    # Prueba básica del sistema
    print("🧪 Probando Google Cloud APIs...")
    
    # Texto de prueba
    test_text = "La inteligencia artificial está transformando el mundo de manera increíble."
    
    # Análisis de sentimientos
    print("\n📊 Análisis de sentimientos:")
    sentiment = google_cloud_apis.analyze_sentiment_advanced(test_text)
    print(f"   Sentimiento: {sentiment.get('overall_sentiment', {}).get('label', 'N/A')}")
    print(f"   Puntuación: {sentiment.get('overall_sentiment', {}).get('score', 0):.2f}")
    
    # Traducción
    print("\n🔄 Traducción:")
    translation = google_cloud_apis.translate_text_google(test_text, target_lang='en')
    print(f"   Original: {test_text[:50]}...")
    print(f"   Traducido: {translation.get('translated_text', 'N/A')[:50]}...")
    
    # Análisis de entidades
    print("\n🏷️ Análisis de entidades:")
    entities = google_cloud_apis.analyze_entities_and_classify(test_text)
    print(f"   Entidades encontradas: {entities.get('entity_count', 0)}")
    
    # Estado de uso
    print("\n📈 Estado de uso:")
    status = google_cloud_apis.get_usage_status()
    print(f"   API Key configurada: {status['api_key_configured']}")
    print(f"   Entradas en cache: {status['cache_entries']}")
    
    print("\n✅ Prueba de Google Cloud APIs completada")