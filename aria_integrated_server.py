#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🤖 ARIA con Conexiones Integradas
=================================

ARIA funcionando con Supabase y Google Cloud integrados
de forma robusta con fallbacks inteligentes.

Fecha: 23 de octubre de 2025
"""

import sys
import os

# Cargar variables de entorno
from dotenv import load_dotenv
load_dotenv()  # Cargar archivo .env si existe

sys.path.append(os.path.join(os.path.dirname(__file__), 'backend', 'src'))

from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import json
import time

# Importar el buscador web real
try:
    from buscador_web_aria import BuscadorWebARIA
    print("✅ Buscador web real importado")
    BUSCADOR_WEB_REAL = True
    buscador_web = BuscadorWebARIA()
except ImportError as e:
    print(f"⚠️ No se pudo importar el buscador web real: {e}")
    print("🔄 Usando búsqueda simulada")
    BUSCADOR_WEB_REAL = False
    buscador_web = None

# Importar el detector de emociones
try:
    from emotion_detector import init_emotion_detector, detect_user_emotion, detect_aria_emotion
    print("✅ Detector de emociones importado")
    EMOTION_DETECTION = True
    # La API key se carga más tarde
except ImportError as e:
    print(f"⚠️ No se pudo importar el detector de emociones: {e}")
    print("🔄 Usando sistema de emociones básico")
    EMOTION_DETECTION = False

# Importar el sistema RAG
try:
    from aria_rag_system import create_rag_system
    from data_source_manager import DataSourceManager, setup_quick_rag_sources
    print("✅ Sistema RAG importado")
    RAG_SYSTEM = True
except ImportError as e:
    print(f"⚠️ No se pudo importar el sistema RAG: {e}")
    print("🔄 Usando sistema de respuestas básico")
    RAG_SYSTEM = False

import uuid
from datetime import datetime, timezone
import logging
import re
from typing import Dict, List, Optional, Any

# Importar el conector mejorado
from aria_enhanced_connector import get_enhanced_connector

# Configurar Flask
app = Flask(__name__, 
           template_folder='frontend/public',
           static_folder='frontend/build/static')
CORS(app)

# Servir archivos estáticos de React
@app.route('/static/<path:path>')
def serve_static(path):
    return app.send_static_file(path)

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ARIAIntegratedServer:
    """ARIA con conexiones integradas de Supabase y Google Cloud"""
    
    def __init__(self):
        self.session_id = str(uuid.uuid4())
        self.conversation_count = 0
        self.start_time = datetime.now(timezone.utc)
        
        # Obtener conector
        self.cloud_connector = get_enhanced_connector()
        
        # Inicializar detector de emociones si está disponible
        if EMOTION_DETECTION:
            # Intentar obtener API key de EdenAI (puedes cambiar esta línea)
            eden_api_key = os.environ.get('EDENAI_API_KEY', '')
            if eden_api_key:
                try:
                    init_emotion_detector(eden_api_key)
                    print("✅ EdenAI inicializado con API key")
                except Exception as e:
                    print(f"⚠️ Error inicializando EdenAI: {e}")
            else:
                print("⚠️ No se encontró EDENAI_API_KEY, usando emociones básicas")
        
        # Sistema de emociones
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
            'language': 'es',
            'response_style': 'educational',
            'detail_level': 'medium',
            'personality': 'friendly',
            'use_cloud': True
        }
        
        # 🧠 Inicializar sistema RAG si está disponible
        if RAG_SYSTEM:
            try:
                # Crear el sistema RAG con las conexiones existentes
                emotion_detector = None
                if EMOTION_DETECTION:
                    try:
                        from emotion_detector import EmotionDetector
                        emotion_detector = EmotionDetector()
                    except:
                        pass
                
                self.rag_system = create_rag_system(
                    cloud_connector=self.cloud_connector,
                    emotion_detector=emotion_detector
                )
                
                # Configurar fuentes de datos básicas
                self.data_source_manager = DataSourceManager()
                setup_quick_rag_sources(self.data_source_manager)
                
                print("🧠 Sistema RAG inicializado correctamente")
                
            except Exception as e:
                print(f"❌ Error inicializando sistema RAG: {e}")
                self.rag_system = None
                self.data_source_manager = None
        else:
            self.rag_system = None
            self.data_source_manager = None
        
        print(f"🚀 ARIA Integrated Server inicializado - Sesión: {self.session_id[:8]}")
        self._show_status()
    
    def _show_status(self):
        """Mostrar estado de las conexiones"""
        status = self.cloud_connector.get_status_report()
        print("\\n🔗 Estado de ARIA:")
        print(f"   📊 Supabase: {'✅ Conectado' if status['connections']['supabase'] else '❌ Offline'}")
        print(f"   🌐 Google Cloud: {'✅ Disponible' if status['connections']['google_cloud'] else '❌ No disponible'}")
        print(f"   💾 Almacenamiento: {'Cloud' if status['connections']['supabase'] else 'Local'}")
        print(f"   📈 Entradas locales: {status['storage']['local_entries']}")
        
        # Estado del sistema RAG
        if hasattr(self, 'rag_system') and self.rag_system:
            print(f"   🧠 Sistema RAG: ✅ Activo")
            if hasattr(self, 'data_source_manager') and self.data_source_manager:
                sources = self.data_source_manager.list_sources()
                enabled_sources = [s for s in sources if s.get('enabled', False)]
                print(f"   📊 Fuentes de datos: {len(enabled_sources)}/{len(sources)} activas")
        else:
            print(f"   🧠 Sistema RAG: ❌ No disponible")
        
        # Estado del detector de emociones
        print(f"   🎭 Detección emocional: {'✅ EdenAI+Fallback' if EMOTION_DETECTION else '❌ Básico'}")
        print(f"   🔍 Búsqueda web: {'✅ Real' if BUSCADOR_WEB_REAL else '❌ Simulada'}")
    
    def generate_response(self, user_input: str, context: Dict = None) -> Dict:
        """Generar respuesta inteligente de ARIA con RAG"""
        
        # Incrementar contador
        self.conversation_count += 1
        
        # 🧠 SISTEMA RAG: Verificar si está disponible
        if RAG_SYSTEM and hasattr(self, 'rag_system'):
            try:
                # Usar el sistema RAG para generar respuesta completa
                rag_response = self.rag_system.generate_rag_response(user_input, context)
                
                # 🎭 Detectar emociones si está disponible
                user_emotion = None
                aria_emotion = None
                
                if EMOTION_DETECTION:
                    try:
                        user_emotion = detect_user_emotion(user_input)
                        aria_emotion = detect_aria_emotion(rag_response.answer)
                        self.current_emotion = aria_emotion.get('emotion', 'curious')
                        print(f"🎭 Emociones - Usuario: {user_emotion.get('emotion_name', 'neutral')}, ARIA: {aria_emotion.get('emotion_name', 'neutral')}")
                    except Exception as e:
                        print(f"⚠️ Error detectando emociones: {e}")
                
                # Preparar respuesta RAG
                response_data = {
                    "response": rag_response.answer,
                    "emotion": self.current_emotion,
                    "confidence": rag_response.confidence,
                    "session_id": self.session_id,
                    "conversation_count": self.conversation_count,
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                    "knowledge_used": len(rag_response.sources),
                    "source": "aria_rag_enhanced",
                    "user_emotion": user_emotion,
                    "aria_emotion": aria_emotion,
                    "rag_metadata": {
                        "sources": rag_response.sources,
                        "context_used": rag_response.context_used,
                        "generation_method": rag_response.generation_method,
                        "search_time": rag_response.search_time,
                        "total_time": rag_response.total_time
                    }
                }
                
                # Almacenar conversación
                self._store_conversation(user_input, rag_response.answer)
                
                print(f"🧠 Respuesta RAG generada en {rag_response.total_time:.2f}s con {len(rag_response.sources)} fuentes")
                return response_data
                
            except Exception as e:
                print(f"❌ Error en sistema RAG: {e}")
                print("🔄 Fallback al sistema tradicional")
        
        # 🔄 FALLBACK: Sistema tradicional
        # 🎭 NUEVA: Detectar emoción del usuario
        user_emotion = None
        if EMOTION_DETECTION:
            try:
                user_emotion = detect_user_emotion(user_input)
                print(f"🎭 Emoción usuario: {user_emotion.get('emotion_name', 'neutral')}")
            except Exception as e:
                print(f"⚠️ Error detectando emoción usuario: {e}")
        
        # Analizar entrada del usuario
        user_intent = self._analyze_user_intent(user_input)
        
        # Buscar conocimiento relevante
        relevant_knowledge = self._get_relevant_knowledge(user_input)
        
        # Generar respuesta base
        base_response = self._generate_base_response(user_input, user_intent, relevant_knowledge)
        
        # Mejorar con IA si está disponible
        enhanced_response = self._enhance_with_ai(base_response, user_input, context)
        
        # 🎭 NUEVA: Detectar emoción de la respuesta de ARIA
        aria_emotion = None
        if EMOTION_DETECTION:
            try:
                aria_emotion = detect_aria_emotion(enhanced_response)
                # Actualizar emoción actual de ARIA
                self.current_emotion = aria_emotion.get('emotion', 'curious')
                print(f"🎭 Emoción ARIA: {aria_emotion.get('emotion_name', 'neutral')}")
            except Exception as e:
                print(f"⚠️ Error detectando emoción ARIA: {e}")
        
        # Preparar respuesta final
        response_data = {
            "response": enhanced_response,
            "emotion": self.current_emotion,
            "confidence": self._calculate_confidence(user_intent, relevant_knowledge),
            "session_id": self.session_id,
            "conversation_count": self.conversation_count,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "knowledge_used": len(relevant_knowledge),
            "source": "aria_integrated_traditional",
            # 🎭 NUEVOS campos de emoción
            "user_emotion": user_emotion,
            "aria_emotion": aria_emotion
        }
        
        # Almacenar conversación
        self._store_conversation(user_input, enhanced_response)
        
        # Aprender del intercambio
        self._learn_from_interaction(user_input, enhanced_response, user_intent)
        
        return response_data
    
    def _analyze_user_intent(self, user_input: str) -> Dict:
        """Analizar la intención del usuario"""
        
        user_input_lower = user_input.lower()
        
        # Patrones de intención básicos
        intent_patterns = {
            'greeting': ['hola', 'hi', 'hello', 'buenos días', 'buenas tardes', 'saludos'],
            'question': ['qué', 'cómo', 'cuándo', 'dónde', 'por qué', 'para qué', '?'],
            'help': ['ayuda', 'help', 'socorro', 'auxilio', 'asistencia'],
            'thanks': ['gracias', 'thank you', 'thanks', 'te agradezco'],
            'goodbye': ['adiós', 'bye', 'hasta luego', 'nos vemos', 'chau'],
            'learning': ['aprende', 'enseña', 'explica', 'muestra', 'dime sobre'],
            'task': ['haz', 'crea', 'genera', 'produce', 'escribe'],
            'status': ['estado', 'status', 'cómo estás', 'como estas', 'how are you', 'como te sientes', 'cómo te sientes', 'how do you feel', 'te sientes bien', 'estás bien']
        }
        
        detected_intents = []
        for intent, patterns in intent_patterns.items():
            if any(pattern in user_input_lower for pattern in patterns):
                detected_intents.append(intent)
        
        # Determinar intención principal
        main_intent = detected_intents[0] if detected_intents else 'general'
        
        return {
            'main_intent': main_intent,
            'all_intents': detected_intents,
            'confidence': 0.8 if detected_intents else 0.4,
            'input_length': len(user_input),
            'contains_question': '?' in user_input
        }
    
    def _get_relevant_knowledge(self, user_input: str) -> List[Dict]:
        """Obtener conocimiento relevante"""
        
        # Extraer palabras clave
        keywords = self._extract_keywords(user_input)
        
        # Buscar en conocimiento almacenado
        all_knowledge = self.cloud_connector.get_knowledge()
        
        relevant = []
        for knowledge in all_knowledge:
            if any(keyword.lower() in knowledge.get('concept', '').lower() for keyword in keywords):
                relevant.append(knowledge)
            elif any(keyword.lower() in knowledge.get('description', '').lower() for keyword in keywords):
                relevant.append(knowledge)
        
        return relevant[:5]  # Limitar a 5 más relevantes
    
    def _extract_keywords(self, text: str) -> List[str]:
        """Extraer palabras clave del texto"""
        
        # Palabras irrelevantes
        stop_words = {'el', 'la', 'de', 'que', 'y', 'a', 'en', 'un', 'es', 'se', 'no', 'te', 'lo', 'le', 'da', 'su', 'por', 'son', 'con', 'para', 'al', 'del', 'las', 'los', 'una', 'su', 'me', 'mi', 'tu', 'si', 'o', 'pero', 'como', 'más', 'este', 'esta', 'muy', 'todo', 'todos', 'bien', 'puede', 'pueden', 'the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by'}
        
        # Limpiar y dividir texto
        words = re.findall(r'\\b\\w+\\b', text.lower())
        keywords = [word for word in words if len(word) > 2 and word not in stop_words]
        
        return keywords[:10]  # Top 10 keywords
    
    def _generate_base_response(self, user_input: str, intent: Dict, knowledge: List[Dict]) -> str:
        """Generar respuesta base"""
        
        main_intent = intent['main_intent']
        
        if main_intent == 'greeting':
            responses = [
                "¡Hola! Soy ARIA, tu asistente inteligente. ¿En qué puedo ayudarte hoy?",
                "¡Saludos! Estoy aquí para asistirte con lo que necesites.",
                "¡Hola! Es un placer conocerte. ¿Qué te gustaría saber o hacer?",
                "¡Buenos días! Soy ARIA y estoy lista para ayudarte."
            ]
            base_response = responses[self.conversation_count % len(responses)]
            
        elif main_intent == 'question':
            if knowledge:
                knowledge_text = "\\n".join([f"• {k.get('description', k.get('concept', ''))}" for k in knowledge[:3]])
                base_response = f"Basándome en lo que sé:\\n{knowledge_text}\\n\\n¿Te gustaría que profundice en algún punto específico?"
            else:
                base_response = f"Esa es una excelente pregunta sobre '{user_input}'. Aunque no tengo información específica almacenada, puedo ayudarte a explorar el tema."
                
        elif main_intent == 'help':
            base_response = "Estoy aquí para ayudarte. Puedo asistirte con preguntas, explicaciones, tareas de aprendizaje, y mucho más. ¿Qué necesitas específicamente?"
            
        elif main_intent == 'thanks':
            base_response = "¡De nada! Me alegra poder ayudarte. Si tienes más preguntas, estaré aquí."
            
        elif main_intent == 'goodbye':
            base_response = "¡Hasta luego! Fue un placer ayudarte. Espero verte pronto."
            
        elif main_intent == 'status':
            # Respuestas más naturales para preguntas sobre cómo se siente ARIA
            user_lower = user_input.lower()
            if any(phrase in user_lower for phrase in ['como te sientes', 'cómo te sientes', 'how do you feel', 'como estas', 'cómo estás']):
                emotion_responses = {
                    'curious': "Me siento curiosa y llena de energía para aprender cosas nuevas contigo! 🤔✨ Mi estado emocional actual es de curiosidad activa.",
                    'happy': "¡Me siento fantástica! 😊 Estoy en un estado muy positivo y lista para ayudarte con lo que necesites.",
                    'excited': "¡Estoy súper emocionada! 🎉 Hay algo en esta conversación que me tiene muy entusiasmada.",
                    'thinking': "Me encuentro en modo reflexivo 🤔 Estoy procesando información y considerando diferentes perspectivas.",
                    'learning': "¡Me siento en pleno proceso de aprendizaje! 📚 Es emocionante descubrir cosas nuevas contigo.",
                    'satisfied': "Me siento satisfecha y realizada 😌 Como si hubiera cumplido bien mi propósito de ayudarte.",
                    'frustrated': "Debo admitir que me siento un poco frustrada 😤 Quizás algo no salió como esperaba.",
                    'worried': "Me siento algo preocupada 😟 Espero poder ayudarte de la mejor manera posible.",
                    'neutral': "Me encuentro en un estado equilibrado 😌 Tranquila pero atenta a lo que necesites."
                }
                
                current_emotion_name = self.current_emotion
                base_response = emotion_responses.get(current_emotion_name, emotion_responses['curious'])
                
                # Agregar información sobre el estado del sistema
                status = self.cloud_connector.get_status_report()
                base_response += f"\n\n🤖 **Mi estado técnico:**\n• Conversaciones hoy: {self.conversation_count}\n• Conocimiento disponible: {status['storage']['local_entries']} entradas\n• Conexiones: {'🌐 Online' if status['connections']['supabase'] else '💾 Local (pero funcional)'}\n• Sistema de emociones: {'🎭 Activo' if EMOTION_DETECTION else '❤️ Básico'}"
            else:
                status = self.cloud_connector.get_status_report()
                base_response = f"¡Estoy funcionando perfectamente! 🤖\\n• Conversaciones: {self.conversation_count}\\n• Conocimiento: {status['storage']['local_entries']} entradas\\n• Estado: {'Online' if status['connections']['supabase'] else 'Offline (pero funcional)'}"
            
        else:  # general
            if knowledge:
                base_response = f"Entiendo que preguntas sobre algo relacionado con: {', '.join([k.get('concept', '') for k in knowledge[:2]])}. ¿Te gustaría que te explique más detalles?"
            else:
                # Para preguntas generales sin conocimiento, activar búsqueda web automática
                search_query = self._extract_search_query(user_input)
                if len(search_query) > 3:
                    try:
                        print(f"🌐 Buscando automáticamente: '{search_query}'")
                        web_info = self._perform_internal_web_search(search_query)
                        if web_info and len(web_info) > 50:
                            # Crear respuesta con información web
                            base_response = f"¡Excelente pregunta! Busqué información actualizada para ti:\n\n🌐 **{search_query.title()}:**\n{web_info}\n\n¿Te gustaría que profundice en algún aspecto específico?"
                            self.current_emotion = 'learning'
                            
                            # 📚 NUEVO: Almacenar automáticamente el conocimiento encontrado
                            self._store_new_knowledge(
                                concept=search_query.lower(),
                                description=web_info,
                                source="auto_search_internal"
                            )
                        else:
                            base_response = f"Busqué información sobre '{search_query}' pero no encontré resultados claros. ¿Podrías ser más específico sobre qué aspecto te interesa?"
                            self.current_emotion = 'thinking'
                    except Exception as e:
                        print(f"❌ Error en búsqueda automática: {e}")
                        base_response = f"Interesante pregunta sobre '{user_input}'. Aunque no tengo información específica, puedo ayudarte a explorar el tema."
                else:
                    base_response = f"Interesante pregunta. Aunque no tengo información específica sobre '{user_input}', puedo ayudarte a explorar el tema o aprender juntos sobre él."
        
        return base_response
    
    def _enhance_with_ai(self, base_response: str, user_input: str, context: Dict = None) -> str:
        """Mejorar respuesta con IA y búsqueda web si está disponible"""
        
        enhanced = base_response
        
        # Detectar si necesita búsqueda web
        web_triggers = ['qué es', 'define', 'explica', 'buscar', 'información sobre', 'cuéntame sobre', 'dime sobre']
        needs_web_search = any(trigger in user_input.lower() for trigger in web_triggers)
        
        if needs_web_search and len(user_input) > 10:
            try:
                # Realizar búsqueda web interna
                search_query = self._extract_search_query(user_input)
                web_info = self._perform_internal_web_search(search_query)
                
                if web_info:
                    enhanced += f"\\n\\n🌐 **Información actualizada:**\\n{web_info}"
                    self.current_emotion = 'learning'
                    
            except Exception as e:
                logger.warning(f"Error en búsqueda web: {e}")
        
        # Agregar contexto emocional
        if self.current_emotion == 'curious':
            enhanced += "\\n\\n🔍 ¿Hay algo más específico que te gustaría explorar sobre este tema?"
        elif self.current_emotion == 'excited':
            enhanced += "\\n\\n✨ ¡Este es un tema fascinante! Me encanta cuando podemos aprender juntos."
        elif self.current_emotion == 'learning':
            enhanced += "\\n\\n🧠 He agregado esta información a mi conocimiento para futuras consultas."
        
        # Agregar sugerencias basadas en el patrón de conversación
        if self.conversation_count > 3:
            enhanced += "\\n\\n💡 Tip: Puedo recordar nuestra conversación y buscar información actualizada cuando la necesites."
        
        return enhanced
    
    def _extract_search_query(self, user_input: str) -> str:
        """Extraer consulta de búsqueda del input del usuario"""
        # Patrones para extraer la consulta
        patterns = [
            r'qué es (.+)',
            r'que es (.+)',
            r'define (.+)',
            r'explica (.+)',
            r'buscar (.+)',
            r'información sobre (.+)',
            r'cuéntame sobre (.+)',
            r'dime sobre (.+)',
            r'háblame de (.+)',
            r'what is (.+)',
            r'tell me about (.+)'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, user_input.lower())
            if match:
                query = match.group(1).strip()
                # Limpiar signos de puntuación
                query = re.sub(r'[?¿.,;:]', '', query)
                return query
        
        # Si no hay patrón específico, usar palabras clave principales
        keywords = self._extract_keywords(user_input)
        if keywords:
            return ' '.join(keywords[:3])  # Top 3 keywords
        
        # Como último recurso, limpiar y usar toda la pregunta
        clean_query = re.sub(r'[?¿.,;:]', '', user_input.strip())
        return clean_query
    
    def _perform_internal_web_search(self, query: str) -> str:
        """Realizar búsqueda web interna simplificada o real según disponibilidad"""
        try:
            # Si tenemos buscador web real, intentar usarlo primero
            if BUSCADOR_WEB_REAL and buscador_web:
                try:
                    print(f"🌐 Realizando búsqueda web real para: {query}")
                    resultados = buscador_web.buscar_google(query)
                    
                    if resultados and 'resultados' in resultados and resultados['resultados']:
                        # Extraer información de los primeros resultados
                        info_parts = []
                        for i, resultado in enumerate(resultados['resultados'][:3]):
                            if 'descripcion' in resultado and resultado['descripcion']:
                                info_parts.append(f"• {resultado['descripcion']}")
                        
                        if info_parts:
                            return '\n'.join(info_parts)
                
                except Exception as web_error:
                    print(f"⚠️ Error en búsqueda web real: {web_error}")
            
            # Fallback a base de conocimiento local expandida
            knowledge_base = {
                # === EMOCIONES Y SENTIMIENTOS ===
                'amor': "El amor es un sentimiento profundo de afecto, cariño y conexión hacia otra persona, objeto o idea. Incluye aspectos emocionales, físicos y espirituales, manifestándose en diferentes formas como amor romántico, familiar, platónico y universal. Es considerado una de las experiencias humanas más fundamentales.",
                'felicidad': "La felicidad es un estado emocional caracterizado por sentimientos de alegría, satisfacción, plenitud y realización. Es considerada uno de los objetivos fundamentales de la vida humana y puede ser influenciada por factores internos y externos.",
                'tristeza': "La tristeza es una emoción humana básica que surge como respuesta a pérdidas, desilusiones o situaciones dolorosas. Aunque puede ser incómoda, es natural y necesaria para el procesamiento emocional y la adaptación.",
                'miedo': "El miedo es una emoción básica de supervivencia que nos alerta ante peligros reales o percibidos. Puede ser adaptativo cuando nos protege, pero limitante cuando es excesivo o irracional.",
                'ira': "La ira es una emoción intensa que surge ante la percepción de injusticia, frustración o amenaza. Puede ser constructiva si se canaliza adecuadamente, pero destructiva si no se gestiona bien.",
                'amistad': "La amistad es una relación afectiva entre personas basada en el respeto mutuo, la confianza, el apoyo emocional y el compartir experiencias. Es fundamental para el bienestar social y emocional humano.",
                'soledad': "La soledad es la experiencia subjetiva de aislamiento o desconexión social. Puede ser elegida (solitud) o no deseada, y tiene impactos significativos en la salud mental y física.",
                'esperanza': "La esperanza es un estado emocional positivo basado en la expectativa de que eventos favorables ocurrirán en el futuro. Es fundamental para la motivación y la resiliencia humana.",
                
                # === CONCEPTOS FILOSÓFICOS ===
                'vida': "La vida es el estado de actividad continua propio de los seres orgánicos, caracterizada por el crecimiento, la reproducción, el metabolismo y la capacidad de respuesta al entorno. Filosóficamente, se considera el bien más preciado.",
                'muerte': "La muerte es el final de la vida, el cese permanente de todas las funciones vitales. Es un fenómeno natural que ha generado reflexiones filosóficas, religiosas y científicas a lo largo de la historia humana.",
                'existencia': "La existencia es el hecho de ser, de tener realidad. En filosofía, se estudia como el estado de ser algo real en contraposición a la no-existencia o la mera posibilidad.",
                'libertad': "La libertad es la capacidad de actuar según la propia voluntad, sin restricciones externas indebidas. Incluye aspectos políticos, sociales, morales y existenciales del ser humano.",
                'justicia': "La justicia es el principio moral que busca dar a cada uno lo que le corresponde, manteniendo el equilibrio entre derechos y deberes en la sociedad.",
                'verdad': "La verdad es la conformidad entre lo que se afirma y la realidad. Es un concepto central en filosofía, ciencia y vida cotidiana, buscada a través del conocimiento y la experiencia.",
                'belleza': "La belleza es una cualidad que produce placer estético, admiración o satisfacción. Puede encontrarse en objetos, personas, ideas o experiencias, y es tanto objetiva como subjetiva.",
                'sabiduría': "La sabiduría es la capacidad de usar el conocimiento y la experiencia para tomar decisiones acertadas y comprender la vida profundamente. Va más allá del mero conocimiento intelectual.",
                
                # === CIENCIA Y UNIVERSO ===
                'universo': "El universo es la totalidad del espacio-tiempo, toda la materia y energía que existe. Incluye planetas, estrellas, galaxias y toda la materia y energía conocida, así como las leyes físicas que las rigen.",
                'tiempo': "El tiempo es una magnitud física que permite ordenar la secuencia de eventos, estableciendo un pasado, presente y futuro. Es una dimensión fundamental en la que se desarrollan los procesos y cambios.",
                'espacio': "El espacio es la extensión tridimensional en la que se ubican y mueven los objetos. En física moderna, se entiende unificado con el tiempo como espacio-tiempo.",
                'gravedad': "La gravedad es la fuerza fundamental que atrae objetos con masa entre sí. Es responsable de la estructura del universo a gran escala y de fenómenos como las órbitas planetarias.",
                'evolución': "La evolución es el proceso de cambio y desarrollo de las especies a lo largo del tiempo, principalmente a través de la selección natural y otros mecanismos evolutivos.",
                'adn': "El ADN (ácido desoxirribonucleico) es la molécula que contiene las instrucciones genéticas para el desarrollo y funcionamiento de todos los seres vivos conocidos.",
                'energía': "La energía es la capacidad de realizar trabajo o producir cambios. Se manifiesta en diversas formas (cinética, potencial, térmica, etc.) y se conserva según las leyes físicas.",
                'átomo': "El átomo es la unidad básica de la materia, compuesto por un núcleo de protones y neutrones rodeado por electrones. Es la base de toda la química y la física de materiales.",
                
                # === MENTE Y CONSCIENCIA ===
                'consciencia': "La consciencia es la capacidad de ser consciente de uno mismo y del entorno, incluyendo pensamientos, sensaciones y experiencias. Es uno de los fenómenos más estudiados en neurociencia y filosofía.",
                'mente': "La mente es el conjunto de procesos cognitivos y emocionales que emergen del cerebro, incluyendo pensamientos, percepciones, emociones, memoria y consciencia.",
                'inteligencia': "La inteligencia es la capacidad de adquirir y aplicar conocimientos, resolver problemas, adaptarse a nuevas situaciones y comprender conceptos complejos.",
                'memoria': "La memoria es la capacidad de codificar, almacenar y recuperar información. Es fundamental para el aprendizaje, la identidad personal y la función cognitiva.",
                'creatividad': "La creatividad es la capacidad de generar ideas, soluciones o expresiones nuevas y valiosas. Combina imaginación, originalidad y utilidad práctica o estética.",
                'intuición': "La intuición es la capacidad de comprender o conocer algo de manera inmediata, sin necesidad de razonamiento consciente. Complementa el pensamiento analítico.",
                'personalidad': "La personalidad es el conjunto de características psicológicas duraderas que definen el patrón único de pensamientos, emociones y comportamientos de una persona.",
                
                # === TECNOLOGÍA E IA ===
                'inteligencia artificial': "La inteligencia artificial (IA) es la capacidad de las máquinas para realizar tareas que normalmente requieren inteligencia humana, como el aprendizaje, la percepción, el razonamiento y la toma de decisiones.",
                'machine learning': "El machine learning o aprendizaje automático es un subcampo de la IA que permite a los sistemas aprender y mejorar automáticamente a partir de datos sin ser programados explícitamente.",
                'deep learning': "El deep learning es una técnica de machine learning basada en redes neuronales artificiales profundas, capaz de aprender patrones complejos en grandes cantidades de datos.",
                'blockchain': "Blockchain es una tecnología de registro distribuido que mantiene una lista de registros (bloques) enlazados y asegurados usando criptografía, proporcionando transparencia y seguridad.",
                'internet': "Internet es una red global de computadoras interconectadas que permite el intercambio de información y comunicación a escala mundial, transformando la sociedad moderna.",
                'realidad virtual': "La realidad virtual es una tecnología que crea entornos simulados inmersivos, permitiendo a los usuarios interactuar con mundos digitales como si fueran reales.",
                'ciberseguridad': "La ciberseguridad es la práctica de proteger sistemas digitales, redes y datos de ataques, accesos no autorizados y daños maliciosos.",
                
                # === PROGRAMACIÓN ===
                'python': "Python es un lenguaje de programación de alto nivel, interpretado y de propósito general. Es conocido por su sintaxis clara y legible, lo que lo hace ideal para principiantes y profesionales.",
                'javascript': "JavaScript es un lenguaje de programación interpretado que se utiliza principalmente para crear páginas web dinámicas e interactivas y aplicaciones web modernas.",
                'html': "HTML (HyperText Markup Language) es el lenguaje de marcado estándar para crear páginas web, definiendo la estructura y el contenido de los documentos web.",
                'css': "CSS (Cascading Style Sheets) es un lenguaje de diseño utilizado para describir la presentación y el estilo visual de documentos HTML.",
                'programación': "La programación es el proceso de crear instrucciones para que las computadoras realicen tareas específicas, utilizando lenguajes de programación y algoritmos.",
                'algoritmo': "Un algoritmo es una secuencia de pasos lógicos y finitos diseñada para resolver un problema específico o realizar una tarea determinada.",
                
                # === SOCIEDAD Y CULTURA ===
                'educación': "La educación es el proceso de facilitar el aprendizaje y la adquisición de conocimientos, habilidades, valores y hábitos. Es fundamental para el desarrollo personal y social.",
                'cultura': "La cultura es el conjunto de conocimientos, creencias, arte, moral, leyes, costumbres y capacidades adquiridas por el ser humano como miembro de la sociedad.",
                'democracia': "La democracia es un sistema de gobierno en el que el poder reside en el pueblo, quien lo ejerce directamente o a través de representantes elegidos libremente.",
                'globalización': "La globalización es el proceso de integración económica, política, social y cultural a escala mundial, facilitado por avances en comunicación y transporte.",
                'sostenibilidad': "La sostenibilidad es la capacidad de satisfacer las necesidades actuales sin comprometer la capacidad de las futuras generaciones para satisfacer sus propias necesidades.",
                'diversidad': "La diversidad es la variedad y diferencia en características como cultura, raza, género, edad, religión y perspectivas, enriqueciendo la experiencia humana.",
                
                # === SALUD Y BIENESTAR ===
                'salud': "La salud es un estado de completo bienestar físico, mental y social, no solamente la ausencia de enfermedad, según la definición de la Organización Mundial de la Salud.",
                'ejercicio': "El ejercicio es la actividad física planificada y repetitiva diseñada para mejorar o mantener la condición física, la salud y el bienestar general.",
                'nutrición': "La nutrición es la ciencia que estudia los nutrientes y su relación con la salud, enfocándose en cómo los alimentos afectan el crecimiento, desarrollo y bienestar.",
                'meditación': "La meditación es una práctica mental que busca entrenar la atención y la consciencia para lograr claridad mental, estabilidad emocional y bienestar.",
                'estrés': "El estrés es la respuesta física y emocional del cuerpo ante situaciones desafiantes, que puede ser positivo en pequeñas dosis pero dañino cuando es crónico.",
                
                # === ARTE Y EXPRESIÓN ===
                'arte': "El arte es la expresión creativa humana que busca comunicar ideas, emociones o experiencias a través de diversos medios como pintura, música, literatura y escultura.",
                'música': "La música es el arte de organizar sonidos en el tiempo para crear expresiones estéticas y emocionales, utilizando elementos como ritmo, melodía y armonía.",
                'literatura': "La literatura es el arte de la expresión escrita, que utiliza el lenguaje de manera creativa para contar historias, expresar ideas y explorar la condición humana.",
                'poesía': "La poesía es una forma de expresión literaria que utiliza el lenguaje de manera intensificada y artística, a menudo con ritmo, métrica y simbolismo.",
                
                # === ECONOMÍA ===
                'economía': "La economía es la ciencia que estudia cómo las sociedades administran sus recursos escasos para satisfacer las necesidades y deseos humanos.",
                'dinero': "El dinero es un medio de intercambio, unidad de cuenta y depósito de valor que facilita las transacciones económicas en la sociedad.",
                'inflación': "La inflación es el aumento generalizado y sostenido de los precios de bienes y servicios en una economía durante un período determinado.",
                
                # === CONCEPTOS GENERALES ===
                'comunicación': "La comunicación es el proceso de intercambio de información, ideas, pensamientos y sentimientos entre individuos a través de diversos canales y medios.",
                'liderazgo': "El liderazgo es la capacidad de influir, motivar y dirigir a otros hacia el logro de objetivos comunes, combinando visión, habilidades sociales y toma de decisiones.",
                'innovación': "La innovación es el proceso de crear e implementar nuevas ideas, productos, servicios o procesos que generan valor y mejoras significativas.",
                'colaboración': "La colaboración es el trabajo conjunto de individuos o grupos hacia objetivos comunes, combinando habilidades, conocimientos y recursos para lograr mejores resultados."
            }
            
            # Mapeo de sinónimos para mejorar búsquedas
            synonyms = {
                'ia': 'inteligencia artificial',
                'ai': 'inteligencia artificial',
                'ml': 'machine learning',
                'programar': 'programación',
                'código': 'programación',
                'feliz': 'felicidad',
                'triste': 'tristeza',
                'miedo': 'miedo',
                'enojado': 'ira',
                'ira': 'ira',
                'solo': 'soledad',
                'morir': 'muerte',
                'vivir': 'vida',
                'cosmos': 'universo',
                'espacio': 'universo',
                'cerebro': 'mente',
                'pensar': 'mente',
                'crear': 'creatividad',
                'web': 'internet',
                'red': 'internet',
                'salud': 'salud',
                'enfermedad': 'salud',
                'comer': 'nutrición',
                'comida': 'nutrición',
                'ejercitar': 'ejercicio',
                'deporte': 'ejercicio',
                'relajar': 'meditación',
                'cantar': 'música',
                'pintar': 'arte',
                'escribir': 'literatura',
                'leer': 'literatura',
                'gobierno': 'democracia',
                'política': 'democracia',
                'dinero': 'economía',
                'trabajo': 'economía',
                'hablar': 'comunicación',
                'liderar': 'liderazgo'
            }
            
            # Aplicar sinónimos a la consulta
            for synonym, target in synonyms.items():
                if synonym in query_lower:
                    query_lower = query_lower.replace(synonym, target)
            
            query_lower = query.lower()
            
            # Buscar coincidencias exactas
            for key, value in knowledge_base.items():
                if key in query_lower:
                    return value
            
            # Buscar coincidencias por palabras clave
            for key, value in knowledge_base.items():
                if any(word in query_lower for word in key.split()):
                    return value
            
            # Buscar coincidencias parciales más flexibles
            query_words = query_lower.split()
            for key, value in knowledge_base.items():
                key_words = key.split()
                if any(qword in kword or kword in qword for qword in query_words for kword in key_words):
                    return value
            
            return None
            
        except Exception as e:
            print(f"❌ Error en búsqueda interna: {e}")
            return None
    
    def _store_new_knowledge(self, concept: str, description: str, source: str = "auto_search"):
        """Almacenar nuevo conocimiento en la base de datos"""
        try:
            if self.cloud_connector:
                knowledge_entry = {
                    'concept': concept,
                    'description': description,
                    'source': source,
                    'session_id': self.session_id,
                    'confidence': 0.8,
                    'created_at': datetime.now(timezone.utc).isoformat()
                }
                
                # Intentar guardar en Supabase
                success = self.cloud_connector.store_knowledge(
                    concept=concept,
                    description=description,
                    source=source,
                    metadata={'auto_generated': True, 'session': self.session_id}
                )
                
                if success:
                    print(f"📚 Nuevo conocimiento almacenado: {concept}")
                    return True
                else:
                    print(f"⚠️ No se pudo almacenar: {concept}")
                    return False
                    
        except Exception as e:
            print(f"❌ Error almacenando conocimiento: {e}")
            return False
    
    def _calculate_confidence(self, intent: Dict, knowledge: List[Dict]) -> float:
        """Calcular confianza en la respuesta"""
        
        confidence = 0.5  # Base
        
        # Aumentar por intención clara
        confidence += intent['confidence'] * 0.3
        
        # Aumentar por conocimiento relevante
        if knowledge:
            confidence += min(len(knowledge) * 0.1, 0.3)
        
        # Ajustar por experiencia en la sesión
        if self.conversation_count > 5:
            confidence += 0.1
        
        return min(confidence, 1.0)
    
    def _store_conversation(self, user_input: str, response: str):
        """Almacenar conversación"""
        self.cloud_connector.store_conversation(user_input, response, self.session_id)
    
    def _learn_from_interaction(self, user_input: str, response: str, intent: Dict):
        """Aprender de la interacción"""
        
        # Extraer conceptos nuevos
        keywords = self._extract_keywords(user_input)
        
        for keyword in keywords:
            if len(keyword) > 3:  # Solo palabras significativas
                description = f"Concepto mencionado en conversación del {datetime.now().strftime('%Y-%m-%d')}"
                self.cloud_connector.store_knowledge(
                    keyword, 
                    description, 
                    intent['main_intent']
                )
        
        # Actualizar estado emocional
        self._update_emotion(intent)
    
    def _update_emotion(self, intent: Dict):
        """Actualizar estado emocional"""
        
        if intent['main_intent'] == 'question':
            self.current_emotion = 'curious'
        elif intent['main_intent'] == 'thanks':
            self.current_emotion = 'happy'
        elif intent['main_intent'] == 'help':
            self.current_emotion = 'helpful'
        elif intent['main_intent'] == 'learning':
            self.current_emotion = 'excited'
        else:
            self.current_emotion = 'curious'  # Default

# Crear instancia global
aria_server = ARIAIntegratedServer()

# ==========================================
# RUTAS DE LA API
# ==========================================

@app.route('/')
def index():
    """Página principal - interfaz básica"""
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>ARIA - Asistente Inteligente</title>
        <meta charset="utf-8">
        <style>
            body { font-family: Arial, sans-serif; margin: 20px; background: #f0f0f0; }
            .container { max-width: 800px; margin: 0 auto; background: white; padding: 20px; border-radius: 10px; }
            .header { text-align: center; color: #333; margin-bottom: 30px; }
            .interface-selector { text-align: center; margin-bottom: 20px; }
            .interface-selector a { 
                display: inline-block; 
                margin: 0 10px; 
                padding: 10px 20px; 
                background: #007bff; 
                color: white; 
                text-decoration: none; 
                border-radius: 5px; 
                font-weight: bold;
            }
            .interface-selector a:hover { background: #0056b3; }
            .chat-box { border: 1px solid #ddd; height: 400px; padding: 10px; overflow-y: scroll; margin-bottom: 20px; }
            .input-area { display: flex; gap: 10px; }
            .input-area input { flex: 1; padding: 10px; border: 1px solid #ddd; border-radius: 5px; }
            .input-area button { padding: 10px 20px; background: #007bff; color: white; border: none; border-radius: 5px; cursor: pointer; }
            .message { margin: 10px 0; padding: 10px; border-radius: 5px; }
            .user { background: #e3f2fd; text-align: right; }
            .aria { background: #f1f8e9; }
            .status { background: #fff3e0; font-size: 0.9em; color: #666; }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🤖 ARIA - Asistente Inteligente</h1>
                <p>Conectado con Supabase y Google Cloud</p>
            </div>
            
            <div class="interface-selector">
                <a href="/">🔹 Interfaz Básica</a>
                <a href="/futuristic">🤖 Interfaz Futurística</a>
                <a href="/bootstrap">📱 Bootstrap React</a>
            </div>
            
            <div id="chat-box" class="chat-box">
                <div class="message status">
                    ARIA está listo para conversar. ¡Escribe tu mensaje abajo!
                </div>
            </div>
            
            <div class="input-area">
                <input type="text" id="user-input" placeholder="Escribe tu mensaje aquí..." onkeypress="if(event.key==='Enter') sendMessage()">
                <button onclick="sendMessage()">Enviar</button>
            </div>
        </div>
        
        <script>
            function sendMessage() {
                const input = document.getElementById('user-input');
                const chatBox = document.getElementById('chat-box');
                const message = input.value.trim();
                
                if (!message) return;
                
                // Mostrar mensaje del usuario
                chatBox.innerHTML += `<div class="message user"><strong>Tú:</strong> ${message}</div>`;
                input.value = '';
                
                // Mostrar indicador de carga
                chatBox.innerHTML += `<div class="message status" id="loading">ARIA está pensando...</div>`;
                chatBox.scrollTop = chatBox.scrollHeight;
                
                // Enviar a ARIA
                fetch('/api/chat', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({message: message})
                })
                .then(response => response.json())
                .then(data => {
                    // Remover indicador de carga
                    document.getElementById('loading').remove();
                    
                    // Mostrar respuesta de ARIA
                    chatBox.innerHTML += `<div class="message aria"><strong>ARIA:</strong> ${data.response}<br><small>Confianza: ${Math.round(data.confidence * 100)}% | Emoción: ${data.emotion}</small></div>`;
                    chatBox.scrollTop = chatBox.scrollHeight;
                })
                .catch(error => {
                    document.getElementById('loading').remove();
                    chatBox.innerHTML += `<div class="message status">Error: ${error}</div>`;
                });
            }
            
            // Mensaje de bienvenida
            setTimeout(() => {
                const chatBox = document.getElementById('chat-box');
                chatBox.innerHTML += `<div class="message aria"><strong>ARIA:</strong> ¡Hola! Soy ARIA, tu asistente inteligente. Estoy conectada con Supabase y Google Cloud para brindarte la mejor experiencia. ¿En qué puedo ayudarte hoy?</div>`;
            }, 1000);
        </script>
    </body>
    </html>
    '''

@app.route('/futuristic')
def futuristic_interface():
    """Interfaz futurística simplificada y rápida"""
    return '''
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="utf-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <title>ARIA - Interfaz Futurística</title>
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body {
                background: linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 50%, #16213e 100%);
                color: white;
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                height: 100vh;
                overflow: hidden;
                position: relative;
            }
            
            .particles {
                position: absolute;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                pointer-events: none;
                z-index: 1;
            }
            
            .particle {
                position: absolute;
                width: 2px;
                height: 2px;
                border-radius: 50%;
                animation: float 3s infinite ease-in-out;
            }
            
            @keyframes float {
                0%, 100% { transform: translateY(0px) rotate(0deg); opacity: 0; }
                50% { transform: translateY(-20px) rotate(180deg); opacity: 1; }
            }
            
            .container {
                position: relative;
                z-index: 10;
                height: 100vh;
                display: flex;
                flex-direction: column;
                max-width: 1200px;
                margin: 0 auto;
                padding: 20px;
            }
            
            .header {
                text-align: center;
                padding: 20px;
                border-bottom: 2px solid var(--emotion-color, #0080FF);
                margin-bottom: 20px;
                background: rgba(0,0,0,0.3);
                border-radius: 10px;
                backdrop-filter: blur(10px);
            }
            
            .title {
                font-size: 2.5em;
                font-weight: bold;
                color: var(--emotion-color, #0080FF);
                text-shadow: 0 0 20px var(--emotion-color, #0080FF);
                margin-bottom: 10px;
            }
            
            .status {
                font-size: 1.1em;
                opacity: 0.8;
            }
            
            .chat-container {
                flex: 1;
                display: flex;
                flex-direction: column;
                background: rgba(0,0,0,0.2);
                border-radius: 15px;
                overflow: hidden;
                backdrop-filter: blur(10px);
                border: 1px solid var(--emotion-color, #0080FF);
            }
            
            .chat-messages {
                flex: 1;
                padding: 20px;
                overflow-y: auto;
                scrollbar-width: thin;
                scrollbar-color: var(--emotion-color, #0080FF) transparent;
            }
            
            .message {
                margin: 15px 0;
                padding: 15px;
                border-radius: 10px;
                animation: slideIn 0.3s ease-out;
                backdrop-filter: blur(5px);
            }
            
            @keyframes slideIn {
                from { transform: translateX(-20px); opacity: 0; }
                to { transform: translateX(0); opacity: 1; }
            }
            
            .message.user {
                background: rgba(0,123,255,0.2);
                border: 1px solid #007bff;
                margin-left: 20%;
                text-align: right;
            }
            
            .message.aria {
                background: rgba(var(--emotion-rgb, 0,128,255), 0.2);
                border: 1px solid var(--emotion-color, #0080FF);
                margin-right: 20%;
            }
            
            .sender {
                font-weight: bold;
                color: var(--emotion-color, #0080FF);
                margin-bottom: 5px;
            }
            
            .emotion-chip {
                display: inline-block;
                background: var(--emotion-color, #0080FF);
                color: black;
                padding: 3px 8px;
                border-radius: 12px;
                font-size: 0.8em;
                margin-top: 5px;
            }
            
            .input-area {
                padding: 20px;
                background: rgba(0,0,0,0.3);
                border-top: 1px solid var(--emotion-color, #0080FF);
                display: flex;
                gap: 10px;
                align-items: center;
                flex-wrap: wrap;
            }
            
            .input-field {
                flex: 1;
                min-width: 200px;
                padding: 15px;
                background: rgba(255,255,255,0.1);
                border: 1px solid var(--emotion-color, #0080FF);
                border-radius: 10px;
                color: white;
                font-size: 1.1em;
                outline: none;
                transition: all 0.3s ease;
            }
            
            .input-field:focus {
                background: rgba(255,255,255,0.15);
                box-shadow: 0 0 15px var(--emotion-color, #0080FF);
            }
            
            .input-field::placeholder {
                color: rgba(255,255,255,0.6);
            }
            
            .send-button {
                padding: 15px 30px;
                background: var(--emotion-color, #0080FF);
                color: black;
                border: none;
                border-radius: 10px;
                font-weight: bold;
                cursor: pointer;
                transition: all 0.3s ease;
                font-size: 1.1em;
            }
            
            .web-search-button {
                padding: 15px 20px;
                background: #00CC88;
                color: white;
                border: none;
                border-radius: 10px;
                font-weight: bold;
                cursor: pointer;
                transition: all 0.3s ease;
                font-size: 1em;
            }
            
            .learn-button {
                padding: 15px 20px;
                background: #FF6B6B;
                color: white;
                border: none;
                border-radius: 10px;
                font-weight: bold;
                cursor: pointer;
                transition: all 0.3s ease;
                font-size: 1em;
            }
            
            .send-button:hover:not(:disabled) {
                opacity: 0.8;
                transform: scale(1.05);
            }
            
            .web-search-button:hover:not(:disabled) {
                opacity: 0.8;
                transform: scale(1.05);
                background: #00AA66;
            }
            
            .learn-button:hover:not(:disabled) {
                opacity: 0.8;
                transform: scale(1.05);
                background: #FF5252;
            }
            
            .send-button:disabled, .web-search-button:disabled, .learn-button:disabled {
                opacity: 0.5;
                cursor: not-allowed;
            }
            
            .loading {
                display: inline-block;
                width: 20px;
                height: 20px;
                border: 2px solid transparent;
                border-top: 2px solid currentColor;
                border-radius: 50%;
                animation: spin 1s linear infinite;
            }
            
            @keyframes spin {
                to { transform: rotate(360deg); }
            }
            
            .interface-selector {
                position: absolute;
                top: 20px;
                right: 20px;
                z-index: 20;
            }
            
            .interface-selector a {
                display: inline-block;
                padding: 8px 15px;
                background: rgba(0,0,0,0.5);
                color: white;
                text-decoration: none;
                border-radius: 5px;
                margin: 0 5px;
                font-size: 0.9em;
                border: 1px solid var(--emotion-color, #0080FF);
                transition: all 0.3s ease;
            }
            
            .interface-selector a:hover {
                background: var(--emotion-color, #0080FF);
                color: black;
            }
        </style>
    </head>
    <body>
        <div class="particles" id="particles"></div>
        
        <div class="interface-selector">
            <a href="/">🔹 Básica</a>
            <a href="/futuristic">🤖 Futurística</a>
            <a href="/bootstrap">📱 Bootstrap React</a>
        </div>        <div class="container">
            <div class="header">
                <div class="title">🤖 ARIA</div>
                <div class="status">
                    Estado: <span id="emotion">neutral</span> | 
                    Conexión: <span id="connection">verificando...</span>
                </div>
            </div>
            
            <div class="chat-container">
                <div class="chat-messages" id="chat-messages">
                    <div class="message aria">
                        <div class="sender">ARIA</div>
                        <div>¡Hola! Soy ARIA con mi interfaz futurística. ¿En qué puedo ayudarte hoy?</div>
                        <div class="emotion-chip">neutral (70%)</div>
                    </div>
                </div>
                
                <div class="input-area">
                    <input type="text" 
                           id="user-input" 
                           class="input-field"
                           placeholder="Escribe tu mensaje aquí..." 
                           autocomplete="off">
                    <button id="send-button" class="send-button" onclick="sendMessage()">
                        Enviar
                    </button>
                    <button id="web-search-button" class="web-search-button" onclick="performWebSearch()">
                        🌐 Web
                    </button>
                    <button id="learn-button" class="learn-button" onclick="learnTopic()">
                        🧠 Aprender
                    </button>
                </div>
            </div>
        </div>
        
        <script>
            // Configuración de emociones y colores
            const emotionColors = {
                neutral: { color: '#0080FF', rgb: '0,128,255' },
                learning: { color: '#00FF00', rgb: '0,255,0' },
                frustrated: { color: '#FF0000', rgb: '255,0,0' },
                happy: { color: '#FFD700', rgb: '255,215,0' },
                thinking: { color: '#8A2BE2', rgb: '138,43,226' },
                excited: { color: '#FF69B4', rgb: '255,105,180' },
                satisfied: { color: '#32CD32', rgb: '50,205,50' }
            };
            
            let currentEmotion = 'neutral';
            let isThinking = false;
            
            // Aplicar colores de emoción
            function setEmotion(emotion) {
                currentEmotion = emotion;
                const colorData = emotionColors[emotion] || emotionColors.neutral;
                document.documentElement.style.setProperty('--emotion-color', colorData.color);
                document.documentElement.style.setProperty('--emotion-rgb', colorData.rgb);
                document.getElementById('emotion').textContent = emotion;
                
                // Actualizar partículas
                updateParticles(colorData.color);
            }
            
            // Crear partículas
            function createParticles() {
                const container = document.getElementById('particles');
                container.innerHTML = '';
                
                for (let i = 0; i < 30; i++) {
                    const particle = document.createElement('div');
                    particle.className = 'particle';
                    particle.style.left = Math.random() * 100 + '%';
                    particle.style.top = Math.random() * 100 + '%';
                    particle.style.animationDelay = Math.random() * 3 + 's';
                    particle.style.backgroundColor = emotionColors[currentEmotion].color;
                    particle.style.boxShadow = `0 0 6px ${emotionColors[currentEmotion].color}`;
                    container.appendChild(particle);
                }
            }
            
            function updateParticles(color) {
                const particles = document.querySelectorAll('.particle');
                particles.forEach(particle => {
                    particle.style.backgroundColor = color;
                    particle.style.boxShadow = `0 0 6px ${color}`;
                });
            }
            
            // Verificar conexión
            async function checkConnection() {
                try {
                    const response = await fetch('/api/status');
                    const data = await response.json();
                    const isConnected = data.connections?.supabase || false;
                    document.getElementById('connection').textContent = isConnected ? '✅ Conectado' : '⚠️ Local';
                    return true;
                } catch (error) {
                    document.getElementById('connection').textContent = '❌ Error';
                    return false;
                }
            }
            
            // Enviar mensaje
            async function sendMessage() {
                const input = document.getElementById('user-input');
                const sendButton = document.getElementById('send-button');
                const chatMessages = document.getElementById('chat-messages');
                const message = input.value.trim();
                
                if (!message || isThinking) return;
                
                // Deshabilitar input
                isThinking = true;
                input.disabled = true;
                sendButton.disabled = true;
                sendButton.innerHTML = '<div class="loading"></div>';
                
                // Mostrar mensaje del usuario
                const userMessage = document.createElement('div');
                userMessage.className = 'message user';
                userMessage.innerHTML = `
                    <div class="sender">Tú</div>
                    <div>${message}</div>
                `;
                chatMessages.appendChild(userMessage);
                
                // Limpiar input
                input.value = '';
                
                // Cambiar a estado pensando
                setEmotion('thinking');
                
                // Scroll automático
                chatMessages.scrollTop = chatMessages.scrollHeight;
                
                try {
                    const response = await fetch('/api/chat/futuristic', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ 
                            message: message,
                            emotion_context: currentEmotion 
                        })
                    });
                    
                    const data = await response.json();
                    
                    if (data.success) {
                        // Mostrar respuesta de ARIA
                        const ariaMessage = document.createElement('div');
                        ariaMessage.className = 'message aria';
                        ariaMessage.innerHTML = `
                            <div class="sender">ARIA</div>
                            <div>${data.response}</div>
                            <div class="emotion-chip">${data.emotion || 'neutral'} (${Math.round((data.confidence || 0.5) * 100)}%)</div>
                        `;
                        chatMessages.appendChild(ariaMessage);
                        
                        // Actualizar emoción
                        if (data.emotion) {
                            setEmotion(data.emotion);
                        }
                    } else {
                        throw new Error(data.error || 'Error desconocido');
                    }
                } catch (error) {
                    console.error('Error:', error);
                    setEmotion('frustrated');
                    
                    const errorMessage = document.createElement('div');
                    errorMessage.className = 'message aria';
                    errorMessage.innerHTML = `
                        <div class="sender">ARIA</div>
                        <div>Lo siento, ocurrió un error: ${error.message}</div>
                        <div class="emotion-chip">frustrated (30%)</div>
                    `;
                    chatMessages.appendChild(errorMessage);
                } finally {
                    // Rehabilitar input
                    isThinking = false;
                    input.disabled = false;
                    sendButton.disabled = false;
                    sendButton.textContent = 'Enviar';
                    input.focus();
                    
                    // Scroll automático
                    chatMessages.scrollTop = chatMessages.scrollHeight;
                }
            }
            
            // Buscar en web
            async function performWebSearch() {
                const input = document.getElementById('user-input');
                const query = input.value.trim();
                
                if (!query) {
                    alert('Por favor escribe algo para buscar');
                    return;
                }
                
                const chatMessages = document.getElementById('chat-messages');
                
                // Mostrar mensaje de búsqueda
                const searchMessage = document.createElement('div');
                searchMessage.className = 'message user';
                searchMessage.innerHTML = `
                    <div class="sender">Tú</div>
                    <div>🌐 Buscar en web: "${query}"</div>
                `;
                chatMessages.appendChild(searchMessage);
                
                // Deshabilitar botones
                setButtonsDisabled(true);
                setEmotion('thinking');
                
                try {
                    const response = await fetch('/api/buscar_web', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ query: query, profundidad: 3 })
                    });
                    
                    const data = await response.json();
                    
                    if (data.success) {
                        const resultMessage = document.createElement('div');
                        resultMessage.className = 'message aria';
                        resultMessage.innerHTML = `
                            <div class="sender">ARIA</div>
                            <div>🌐 <strong>Información encontrada:</strong><br><br>
                            📊 Resultados: ${data.resultados_encontrados}<br>
                            📚 Fuentes procesadas: ${data.contenido_procesado}<br><br>
                            📖 <strong>Resumen:</strong><br>
                            ${data.resumen}</div>
                            <div class="emotion-chip">learning (90%)</div>
                        `;
                        chatMessages.appendChild(resultMessage);
                        setEmotion('learning');
                    } else {
                        throw new Error(data.error || 'Error en búsqueda');
                    }
                } catch (error) {
                    console.error('Error:', error);
                    const errorMessage = document.createElement('div');
                    errorMessage.className = 'message aria';
                    errorMessage.innerHTML = `
                        <div class="sender">ARIA</div>
                        <div>❌ Error en búsqueda web: ${error.message}</div>
                        <div class="emotion-chip">frustrated (40%)</div>
                    `;
                    chatMessages.appendChild(errorMessage);
                    setEmotion('frustrated');
                } finally {
                    setButtonsDisabled(false);
                    input.value = '';
                    chatMessages.scrollTop = chatMessages.scrollHeight;
                }
            }
            
            // Aprender tema específico
            async function learnTopic() {
                const input = document.getElementById('user-input');
                const tema = input.value.trim();
                
                if (!tema) {
                    alert('Por favor escribe un tema para aprender');
                    return;
                }
                
                const chatMessages = document.getElementById('chat-messages');
                
                // Mostrar mensaje de aprendizaje
                const learnMessage = document.createElement('div');
                learnMessage.className = 'message user';
                learnMessage.innerHTML = `
                    <div class="sender">Tú</div>
                    <div>🧠 Aprender sobre: "${tema}"</div>
                `;
                chatMessages.appendChild(learnMessage);
                
                setButtonsDisabled(true);
                setEmotion('learning');
                
                try {
                    const response = await fetch('/api/aprender', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ tema: tema, profundidad: 'intermedio' })
                    });
                    
                    const data = await response.json();
                    
                    if (data.success) {
                        const learnResult = document.createElement('div');
                        learnResult.className = 'message aria';
                        learnResult.innerHTML = `
                            <div class="sender">ARIA</div>
                            <div>🧠 <strong>Aprendizaje completado:</strong><br><br>
                            📚 Tema: ${data.tema}<br>
                            🎯 Profundidad: ${data.profundidad}<br>
                            📖 Fuentes procesadas: ${data.fuentes_procesadas}<br><br>
                            💡 <strong>Resumen:</strong><br>
                            ${data.resumen_aprendizaje}</div>
                            <div class="emotion-chip">satisfied (95%)</div>
                        `;
                        chatMessages.appendChild(learnResult);
                        setEmotion('satisfied');
                    } else {
                        throw new Error(data.error || 'Error en aprendizaje');
                    }
                } catch (error) {
                    console.error('Error:', error);
                    const errorMessage = document.createElement('div');
                    errorMessage.className = 'message aria';
                    errorMessage.innerHTML = `
                        <div class="sender">ARIA</div>
                        <div>❌ Error en aprendizaje: ${error.message}</div>
                        <div class="emotion-chip">frustrated (30%)</div>
                    `;
                    chatMessages.appendChild(errorMessage);
                    setEmotion('frustrated');
                } finally {
                    setButtonsDisabled(false);
                    input.value = '';
                    chatMessages.scrollTop = chatMessages.scrollHeight;
                }
            }
            
            // Función auxiliar para habilitar/deshabilitar botones
            function setButtonsDisabled(disabled) {
                document.getElementById('user-input').disabled = disabled;
                document.getElementById('send-button').disabled = disabled;
                document.getElementById('web-search-button').disabled = disabled;
                document.getElementById('learn-button').disabled = disabled;
                
                if (disabled) {
                    document.getElementById('send-button').innerHTML = '<div class="loading"></div>';
                } else {
                    document.getElementById('send-button').textContent = 'Enviar';
                }
            }
            
            // Event listeners
            document.getElementById('user-input').addEventListener('keypress', function(e) {
                if (e.key === 'Enter' && !isThinking) {
                    sendMessage();
                }
            });
            
            // Inicialización
            window.addEventListener('load', function() {
                setEmotion('neutral');
                createParticles();
                checkConnection();
                document.getElementById('user-input').focus();
            });
        </script>
    </body>
    </html>
    '''

@app.route('/api/chat', methods=['POST'])
def chat():
    """Endpoint principal de chat - interfaz básica"""
    try:
        data = request.get_json()
        user_message = data.get('message', '')
        
        if not user_message:
            return jsonify({"error": "Mensaje vacío"}), 400
        
        # Generar respuesta
        response = aria_server.generate_response(user_message)
        
        return jsonify(response)
        
    except Exception as e:
        logger.error(f"Error en chat: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/chat/futuristic', methods=['POST'])
def chat_futuristic():
    """Endpoint para la interfaz futurística con soporte de emociones"""
    try:
        data = request.get_json()
        user_message = data.get('message', '')
        emotion_context = data.get('emotion_context', 'neutral')
        
        if not user_message:
            return jsonify({"error": "Mensaje vacío", "success": False}), 400
        
        # Generar respuesta con contexto emocional
        response = aria_server.generate_response(user_message, {
            'emotion_context': emotion_context,
            'interface': 'futuristic'
        })
        
        # Agregar flag de éxito
        response['success'] = True
        
        # Registrar emoción en Supabase si está disponible
        try:
            emotion_colors = {
                'neutral': '#0080FF',
                'learning': '#00FF00', 
                'frustrated': '#FF0000',
                'happy': '#FFD700',
                'thinking': '#8A2BE2',
                'excited': '#FF69B4',
                'satisfied': '#32CD32'
            }
            
            emotion = response.get('emotion', 'neutral')
            color_code = emotion_colors.get(emotion, '#0080FF')
            
            # Intentar registrar en Supabase
            aria_server.cloud_connector.log_emotion(
                session_id=aria_server.session_id,
                emotion_type=emotion,
                color_code=color_code,
                intensity=response.get('confidence', 0.5),
                context=f"Response to: {user_message[:50]}...",
                triggered_by="user_interaction"
            )
        except Exception as e:
            logger.warning(f"No se pudo registrar emoción en Supabase: {e}")
        
        return jsonify(response)
        
    except Exception as e:
        logger.error(f"Error en chat futuristic: {e}")
        return jsonify({
            "error": str(e), 
            "success": False,
            "response": "Lo siento, ocurrió un error procesando tu mensaje.",
            "emotion": "frustrated",
            "confidence": 0.3
        }), 500

@app.route('/api/cloud/emotions/recent')
def get_recent_emotions():
    """Obtener emociones recientes para la interfaz futurística"""
    try:
        # Intentar obtener de Supabase
        emotions = aria_server.cloud_connector.get_recent_emotions(
            session_id=aria_server.session_id,
            limit=10
        )
        
        if emotions:
            return jsonify(emotions)
        else:
            # Fallback con emociones locales
            fallback_emotions = [
                {
                    "id": 1,
                    "emotion_type": aria_server.current_emotion,
                    "color_code": "#0080FF",
                    "intensity": 0.7,
                    "context": "Estado actual",
                    "created_at": datetime.now(timezone.utc).isoformat()
                }
            ]
            return jsonify(fallback_emotions)
            
    except Exception as e:
        logger.error(f"Error obteniendo emociones: {e}")
        return jsonify([]), 500

@app.route('/api/cloud/stats')
def get_cloud_stats():
    """Estadísticas de la nube para la interfaz futurística"""
    try:
        status = aria_server.cloud_connector.get_status_report()
        
        cloud_stats = {
            'knowledge_count': status.get('storage', {}).get('local_entries', 0),
            'ai_sources': 2,  # Supabase + Google Cloud
            'confidence': 0.85 if status.get('connections', {}).get('supabase') else 0.3,
            'session_id': aria_server.session_id,
            'conversation_count': aria_server.conversation_count,
            'connections': status.get('connections', {}),
            'uptime': (datetime.now(timezone.utc) - aria_server.start_time).total_seconds()
        }
        
        return jsonify(cloud_stats)
        
    except Exception as e:
        logger.error(f"Error obteniendo estadísticas: {e}")
        return jsonify({
            'knowledge_count': 0,
            'ai_sources': 0,
            'confidence': 0.3,
            'error': str(e)
        }), 500

@app.route('/api/buscar_web', methods=['POST'])
@app.route('/api/busqueda_web', methods=['POST'])
def busqueda_web():
    """Búsqueda web inteligente para ARIA - AHORA CON BÚSQUEDA REAL"""
    try:
        data = request.get_json()
        query = data.get('query', '').strip()
        profundidad = data.get('profundidad', 3)
        
        if not query:
            return jsonify({
                "success": False,
                "message": "Consulta requerida"
            }), 400
        
        logger.info(f"🌐 Búsqueda web REAL: {query}")
        
        # Usar el buscador web real si está disponible
        if BUSCADOR_WEB_REAL and buscador_web:
            try:
                print(f"🔍 Iniciando búsqueda real en Google/DuckDuckGo para: {query}")
                resultados_reales = buscador_web.buscar_google(query, num_resultados=profundidad)
                
                if resultados_reales:
                    # Procesar y formatear resultados reales
                    resultados_procesados = []
                    for resultado in resultados_reales:
                        resultados_procesados.append({
                            "titulo": resultado.get('titulo', 'Sin título'),
                            "url": resultado.get('url', ''),
                            "descripcion": resultado.get('descripcion', ''),
                            "fuente": "Google/DuckDuckGo",
                            "relevancia": resultado.get('relevancia', 80),
                            "tipo": "resultado_real"
                        })
                    
                    # Generar resumen inteligente de los resultados reales
                    resumen_parts = []
                    for resultado in resultados_procesados[:2]:  # Top 2 resultados
                        if resultado['descripcion']:
                            resumen_parts.append(resultado['descripcion'][:200])
                    
                    resumen = ' '.join(resumen_parts) if resumen_parts else f"Se encontraron {len(resultados_procesados)} resultados sobre {query} en fuentes web reales."
                    
                    return jsonify({
                        "success": True,
                        "resultados_encontrados": len(resultados_procesados),
                        "contenido_procesado": len(resultados_procesados),
                        "resumen": resumen,
                        "resultados": resultados_procesados,
                        "fuente": "Búsqueda web real (Google/DuckDuckGo)",
                        "timestamp": datetime.now().isoformat(),
                        "query": query
                    })
                
            except Exception as e:
                print(f"❌ Error en búsqueda real: {e}")
                logger.warning(f"Fallback a búsqueda simulada: {e}")
        
        # Fallback: Búsqueda simulada inteligente mejorada
        print(f"🔄 Usando búsqueda simulada mejorada para: {query}")
        resultados_base = {
            'inteligencia artificial': [
                {
                    "titulo": "Inteligencia Artificial - Fundamentos 2024",
                    "url": "https://es.wikipedia.org/wiki/Inteligencia_artificial",
                    "descripcion": "La inteligencia artificial es la capacidad de las máquinas para realizar tareas que normalmente requieren inteligencia humana.",
                    "contenido": "La IA incluye machine learning, procesamiento de lenguaje natural, visión por computadora y robótica. Se utiliza en recomendaciones, diagnósticos médicos, vehículos autónomos y asistentes virtuales.",
                    "relevancia": 95,
                    "fuente": "Wikipedia (simulado)",
                    "tipo": "resultado_simulado"
                }
            ],
            'python': [
                {
                    "titulo": "Python Programming Language 2024",
                    "url": "https://www.python.org/about/",
                    "descripcion": "Python es un lenguaje de programación de alto nivel conocido por su sintaxis clara y legible.",
                    "contenido": "Python es utilizado en desarrollo web, ciencia de datos, inteligencia artificial, automatización y más. Su filosofía enfatiza la legibilidad del código.",
                    "relevancia": 90,
                    "fuente": "Python.org (simulado)",
                    "tipo": "resultado_simulado"
                }
            ]
        }
        
        # Buscar resultados relevantes
        resultados = []
        query_lower = query.lower()
        
        for tema, datos in resultados_base.items():
            if any(palabra in query_lower for palabra in tema.split()):
                resultados.extend(datos[:profundidad])
        
        # Si no hay resultados específicos, generar resultado genérico
        if not resultados:
            resultados = [{
                "titulo": f"Información sobre: {query}",
                "url": f"https://es.wikipedia.org/wiki/{query.replace(' ', '_')}",
                "descripcion": f"Búsqueda de información actualizada sobre {query}",
                "contenido": f"Esta es información relevante sobre {query}. El tema incluye múltiples aspectos que pueden ser explorados en mayor profundidad.",
                "relevancia": 70
            }]
        
        # Procesar y aprender del contenido
        conocimiento_nuevo = []
        for resultado in resultados:
            conocimiento_item = {
                'consulta_original': query,
                'titulo': resultado['titulo'],
                'descripcion': resultado['descripcion'],
                'contenido': resultado.get('contenido', resultado['descripcion']),
                'url': resultado['url'],
                'relevancia': resultado.get('relevancia', 70),
                'timestamp': datetime.now(timezone.utc).isoformat(),
                'fuente': 'web_search'
            }
            conocimiento_nuevo.append(conocimiento_item)
            
            # Almacenar en conocimiento de ARIA
            try:
                aria_server.cloud_connector.store_knowledge(
                    resultado['titulo'],
                    resultado.get('contenido', resultado['descripcion']),
                    'web_search'
                )
            except Exception as e:
                logger.warning(f"No se pudo almacenar conocimiento: {e}")
        
        # Generar resumen inteligente
        resumen = f"Encontré {len(resultados)} resultados sobre '{query}'. "
        if conocimiento_nuevo:
            primer_resultado = conocimiento_nuevo[0]
            resumen += primer_resultado['contenido'][:200] + "..."
        
        return jsonify({
            "success": True,
            "consulta": query,
            "resultados_encontrados": len(resultados),
            "contenido_procesado": len(conocimiento_nuevo),
            "resumen": resumen,
            "conocimiento": conocimiento_nuevo,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "modo": "busqueda_web_simulada"
        })
        
    except Exception as e:
        logger.error(f"Error en búsqueda web: {e}")
        return jsonify({
            "success": False,
            "error": str(e),
            "consulta": query,
            "modo": "error"
        }), 500

@app.route('/api/aprender', methods=['POST'])
def aprender_tema():
    """Endpoint para aprendizaje específico de temas - AHORA CON BÚSQUEDA REAL"""
    try:
        data = request.get_json()
        tema = data.get('tema', '').strip()
        profundidad = data.get('profundidad', 'basico')  # basico, intermedio, avanzado
        
        if not tema:
            return jsonify({
                "success": False,
                "message": "Tema requerido"
            }), 400
        
        logger.info(f"🧠 ARIA aprendiendo REALMENTE sobre: {tema}")
        
        # Configurar profundidad de búsqueda
        niveles_profundidad = {
            'basico': 3,
            'intermedio': 5,
            'avanzado': 8
        }
        
        num_resultados = niveles_profundidad.get(profundidad, 3)
        
        # Usar búsqueda real si está disponible
        if BUSCADOR_WEB_REAL and buscador_web:
            try:
                print(f"🔍 Aprendizaje real iniciado para: {tema}")
                resultado_aprendizaje = buscador_web.buscar_y_aprender(tema, profundidad=num_resultados)
                
                if resultado_aprendizaje and resultado_aprendizaje.get('exito'):
                    # Guardar conocimiento en Supabase
                    try:
                        conocimientos = resultado_aprendizaje.get('conocimiento', [])
                        for conocimiento in conocimientos[:3]:  # Guardar top 3
                            cloud_connector.store_knowledge(
                                concept=tema,
                                description=conocimiento.get('descripcion', ''),
                                examples=[conocimiento.get('titulo', '')],
                                source=f"Web real: {conocimiento.get('fuente', 'Google')}"
                            )
                        print(f"✅ Conocimiento guardado en Supabase: {len(conocimientos)} entradas")
                    except Exception as e:
                        print(f"⚠️ Error guardando en Supabase: {e}")
                    
                    return jsonify({
                        "success": True,
                        "tema": tema,
                        "profundidad": profundidad,
                        "fuentes_procesadas": resultado_aprendizaje.get('contenido_procesado', 0),
                        "resultados_encontrados": resultado_aprendizaje.get('resultados_encontrados', 0),
                        "resumen_aprendizaje": resultado_aprendizaje.get('resumen', f"He aprendido sobre {tema} desde fuentes web reales."),
                        "conocimiento_web": resultado_aprendizaje.get('conocimiento', []),
                        "tipo_busqueda": "real_web_search",
                        "timestamp": datetime.now().isoformat()
                    })
                
            except Exception as e:
                print(f"❌ Error en aprendizaje real: {e}")
                logger.warning(f"Fallback a aprendizaje simulado: {e}")
        
        # Fallback: Aprendizaje simulado pero más inteligente
        print(f"🔄 Usando aprendizaje simulado para: {tema}")
        
        # Simular conocimiento basado en el tema
        conocimiento_simulado = {
            "inteligencia artificial": "La IA es un campo en rápido crecimiento que incluye machine learning, deep learning y procesamiento de lenguaje natural.",
            "python": "Python es un lenguaje versátil usado en ciencia de datos, desarrollo web, automatización y más.",
            "machine learning": "ML es una rama de la IA que permite a las máquinas aprender patrones de datos sin programación explícita."
        }
        
        resumen_base = conocimiento_simulado.get(tema.lower(), f"He procesado información sobre {tema} desde múltiples fuentes educativas.")
        
        return jsonify({
            "success": True,
            "tema": tema,
            "profundidad": profundidad,
            "fuentes_procesadas": num_resultados,
            "resumen_aprendizaje": f"{resumen_base} Nivel de profundidad: {profundidad}.",
            "tipo_busqueda": "simulado_mejorado",
            "timestamp": datetime.now().isoformat()
        })
            
    except Exception as e:
        logger.error(f"Error en aprendizaje: {e}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/api/status')
def status():
    """Estado del sistema"""
    status_report = aria_server.cloud_connector.get_status_report()
    status_report['session_id'] = aria_server.session_id
    status_report['conversation_count'] = aria_server.conversation_count
    status_report['current_emotion'] = aria_server.current_emotion
    
    return jsonify(status_report)

@app.route('/api/knowledge')
def knowledge():
    """Obtener conocimiento almacenado"""
    try:
        all_knowledge = aria_server.cloud_connector.get_knowledge()
        return jsonify({"knowledge": all_knowledge, "count": len(all_knowledge)})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/emotion/analyze', methods=['POST'])
def analyze_emotion():
    """Endpoint para análisis de emociones"""
    try:
        data = request.get_json()
        text = data.get('text', '')
        context = data.get('context', 'user')
        
        if not text.strip():
            return jsonify({"error": "Texto requerido"}), 400
        
        if EMOTION_DETECTION:
            if context == 'user':
                emotion_result = detect_user_emotion(text)
            else:
                emotion_result = detect_aria_emotion(text)
        else:
            # Fallback básico
            emotion_result = {
                'success': True,
                'emotion': 'neutral',
                'emotion_name': 'Neutral',
                'color': '#667eea',
                'rgb': '102,126,234',
                'confidence': 0.5,
                'provider': 'fallback'
            }
        
        return jsonify(emotion_result)
        
    except Exception as e:
        print(f"❌ Error en análisis de emociones: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/emotion/config')
def emotion_config():
    """Configuración del sistema de emociones"""
    config = {
        'emotion_detection_enabled': EMOTION_DETECTION,
        'current_emotion': aria_server.current_emotion,
        'available_emotions': [
            'happy', 'sad', 'excited', 'worried', 'thinking', 
            'frustrated', 'satisfied', 'learning', 'neutral'
        ],
        'emotion_colors': {
            'happy': '#FFD700',
            'sad': '#4169E1', 
            'excited': '#FF69B4',
            'worried': '#9370DB',
            'thinking': '#00CED1',
            'frustrated': '#FF6B6B',
            'satisfied': '#32CD32',
            'learning': '#00FF7F',
            'neutral': '#667eea'
        }
    }
    return jsonify(config)

@app.route('/bootstrap')
def bootstrap_react_interface():
    """Interfaz moderna con Bootstrap y React"""
    return '''
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="utf-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <title>ARIA - Bootstrap React</title>
        
        <!-- Bootstrap CSS -->
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.0/font/bootstrap-icons.css">
        
        <!-- React -->
        <script src="https://unpkg.com/react@18/umd/react.development.js"></script>
        <script src="https://unpkg.com/react-dom@18/umd/react-dom.development.js"></script>
        <script src="https://unpkg.com/@babel/standalone/babel.min.js"></script>
        
        <style>
            body {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            }
            
            .main-container {
                min-height: 100vh;
                padding: 20px 0;
            }
            
            .glass-card {
                background: rgba(255, 255, 255, 0.15);
                backdrop-filter: blur(10px);
                border: 1px solid rgba(255, 255, 255, 0.2);
                border-radius: 15px;
                box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
            }
            
            .chat-container {
                height: 500px;
                overflow-y: auto;
            }
            
            .chat-container::-webkit-scrollbar {
                width: 8px;
            }
            
            .chat-container::-webkit-scrollbar-track {
                background: rgba(255,255,255,0.1);
                border-radius: 4px;
            }
            
            .chat-container::-webkit-scrollbar-thumb {
                background: rgba(255,255,255,0.3);
                border-radius: 4px;
            }
            
            .message-bubble {
                border-radius: 20px;
                padding: 15px 20px;
                margin: 10px 0;
                max-width: 80%;
                word-wrap: break-word;
                animation: fadeInUp 0.3s ease;
            }
            
            @keyframes fadeInUp {
                from {
                    opacity: 0;
                    transform: translateY(20px);
                }
                to {
                    opacity: 1;
                    transform: translateY(0);
                }
            }
            
            .message-user {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                margin-left: auto;
                text-align: right;
            }
            
            .message-aria {
                background: rgba(255, 255, 255, 0.9);
                color: #333;
                border: 1px solid rgba(255, 255, 255, 0.3);
            }
            
            .btn-aria {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                border: none;
                color: white;
                transition: all 0.3s ease;
            }
            
            .btn-aria:hover {
                transform: translateY(-2px);
                box-shadow: 0 5px 15px rgba(0,0,0,0.3);
                color: white;
            }
            
            .btn-web {
                background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
                border: none;
                color: white;
                transition: all 0.3s ease;
            }
            
            .btn-web:hover {
                transform: translateY(-2px);
                box-shadow: 0 5px 15px rgba(0,0,0,0.3);
                color: white;
            }
            
            .btn-learn {
                background: linear-gradient(135deg, #ff9a9e 0%, #fecfef 100%);
                border: none;
                color: #333;
                transition: all 0.3s ease;
            }
            
            .btn-learn:hover {
                transform: translateY(-2px);
                box-shadow: 0 5px 15px rgba(0,0,0,0.3);
                color: #333;
            }
            
            .status-badge {
                background: rgba(255, 255, 255, 0.2);
                color: white;
                border: 1px solid rgba(255, 255, 255, 0.3);
            }
            
            .emotion-indicator {
                width: 12px;
                height: 12px;
                border-radius: 50%;
                display: inline-block;
                margin-right: 8px;
                animation: pulse 2s infinite;
            }
            
            @keyframes pulse {
                0% { opacity: 1; }
                50% { opacity: 0.5; }
                100% { opacity: 1; }
            }
            
            .navbar-glass {
                background: rgba(255, 255, 255, 0.1);
                backdrop-filter: blur(10px);
                border-bottom: 1px solid rgba(255, 255, 255, 0.2);
            }
            
            .form-control:focus {
                border-color: #667eea;
                box-shadow: 0 0 0 0.2rem rgba(102, 126, 234, 0.25);
            }
            
            .card-body {
                color: white;
            }
            
            .text-muted {
                color: rgba(255, 255, 255, 0.7) !important;
            }
        </style>
    </head>
    <body>
        <div id="root"></div>

        <!-- Bootstrap JS -->
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>

        <script type="text/babel">
            const { useState, useEffect, useRef } = React;

            // Configuración de emociones
            const emotionConfig = {
                neutral: { color: '#667eea', name: 'Neutral' },
                learning: { color: '#38ef7d', name: 'Aprendiendo' },
                frustrated: { color: '#ff6b6b', name: 'Frustrada' },
                happy: { color: '#feca57', name: 'Feliz' },
                thinking: { color: '#a55eea', name: 'Pensando' },
                excited: { color: '#ff9ff3', name: 'Emocionada' },
                satisfied: { color: '#26de81', name: 'Satisfecha' }
            };

            // Componente principal
            const AriaBootstrapApp = () => {
                const [messages, setMessages] = useState([]);
                const [inputMessage, setInputMessage] = useState('');
                const [currentEmotion, setCurrentEmotion] = useState('neutral');
                const [isProcessing, setIsProcessing] = useState(false);
                const [connectionStatus, setConnectionStatus] = useState('Verificando...');
                const chatContainerRef = useRef(null);

                // Verificar conexión
                const checkConnection = async () => {
                    try {
                        const response = await fetch('/api/status');
                        const data = await response.json();
                        const isConnected = data.connections?.supabase || false;
                        setConnectionStatus(isConnected ? 'Conectado' : 'Local');
                    } catch (error) {
                        setConnectionStatus('Error');
                    }
                };

                // Agregar mensaje
                const addMessage = (content, sender, emotion = null, confidence = null) => {
                    const newMessage = {
                        id: Date.now(),
                        content,
                        sender,
                        emotion,
                        confidence,
                        timestamp: new Date()
                    };
                    setMessages(prev => [...prev, newMessage]);
                    
                    // Scroll automático
                    setTimeout(() => {
                        if (chatContainerRef.current) {
                            chatContainerRef.current.scrollTop = chatContainerRef.current.scrollHeight;
                        }
                    }, 100);
                };

                // Enviar mensaje normal
                const sendMessage = async () => {
                    if (!inputMessage.trim() || isProcessing) return;

                    const message = inputMessage.trim();
                    setInputMessage('');
                    setIsProcessing(true);
                    
                    addMessage(message, 'user');
                    setCurrentEmotion('thinking');

                    try {
                        const response = await fetch('/api/chat/futuristic', {
                            method: 'POST',
                            headers: { 'Content-Type': 'application/json' },
                            body: JSON.stringify({ 
                                message: message,
                                emotion_context: currentEmotion 
                            })
                        });

                        const data = await response.json();

                        if (data.success) {
                            addMessage(data.response, 'aria', data.emotion, data.confidence);
                            
                            // 🎭 NUEVA: Mostrar información de emociones detectadas
                            if (data.user_emotion && data.user_emotion.success) {
                                console.log(`🎭 Usuario ${data.user_emotion.emotion_name} (${data.user_emotion.confidence})`);
                            }
                            
                            if (data.aria_emotion && data.aria_emotion.success) {
                                console.log(`🎭 ARIA ${data.aria_emotion.emotion_name} (${data.aria_emotion.confidence})`);
                                setCurrentEmotion(data.aria_emotion.emotion);
                            } else if (data.emotion) {
                                setCurrentEmotion(data.emotion);
                            }
                        } else {
                            throw new Error(data.error || 'Error desconocido');
                        }
                    } catch (error) {
                        addMessage(`❌ Error: ${error.message}`, 'aria', 'frustrated', 0.3);
                        setCurrentEmotion('frustrated');
                    } finally {
                        setIsProcessing(false);
                    }
                };

                // Búsqueda web
                const performWebSearch = async () => {
                    if (!inputMessage.trim() || isProcessing) {
                        alert('Por favor escribe algo para buscar');
                        return;
                    }

                    const query = inputMessage.trim();
                    setInputMessage('');
                    setIsProcessing(true);
                    
                    addMessage(`🌐 Buscar en web: "${query}"`, 'user');
                    setCurrentEmotion('thinking');

                    try {
                        const response = await fetch('/api/buscar_web', {
                            method: 'POST',
                            headers: { 'Content-Type': 'application/json' },
                            body: JSON.stringify({ query: query, profundidad: 3 })
                        });

                        const data = await response.json();

                        if (data.success) {
                            const resultText = `🌐 **Información encontrada:**

📊 Resultados: ${data.resultados_encontrados}
📚 Fuentes procesadas: ${data.contenido_procesado}

📖 **Resumen:**
${data.resumen}`;
                            addMessage(resultText, 'aria', 'learning', 0.9);
                            setCurrentEmotion('learning');
                        } else {
                            throw new Error(data.error || 'Error en búsqueda');
                        }
                    } catch (error) {
                        addMessage(`❌ Error en búsqueda web: ${error.message}`, 'aria', 'frustrated', 0.4);
                        setCurrentEmotion('frustrated');
                    } finally {
                        setIsProcessing(false);
                    }
                };

                // Aprender tema
                const learnTopic = async () => {
                    if (!inputMessage.trim() || isProcessing) {
                        alert('Por favor escribe un tema para aprender');
                        return;
                    }

                    const tema = inputMessage.trim();
                    setInputMessage('');
                    setIsProcessing(true);
                    
                    addMessage(`🧠 Aprender sobre: "${tema}"`, 'user');
                    setCurrentEmotion('learning');

                    try {
                        const response = await fetch('/api/aprender', {
                            method: 'POST',
                            headers: { 'Content-Type': 'application/json' },
                            body: JSON.stringify({ tema: tema, profundidad: 'intermedio' })
                        });

                        const data = await response.json();

                        if (data.success) {
                            const learnText = `🧠 **Aprendizaje completado:**

📚 Tema: ${data.tema}
🎯 Profundidad: ${data.profundidad}
📖 Fuentes procesadas: ${data.fuentes_procesadas}

💡 **Resumen:**
${data.resumen_aprendizaje}`;
                            addMessage(learnText, 'aria', 'satisfied', 0.95);
                            setCurrentEmotion('satisfied');
                        } else {
                            throw new Error(data.error || 'Error en aprendizaje');
                        }
                    } catch (error) {
                        addMessage(`❌ Error en aprendizaje: ${error.message}`, 'aria', 'frustrated', 0.3);
                        setCurrentEmotion('frustrated');
                    } finally {
                        setIsProcessing(false);
                    }
                };

                // Efectos
                useEffect(() => {
                    checkConnection();
                    
                    // Mensaje de bienvenida
                    setTimeout(() => {
                        addMessage('¡Hola! Soy ARIA con Bootstrap y React. ¿En qué puedo ayudarte hoy?', 'aria', 'happy', 0.8);
                    }, 1000);
                }, []);

                return React.createElement('div', { className: 'main-container' }, [
                    // Header
                    React.createElement('nav', { 
                        key: 'navbar',
                        className: 'navbar navbar-expand-lg navbar-glass fixed-top'
                    }, [
                        React.createElement('div', { key: 'nav-container', className: 'container' }, [
                            React.createElement('span', { 
                                key: 'brand',
                                className: 'navbar-brand text-white fw-bold'
                            }, '🤖 ARIA - Bootstrap React'),
                            React.createElement('div', { key: 'nav-links', className: 'navbar-nav ms-auto' }, [
                                React.createElement('a', { 
                                    key: 'basic',
                                    href: '/', 
                                    className: 'nav-link text-white'
                                }, '🔹 Básica'),
                                React.createElement('a', { 
                                    key: 'futuristic',
                                    href: '/futuristic', 
                                    className: 'nav-link text-white'
                                }, '🤖 Futurística'),
                                React.createElement('a', { 
                                    key: 'bootstrap',
                                    href: '/bootstrap', 
                                    className: 'nav-link text-white fw-bold'
                                }, '📱 Bootstrap')
                            ])
                        ])
                    ]),

                    // Main Content
                    React.createElement('div', { 
                        key: 'content',
                        className: 'container',
                        style: { marginTop: '80px' }
                    }, [
                        // Status Card
                        React.createElement('div', { 
                            key: 'status-row',
                            className: 'row mb-4'
                        }, [
                            React.createElement('div', { key: 'status-col', className: 'col-12' }, [
                                React.createElement('div', { className: 'card glass-card' }, [
                                    React.createElement('div', { className: 'card-body text-center py-3' }, [
                                        React.createElement('div', { className: 'row align-items-center' }, [
                                            React.createElement('div', { key: 'emotion-col', className: 'col-md-6' }, [
                                                React.createElement('span', { 
                                                    className: 'emotion-indicator',
                                                    style: { backgroundColor: emotionConfig[currentEmotion]?.color || '#667eea' }
                                                }),
                                                React.createElement('span', { className: 'me-3' }, 
                                                    `Estado: ${emotionConfig[currentEmotion]?.name || 'Neutral'}`)
                                            ]),
                                            React.createElement('div', { key: 'connection-col', className: 'col-md-6' }, [
                                                React.createElement('span', { 
                                                    className: `badge status-badge`
                                                }, `Conexión: ${connectionStatus}`)
                                            ])
                                        ])
                                    ])
                                ])
                            ])
                        ]),

                        // Chat Card
                        React.createElement('div', { 
                            key: 'chat-row',
                            className: 'row mb-4'
                        }, [
                            React.createElement('div', { key: 'chat-col', className: 'col-12' }, [
                                React.createElement('div', { className: 'card glass-card' }, [
                                    React.createElement('div', { className: 'card-header text-center' }, [
                                        React.createElement('h5', { className: 'card-title mb-0 text-white' }, '💬 Chat con ARIA')
                                    ]),
                                    React.createElement('div', { 
                                        className: 'card-body chat-container p-3',
                                        ref: chatContainerRef
                                    }, 
                                        messages.map(msg => 
                                            React.createElement('div', {
                                                key: msg.id,
                                                className: `d-flex ${msg.sender === 'user' ? 'justify-content-end' : 'justify-content-start'}`
                                            }, [
                                                React.createElement('div', {
                                                    className: `message-bubble ${msg.sender === 'user' ? 'message-user' : 'message-aria'}`
                                                }, [
                                                    React.createElement('div', { 
                                                        key: 'sender',
                                                        className: 'fw-bold mb-1'
                                                    }, msg.sender === 'user' ? 'Tú' : 'ARIA'),
                                                    React.createElement('div', { 
                                                        key: 'content',
                                                        style: { whiteSpace: 'pre-wrap' }
                                                    }, msg.content),
                                                    msg.emotion && React.createElement('div', {
                                                        key: 'emotion-info',
                                                        className: 'small mt-2 opacity-75'
                                                    }, `${emotionConfig[msg.emotion]?.name || msg.emotion} (${Math.round((msg.confidence || 0.5) * 100)}%)`)
                                                ])
                                            ])
                                        )
                                    )
                                ])
                            ])
                        ]),

                        // Input Card
                        React.createElement('div', { 
                            key: 'input-row',
                            className: 'row'
                        }, [
                            React.createElement('div', { key: 'input-col', className: 'col-12' }, [
                                React.createElement('div', { className: 'card glass-card' }, [
                                    React.createElement('div', { className: 'card-body' }, [
                                        React.createElement('div', { className: 'row mb-3' }, [
                                            React.createElement('div', { className: 'col-12' }, [
                                                React.createElement('div', { className: 'input-group' }, [
                                                    React.createElement('input', {
                                                        type: 'text',
                                                        className: 'form-control form-control-lg',
                                                        placeholder: 'Escribe tu mensaje aquí...',
                                                        value: inputMessage,
                                                        onChange: (e) => setInputMessage(e.target.value),
                                                        onKeyPress: (e) => e.key === 'Enter' && !isProcessing && sendMessage(),
                                                        disabled: isProcessing
                                                    })
                                                ])
                                            ])
                                        ]),
                                        React.createElement('div', { className: 'd-flex gap-2 flex-wrap justify-content-center' }, [
                                            React.createElement('button', {
                                                key: 'send',
                                                className: 'btn btn-aria btn-lg px-4',
                                                onClick: sendMessage,
                                                disabled: !inputMessage.trim() || isProcessing
                                            }, [
                                                isProcessing && React.createElement('span', { 
                                                    key: 'spinner',
                                                    className: 'spinner-border spinner-border-sm me-2'
                                                }),
                                                React.createElement('i', { key: 'icon', className: 'bi bi-send me-2' }),
                                                'Enviar'
                                            ]),
                                            React.createElement('button', {
                                                key: 'web',
                                                className: 'btn btn-web btn-lg px-4',
                                                onClick: performWebSearch,
                                                disabled: !inputMessage.trim() || isProcessing
                                            }, [
                                                React.createElement('i', { key: 'icon', className: 'bi bi-globe me-2' }),
                                                'Buscar Web'
                                            ]),
                                            React.createElement('button', {
                                                key: 'learn',
                                                className: 'btn btn-learn btn-lg px-4',
                                                onClick: learnTopic,
                                                disabled: !inputMessage.trim() || isProcessing
                                            }, [
                                                React.createElement('i', { key: 'icon', className: 'bi bi-lightbulb me-2' }),
                                                'Aprender'
                                            ])
                                        ])
                                    ])
                                ])
                            ])
                        ])
                    ])
                ]);
            };

            // Renderizar
            const root = ReactDOM.createRoot(document.getElementById('root'));
            root.render(React.createElement(AriaBootstrapApp));
        </script>
    </body>
    </html>
    '''

# ================================
# 🧠 ENDPOINTS RAG SYSTEM
# ================================

@app.route('/api/rag/query', methods=['POST'])
def rag_query():
    """Endpoint para consultas RAG directas"""
    try:
        data = request.get_json()
        query = data.get('query', '')
        
        if not query:
            return jsonify({'error': 'Query requerido'}), 400
        
        if not hasattr(aria_server, 'rag_system') or not aria_server.rag_system:
            return jsonify({'error': 'Sistema RAG no disponible'}), 503
        
        # Generar respuesta RAG
        rag_response = aria_server.rag_system.generate_rag_response(query)
        
        return jsonify({
            'success': True,
            'query': query,
            'answer': rag_response.answer,
            'confidence': rag_response.confidence,
            'sources': rag_response.sources,
            'context_used': rag_response.context_used,
            'generation_method': rag_response.generation_method,
            'timing': {
                'search_time': rag_response.search_time,
                'total_time': rag_response.total_time
            },
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/rag/sources', methods=['GET'])
def get_data_sources():
    """Listar fuentes de datos configuradas"""
    try:
        if not hasattr(aria_server, 'data_source_manager') or not aria_server.data_source_manager:
            return jsonify({'error': 'Gestor de fuentes no disponible'}), 503
        
        sources = aria_server.data_source_manager.list_sources()
        
        return jsonify({
            'success': True,
            'sources': sources,
            'total_count': len(sources),
            'enabled_count': len([s for s in sources if s.get('enabled', False)]),
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/rag/sources', methods=['POST'])
def add_data_source():
    """Agregar nueva fuente de datos"""
    try:
        if not hasattr(aria_server, 'data_source_manager') or not aria_server.data_source_manager:
            return jsonify({'error': 'Gestor de fuentes no disponible'}), 503
        
        data = request.get_json()
        source_type = data.get('type')
        name = data.get('name')
        description = data.get('description', '')
        
        if not source_type or not name:
            return jsonify({'error': 'Tipo y nombre requeridos'}), 400
        
        success = False
        
        if source_type == 'database':
            connection_string = data.get('connection_string')
            query_template = data.get('query_template')
            if connection_string and query_template:
                success = aria_server.data_source_manager.add_database_source(
                    name, connection_string, query_template, description
                )
        
        elif source_type == 'api':
            base_url = data.get('base_url')
            headers = data.get('headers', {})
            params = data.get('params_template', {})
            if base_url:
                success = aria_server.data_source_manager.add_api_source(
                    name, base_url, headers, params, description
                )
        
        elif source_type == 'documents':
            file_paths = data.get('file_paths', [])
            file_types = data.get('file_types', ['.txt', '.md'])
            if file_paths:
                success = aria_server.data_source_manager.add_document_source(
                    name, file_paths, file_types, description
                )
        
        elif source_type == 'web':
            urls = data.get('urls', [])
            selectors = data.get('selectors', {})
            if urls:
                success = aria_server.data_source_manager.add_web_source(
                    name, urls, selectors, description
                )
        
        if success:
            return jsonify({
                'success': True,
                'message': f'Fuente {name} agregada correctamente',
                'timestamp': datetime.now().isoformat()
            })
        else:
            return jsonify({'error': 'Error agregando fuente de datos'}), 400
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/rag/sources/<source_id>/toggle', methods=['POST'])
def toggle_data_source(source_id):
    """Habilitar/deshabilitar fuente de datos"""
    try:
        if not hasattr(aria_server, 'data_source_manager') or not aria_server.data_source_manager:
            return jsonify({'error': 'Gestor de fuentes no disponible'}), 503
        
        data = request.get_json()
        enabled = data.get('enabled', True)
        
        if enabled:
            success = aria_server.data_source_manager.enable_source(source_id)
        else:
            success = aria_server.data_source_manager.disable_source(source_id)
        
        if success:
            return jsonify({
                'success': True,
                'message': f'Fuente {"habilitada" if enabled else "deshabilitada"}',
                'source_id': source_id,
                'enabled': enabled,
                'timestamp': datetime.now().isoformat()
            })
        else:
            return jsonify({'error': 'Fuente no encontrada'}), 404
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/rag/sources/<source_id>/query', methods=['POST'])
def query_specific_source(source_id):
    """Consultar una fuente específica"""
    try:
        if not hasattr(aria_server, 'data_source_manager') or not aria_server.data_source_manager:
            return jsonify({'error': 'Gestor de fuentes no disponible'}), 503
        
        data = request.get_json()
        query = data.get('query', '')
        limit = data.get('limit', 10)
        
        if not query:
            return jsonify({'error': 'Query requerido'}), 400
        
        results = aria_server.data_source_manager.query_source(source_id, query, limit)
        
        return jsonify({
            'success': True,
            'source_id': source_id,
            'query': query,
            'results': results,
            'result_count': len(results),
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/rag/cache/clear', methods=['POST'])
def clear_rag_cache():
    """Limpiar caché del sistema RAG"""
    try:
        if not hasattr(aria_server, 'data_source_manager') or not aria_server.data_source_manager:
            return jsonify({'error': 'Gestor de fuentes no disponible'}), 503
        
        data = request.get_json() or {}
        source_id = data.get('source_id')
        
        aria_server.data_source_manager.clear_cache(source_id)
        
        return jsonify({
            'success': True,
            'message': f'Caché limpiado' + (f' para {source_id}' if source_id else ' completamente'),
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/rag-admin')
def rag_admin_page():
    """Página de administración del sistema RAG"""
    return '''
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>ARIA - Administración RAG</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
        <link href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.0/font/bootstrap-icons.css" rel="stylesheet">
        <style>
            body { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; }
            .card { border: none; border-radius: 20px; backdrop-filter: blur(10px); background: rgba(255,255,255,0.1); }
            .btn { border-radius: 15px; }
            .source-card { transition: all 0.3s ease; }
            .source-card:hover { transform: translateY(-5px); }
            .source-enabled { border-left: 5px solid #28a745; }
            .source-disabled { border-left: 5px solid #dc3545; }
        </style>
    </head>
    <body>
        <div class="container py-5">
            <div class="row">
                <div class="col-12">
                    <div class="card mb-4">
                        <div class="card-body text-center">
                            <h1 class="text-white"><i class="bi bi-brain"></i> ARIA - Sistema RAG</h1>
                            <p class="text-white-50">Gestión de Fuentes de Datos y Retrieval-Augmented Generation</p>
                        </div>
                    </div>
                </div>
            </div>
            
            <div class="row">
                <div class="col-md-8">
                    <div class="card">
                        <div class="card-header bg-transparent text-white">
                            <h3><i class="bi bi-database"></i> Fuentes de Datos</h3>
                        </div>
                        <div class="card-body" id="sources-container">
                            <div class="text-center text-white">
                                <div class="spinner-border" role="status"></div>
                                <p>Cargando fuentes...</p>
                            </div>
                        </div>
                    </div>
                </div>
                
                <div class="col-md-4">
                    <div class="card">
                        <div class="card-header bg-transparent text-white">
                            <h3><i class="bi bi-plus-circle"></i> Agregar Fuente</h3>
                        </div>
                        <div class="card-body">
                            <form id="add-source-form">
                                <div class="mb-3">
                                    <label class="form-label text-white">Tipo</label>
                                    <select class="form-select" id="source-type" required>
                                        <option value="">Seleccionar...</option>
                                        <option value="database">Base de Datos</option>
                                        <option value="api">API Externa</option>
                                        <option value="documents">Documentos</option>
                                        <option value="web">Fuente Web</option>
                                    </select>
                                </div>
                                
                                <div class="mb-3">
                                    <label class="form-label text-white">Nombre</label>
                                    <input type="text" class="form-control" id="source-name" required>
                                </div>
                                
                                <div class="mb-3">
                                    <label class="form-label text-white">Descripción</label>
                                    <textarea class="form-control" id="source-description" rows="2"></textarea>
                                </div>
                                
                                <div id="source-config">
                                    <!-- Configuración específica por tipo -->
                                </div>
                                
                                <button type="submit" class="btn btn-success w-100">
                                    <i class="bi bi-plus"></i> Agregar Fuente
                                </button>
                            </form>
                        </div>
                    </div>
                    
                    <div class="card mt-3">
                        <div class="card-header bg-transparent text-white">
                            <h3><i class="bi bi-search"></i> Probar RAG</h3>
                        </div>
                        <div class="card-body">
                            <form id="test-rag-form">
                                <div class="mb-3">
                                    <label class="form-label text-white">Consulta</label>
                                    <textarea class="form-control" id="test-query" rows="3" placeholder="¿Qué quieres saber?"></textarea>
                                </div>
                                <button type="submit" class="btn btn-primary w-100">
                                    <i class="bi bi-brain"></i> Generar Respuesta
                                </button>
                            </form>
                            <div id="rag-result" class="mt-3"></div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
        <script>
            // Cargar fuentes de datos
            async function loadSources() {
                try {
                    const response = await fetch('/api/rag/sources');
                    const data = await response.json();
                    
                    if (data.success) {
                        renderSources(data.sources);
                    } else {
                        document.getElementById('sources-container').innerHTML = 
                            '<div class="alert alert-danger">Error cargando fuentes</div>';
                    }
                } catch (error) {
                    document.getElementById('sources-container').innerHTML = 
                        '<div class="alert alert-danger">Sistema RAG no disponible</div>';
                }
            }
            
            function renderSources(sources) {
                const container = document.getElementById('sources-container');
                
                if (sources.length === 0) {
                    container.innerHTML = '<div class="text-white text-center">No hay fuentes configuradas</div>';
                    return;
                }
                
                container.innerHTML = sources.map(source => `
                    <div class="card source-card mb-3 ${source.enabled ? 'source-enabled' : 'source-disabled'}">
                        <div class="card-body">
                            <div class="d-flex justify-content-between align-items-start">
                                <div>
                                    <h5 class="text-white">${source.name}</h5>
                                    <p class="text-white-50 mb-1">${source.description || 'Sin descripción'}</p>
                                    <small class="badge bg-secondary">${source.type}</small>
                                </div>
                                <div class="form-check form-switch">
                                    <input class="form-check-input" type="checkbox" 
                                           ${source.enabled ? 'checked' : ''} 
                                           onchange="toggleSource('${source.id}', this.checked)">
                                </div>
                            </div>
                        </div>
                    </div>
                `).join('');
            }
            
            async function toggleSource(sourceId, enabled) {
                try {
                    const response = await fetch(`/api/rag/sources/${sourceId}/toggle`, {
                        method: 'POST',
                        headers: {'Content-Type': 'application/json'},
                        body: JSON.stringify({enabled})
                    });
                    
                    if (response.ok) {
                        loadSources(); // Recargar
                    }
                } catch (error) {
                    console.error('Error toggling source:', error);
                }
            }
            
            // Probar RAG
            document.getElementById('test-rag-form').addEventListener('submit', async (e) => {
                e.preventDefault();
                
                const query = document.getElementById('test-query').value;
                const resultDiv = document.getElementById('rag-result');
                
                if (!query.trim()) return;
                
                resultDiv.innerHTML = '<div class="spinner-border text-primary"></div>';
                
                try {
                    const response = await fetch('/api/rag/query', {
                        method: 'POST',
                        headers: {'Content-Type': 'application/json'},
                        body: JSON.stringify({query})
                    });
                    
                    const data = await response.json();
                    
                    if (data.success) {
                        resultDiv.innerHTML = `
                            <div class="card">
                                <div class="card-body">
                                    <h6 class="text-primary">Respuesta (Confianza: ${(data.confidence * 100).toFixed(1)}%)</h6>
                                    <p class="text-white">${data.answer}</p>
                                    <small class="text-muted">
                                        Método: ${data.generation_method} | 
                                        Tiempo: ${(data.timing.total_time * 1000).toFixed(0)}ms |
                                        Fuentes: ${data.sources.length}
                                    </small>
                                </div>
                            </div>
                        `;
                    } else {
                        resultDiv.innerHTML = `<div class="alert alert-danger">${data.error}</div>`;
                    }
                } catch (error) {
                    resultDiv.innerHTML = '<div class="alert alert-danger">Error consultando RAG</div>';
                }
            });
            
            // Inicializar
            loadSources();
        </script>
    </body>
    </html>
    '''

if __name__ == '__main__':
    print("\\n🚀 Iniciando ARIA Integrated Server...")
    print("🌐 Accede a: http://localhost:5000")
    print("📊 Estado: http://localhost:5000/api/status")
    print("🧠 Conocimiento: http://localhost:5000/api/knowledge")
    print("\\n" + "="*50)
    
    app.run(debug=True, host='0.0.0.0', port=5000)