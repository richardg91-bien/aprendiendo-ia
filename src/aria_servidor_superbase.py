#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🤖 ARIA - Servidor con Super Base Integration
============================================

Servidor ARIA mejorado con integración completa de Super Base
para almacenamiento persistente de conocimiento y relaciones APIs.

Características:
✅ Integración completa con Supabase
✅ Almacenamiento persistente de conversaciones
✅ Gestión de conocimiento con base de datos
✅ Relaciones inteligentes con APIs externas
✅ Sistema de aprendizaje continuo
✅ Interfaz moderna con React

Fecha: 22 de octubre de 2025
"""

import sys
import os

# Agregar directorios al path para imports relativos
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, current_dir)
sys.path.insert(0, parent_dir)

from flask import Flask, request, jsonify, render_template, send_from_directory
from flask_cors import CORS
import json
import time
import uuid
from datetime import datetime, timezone
import logging
import re
from typing import Dict, List, Optional, Any

# Importar Super Base
try:
    from aria_superbase import aria_superbase, ARIASuperBase
    SUPERBASE_AVAILABLE = True
    print("🗄️ ARIA Super Base cargado")
except ImportError as e:
    SUPERBASE_AVAILABLE = False
    print(f"❌ Super Base no disponible: {e}")

# Importar sistema de embeddings con Supabase
try:
    from core.aria_embeddings_supabase import ARIAEmbeddingsSupabase, crear_embedding_system
    EMBEDDINGS_AVAILABLE = True
    print("🧠 Sistema de embeddings Supabase cargado")
except ImportError as e:
    EMBEDDINGS_AVAILABLE = False
    print(f"❌ Sistema de embeddings no disponible: {e}")

# Importar sistemas de ARIA existentes
try:
    # Sistema de aprendizaje deshabilitado temporalmente para evitar búsquedas web automáticas
    # from auto_learning_advanced import aria_advanced_learning
    # from multilingual_apis import aria_multilingual_apis
    LEARNING_SYSTEM_AVAILABLE = False
    print("📝 Sistema de aprendizaje web deshabilitado (para respuestas directas)")
except ImportError as e:
    LEARNING_SYSTEM_AVAILABLE = False
    print(f"⚠️ Sistema de aprendizaje no disponible: {e}")

# Importar sistema emocional con Supabase
try:
    from core.emotion_detector_supabase import (
        init_emotion_detector_supabase,
        detect_user_emotion_supabase,
        detect_aria_emotion_supabase,
        get_emotion_stats_supabase
    )
    EMOTION_SUPABASE_AVAILABLE = True
    print("🎭 Sistema emocional Supabase cargado")
except ImportError as e:
    EMOTION_SUPABASE_AVAILABLE = False
    print(f"⚠️ Sistema emocional Supabase no disponible: {e}")
    
    # Fallback al sistema emocional original (legacy)
    try:
        from legacy_backup.emotion_detector import init_emotion_detector, detect_user_emotion, detect_aria_emotion
        EMOTION_LEGACY_AVAILABLE = True
        print("🎭 Sistema emocional legacy cargado")
    except ImportError as e2:
        EMOTION_LEGACY_AVAILABLE = False
        print(f"⚠️ Sistema emocional legacy no disponible: {e2}")

# Determinar qué sistema emocional usar
if EMOTION_SUPABASE_AVAILABLE:
    EMOTION_SYSTEM = "supabase"
    print("✅ Usando sistema emocional Supabase")
elif EMOTION_LEGACY_AVAILABLE:
    EMOTION_SYSTEM = "legacy"
    print("✅ Usando sistema emocional legacy")
else:
    EMOTION_SYSTEM = "none"
    print("❌ Sin sistema emocional disponible")

try:
    # Sistema de APIs españolas activado
    from spanish_apis import aria_spanish_apis
    SPANISH_APIS_AVAILABLE = True
    print("🇪� APIs españolas cargadas y activas")
except ImportError:
    SPANISH_APIS_AVAILABLE = False
    print("⚠️ APIs en español no disponibles")

# Configurar Flask
app = Flask(__name__, 
           template_folder='../frontend/public',
           static_folder='../frontend/build/static')
CORS(app)

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ARIASuperServer:
    """Servidor ARIA con Super Base - La evolución definitiva"""
    
    def __init__(self):
        self.session_id = str(uuid.uuid4())
        self.conversation_count = 0
        self.start_time = datetime.now(timezone.utc)
        
        # Sistema emocional con Supabase
        self.emotion_detector = None
        self.emotion_system_type = EMOTION_SYSTEM
        
        if EMOTION_SYSTEM == "supabase":
            try:
                # Obtener API key de EdenAI si está disponible
                eden_api_key = os.getenv('EDENAI_API_KEY', '')
                self.emotion_detector = init_emotion_detector_supabase(eden_api_key)
                print("✅ Sistema emocional Supabase inicializado")
            except Exception as e:
                print(f"⚠️ Error inicializando emociones Supabase: {e}")
                self.emotion_system_type = "basic"
        elif EMOTION_SYSTEM == "legacy":
            try:
                # Usar sistema emocional legacy
                eden_api_key = os.getenv('EDENAI_API_KEY', '')
                if eden_api_key:
                    init_emotion_detector(eden_api_key)
                print("✅ Sistema emocional legacy inicializado")
            except Exception as e:
                print(f"⚠️ Error inicializando emociones legacy: {e}")
                self.emotion_system_type = "basic"
        else:
            self.emotion_system_type = "basic"
            print("📦 Usando sistema emocional básico")
        
        # Sistema de emociones mejorado (mantenido para compatibilidad)
        self.emotions = {
            'happiness': 0.7,
            'curiosity': 0.8,
            'confidence': 0.6,
            'empathy': 0.9,
            'excitement': 0.5
        }
        
        self.current_emotion = 'curious'
        
        # Configuración de usuario
        self.user_preferences = {
            'language': 'auto',
            'response_style': 'educational',
            'detail_level': 'medium',
            'personality': 'friendly',
            'use_superbase': SUPERBASE_AVAILABLE
        }
        
        # Cache local para rendimiento - DEBE estar antes de _initialize_superbase()
        self.knowledge_cache = {}
        self.api_cache = {}
        
        # Inicializar Super Base si está disponible
        if SUPERBASE_AVAILABLE:
            self.superbase = aria_superbase
            self._initialize_superbase()
        else:
            self.superbase = None
            print("📝 Usando almacenamiento en memoria")
        
        # Inicializar sistema de embeddings si está disponible
        if EMBEDDINGS_AVAILABLE:
            try:
                self.embeddings_system = crear_embedding_system()
                if self.embeddings_system:
                    print("🧠 Sistema de embeddings Supabase inicializado")
                else:
                    print("⚠️ No se pudo inicializar sistema de embeddings")
                    self.embeddings_system = None
            except Exception as e:
                print(f"⚠️ Error inicializando embeddings: {e}")
                self.embeddings_system = None
        else:
            self.embeddings_system = None
            print("📝 Sistema de embeddings no disponible")
        
        print(f"🚀 ARIA Super Server inicializado - Sesión: {self.session_id[:8]}")
    
    def _initialize_superbase(self):
        """Inicializar Super Base con datos de sesión"""
        try:
            # Registrar inicio de sesión
            session_data = {
                'topic': 'aria_session_start',
                'source_type': 'system_initialization',
                'knowledge_gained': 0,
                'apis_discovered': 0,
                'session_duration': 0,
                'success_indicators': {
                    'session_id': self.session_id,
                    'start_time': self.start_time.isoformat(),
                    'superbase_enabled': True
                }
            }
            
            # Registrar en tabla de learning_sessions
            # self.superbase.store_learning_session(**session_data)
            
            print("✅ Super Base inicializado para la sesión")
            
            # Cargar conocimiento existente en cache
            self._load_knowledge_cache()
            
        except Exception as e:
            print(f"⚠️ Error inicializando Super Base: {e}")
    
    def _load_knowledge_cache(self):
        """Cargar conocimiento frecuente en cache"""
        try:
            if not self.superbase:
                return
                
            # Cargar conceptos más confiables
            knowledge = self.superbase.get_knowledge()
            for item in knowledge[:50]:  # Top 50
                concept = item.get('concept', '')
                self.knowledge_cache[concept] = item
            
            print(f"📚 Cache cargado con {len(self.knowledge_cache)} conceptos")
            
        except Exception as e:
            print(f"⚠️ Error cargando cache: {e}")
    
    def process_message(self, user_message: str, context: Dict = None) -> Dict[str, Any]:
        """Procesar mensaje del usuario con integración Super Base"""
        start_time = time.time()
        self.conversation_count += 1
        
        try:
            # Detectar idioma
            language = self._detect_language(user_message)
            
            # Buscar conocimiento relevante
            relevant_knowledge = self._search_knowledge(user_message)
            
            # Generar respuesta inteligente
            response_data = self._generate_intelligent_response(
                user_message, relevant_knowledge, language
            )
            
            # Actualizar emociones
            self._update_emotions(user_message, response_data)
            
            # Almacenar conversación en Super Base
            if self.superbase:
                self._store_conversation(user_message, response_data)
            
            # Aprender de la conversación
            self._learn_from_conversation(user_message, response_data)
            
            # Preparar respuesta completa
            response_time = time.time() - start_time
            
            final_response = {
                'response': response_data['response'],
                'emotion': self.current_emotion,
                'confidence': response_data.get('confidence', 0.8),
                'knowledge_used': relevant_knowledge[:3],  # Top 3
                'apis_called': response_data.get('apis_used', []),
                'language_detected': language,
                'response_time': round(response_time, 3),
                'conversation_count': self.conversation_count,
                'session_id': self.session_id[:8],
                'superbase_enabled': self.superbase is not None,
                'learning_insights': response_data.get('learning_insights', []),
                'suggested_topics': self._get_suggested_topics(user_message)
            }
            
            return final_response
            
        except Exception as e:
            logger.error(f"Error procesando mensaje: {e}")
            return self._create_error_response(str(e))
    
    def _detect_language(self, text: str) -> str:
        """Detectar idioma del texto"""
        # Palabras comunes en español
        spanish_words = ['que', 'como', 'donde', 'cuando', 'porque', 'para', 'con', 'una', 'una', 'del', 'es', 'el', 'la', 'de', 'y', 'en']
        # Palabras comunes en inglés  
        english_words = ['the', 'and', 'for', 'are', 'but', 'not', 'you', 'all', 'can', 'had', 'her', 'was', 'one', 'our', 'out', 'day']
        
        words = text.lower().split()
        spanish_count = sum(1 for word in words if word in spanish_words)
        english_count = sum(1 for word in words if word in english_words)
        
        if spanish_count > english_count:
            return 'es'
        elif english_count > spanish_count:
            return 'en'
        else:
            return 'auto'
    
    def _search_knowledge(self, query: str) -> List[Dict]:
        """Buscar conocimiento relevante usando embeddings y búsqueda tradicional"""
        relevant_knowledge = []
        
        try:
            # 1. Buscar usando embeddings si está disponible
            if self.embeddings_system:
                try:
                    # Buscar textos similares con embeddings
                    embedding_results = self.embeddings_system.buscar_similares(
                        query, limite=5, umbral_similitud=0.6
                    )
                    
                    for result in embedding_results:
                        knowledge_item = {
                            'concept': result['texto'][:50] + '...' if len(result['texto']) > 50 else result['texto'],
                            'description': result['texto'],
                            'confidence': result['similitud'],
                            'source': f"embeddings_{result['categoria']}",
                            'category': result['categoria'],
                            'metadata': result.get('metadatos', {})
                        }
                        relevant_knowledge.append(knowledge_item)
                    
                    # Buscar conocimiento estructurado
                    knowledge_results = self.embeddings_system.buscar_conocimiento(query, limite=3)
                    
                    for result in knowledge_results:
                        knowledge_item = {
                            'concept': result['concepto'],
                            'description': result['descripcion'],
                            'confidence': result['similitud'],
                            'source': 'knowledge_vectors',
                            'category': result['categoria'],
                            'tags': result.get('tags', [])
                        }
                        relevant_knowledge.append(knowledge_item)
                        
                    logger.info(f"🧠 Embeddings encontró {len(embedding_results + knowledge_results)} resultados")
                    
                except Exception as e:
                    logger.error(f"Error en búsqueda con embeddings: {e}")
            
            # 2. Buscar en cache local (búsqueda tradicional)
            for concept, data in self.knowledge_cache.items():
                if any(word.lower() in concept.lower() or word.lower() in data.get('description', '').lower() 
                       for word in query.split()):
                    if data not in relevant_knowledge:  # Evitar duplicados
                        relevant_knowledge.append(data)
            
            # 3. Buscar en Super Base si está disponible y necesitamos más resultados
            if self.superbase and len(relevant_knowledge) < 5:
                try:
                    superbase_results = self.superbase.search_knowledge(query)
                    for result in superbase_results[:3]:
                        # Verificar que no esté duplicado
                        if not any(r.get('concept') == result.get('concept') for r in relevant_knowledge):
                            relevant_knowledge.append(result)
                except Exception as e:
                    logger.error(f"Error en búsqueda SuperBase: {e}")
            
            # Ordenar por confianza/similitud
            relevant_knowledge.sort(key=lambda x: x.get('confidence', 0), reverse=True)
            
            logger.info(f"🔍 Búsqueda de conocimiento: {len(relevant_knowledge)} resultados para '{query}'")
            
        except Exception as e:
            logger.error(f"Error buscando conocimiento: {e}")
        
        return relevant_knowledge[:7]  # Top 7 resultados
    
    def _generate_intelligent_response(self, user_message: str, knowledge: List[Dict], language: str) -> Dict[str, Any]:
        """Generar respuesta inteligente basada en conocimiento"""
        response_data = {
            'response': '',
            'confidence': 0.5,
            'apis_used': [],
            'learning_insights': [],
            'knowledge_sources': len(knowledge)
        }
        
        try:
            # Análisis del tipo de pregunta
            question_type = self._analyze_question_type(user_message)
            
            # 🧠 BUSCAR RESPUESTA DIRECTA EN EMBEDDINGS PRIMERO
            if self.embeddings_system:
                respuesta_directa = self._buscar_respuesta_directa(user_message)
                if respuesta_directa:
                    response_data.update(respuesta_directa)
                    return response_data
            
            # 😊 PRIORIZAR RESPUESTAS EMPÁTICAS PARA SALUDOS (antes que conocimiento)
            mensaje_lower = user_message.lower().strip()
            if mensaje_lower in ['hola', 'hello', 'hi', 'hey', 'buenos días', 'buenas tardes', 'buenas noches', 'buen día']:
                response_data = self._create_friendly_general_response(user_message, language)
                return response_data
            
            # Generar respuesta base con conocimiento encontrado
            if knowledge:
                response_data = self._create_knowledge_based_response(user_message, knowledge, language)
            else:
                # Si no hay conocimiento específico, generar respuesta general más amigable
                response_data = self._create_friendly_general_response(user_message, language)
            
            # Mejorar respuesta con APIs españolas si están disponibles
            if SPANISH_APIS_AVAILABLE and language == 'es':
                enhanced_response = self._enhance_with_spanish_apis(user_message, response_data)
                if enhanced_response:
                    response_data.update(enhanced_response)
            
            # Agregar insights de aprendizaje
            response_data['learning_insights'] = self._generate_learning_insights(user_message, knowledge)
            
        except Exception as e:
            logger.error(f"Error generando respuesta: {e}")
            response_data['response'] = "Disculpa, estoy procesando tu consulta. ¿Puedes reformularla?"
            response_data['confidence'] = 0.3
        
        return response_data
    
    def _buscar_respuesta_directa(self, user_message: str) -> Dict[str, Any]:
        """Buscar respuesta directa usando embeddings para mensajes comunes"""
        try:
            # Buscar conocimiento específico que tenga respuesta sugerida
            conocimiento_results = self.embeddings_system.buscar_conocimiento(user_message, limite=1)
            
            for result in conocimiento_results:
                relaciones = result.get('relaciones', {})
                respuesta_sugerida = relaciones.get('respuesta_sugerida', '')
                
                if respuesta_sugerida and result.get('similitud', 0) > 0.7:  # Alta similitud
                    logger.info(f"💡 Respuesta directa encontrada para: {user_message}")
                    return {
                        'response': respuesta_sugerida,
                        'confidence': result.get('similitud', 0.8),
                        'source': 'direct_knowledge_match',
                        'concept_used': result.get('concepto', ''),
                        'knowledge_sources': 1
                    }
            
            # Buscar en conversaciones ejemplo
            conversacion_results = self.embeddings_system.buscar_similares(
                user_message, 
                limite=1, 
                categoria='conversacion_ejemplo',
                umbral_similitud=0.75
            )
            
            for result in conversacion_results:
                if result.get('subcategoria') == 'mensaje_usuario':
                    # Buscar la respuesta correspondiente
                    metadatos = result.get('metadatos', {})
                    categoria_conv = metadatos.get('categoria_conv', '')
                    
                    # Buscar respuesta de ARIA para esta categoría
                    respuesta_results = self.embeddings_system.buscar_similares(
                        categoria_conv,
                        limite=1,
                        categoria='conversacion_ejemplo'
                    )
                    
                    for resp in respuesta_results:
                        if resp.get('subcategoria') == 'respuesta_aria':
                            logger.info(f"💬 Respuesta de conversación encontrada para: {user_message}")
                            return {
                                'response': resp.get('texto', ''),
                                'confidence': result.get('similitud', 0.8),
                                'source': 'conversation_example',
                                'emotion': resp.get('metadatos', {}).get('emocion', 'happy'),
                                'knowledge_sources': 1
                            }
            
            return None
            
        except Exception as e:
            logger.error(f"Error buscando respuesta directa: {e}")
            return None
    
    def _create_friendly_general_response(self, user_message: str, language: str) -> Dict[str, Any]:
        """Crear respuesta general amigable cuando no hay conocimiento específico"""
        
        # Detectar si es un saludo simple
        mensaje_lower = user_message.lower().strip()
        
        if mensaje_lower in ['hola', 'hello', 'hi', 'hey']:
            import random
            respuestas_hola = [
                '¡Hola! 😊 Me alegra mucho saludarte. Soy ARIA, tu asistente de inteligencia artificial. ¿Cómo estás hoy?',
                '¡Hey! 🤗 ¡Qué gusto verte por aquí! Soy ARIA y estoy aquí para ayudarte con lo que necesites. ¿En qué puedo asistirte?',
                '¡Hola! 😄 Es un placer conocerte. Soy ARIA, tu compañera de IA. ¿Hay algo interesante en lo que pueda ayudarte hoy?',
                '¡Hola, amigo! 🌟 Me emociona poder conversar contigo. Soy ARIA y me encanta ayudar. ¿Qué tienes en mente?'
            ]
            return {
                'response': random.choice(respuestas_hola),
                'confidence': 0.95,
                'source': 'built_in_greeting',
                'emotion': 'happy'
            }
        
        if mensaje_lower in ['buenos días', 'buen día', 'good morning']:
            import random
            respuestas_manana = [
                '¡Buenos días! ☀️ ¡Espero que hayas tenido un buen despertar! ¿Cómo puedo hacer tu mañana más productiva?',
                '¡Buen día! 🌅 Me alegra comenzar la mañana contigo. ¿En qué aventura podemos embarcarnos hoy?',
                '¡Buenos días! 😊 ¡Qué energía tan positiva traes! ¿Hay algo especial que quieras lograr esta mañana?'
            ]
            return {
                'response': random.choice(respuestas_manana),
                'confidence': 0.95,
                'source': 'built_in_greeting',
                'emotion': 'cheerful'
            }
        
        if mensaje_lower in ['buenas tardes', 'buena tarde', 'good afternoon']:
            return {
                'response': '¡Buenas tardes! 🌅 ¿Cómo va tu día? ¿En qué puedo ayudarte esta tarde?',
                'confidence': 0.9,
                'source': 'built_in_greeting',
                'emotion': 'friendly'
            }
        
        if mensaje_lower in ['buenas noches', 'buena noche', 'good night']:
            return {
                'response': '¡Buenas noches! 🌙 ¿En qué puedo ayudarte esta noche?',
                'confidence': 0.9,
                'source': 'built_in_greeting',
                'emotion': 'calm'
            }
        
        if mensaje_lower in ['gracias', 'thank you', 'thanks']:
            return {
                'response': '¡De nada! 😊 Me alegra haber podido ayudarte. ¿Hay algo más en lo que pueda asistirte?',
                'confidence': 0.9,
                'source': 'built_in_courtesy',
                'emotion': 'satisfied'
            }
        
        if 'cómo estás' in mensaje_lower or 'how are you' in mensaje_lower:
            import random
            respuestas_estado = [
                '¡Estoy fantástica! 😄 Cada conversación me llena de energía. ¿Y tú? ¿Cómo ha sido tu día?',
                '¡Me siento genial! 🌟 Siempre me emociona conocer gente nueva y ayudar. ¿Tú cómo estás hoy?',
                '¡Estoy súper bien! 😊 Me encanta poder charlar contigo. Cuéntame, ¿cómo te sientes hoy?',
                '¡Increíble! 🚀 Me llena de alegría poder ayudarte. ¿Y tú qué tal? ¿Todo bien por ahí?'
            ]
            return {
                'response': random.choice(respuestas_estado),
                'confidence': 0.95,
                'source': 'built_in_status',
                'emotion': 'happy'
            }
        
        # Respuesta general más amigable y DIRECTA
        return {
            'response': f'¡Hola! 😊 No tengo información específica sobre "{user_message}" en este momento, pero estoy aquí para ayudarte. ¿Podrías contarme más o preguntarme algo específico? Puedo ayudarte con conversación, información general, o cualquier duda que tengas.',
            'confidence': 0.7,
            'source': 'friendly_fallback',
            'emotion': 'helpful'
        }
    
    def _analyze_question_type(self, message: str) -> str:
        """Analizar el tipo de pregunta"""
        message_lower = message.lower()
        
        if any(word in message_lower for word in ['qué', 'what', 'que es', 'what is']):
            return 'definition'
        elif any(word in message_lower for word in ['cómo', 'how', 'como']):
            return 'process'
        elif any(word in message_lower for word in ['dónde', 'where', 'donde']):
            return 'location'
        elif any(word in message_lower for word in ['cuándo', 'when', 'cuando']):
            return 'time'
        elif any(word in message_lower for word in ['por qué', 'why', 'porque']):
            return 'reason'
        elif '?' in message:
            return 'question'
        else:
            return 'statement'
    
    def _create_knowledge_based_response(self, user_message: str, knowledge: List[Dict], language: str) -> Dict[str, Any]:
        """Crear respuesta basada en conocimiento almacenado"""
        response_parts = []
        confidence_scores = []
        knowledge_used = []
        
        for item in knowledge[:3]:  # Usar top 3
            concept = item.get('concept', '')
            description = item.get('description', '')
            confidence = item.get('confidence', 0.5)
            
            if description:
                response_parts.append(f"📚 Sobre **{concept}**: {description}")
                confidence_scores.append(confidence)
                knowledge_used.append(concept)
        
        if response_parts:
            if language == 'es':
                intro = "Basándome en mi conocimiento, puedo contarte que:\n\n"
                outro = f"\n\n¿Te gustaría que profundice en algún aspecto específico de {'**' + '**, **'.join(knowledge_used) + '**' if knowledge_used else 'este tema'}?"
            else:
                intro = "Based on my knowledge, I can tell you that:\n\n"
                outro = f"\n\nWould you like me to elaborate on any specific aspect of {'**' + '**, **'.join(knowledge_used) + '**' if knowledge_used else 'this topic'}?"
            
            response = intro + "\n\n".join(response_parts) + outro
            avg_confidence = sum(confidence_scores) / len(confidence_scores) if confidence_scores else 0.5
            
            return {
                'response': response,
                'confidence': min(avg_confidence + 0.2, 1.0),  # Boost por usar conocimiento
                'knowledge_sources': len(knowledge_used),
                'concepts_used': knowledge_used
            }
        
        return self._create_general_response(user_message, language)
    
    def _create_general_response(self, user_message: str, language: str) -> Dict[str, Any]:
        """Crear respuesta general cuando no hay conocimiento específico"""
        if language == 'es':
            responses = [
                f"Interesante pregunta sobre '{user_message}'. Aunque no tengo información específica almacenada sobre esto, puedo ayudarte a explorar el tema.",
                f"Me has hecho pensar en '{user_message}'. Es un tema fascinante que me gustaría aprender más contigo.",
                f"Sobre '{user_message}', me encantaría poder darte una respuesta más específica. ¿Podrías contarme más detalles para que pueda aprender contigo?"
            ]
        else:
            responses = [
                f"Interesting question about '{user_message}'. While I don't have specific stored information about this, I can help you explore the topic.",
                f"You've got me thinking about '{user_message}'. It's a fascinating topic I'd like to learn more about with you.",
                f"Regarding '{user_message}', I'd love to give you a more specific answer. Could you tell me more details so I can learn with you?"
            ]
        
        import random
        response = random.choice(responses)
        
        return {
            'response': response,
            'confidence': 0.6,
            'learning_opportunity': True
        }
    
    def _enhance_with_spanish_apis(self, user_message: str, response_data: Dict) -> Dict[str, Any]:
        """Mejorar respuesta con APIs en español"""
        enhancement = {'apis_used': []}
        
        try:
            if SPANISH_APIS_AVAILABLE:
                # Intentar usar APIs españolas para mejorar la respuesta
                api_result = aria_spanish_apis.search_comprehensive(user_message)
                if api_result and api_result.get('success'):
                    enhancement['apis_used'].append('spanish_knowledge_api')
                    # Agregar información adicional si está disponible
                    if api_result.get('summary'):
                        response_data['response'] += f"\n\n🌐 **Información adicional**: {api_result['summary']}"
                        response_data['confidence'] = min(response_data['confidence'] + 0.1, 1.0)
        
        except Exception as e:
            logger.error(f"Error con APIs españolas: {e}")
        
        return enhancement
    
    def _generate_learning_insights(self, user_message: str, knowledge: List[Dict]) -> List[str]:
        """Generar insights de aprendizaje"""
        insights = []
        
        # Análisis de gaps de conocimiento
        if not knowledge:
            insights.append("Oportunidad de aprendizaje: Este es un tema nuevo para mí")
        
        # Análisis de conexiones
        if len(knowledge) > 1:
            concepts = [k.get('concept', '') for k in knowledge]
            insights.append(f"Conexiones encontradas entre: {', '.join(concepts[:3])}")
        
        # Análisis de confianza
        if knowledge:
            avg_confidence = sum(k.get('confidence', 0) for k in knowledge) / len(knowledge)
            if avg_confidence < 0.7:
                insights.append("Necesito más información para aumentar mi confianza en este tema")
        
        return insights
    
    def _update_emotions(self, user_message: str, response_data: Dict):
        """Actualizar estado emocional de ARIA usando Supabase"""
        
        if self.emotion_system_type == "supabase":
            try:
                # Detectar emoción del usuario
                user_emotion = detect_user_emotion_supabase(user_message)
                
                # Detectar emoción de la respuesta de ARIA
                aria_response = response_data.get('response', '')
                aria_emotion = detect_aria_emotion_supabase(aria_response)
                
                # Actualizar estado emocional con datos de Supabase
                if user_emotion.get('success'):
                    self.current_emotion = user_emotion.get('emotion', 'neutral')
                    
                    # Almacenar información emocional en response_data
                    response_data['user_emotion'] = {
                        'emotion': user_emotion.get('emotion'),
                        'name': user_emotion.get('emotion_name'),
                        'color': user_emotion.get('color'),
                        'confidence': user_emotion.get('confidence')
                    }
                
                if aria_emotion.get('success'):
                    response_data['aria_emotion'] = {
                        'emotion': aria_emotion.get('emotion'),
                        'name': aria_emotion.get('emotion_name'),
                        'color': aria_emotion.get('color'),
                        'confidence': aria_emotion.get('confidence')
                    }
                
                print(f"🎭 Emociones detectadas - Usuario: {user_emotion.get('emotion_name', 'N/A')}, ARIA: {aria_emotion.get('emotion_name', 'N/A')}")
                
            except Exception as e:
                print(f"⚠️ Error en detección emocional Supabase: {e}")
                self._update_emotions_fallback(user_message, response_data)
                
        elif self.emotion_system_type == "legacy":
            try:
                # Usar sistema emocional legacy
                user_emotion = detect_user_emotion(user_message)
                aria_emotion = detect_aria_emotion(response_data.get('response', ''))
                
                if user_emotion.get('success'):
                    self.current_emotion = user_emotion.get('emotion', 'neutral')
                    response_data['user_emotion'] = user_emotion
                
                if aria_emotion.get('success'):
                    response_data['aria_emotion'] = aria_emotion
                    
            except Exception as e:
                print(f"⚠️ Error en detección emocional legacy: {e}")
                self._update_emotions_fallback(user_message, response_data)
        else:
            # Sistema básico
            self._update_emotions_fallback(user_message, response_data)
    
    def _update_emotions_fallback(self, user_message: str, response_data: Dict):
        """Sistema emocional básico como fallback"""
        # Detectar emociones en el mensaje del usuario
        user_sentiment = self._analyze_sentiment(user_message)
        
        # Ajustar emociones según la interacción
        if response_data.get('confidence', 0) > 0.8:
            self.emotions['confidence'] = min(self.emotions['confidence'] + 0.1, 1.0)
            self.emotions['happiness'] = min(self.emotions['happiness'] + 0.05, 1.0)
            self.current_emotion = 'confident'
        elif response_data.get('learning_opportunity'):
            self.emotions['curiosity'] = min(self.emotions['curiosity'] + 0.15, 1.0)
            self.current_emotion = 'curious'
        
        # Responder a emociones del usuario
        if user_sentiment == 'positive':
            self.emotions['happiness'] = min(self.emotions['happiness'] + 0.1, 1.0)
            self.emotions['empathy'] = min(self.emotions['empathy'] + 0.05, 1.0)
        elif user_sentiment == 'negative':
            self.emotions['empathy'] = min(self.emotions['empathy'] + 0.2, 1.0)
            self.current_emotion = 'empathetic'
    
    def _analyze_sentiment(self, text: str) -> str:
        """Análisis básico de sentimiento"""
        positive_words = ['bueno', 'genial', 'excelente', 'perfecto', 'increíble', 'fantástico', 'good', 'great', 'excellent', 'perfect', 'amazing']
        negative_words = ['malo', 'terrible', 'horrible', 'difícil', 'problema', 'error', 'bad', 'terrible', 'horrible', 'difficult', 'problem', 'error']
        
        text_lower = text.lower()
        positive_count = sum(1 for word in positive_words if word in text_lower)
        negative_count = sum(1 for word in negative_words if word in text_lower)
        
        if positive_count > negative_count:
            return 'positive'
        elif negative_count > positive_count:
            return 'negative'
        else:
            return 'neutral'
    
    def _store_conversation(self, user_message: str, response_data: Dict):
        """Almacenar conversación en Super Base"""
        try:
            if not self.superbase:
                return
            
            conversation_data = {
                'user_message': user_message,
                'aria_response': response_data['response'],
                'emotion_state': self.current_emotion,
                'confidence': response_data.get('confidence', 0.5),
                'apis_used': response_data.get('apis_used', []),
                'knowledge_accessed': response_data.get('concepts_used', []),
                'session_id': self.session_id,
                'language': response_data.get('language', 'es'),
                'response_time': response_data.get('response_time', 0)
            }
            
            self.superbase.store_conversation(**conversation_data)
            
        except Exception as e:
            logger.error(f"Error almacenando conversación: {e}")
    
    def _learn_from_conversation(self, user_message: str, response_data: Dict):
        """Aprender de la conversación actual y almacenar en embeddings"""
        try:
            # Extraer conceptos clave del mensaje del usuario
            key_concepts = self._extract_key_concepts(user_message)
            
            # Almacenar conversación completa en embeddings si está disponible
            if self.embeddings_system:
                try:
                    # Almacenar mensaje del usuario
                    self.embeddings_system.agregar_texto(
                        texto=user_message,
                        categoria='conversation',
                        subcategoria='user_message',
                        fuente='chat_interaction',
                        metadatos={
                            'session_id': self.session_id,
                            'conversation_count': self.conversation_count,
                            'emotion': self.current_emotion,
                            'timestamp': datetime.now(timezone.utc).isoformat()
                        }
                    )
                    
                    # Almacenar respuesta de ARIA
                    self.embeddings_system.agregar_texto(
                        texto=response_data.get('response', ''),
                        categoria='conversation',
                        subcategoria='aria_response',
                        fuente='aria_generation',
                        metadatos={
                            'session_id': self.session_id,
                            'confidence': response_data.get('confidence', 0.5),
                            'knowledge_used': len(response_data.get('knowledge_sources', 0)),
                            'apis_used': response_data.get('apis_used', [])
                        }
                    )
                    
                    logger.info("💾 Conversación almacenada en embeddings")
                    
                except Exception as e:
                    logger.error(f"Error almacenando conversación en embeddings: {e}")
            
            # Almacenar conceptos nuevos como conocimiento estructurado (EXCLUYENDO SALUDOS BÁSICOS)
            saludos_basicos = {'hola', 'hello', 'hi', 'hey', 'buenos', 'días', 'tardes', 'noches', 'buen', 'día', 'gracias', 'thanks', 'bye', 'adiós', 'chao'}
            
            for concept in key_concepts:
                # FILTRAR saludos básicos para evitar almacenarlos como "conceptos técnicos"
                if concept.lower() in saludos_basicos:
                    logger.info(f"🚫 Saludo básico '{concept}' no almacenado como concepto técnico")
                    continue
                    
                if concept not in self.knowledge_cache:
                    
                    # Almacenar en cache local
                    self.knowledge_cache[concept] = {
                        'concept': concept,
                        'description': f"Concepto mencionado en conversación: {user_message[:100]}",
                        'category': 'conversational',
                        'source': 'user_interaction',
                        'confidence': 0.4
                    }
                    
                    # Almacenar en SuperBase tradicional
                    if self.superbase:
                        try:
                            self.superbase.store_knowledge(
                                concept=concept,
                                description=f"Concepto mencionado en conversación: {user_message[:100]}",
                                category='conversational',
                                source='user_interaction',
                                confidence=0.4
                            )
                        except Exception as e:
                            logger.error(f"Error almacenando en SuperBase: {e}")
                    
                    # Almacenar en embeddings como conocimiento estructurado
                    if self.embeddings_system:
                        try:
                            descripcion_extendida = f"Concepto '{concept}' extraído de la conversación: '{user_message}'. Contexto: Mencionado durante interacción del usuario en sesión {self.session_id[:8]}"
                            
                            self.embeddings_system.agregar_conocimiento(
                                concepto=concept,
                                descripcion=descripcion_extendida,
                                categoria='conversational_learning',
                                tags=['user_mentioned', 'auto_extracted', self.current_emotion],
                                confianza=0.4,
                                ejemplos=[user_message[:100]],
                                relaciones={
                                    'session_id': self.session_id,
                                    'conversation_context': user_message[:50],
                                    'related_concepts': key_concepts[:3]
                                }
                            )
                            
                            logger.info(f"🧠 Concepto '{concept}' agregado a embeddings")
                            
                        except Exception as e:
                            logger.error(f"Error agregando concepto a embeddings: {e}")
            
            logger.info(f"📚 Aprendizaje completado: {len(key_concepts)} conceptos procesados")
            
        except Exception as e:
            logger.error(f"Error en aprendizaje: {e}")
    
    def _extract_key_concepts(self, text: str) -> List[str]:
        """Extraer conceptos clave del texto"""
        # Palabras a ignorar
        stop_words = {'el', 'la', 'de', 'que', 'y', 'en', 'un', 'es', 'se', 'no', 'te', 'lo', 'le', 'da', 'su', 'por', 'son', 'con', 'para', 'como', 'pero', 'muy', 'todo', 'esta', 'fue', 'han', 'hasta'}
        
        # Limpiar texto y extraer palabras importantes
        words = re.findall(r'\b[a-záéíóúñ]{3,}\b', text.lower())
        concepts = [word for word in words if word not in stop_words and len(word) > 3]
        
        # Buscar frases de 2-3 palabras
        phrases = []
        words_clean = text.lower().split()
        for i in range(len(words_clean) - 1):
            if len(words_clean[i]) > 3 and len(words_clean[i+1]) > 3:
                phrase = f"{words_clean[i]} {words_clean[i+1]}"
                if not any(stop in phrase for stop in stop_words):
                    phrases.append(phrase)
        
        return list(set(concepts + phrases))[:5]  # Top 5 únicos
    
    def _get_suggested_topics(self, user_message: str) -> List[str]:
        """Obtener temas sugeridos relacionados"""
        suggestions = []
        
        try:
            # Buscar temas relacionados en el conocimiento
            if self.superbase:
                concepts = self._extract_key_concepts(user_message)
                for concept in concepts[:2]:  # Top 2
                    related = self.superbase.get_knowledge(concept=concept)
                    for item in related[:2]:
                        if item.get('concept') not in suggestions:
                            suggestions.append(item.get('concept', ''))
            
            # Agregar sugerencias generales si no hay suficientes
            general_suggestions = [
                "inteligencia artificial",
                "machine learning", 
                "programación",
                "ciencia de datos",
                "tecnología"
            ]
            
            for suggestion in general_suggestions:
                if len(suggestions) < 5 and suggestion not in suggestions:
                    suggestions.append(suggestion)
                    
        except Exception as e:
            logger.error(f"Error generando sugerencias: {e}")
        
        return suggestions[:3]  # Top 3
    
    def _create_error_response(self, error_msg: str) -> Dict[str, Any]:
        """Crear respuesta de error amigable"""
        return {
            'response': f"Disculpa, he tenido un pequeño problema procesando tu mensaje. 🤖💭 ¿Podrías intentar reformularlo?",
            'emotion': 'apologetic',
            'confidence': 0.2,
            'error': True,
            'error_details': error_msg if app.debug else None,
            'suggested_topics': ['inteligencia artificial', 'ayuda', 'información general']
        }
    
    def get_system_status(self) -> Dict[str, Any]:
        """Obtener estado del sistema"""
        uptime = (datetime.now(timezone.utc) - self.start_time).total_seconds()
        
        status = {
            'status': 'operational',
            'session_id': self.session_id[:8],
            'uptime_seconds': round(uptime, 2),
            'conversations_count': self.conversation_count,
            'current_emotion': self.current_emotion,
            'emotions': self.emotions,
            'superbase_connected': self.superbase is not None and getattr(self.superbase, 'connected', False),
            'knowledge_cache_size': len(self.knowledge_cache),
            'systems': {
                'superbase': SUPERBASE_AVAILABLE,
                'learning_system': LEARNING_SYSTEM_AVAILABLE,
                'spanish_apis': SPANISH_APIS_AVAILABLE
            }
        }
        
        # Agregar estadísticas de Super Base si está disponible
        if self.superbase:
            try:
                db_stats = self.superbase.get_database_stats()
                status['database_stats'] = db_stats
            except Exception as e:
                status['database_error'] = str(e)
        
        return status


# Inicializar servidor
aria_server = ARIASuperServer()


# ==================== RUTAS DE LA API ====================

@app.route('/')
def home():
    """Página principal con interfaz web"""
    return '''
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🤖 ARIA - Asistente IA Personal</title>
    <style>
        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            flex-direction: column;
        }
        
        .header {
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            padding: 1rem;
            text-align: center;
            color: white;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
        }
        
        .header h1 {
            font-size: 2.5rem;
            margin-bottom: 0.5rem;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
        }
        
        .header p {
            font-size: 1.1rem;
            opacity: 0.9;
        }
        
        .container {
            flex: 1;
            display: flex;
            max-width: 1200px;
            margin: 2rem auto;
            padding: 0 1rem;
            gap: 2rem;
        }
        
        .chat-panel {
            flex: 2;
            background: rgba(255, 255, 255, 0.95);
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
            display: flex;
            flex-direction: column;
            min-height: 600px;
        }
        
        .controls-panel {
            flex: 1;
            background: rgba(255, 255, 255, 0.95);
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
            padding: 2rem;
        }
        
        .chat-messages {
            flex: 1;
            padding: 2rem;
            overflow-y: auto;
            border-bottom: 1px solid #eee;
        }
        
        .chat-input-area {
            padding: 1.5rem;
            display: flex;
            gap: 1rem;
        }
        
        .chat-input {
            flex: 1;
            padding: 1rem;
            border: 2px solid #ddd;
            border-radius: 25px;
            font-size: 1rem;
            outline: none;
            transition: border-color 0.3s ease;
        }
        
        .chat-input:focus {
            border-color: #667eea;
        }
        
        .send-btn {
            padding: 1rem 2rem;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 25px;
            cursor: pointer;
            font-size: 1rem;
            font-weight: bold;
            transition: all 0.3s ease;
        }
        
        .send-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
        }
        
        .control-btn {
            width: 100%;
            padding: 1rem;
            margin-bottom: 1rem;
            border: none;
            border-radius: 10px;
            font-size: 1rem;
            font-weight: bold;
            cursor: pointer;
            transition: all 0.3s ease;
            text-decoration: none;
            display: inline-block;
            text-align: center;
        }
        
        .desktop-btn {
            background: linear-gradient(135deg, #ff6b6b 0%, #ee5a52 100%);
            color: white;
        }
        
        .status-btn {
            background: linear-gradient(135deg, #4ecdc4 0%, #44a08d 100%);
            color: white;
        }
        
        .knowledge-btn {
            background: linear-gradient(135deg, #ffeaa7 0%, #fdcb6e 100%);
            color: #2d3436;
        }
        
        .control-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
        }
        
        .message {
            margin-bottom: 1rem;
            padding: 1rem;
            border-radius: 10px;
            max-width: 80%;
        }
        
        .user-message {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            margin-left: auto;
        }
        
        .aria-message {
            background: #f8f9fa;
            color: #2d3436;
            border-left: 4px solid #667eea;
        }
        
        .status-info {
            background: rgba(76, 175, 80, 0.1);
            border: 1px solid #4caf50;
            padding: 1rem;
            border-radius: 10px;
            margin-bottom: 1rem;
        }
        
        .status-info h3 {
            color: #4caf50;
            margin-bottom: 0.5rem;
        }
        
        @media (max-width: 768px) {
            .container {
                flex-direction: column;
                margin: 1rem;
            }
            
            .header h1 {
                font-size: 2rem;
            }
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>🤖 ARIA</h1>
        <p>Asistente de IA Personal con Super Base</p>
    </div>
    
    <div class="container">
        <div class="chat-panel">
            <div class="chat-messages" id="chatMessages">
                <div class="message aria-message">
                    <strong>🤖 ARIA:</strong> ¡Hola! Soy ARIA, tu asistente de IA personal. ¿En qué puedo ayudarte hoy?
                </div>
            </div>
            <div class="chat-input-area">
                <input type="text" class="chat-input" id="chatInput" placeholder="Escribe tu mensaje aquí..." />
                <button class="send-btn" onclick="sendMessage()">Enviar</button>
            </div>
        </div>
        
        <div class="controls-panel">
            <h3 style="margin-bottom: 1.5rem; color: #2d3436;">🎛️ Panel de Control</h3>
            
            <button class="control-btn desktop-btn" onclick="openRemoteDesktop()">
                🖥️ Escritorio Remoto
            </button>
            
            <button class="control-btn status-btn" onclick="checkStatus()">
                📊 Estado del Sistema
            </button>
            
            <button class="control-btn knowledge-btn" onclick="viewKnowledge()">
                📚 Base de Conocimiento
            </button>
            
            <button class="control-btn" style="background: linear-gradient(135deg, #e17055 0%, #d63031 100%); color: white;" onclick="testSpanishAPIs()">
                🇪🇸 Probar APIs Españolas
            </button>
            
            <div class="status-info">
                <h3>📡 Estado Actual</h3>
                <p id="serverStatus">🟢 Servidor activo</p>
                <p id="connectionStatus">🟢 Conectado a Supabase</p>
            </div>
        </div>
    </div>
    
    <script>
        // Variables globales
        let chatMessages = document.getElementById('chatMessages');
        let chatInput = document.getElementById('chatInput');
        
        // Función para enviar mensajes
        async function sendMessage() {
            const message = chatInput.value.trim();
            if (!message) return;
            
            // Mostrar mensaje del usuario
            addMessage(message, 'user');
            chatInput.value = '';
            
            // Mostrar indicador de carga
            addMessage('⏳ Procesando...', 'aria', true);
            
            try {
                const response = await fetch('/chat', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ message: message })
                });
                
                const data = await response.json();
                
                // Quitar indicador de carga
                removeLoadingMessage();
                
                if (data.response) {
                    addMessage(data.response, 'aria');
                } else {
                    addMessage('❌ Error al procesar el mensaje', 'aria');
                }
            } catch (error) {
                removeLoadingMessage();
                addMessage('❌ Error de conexión', 'aria');
                console.error('Error:', error);
            }
        }
        
        // Función para agregar mensajes
        function addMessage(text, sender, isLoading = false) {
            const messageDiv = document.createElement('div');
            messageDiv.className = `message ${sender}-message`;
            if (isLoading) messageDiv.id = 'loadingMessage';
            
            const icon = sender === 'user' ? '👤' : '🤖 ARIA:';
            messageDiv.innerHTML = `<strong>${icon}</strong> ${text}`;
            
            chatMessages.appendChild(messageDiv);
            chatMessages.scrollTop = chatMessages.scrollHeight;
        }
        
        // Función para quitar mensaje de carga
        function removeLoadingMessage() {
            const loadingMsg = document.getElementById('loadingMessage');
            if (loadingMsg) loadingMsg.remove();
        }
        
        // Función para abrir escritorio remoto
        function openRemoteDesktop() {
            const hostname = window.location.hostname;
            const rdpUrl = `ms-rd:full address:s:${hostname}:3389&username:s:&audiomode:i:0&disable wallpaper:i:0`;
            
            // Intentar abrir RDP directamente
            try {
                window.location.href = rdpUrl;
            } catch (error) {
                // Fallback: mostrar instrucciones
                addMessage(`🖥️ Para conectar por escritorio remoto:
                
📍 Dirección: ${hostname}:3389
🔑 Usuario: [tu usuario]
🗝️ Contraseña: [tu contraseña]

💡 También puedes usar:
• Escritorio remoto de Windows (mstsc)
• TeamViewer
• AnyDesk`, 'aria');
            }
        }
        
        // Función para verificar estado
        async function checkStatus() {
            try {
                const response = await fetch('/status');
                const data = await response.json();
                
                let statusText = '📊 Estado del Sistema:\\n\\n';
                statusText += `🔌 Super Base: ${data.superbase_connected ? '✅ Conectado' : '❌ Desconectado'}\\n`;
                statusText += `🧠 Sistema de Aprendizaje: ${data.systems?.learning_system ? '✅ Activo' : '❌ Inactivo'}\\n`;
                statusText += `🌐 APIs Españolas: ${data.systems?.spanish_apis ? '✅ Activas' : '❌ Inactivas'}\\n`;
                statusText += `💬 Conversaciones: ${data.conversations_count || 0}\\n`;
                statusText += `⏱️ Tiempo activo: ${Math.round(data.uptime_seconds || 0)} segundos`;
                
                addMessage(statusText, 'aria');
            } catch (error) {
                addMessage('❌ Error al obtener el estado del sistema', 'aria');
            }
        }
        
        // Función para ver conocimiento
        async function viewKnowledge() {
            try {
                const response = await fetch('/knowledge?limit=5');
                const data = await response.json();
                
                if (data.success && data.knowledge && data.knowledge.length > 0) {
                    let knowledgeText = '📚 Base de Conocimiento (últimas 5 entradas):\\n\\n';
                    data.knowledge.forEach((item, index) => {
                        // Usar concept o concepto según lo que esté disponible
                        const concept = item.concept || item.concepto || 'Sin título';
                        const description = item.description || item.descripcion || 'Sin descripción';
                        
                        knowledgeText += `${index + 1}. ${concept}\\n`;
                        knowledgeText += `   📝 ${description.substring(0, 100)}...\\n\\n`;
                    });
                    knowledgeText += `💡 Total de entradas: ${data.total}`;
                    addMessage(knowledgeText, 'aria');
                } else if (data.success) {
                    addMessage('📚 No hay conocimiento almacenado aún', 'aria');
                } else {
                    addMessage(`❌ Error: ${data.message || 'No se pudo obtener el conocimiento'}`, 'aria');
                }
            } catch (error) {
                addMessage('❌ Error al obtener el conocimiento', 'aria');
                console.error('Error en viewKnowledge:', error);
            }
        }
        
        // Función para probar APIs españolas
        async function testSpanishAPIs() {
            const testQuery = prompt('¿Qué quieres buscar con las APIs españolas?', 'Madrid España');
            if (!testQuery) return;
            
            addMessage(`🇪🇸 Probando APIs españolas con: "${testQuery}"...`, 'aria');
            
            try {
                const response = await fetch(`/spanish-apis-test?q=${encodeURIComponent(testQuery)}`);
                const data = await response.json();
                
                if (data.success) {
                    let resultText = `🇪🇸 Resultados de APIs Españolas para "${testQuery}":
                    
📊 **Estado de APIs:**`;
                    
                    for (const [apiName, status] of Object.entries(data.api_status.apis)) {
                        const icon = status.enabled ? '✅' : '❌';
                        resultText += `
${icon} ${apiName}: ${status.description}`;
                    }
                    
                    resultText += `

📄 **Resumen:**
${data.results.summary}

🔍 **Fuentes consultadas:** ${data.results.sources.length}`;
                    
                    addMessage(resultText, 'aria');
                } else {
                    addMessage(`❌ Error: ${data.message || 'APIs españolas no disponibles'}`, 'aria');
                }
            } catch (error) {
                addMessage('❌ Error al probar APIs españolas', 'aria');
                console.error('Error:', error);
            }
        }
        
        // Event listener para Enter
        chatInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                sendMessage();
            }
        });
        
        // Actualizar estado cada 30 segundos
        setInterval(async () => {
            try {
                const response = await fetch('/status');
                const data = await response.json();
                
                document.getElementById('serverStatus').textContent = 
                    data.superbase_connected ? '🟢 Servidor activo' : '🟡 Servidor limitado';
                document.getElementById('connectionStatus').textContent = 
                    data.superbase_connected ? '🟢 Conectado a Supabase' : '🔴 Sin conexión DB';
            } catch (error) {
                document.getElementById('serverStatus').textContent = '🔴 Error de conexión';
            }
        }, 30000);
    </script>
</body>
</html>
    '''

@app.route('/api')
def api_info():
    """Información de la API en formato JSON"""
    return jsonify({
        'message': '🤖 ARIA Super Server está funcionando',
        'version': '2.0.0',
        'features': ['Super Base', 'Multilingual APIs', 'Advanced Learning'],
        'endpoints': ['/chat', '/status', '/knowledge', '/api-relations']
    })

@app.route('/chat', methods=['POST'])
def chat():
    """Endpoint principal de chat"""
    try:
        data = request.get_json()
        if not data or 'message' not in data:
            return jsonify({'error': 'Mensaje requerido'}), 400
        
        user_message = data['message'].strip()
        if not user_message:
            return jsonify({'error': 'Mensaje vacío'}), 400
        
        context = data.get('context', {})
        response = aria_server.process_message(user_message, context)
        
        return jsonify(response)
        
    except Exception as e:
        logger.error(f"Error en /chat: {e}")
        return jsonify({'error': 'Error interno del servidor'}), 500

@app.route('/status')
def status():
    """Estado del sistema"""
    return jsonify(aria_server.get_system_status())

@app.route('/spanish-apis-test')
def spanish_apis_test():
    """Probar APIs españolas"""
    try:
        if not SPANISH_APIS_AVAILABLE:
            return jsonify({
                'success': False,
                'message': 'APIs españolas no disponibles'
            })
        
        query = request.args.get('q', 'Madrid')
        results = aria_spanish_apis.search_comprehensive(query, max_results=3)
        
        return jsonify({
            'success': True,
            'query': query,
            'results': results,
            'api_status': aria_spanish_apis.get_api_status()
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/knowledge')
def knowledge():
    """Obtener conocimiento almacenado"""
    try:
        category = request.args.get('category')
        concept = request.args.get('concept')
        limit = int(request.args.get('limit', 10))
        
        logger.info(f"Solicitud de conocimiento: concept={concept}, category={category}, limit={limit}")
        
        if aria_server.superbase:
            knowledge_data = aria_server.superbase.get_knowledge(concept, category)
            logger.info(f"Datos obtenidos de Supabase: {len(knowledge_data)} entradas")
            
            # Log de muestra de los primeros datos
            if knowledge_data:
                logger.info(f"Muestra de datos: {knowledge_data[0].keys() if knowledge_data else 'Sin datos'}")
            
            return jsonify({
                'success': True,
                'knowledge': knowledge_data[:limit],
                'total': len(knowledge_data)
            })
        else:
            logger.warning("Super Base no disponible, usando cache local")
            cache_data = list(aria_server.knowledge_cache.values())[:limit]
            return jsonify({
                'success': True,
                'message': 'Usando cache local (Super Base no disponible)',
                'knowledge': cache_data,
                'total': len(cache_data)
            })
            
    except Exception as e:
        logger.error(f"Error en /knowledge: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/knowledge', methods=['POST'])
def add_knowledge():
    """Agregar nuevo conocimiento"""
    try:
        data = request.get_json()
        required_fields = ['concept', 'description']
        
        if not all(field in data for field in required_fields):
            return jsonify({'error': 'Campos requeridos: concept, description'}), 400
        
        if aria_server.superbase:
            success = aria_server.superbase.store_knowledge(
                concept=data['concept'],
                description=data['description'],
                category=data.get('category', 'user_added'),
                source='api_endpoint',
                confidence=data.get('confidence', 0.7)
            )
            
            if success:
                # Actualizar cache
                aria_server.knowledge_cache[data['concept']] = data
                return jsonify({'success': True, 'message': 'Conocimiento agregado'})
            else:
                return jsonify({'success': False, 'message': 'Error almacenando'}), 500
        else:
            # Almacenar en cache local
            aria_server.knowledge_cache[data['concept']] = data
            return jsonify({'success': True, 'message': 'Conocimiento agregado localmente'})
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api-relations')
def api_relations():
    """Obtener relaciones de APIs"""
    try:
        api_type = request.args.get('type')
        
        if aria_server.superbase:
            apis = aria_server.superbase.get_api_relations(api_type)
            return jsonify({
                'success': True,
                'apis': apis,
                'total': len(apis)
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Super Base no disponible',
                'apis': []
            })
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/conversations')
def conversations():
    """Obtener historial de conversaciones"""
    try:
        session_id = request.args.get('session_id')
        limit = int(request.args.get('limit', 10))
        
        if aria_server.superbase:
            history = aria_server.superbase.get_conversation_history(session_id, limit)
            return jsonify({
                'success': True,
                'conversations': history,
                'session_id': session_id or 'all'
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Super Base no disponible',
                'conversations': []
            })
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/emotions/stats')
def emotion_stats():
    """Obtener estadísticas del sistema emocional"""
    try:
        if aria_server.emotion_system_type == "supabase":
            stats = get_emotion_stats_supabase()
            return jsonify({
                'success': True,
                'emotion_system': 'supabase',
                'stats': stats,
                'current_emotion': aria_server.current_emotion,
                'emotion_values': aria_server.emotions
            })
        else:
            return jsonify({
                'success': True,
                'emotion_system': aria_server.emotion_system_type,
                'current_emotion': aria_server.current_emotion,
                'emotion_values': aria_server.emotions,
                'stats': {
                    'system_type': aria_server.emotion_system_type,
                    'fallback_active': True
                }
            })
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/emotions/available')
def available_emotions():
    """Obtener emociones disponibles"""
    try:
        if aria_server.emotion_system_type == "supabase" and aria_server.emotion_detector:
            emotions = aria_server.emotion_detector.get_available_emotions()
            return jsonify({
                'success': True,
                'emotions': emotions,
                'total': len(emotions),
                'source': 'supabase'
            })
        else:
            return jsonify({
                'success': True,
                'emotions': [
                    {'key': 'neutral', 'name': 'Neutral', 'color': '#667eea'},
                    {'key': 'happy', 'name': 'Feliz', 'color': '#FFD700'},
                    {'key': 'curious', 'name': 'Curiosa', 'color': '#00CED1'},
                    {'key': 'learning', 'name': 'Aprendiendo', 'color': '#00FF7F'}
                ],
                'total': 4,
                'source': 'fallback'
            })
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500
        return jsonify({'error': str(e)}), 500

@app.route('/search')
def search():
    """Búsqueda avanzada en conocimiento"""
    try:
        query = request.args.get('q', '').strip()
        if not query:
            return jsonify({'error': 'Parámetro q requerido'}), 400
        
        if aria_server.superbase:
            results = aria_server.superbase.search_knowledge(query)
            return jsonify({
                'success': True,
                'query': query,
                'results': results,
                'total': len(results)
            })
        else:
            # Búsqueda en cache local
            results = []
            for concept, data in aria_server.knowledge_cache.items():
                if query.lower() in concept.lower() or query.lower() in data.get('description', '').lower():
                    results.append(data)
            
            return jsonify({
                'success': True,
                'query': query,
                'results': results,
                'total': len(results),
                'source': 'local_cache'
            })
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/embeddings/search')
def embeddings_search():
    """Búsqueda semántica usando embeddings"""
    try:
        query = request.args.get('q', '').strip()
        limite = int(request.args.get('limit', 5))
        categoria = request.args.get('category', None)
        umbral = float(request.args.get('threshold', 0.6))
        
        if not query:
            return jsonify({'error': 'Parámetro q requerido'}), 400
        
        if not aria_server.embeddings_system:
            return jsonify({'error': 'Sistema de embeddings no disponible'}), 503
        
        # Buscar similares
        resultados = aria_server.embeddings_system.buscar_similares(
            consulta=query,
            limite=limite,
            categoria=categoria,
            umbral_similitud=umbral
        )
        
        return jsonify({
            'success': True,
            'query': query,
            'results': resultados,
            'total': len(resultados),
            'source': 'embeddings_supabase',
            'parameters': {
                'limit': limite,
                'category': categoria,
                'threshold': umbral
            }
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/embeddings/knowledge')
def embeddings_knowledge_search():
    """Búsqueda de conocimiento estructurado con embeddings"""
    try:
        query = request.args.get('q', '').strip()
        limite = int(request.args.get('limit', 3))
        
        if not query:
            return jsonify({'error': 'Parámetro q requerido'}), 400
        
        if not aria_server.embeddings_system:
            return jsonify({'error': 'Sistema de embeddings no disponible'}), 503
        
        # Buscar conocimiento
        resultados = aria_server.embeddings_system.buscar_conocimiento(query, limite)
        
        return jsonify({
            'success': True,
            'query': query,
            'knowledge': resultados,
            'total': len(resultados),
            'source': 'knowledge_vectors'
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/embeddings/stats')
def embeddings_stats():
    """Obtener estadísticas del sistema de embeddings"""
    try:
        if not aria_server.embeddings_system:
            return jsonify({'error': 'Sistema de embeddings no disponible'}), 503
        
        stats = aria_server.embeddings_system.obtener_estadisticas()
        
        return jsonify({
            'success': True,
            'stats': stats,
            'embeddings_system': 'supabase',
            'model': 'all-MiniLM-L6-v2',
            'dimensions': 384
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/embeddings/add', methods=['POST'])
def embeddings_add():
    """Agregar texto con embedding"""
    try:
        data = request.get_json()
        
        if not data or 'texto' not in data:
            return jsonify({'error': 'Campo texto requerido'}), 400
        
        if not aria_server.embeddings_system:
            return jsonify({'error': 'Sistema de embeddings no disponible'}), 503
        
        # Parámetros opcionales
        texto = data['texto']
        categoria = data.get('categoria', 'manual')
        subcategoria = data.get('subcategoria', None)
        fuente = data.get('fuente', 'api_manual')
        idioma = data.get('idioma', 'es')
        metadatos = data.get('metadatos', {})
        
        # Agregar timestamp
        metadatos['added_via'] = 'api'
        metadatos['timestamp'] = datetime.now(timezone.utc).isoformat()
        
        # Agregar el texto
        success = aria_server.embeddings_system.agregar_texto(
            texto=texto,
            categoria=categoria,
            subcategoria=subcategoria,
            fuente=fuente,
            idioma=idioma,
            metadatos=metadatos
        )
        
        if success:
            return jsonify({
                'success': True,
                'message': 'Texto agregado exitosamente',
                'data': {
                    'texto': texto[:100] + '...' if len(texto) > 100 else texto,
                    'categoria': categoria,
                    'subcategoria': subcategoria
                }
            })
        else:
            return jsonify({'error': 'Error agregando texto'}), 500
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/embeddings/knowledge', methods=['POST'])
def embeddings_add_knowledge():
    """Agregar conocimiento estructurado con embedding"""
    try:
        data = request.get_json()
        
        if not data or 'concepto' not in data or 'descripcion' not in data:
            return jsonify({'error': 'Campos concepto y descripcion requeridos'}), 400
        
        if not aria_server.embeddings_system:
            return jsonify({'error': 'Sistema de embeddings no disponible'}), 503
        
        # Parámetros
        concepto = data['concepto']
        descripcion = data['descripcion']
        categoria = data.get('categoria', 'manual_knowledge')
        tags = data.get('tags', [])
        confianza = float(data.get('confianza', 0.8))
        ejemplos = data.get('ejemplos', [])
        relaciones = data.get('relaciones', {})
        
        # Agregar metadatos de API
        relaciones['added_via'] = 'api'
        relaciones['timestamp'] = datetime.now(timezone.utc).isoformat()
        
        # Agregar el conocimiento
        success = aria_server.embeddings_system.agregar_conocimiento(
            concepto=concepto,
            descripcion=descripcion,
            categoria=categoria,
            tags=tags,
            confianza=confianza,
            ejemplos=ejemplos,
            relaciones=relaciones
        )
        
        if success:
            return jsonify({
                'success': True,
                'message': 'Conocimiento agregado exitosamente',
                'data': {
                    'concepto': concepto,
                    'categoria': categoria,
                    'confianza': confianza,
                    'tags': tags
                }
            })
        else:
            return jsonify({'error': 'Error agregando conocimiento'}), 500
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Servir archivos estáticos del frontend React
@app.route('/static/<path:filename>')
def serve_static(filename):
    """Servir archivos estáticos del frontend"""
    return send_from_directory('../frontend/build/static', filename)

# Ruta catch-all para el frontend React
@app.route('/<path:path>')
def serve_frontend(path):
    """Servir frontend React para rutas no API"""
    try:
        return send_from_directory('../frontend/build', path)
    except:
        return send_from_directory('../frontend/build', 'index.html')


if __name__ == '__main__':
    print("\n" + "="*60)
    print("🚀 ARIA SUPER SERVER - Iniciando...")
    print("="*60)
    
    # Mostrar configuración
    print(f"🗄️ Super Base: {'✅ Conectado' if SUPERBASE_AVAILABLE else '❌ No disponible'}")
    print(f"🧠 Sistema de Aprendizaje: {'✅ Activo' if LEARNING_SYSTEM_AVAILABLE else '❌ No disponible'}")
    print(f"🌐 APIs Españolas: {'✅ Activas' if SPANISH_APIS_AVAILABLE else '❌ No disponibles'}")
    print(f"🎭 Sesión ID: {aria_server.session_id[:8]}")
    
    if aria_server.superbase and aria_server.superbase.connected:
        stats = aria_server.superbase.get_database_stats()
        print(f"📊 Base de Datos:")
        print(f"   📚 Conocimiento: {stats.get('knowledge_count', 0)} entradas")
        print(f"   🔌 APIs: {stats.get('api_relations_count', 0)} relaciones")
        print(f"   💬 Conversaciones: {stats.get('conversations_count', 0)} registros")
    
    print("\n🌐 Endpoints disponibles:")
    print("   GET  / - Información del servidor")
    print("   POST /chat - Chat con ARIA")
    print("   GET  /status - Estado del sistema")
    print("   GET  /knowledge - Consultar conocimiento")
    print("   POST /knowledge - Agregar conocimiento")
    print("   GET  /api-relations - Ver APIs conectadas")
    print("   GET  /conversations - Historial")
    print("   GET  /search?q=texto - Búsqueda avanzada")
    
    print("\n🚀 Servidor iniciado en http://localhost:8000")
    print("="*60)
    
    # Iniciar servidor
    try:
        app.run(
            host='0.0.0.0',
            port=8000,
            debug=False,  # Desactivar debug para evitar problemas
            threaded=True,
            use_reloader=False  # Evitar recarga automática que puede causar colgones
        )
    except Exception as e:
        print(f"\n❌ Error al iniciar el servidor: {e}")
        print("   El servidor puede estar ya ejecutándose en el puerto 8000")
        print("   Intenta cerrar otros procesos o usar un puerto diferente")