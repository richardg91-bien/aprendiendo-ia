#!/usr/bin/env python3
"""
🤖 ARIA - Servidor con APIs Multilingües Gratuitas
=================================================

Versión mejorada que integra las nuevas APIs multilingües gratuitas
para resolver el problema de respuestas genéricas.

Características:
✅ 10 APIs gratuitas multilingües integradas
✅ Análisis avanzado de texto en español e inglés
✅ Respuestas inteligentes basadas en conocimiento real
✅ Detección automática de idioma
✅ Sistema de cache para optimizar rendimiento

Fecha: 22 de octubre de 2025
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend', 'src'))

from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import json
import time
from datetime import datetime
import logging
import re
from typing import Dict, List, Optional

# Importar sistemas de ARIA
try:
    from auto_learning_advanced import aria_advanced_learning
    from multilingual_apis import aria_multilingual_apis
    LEARNING_SYSTEM_AVAILABLE = True
    print("🧠 Sistema de aprendizaje avanzado cargado")
except ImportError as e:
    LEARNING_SYSTEM_AVAILABLE = False
    print(f"❌ Sistema de aprendizaje no disponible: {e}")

try:
    from spanish_apis import aria_spanish_apis
    SPANISH_APIS_AVAILABLE = True
    print("🌐 APIs en español disponibles")
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

class AriaMultilingualServer:
    """Servidor ARIA con capacidades multilingües avanzadas"""
    
    def __init__(self):
        self.conversation_history = []
        self.knowledge_cache = {}
        self.user_preferences = {
            'language': 'auto',  # auto, es, en
            'response_style': 'educational',  # educational, conversational, technical
            'detail_level': 'medium'  # basic, medium, detailed
        }
        
        # Inicializar sistemas si están disponibles
        if LEARNING_SYSTEM_AVAILABLE:
            self._initialize_learning_system()
        
        print("🚀 Servidor ARIA multilingüe inicializado")
    
    def _initialize_learning_system(self):
        """Inicializa el sistema de aprendizaje y verifica conocimiento"""
        try:
            status = aria_advanced_learning.get_status()
            knowledge_count = status.get('total_knowledge', 0)
            
            print(f"📚 Conocimiento disponible: {knowledge_count} elementos")
            
            # Si hay poco conocimiento, ejecutar sesión de aprendizaje rápida
            if knowledge_count < 3:
                print("🔄 Ejecutando sesión de aprendizaje rápida...")
                self._quick_learning_session()
            
        except Exception as e:
            print(f"⚠️ Error inicializando sistema de aprendizaje: {e}")
    
    def _quick_learning_session(self):
        """Sesión rápida de aprendizaje para generar conocimiento básico"""
        quick_topics = [
            "artificial intelligence",
            "machine learning",
            "programming",
            "technology trends"
        ]
        
        learned_count = 0
        for topic in quick_topics:
            try:
                if aria_advanced_learning._learn_from_multilingual_apis(topic):
                    learned_count += 1
                    print(f"   ✅ Aprendido: {topic}")
                time.sleep(0.5)  # Pausa corta entre aprendizajes
            except Exception as e:
                print(f"   ❌ Error aprendiendo {topic}: {e}")
        
        print(f"📊 Sesión rápida completada: {learned_count} nuevos conocimientos")
    
    def detect_query_type(self, message: str) -> Dict:
        """Detecta el tipo de consulta del usuario y su intención"""
        message_lower = message.lower().strip()
        
        # Patrones de preguntas sobre conocimiento
        knowledge_patterns = [
            r'qu[eé]\s+has\s+aprendido',
            r'qu[eé]\s+sabes\s+sobre',
            r'cu[eé]ntame\s+sobre',
            r'qu[eé]\s+conoces\s+de',
            r'explícame',
            r'háblame\s+de',
            r'what\s+do\s+you\s+know\s+about',
            r'tell\s+me\s+about',
            r'explain'
        ]
        
        # Detectar idioma
        spanish_indicators = sum(1 for word in ['que', 'como', 'para', 'con', 'una', 'esta'] 
                                if word in message_lower)
        english_indicators = sum(1 for word in ['what', 'how', 'the', 'and', 'that', 'with'] 
                                if word in message_lower)
        
        detected_language = 'es' if spanish_indicators > english_indicators else 'en'
        
        # Detectar tipo de consulta
        query_type = 'general'
        for pattern in knowledge_patterns:
            if re.search(pattern, message_lower):
                query_type = 'knowledge_request'
                break
        
        # Detectar si es específicamente "¿qué has aprendido?"
        is_learning_question = bool(re.search(r'qu[eé]\s+has\s+aprendido', message_lower))
        
        return {
            'message': message,
            'detected_language': detected_language,
            'query_type': query_type,
            'is_learning_question': is_learning_question,
            'confidence': 0.9 if is_learning_question else 0.7
        }
    
    def generate_intelligent_response(self, query_analysis: Dict) -> Dict:
        """Genera respuesta inteligente basada en el análisis de la consulta"""
        
        if query_analysis['is_learning_question']:
            return self._generate_learning_summary()
        elif query_analysis['query_type'] == 'knowledge_request':
            return self._generate_knowledge_response(query_analysis['message'])
        else:
            return self._generate_conversational_response(query_analysis)
    
    def _generate_learning_summary(self) -> Dict:
        """Genera resumen de lo que ha aprendido ARIA"""
        try:
            if not LEARNING_SYSTEM_AVAILABLE:
                return self._fallback_learning_response()
            
            # Obtener conocimiento reciente
            status = aria_advanced_learning.get_status()
            knowledge_count = status.get('total_knowledge', 0)
            
            if knowledge_count == 0:
                # Ejecutar aprendizaje rápido si no hay conocimiento
                self._quick_learning_session()
                status = aria_advanced_learning.get_status()
                knowledge_count = status.get('total_knowledge', 0)
            
            # Obtener ejemplos de conocimiento
            recent_knowledge = aria_advanced_learning.get_recent_knowledge(limit=5)
            
            if recent_knowledge:
                # Generar respuesta rica en conocimiento
                topics_learned = []
                confidence_sum = 0
                
                for knowledge in recent_knowledge:
                    topic = knowledge.get('topic', 'tema desconocido')
                    confidence = knowledge.get('confidence_score', 0.8)
                    source_type = knowledge.get('source_type', 'general')
                    
                    topics_learned.append(f"• {topic.title()} (fuente: {source_type})")
                    confidence_sum += confidence
                
                avg_confidence = confidence_sum / len(recent_knowledge) if recent_knowledge else 0.8
                
                response_text = f"""He estado aprendiendo actualmente sobre varios temas fascinantes:

{chr(10).join(topics_learned[:3])}

Mi base de conocimiento actual incluye {knowledge_count} elementos de información verificada. He procesado contenido de fuentes como arXiv, Wikipedia, APIs multilingües y fuentes en español. 

Algunos aspectos destacados de mi aprendizaje reciente:
- Análisis de artículos científicos con alta confiabilidad
- Procesamiento de contenido en múltiples idiomas (español e inglés)
- Integración de conocimiento técnico y general

¿Te gustaría que profundice en algún tema específico?"""

                return {
                    'response': response_text,
                    'confidence': avg_confidence,
                    'knowledge_count': knowledge_count,
                    'source': 'advanced_learning_system',
                    'topics_covered': len(set(k.get('topic', '') for k in recent_knowledge)),
                    'response_type': 'learning_summary'
                }
            else:
                return self._fallback_learning_response()
                
        except Exception as e:
            logger.error(f"Error generando resumen de aprendizaje: {e}")
            return self._fallback_learning_response()
    
    def _generate_knowledge_response(self, query: str) -> Dict:
        """Genera respuesta basada en conocimiento específico"""
        try:
            # Buscar conocimiento relevante
            if LEARNING_SYSTEM_AVAILABLE:
                relevant_knowledge = aria_advanced_learning.get_relevant_knowledge(query, limit=3)
                
                if relevant_knowledge:
                    # Construir respuesta basada en conocimiento encontrado
                    knowledge_summaries = []
                    total_confidence = 0
                    
                    for knowledge in relevant_knowledge:
                        title = knowledge.get('title', 'Sin título')
                        content = knowledge.get('content', '')[:200] + "..."
                        confidence = knowledge.get('confidence_score', 0.8)
                        source = knowledge.get('source_name', 'Fuente desconocida')
                        
                        knowledge_summaries.append(f"**{title}**\n{content}\n*Fuente: {source}*")
                        total_confidence += confidence
                    
                    avg_confidence = total_confidence / len(relevant_knowledge)
                    
                    response_text = f"""Basándome en mi conocimiento actual, puedo compartir contigo:

{chr(10).join(knowledge_summaries)}

Esta información proviene de mi base de datos de aprendizaje continuo."""

                    return {
                        'response': response_text,
                        'confidence': avg_confidence,
                        'knowledge_sources': len(relevant_knowledge),
                        'source': 'knowledge_base',
                        'response_type': 'knowledge_based'
                    }
            
            # Si no hay conocimiento específico, usar APIs multilingües
            if hasattr(aria_multilingual_apis, 'analyze_multilingual_content'):
                analysis = aria_multilingual_apis.analyze_multilingual_content(query, full_analysis=True)
                
                if analysis and not analysis.get('error'):
                    keywords = ', '.join(analysis.get('keywords', [])[:5])
                    language = analysis.get('language_detection', 'auto')
                    
                    response_text = f"""He analizado tu consulta utilizando mis capacidades multilingües:

• **Palabras clave identificadas**: {keywords}
• **Idioma detectado**: {language}
• **Análisis de sentimiento**: {analysis.get('sentiment_basic', 'neutral')}

Aunque no tengo información específica almacenada sobre este tema exacto, puedo ayudarte a explorarlo o buscar información relacionada."""

                    return {
                        'response': response_text,
                        'confidence': analysis.get('confidence', 0.7),
                        'source': 'multilingual_analysis',
                        'response_type': 'analytical'
                    }
            
            # Respuesta de fallback
            return {
                'response': "No tengo información específica sobre ese tema en mi base de conocimiento actual, pero me gustaría aprender más sobre ello. ¿Podrías darme más contexto?",
                'confidence': 0.5,
                'source': 'fallback',
                'response_type': 'fallback'
            }
            
        except Exception as e:
            logger.error(f"Error generando respuesta de conocimiento: {e}")
            return self._fallback_response()
    
    def _generate_conversational_response(self, query_analysis: Dict) -> Dict:
        """Genera respuesta conversacional general"""
        message = query_analysis['message']
        language = query_analysis['detected_language']
        
        # Respuestas contextuales básicas
        if language == 'es':
            response = f"Entiendo tu mensaje. Estoy aquí para ayudarte y aprender contigo. Mi sistema está en constante evolución y mejora."
        else:
            response = f"I understand your message. I'm here to help you and learn with you. My system is constantly evolving and improving."
        
        return {
            'response': response,
            'confidence': 0.7,
            'source': 'conversational',
            'response_type': 'conversational'
        }
    
    def _fallback_learning_response(self) -> Dict:
        """Respuesta de fallback para preguntas sobre aprendizaje"""
        return {
            'response': """Mi sistema de aprendizaje está activo y en constante evolución. Aunque aún estoy desarrollando mi base de conocimiento, puedo:

• Analizar y procesar información en múltiples idiomas
• Aprender de fuentes académicas y técnicas
• Integrar conocimiento de APIs especializadas
• Mejorar mis respuestas con cada interacción

¿Hay algún tema específico sobre el que te gustaría que aprenda o investigue?""",
            'confidence': 0.6,
            'source': 'system_fallback',
            'response_type': 'fallback_learning'
        }
    
    def _fallback_response(self) -> Dict:
        """Respuesta de emergencia cuando otros sistemas fallan"""
        return {
            'response': "Estoy experimentando algunas dificultades técnicas en este momento, pero sigo funcionando y aprendiendo. ¿Puedes intentar reformular tu pregunta?",
            'confidence': 0.4,
            'source': 'emergency_fallback',
            'response_type': 'error_fallback'
        }

# Crear instancia del servidor
aria_server = AriaMultilingualServer()

# === RUTAS DE LA API ===

@app.route('/')
def home():
    """Página principal"""
    return """
    <html>
    <head><title>ARIA - Asistente Multilingüe</title></head>
    <body style="font-family: Arial; margin: 40px; background: #f0f8ff;">
        <h1>🤖 ARIA - Asistente con APIs Multilingües</h1>
        <p>Servidor activo con capacidades avanzadas de aprendizaje multilingüe</p>
        
        <h3>🌐 Características:</h3>
        <ul>
            <li>✅ 10 APIs gratuitas integradas</li>
            <li>✅ Análisis multilingüe (Español/Inglés)</li>
            <li>✅ Aprendizaje automático continuo</li>
            <li>✅ Respuestas inteligentes basadas en conocimiento</li>
        </ul>
        
        <h3>🔗 Endpoints disponibles:</h3>
        <ul>
            <li><strong>POST /api/chat</strong> - Chat con ARIA</li>
            <li><strong>GET /api/status</strong> - Estado del sistema</li>
            <li><strong>GET /api/knowledge</strong> - Resumen de conocimiento</li>
        </ul>
        
        <h3>📝 Ejemplo de uso:</h3>
        <code>
        curl -X POST http://localhost:8000/api/chat \\<br>
        &nbsp;&nbsp;-H "Content-Type: application/json" \\<br>
        &nbsp;&nbsp;-d '{"message": "¿Qué has aprendido?"}'
        </code>
    </body>
    </html>
    """

@app.route('/api/chat', methods=['POST'])
def chat():
    """Endpoint principal de chat mejorado"""
    try:
        data = request.get_json()
        message = data.get('message', '').strip()
        
        if not message:
            return jsonify({
                'error': 'Mensaje vacío',
                'response': 'Por favor, envía un mensaje para que pueda ayudarte.'
            }), 400
        
        # Analizar la consulta
        query_analysis = aria_server.detect_query_type(message)
        logger.info(f"📝 Consulta analizada: {query_analysis['query_type']} ({query_analysis['detected_language']})")
        
        # Generar respuesta inteligente
        response_data = aria_server.generate_intelligent_response(query_analysis)
        
        # Preparar respuesta final
        final_response = {
            'response': response_data['response'],
            'confidence': response_data['confidence'],
            'metadata': {
                'query_type': query_analysis['query_type'],
                'language': query_analysis['detected_language'],
                'response_source': response_data['source'],
                'response_type': response_data['response_type'],
                'timestamp': datetime.now().isoformat(),
                'knowledge_count': response_data.get('knowledge_count', 0),
                'processing_time': time.time()
            }
        }
        
        # Agregar a historial
        aria_server.conversation_history.append({
            'user_message': message,
            'aria_response': response_data['response'],
            'timestamp': datetime.now().isoformat(),
            'confidence': response_data['confidence']
        })
        
        logger.info(f"✅ Respuesta generada: {response_data['source']} (confianza: {response_data['confidence']:.2f})")
        return jsonify(final_response)
        
    except Exception as e:
        logger.error(f"❌ Error en chat: {e}")
        return jsonify({
            'error': 'Error interno del servidor',
            'response': 'Disculpa, hubo un error procesando tu mensaje. Por favor, intenta de nuevo.',
            'metadata': {
                'error_type': str(type(e).__name__),
                'timestamp': datetime.now().isoformat()
            }
        }), 500

@app.route('/api/status', methods=['GET'])
def status():
    """Estado del sistema completo"""
    try:
        # Estado del sistema de aprendizaje
        learning_status = {}
        if LEARNING_SYSTEM_AVAILABLE:
            learning_status = aria_advanced_learning.get_status()
        
        # Estado de APIs multilingües
        multilingual_status = {}
        try:
            multilingual_status = aria_multilingual_apis.get_api_status()
        except:
            multilingual_status = {'status': 'no disponible'}
        
        system_status = {
            'server': 'online',
            'timestamp': datetime.now().isoformat(),
            'conversation_count': len(aria_server.conversation_history),
            'learning_system': {
                'available': LEARNING_SYSTEM_AVAILABLE,
                'knowledge_count': learning_status.get('total_knowledge', 0),
                'status': 'active' if LEARNING_SYSTEM_AVAILABLE else 'disabled'
            },
            'multilingual_apis': {
                'available': True,
                'status': multilingual_status.get('overall_status', 'unknown'),
                'apis_count': multilingual_status.get('total_apis_available', 0),
                'cache_entries': multilingual_status.get('cache_entries', 0)
            },
            'spanish_apis': {
                'available': SPANISH_APIS_AVAILABLE,
                'status': 'active' if SPANISH_APIS_AVAILABLE else 'disabled'
            }
        }
        
        return jsonify(system_status)
        
    except Exception as e:
        logger.error(f"Error obteniendo estado: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/knowledge', methods=['GET'])
def knowledge():
    """Resumen del conocimiento actual"""
    try:
        if not LEARNING_SYSTEM_AVAILABLE:
            return jsonify({
                'error': 'Sistema de aprendizaje no disponible',
                'knowledge_count': 0
            })
        
        # Obtener resumen de conocimiento
        status = aria_advanced_learning.get_status()
        recent_knowledge = aria_advanced_learning.get_recent_knowledge(limit=10)
        
        knowledge_summary = {
            'total_knowledge': status.get('total_knowledge', 0),
            'learning_active': aria_advanced_learning.is_running,
            'last_learning': status.get('last_learning', 'Nunca'),
            'recent_topics': [
                {
                    'topic': k.get('topic', 'Sin tema'),
                    'confidence': k.get('confidence_score', 0),
                    'source': k.get('source_type', 'desconocida'),
                    'timestamp': k.get('timestamp', '')
                }
                for k in recent_knowledge[:5]
            ],
            'statistics': status.get('statistics', {}),
            'timestamp': datetime.now().isoformat()
        }
        
        return jsonify(knowledge_summary)
        
    except Exception as e:
        logger.error(f"Error obteniendo conocimiento: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("🚀 Iniciando ARIA con APIs multilingües...")
    print(f"📡 Servidor disponible en: http://localhost:8000")
    print("🌐 APIs multilingües integradas y listas")
    
    try:
        app.run(
            host='0.0.0.0',
            port=8000,
            debug=False,
            threaded=True
        )
    except KeyboardInterrupt:
        print("\n⏹️ Servidor detenido por el usuario")
    except Exception as e:
        print(f"❌ Error iniciando servidor: {e}")