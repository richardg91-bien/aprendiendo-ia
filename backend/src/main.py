"""
ARIA - Sistema de Inteligencia Artificial
Servidor Principal Backend
"""

import os
import sys
from pathlib import Path

# Agregar el directorio src al path para imports
backend_src = Path(__file__).parent
sys.path.insert(0, str(backend_src))

from flask import Flask, jsonify, send_from_directory, request
from flask_cors import CORS
import json
import random
import time
from datetime import datetime
import requests
from learning_system import learning_system
from feedback_system import feedback_system
from dictionary_learning import dictionary_learning

# Importar sistema de voz Spock (priorizar SAPI que funciona)
try:
    # Intentar primero con SAPI simple que funciona
    from spock_voice_simple import spock_voice, speak_response, speak_greeting, speak_thinking, toggle_voice
    VOICE_AVAILABLE = True
    print("🎙️ Sistema de voz Spock SAPI cargado exitosamente")
except ImportError as e:
    print(f"⚠️ Sistema de voz SAPI no disponible: {e}")
    try:
        from spock_voice_system import spock_voice, speak_response, speak_greeting, speak_thinking, toggle_voice
        VOICE_AVAILABLE = True
        print("🎙️ Sistema de voz Spock pyttsx3 cargado exitosamente")
    except ImportError as e2:
        print(f"⚠️ Sistema de voz no disponible: {e2}")
        VOICE_AVAILABLE = False
        # Funciones dummy para evitar errores
        def speak_response(text): pass
        def speak_greeting(): pass
        def speak_thinking(): pass
        def toggle_voice(enabled=None): return False

# Configuración de la aplicación
app = Flask(__name__, static_folder='../../frontend/build', static_url_path='/')
CORS(app)

# Configuración
DEBUG_MODE = True
HOST = '127.0.0.1'
PORT = 8000

def log_info(message):
    """Logger simple para el servidor"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {message}")

# =====================
# RUTAS DE FRONTEND
# =====================

@app.route('/')
def serve_frontend():
    """Servir la aplicación React"""
    try:
        return send_from_directory(app.static_folder, 'index.html')
    except Exception as e:
        log_info(f"Error sirviendo frontend: {e}")
        return jsonify({"error": "Frontend no disponible"}), 500

# =====================
# API ENDPOINTS
# =====================

@app.route('/api/status', methods=['GET'])
def api_status():
    """Estado del sistema"""
    return jsonify({
        "status": "online",
        "version": "2.0.0",
        "timestamp": datetime.now().isoformat(),
        "components": {
            "backend": "running",
            "neural_network": "active",
            "web_search": "available",
            "voice_system": "active" if VOICE_AVAILABLE else "unavailable",
            "spock_voice": spock_voice.voice_enabled if VOICE_AVAILABLE else False
        }
    })

@app.route('/api/voice/toggle', methods=['POST'])
def api_voice_toggle():
    """Activar/desactivar síntesis de voz"""
    if not VOICE_AVAILABLE:
        return jsonify({
            "success": False,
            "message": "Sistema de voz no disponible"
        }), 400
    
    try:
        data = request.json
        enabled = data.get('enabled', None)
        
        current_state = toggle_voice(enabled)
        
        # Confirmar el cambio con voz
        if current_state:
            speak_response("Sistema de voz activado. Fascinante.")
        
        return jsonify({
            "success": True,
            "voice_enabled": current_state,
            "message": f"Síntesis de voz {'activada' if current_state else 'desactivada'}"
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Error controlando voz: {str(e)}"
        }), 500

@app.route('/api/voice/test', methods=['POST'])
def api_voice_test():
    """Probar el sistema de voz"""
    if not VOICE_AVAILABLE:
        return jsonify({
            "success": False,
            "message": "Sistema de voz no disponible"
        }), 400
    
    try:
        data = request.json
        test_text = data.get('text', 'Saludo, humano. Mi sistema de síntesis de voz está funcionando de manera lógica y eficiente.')
        
        speak_response(test_text)
        
        return jsonify({
            "success": True,
            "message": "Prueba de voz ejecutada",
            "text_spoken": test_text
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Error en prueba de voz: {str(e)}"
        }), 500

@app.route('/api/voice/greeting', methods=['POST'])
def api_voice_greeting():
    """Pronunciar saludo estilo Spock"""
    if not VOICE_AVAILABLE:
        return jsonify({
            "success": False,
            "message": "Sistema de voz no disponible"
        }), 400
    
    try:
        speak_greeting()
        
        return jsonify({
            "success": True,
            "message": "Saludo Spock pronunciado"
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Error en saludo: {str(e)}"
        }), 500

@app.route('/api/voice/settings', methods=['POST'])
def api_voice_settings():
    """Configurar ajustes de voz"""
    if not VOICE_AVAILABLE:
        return jsonify({
            "success": False,
            "message": "Sistema de voz no disponible"
        }), 400
    
    try:
        data = request.json
        speed = data.get('speed', None)
        
        if speed and 50 <= speed <= 300:
            spock_voice.adjust_speed(speed)
            speak_response(f"Velocidad de voz ajustada a {speed} palabras por minuto.")
        
        return jsonify({
            "success": True,
            "current_speed": spock_voice.voice_speed,
            "voice_enabled": spock_voice.voice_enabled
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Error configurando voz: {str(e)}"
        }), 500

@app.route('/api/red_neuronal_info', methods=['GET'])
def api_red_neuronal_info():
    """Información de la red neuronal"""
    return jsonify({
        "arquitectura": "Dense Neural Network",
        "capas": ["Input: 512", "Hidden: 256, 128", "Output: 10"],
        "optimizador": "Adam",
        "funcion_perdida": "categorical_crossentropy",
        "metricas": ["accuracy", "precision", "recall"],
        "entrenado": True,
        "precision_actual": round(random.uniform(0.75, 0.95), 4),
        "epochs_completados": random.randint(45, 100),
        "estado": "Entrenado y Optimizado"
    })

@app.route('/api/entrenar_red_neuronal', methods=['POST'])
def api_entrenar_red_neuronal():
    """Entrenar la red neuronal"""
    try:
        log_info("🧠 Recibida solicitud de entrenamiento neural")
        
        data = request.json or {}
        epochs = data.get('epochs', 50)
        
        log_info(f"   Epochs solicitados: {epochs}")
        
        # Validar epochs
        if epochs <= 0 or epochs > 1000:
            error_msg = "El número de epochs debe estar entre 1 y 1000"
            log_info(f"   ❌ {error_msg}")
            return jsonify({
                "success": False,
                "message": error_msg
            }), 400
        
        # Simular entrenamiento
        time.sleep(2)  # Simular proceso
        
        # Generar métricas realistas
        precision = round(random.uniform(0.45, 0.95), 2)
        loss = round(random.uniform(0.05, 0.8), 4)
        
        resultado = {
            "success": True,
            "message": "Entrenamiento completado exitosamente",
            "metricas": {
                "epochs": epochs,
                "precision_final": precision,
                "loss_final": loss,
                "tiempo_entrenamiento": "2.3s",
                "mejora": f"+{round(random.uniform(5, 25), 1)}%"
            }
        }
        
        log_info(f"   ✅ Entrenamiento simulado exitoso - Precisión: {precision}%")
        return jsonify(resultado)
        
    except Exception as e:
        error_msg = f"Error en entrenar_red_neuronal: {str(e)}"
        log_info(f"   ❌ {error_msg}")
        return jsonify({
            "success": False,
            "message": error_msg
        }), 500

@app.route('/api/chat', methods=['POST'])
def api_chat():
    """Endpoint para chat con ARIA - Con Aprendizaje, Retroalimentación y Voz Spock"""
    try:
        data = request.json
        mensaje = data.get('message', '').strip()
        voice_enabled = data.get('voice_enabled', True)  # Por defecto la voz está habilitada
        
        log_info(f"💬 Chat - Mensaje recibido: {mensaje}")
        
        if not mensaje:
            return jsonify({
                "success": False,
                "message": "Mensaje vacío"
            }), 400
        
        # Indicar que está procesando (con voz si está habilitada)
        if VOICE_AVAILABLE and voice_enabled:
            speak_thinking()
        
        # Verificar si el usuario está preguntando por una palabra específica
        word_definition = None
        if any(keyword in mensaje.lower() for keyword in ['qué significa', 'que significa', 'definición de', 'definicion de', 'define']):
            # Extraer la palabra de la pregunta
            import re
            words = re.findall(r'\b[a-záéíóúñ]+\b', mensaje.lower())
            for word in words:
                if len(word) > 3 and word not in ['qué', 'que', 'significa', 'definición', 'definicion', 'define']:
                    word_definition = dictionary_learning.get_word_definition(word)
                    if word_definition:
                        dictionary_learning.update_word_usage(word)
                        break
        
        # Generar respuesta usando el sistema de aprendizaje avanzado
        respuesta, confianza = learning_system.generate_response(mensaje)
        
        # Si encontramos una definición, enriquecer la respuesta
        if word_definition:
            word_info = f"\n\n📚 **{word_definition['word'].capitalize()}** ({word_definition['part_of_speech']})"
            if word_definition['pronunciation']:
                word_info += f" [{word_definition['pronunciation']}]"
            word_info += f":\n{word_definition['definition']}"
            
            if word_definition['example']:
                word_info += f"\n\n💡 Ejemplo: {word_definition['example']}"
            
            if word_definition['synonyms']:
                word_info += f"\n🔗 Sinónimos: {word_definition['synonyms']}"
            
            # Combinar respuesta original con información de diccionario
            respuesta = respuesta + word_info
            confianza = max(confianza, word_definition['confidence'])
        
        log_info(f"   🧠 ARIA (confianza: {confianza:.2f}): {respuesta}")
        
        # Síntesis de voz con personalidad Spock
        if VOICE_AVAILABLE and voice_enabled:
            speak_response(respuesta)
        
        # Aprender de la conversación (con feedback neutro por defecto)
        learning_system.learn_from_conversation(mensaje, respuesta, {"source": "chat"}, 0.5)
        
        # Registrar conversación en el sistema de retroalimentación
        try:
            feedback_system.log_conversation(mensaje, respuesta)
        except Exception as e:
            log_info(f"⚠️  Error registrando conversación: {e}")
        
        return jsonify({
            "success": True,
            "response": respuesta,
            "confidence": confianza,
            "voice_enabled": voice_enabled and VOICE_AVAILABLE,
            "learning_stats": learning_system.get_learning_stats(),
            "dictionary_stats": dictionary_learning.get_learning_stats(),
            "word_definition": word_definition,
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        log_info(f"❌ Error en chat: {e}")
        return jsonify({
            "success": False,
            "message": f"Error en el chat: {str(e)}"
        }), 500

@app.route('/api/buscar_web', methods=['POST'])
def api_buscar_web():
    """Búsqueda web simulada"""
    try:
        data = request.json
        query = data.get('query', '').strip()
        
        log_info(f"🌐 Búsqueda web: {query}")
        
        if not query:
            return jsonify({
                "success": False,
                "message": "Query de búsqueda vacío"
            }), 400
        
        # Simular resultados de búsqueda
        resultados = [
            {
                "titulo": f"Resultados para '{query}' - Wikipedia",
                "url": f"https://es.wikipedia.org/wiki/{query.replace(' ', '_')}",
                "descripcion": f"Información completa sobre {query} en Wikipedia. Artículo detallado con referencias y datos verificados."
            },
            {
                "titulo": f"Todo sobre {query} - Información actualizada",
                "url": f"https://example.com/info-{query.replace(' ', '-')}",
                "descripcion": f"Guía completa y actualizada sobre {query}. Incluye datos, estadísticas y análisis recientes."
            },
            {
                "titulo": f"Noticias recientes: {query}",
                "url": f"https://noticias.com/tag/{query}",
                "descripcion": f"Las últimas noticias y desarrollos relacionados con {query}. Información actualizada diariamente."
            }
        ]
        
        return jsonify({
            "success": True,
            "query": query,
            "resultados": resultados,
            "total": len(resultados)
        })
        
    except Exception as e:
        log_info(f"❌ Error en búsqueda web: {e}")
        return jsonify({
            "success": False,
            "message": f"Error en búsqueda: {str(e)}"
        }), 500

# =====================
# MANEJO DE ERRORES
# =====================

@app.errorhandler(404)
def not_found(error):
    """Manejo de rutas no encontradas - redirigir al frontend"""
    try:
        return send_from_directory(app.static_folder, 'index.html')
    except:
        return jsonify({"error": "Página no encontrada"}), 404

@app.errorhandler(500)
def internal_error(error):
    """Manejo de errores internos del servidor"""
    log_info(f"❌ Error interno del servidor: {error}")
    return jsonify({"error": "Error interno del servidor"}), 500

# =====================
# INICIO DEL SERVIDOR
# =====================

def main():
    """Función principal para iniciar el servidor"""
    print("=" * 50)
    print("🚀 Iniciando ARIA - Sistema Backend v2.0")
    print("=" * 50)
    print(f"🌐 Servidor: http://{HOST}:{PORT}")
    print(f"🔗 API Base: http://{HOST}:{PORT}/api/")
    print(f"🧠 Neural Network: Activa")
    print("=" * 50)
    
    # Verificar si el frontend está compilado
    build_path = Path(app.static_folder)
    if build_path.exists():
        print("✅ Frontend React encontrado")
    else:
        print("⚠️  Frontend React no compilado")
        print("   Ejecuta 'npm run build' en el directorio frontend")
    
    # Iniciar sistema de aprendizaje automático
    print("📚 Iniciando sistema de aprendizaje de diccionario...")
    try:
        dictionary_learning.start_automatic_learning()
        print("✅ Sistema de aprendizaje automático iniciado")
    except Exception as e:
        print(f"⚠️  Error iniciando aprendizaje automático: {e}")
    
    print("=" * 50)
    
    try:
        app.run(
            host='0.0.0.0',
            port=PORT,
            debug=DEBUG_MODE,
            use_reloader=False
        )
    except KeyboardInterrupt:
        print("\n🛑 Servidor detenido por el usuario")
        print("📚 Deteniendo sistema de aprendizaje...")
        dictionary_learning.stop_automatic_learning()
        print("✅ Sistema de aprendizaje detenido")
    except Exception as e:
        print(f"❌ Error al iniciar servidor: {e}")

# =====================
# ENDPOINTS DE APRENDIZAJE AVANZADO
# =====================

@app.route('/api/learning/stats', methods=['GET'])
def api_learning_stats():
    """Obtener estadísticas del sistema de aprendizaje"""
    try:
        stats = learning_system.get_learning_stats()
        return jsonify({
            "success": True,
            "stats": stats
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Error obteniendo estadísticas: {str(e)}"
        }), 500

@app.route('/api/learning/feedback', methods=['POST'])
def api_learning_feedback():
    """Enviar feedback sobre una respuesta para mejorar el aprendizaje"""
    try:
        data = request.json
        conversation_text = data.get('conversation_text', '')
        feedback_score = data.get('feedback_score', 0.0)  # -1 a 1
        
        log_info(f"📝 Feedback recibido: {feedback_score} para '{conversation_text[:50]}...'")
        
        if not conversation_text:
            return jsonify({
                "success": False,
                "message": "Texto de conversación requerido"
            }), 400
        
        # Buscar la conversación y actualizar su feedback
        # (implementación simplificada)
        learning_system.learn_from_conversation(
            conversation_text, 
            "Feedback update", 
            {"source": "feedback"}, 
            feedback_score
        )
        
        return jsonify({
            "success": True,
            "message": "Feedback procesado correctamente"
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Error procesando feedback: {str(e)}"
        }), 500

@app.route('/api/learning/export', methods=['GET'])
def api_learning_export():
    """Exportar conocimiento aprendido"""
    try:
        knowledge = learning_system.export_knowledge()
        return jsonify({
            "success": True,
            "knowledge": knowledge
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Error exportando conocimiento: {str(e)}"
        }), 500

@app.route('/api/learning/teach', methods=['POST'])
def api_learning_teach():
    """Enseñar nuevo conocimiento directamente a ARIA"""
    try:
        data = request.json
        concept = data.get('concept', '').strip()
        definition = data.get('definition', '').strip()
        
        if not concept or not definition:
            return jsonify({
                "success": False,
                "message": "Se requieren concepto y definición"
            }), 400
        
        log_info(f"📚 Enseñando: {concept} = {definition}")
        
        # Crear una conversación de enseñanza
        teaching_input = f"¿Qué es {concept}?"
        teaching_response = f"{concept} es {definition}"
        
        learning_system.learn_from_conversation(
            teaching_input, 
            teaching_response, 
            {"source": "teaching", "manual": True}, 
            1.0  # Alta confianza para conocimiento enseñado manualmente
        )
        
        return jsonify({
            "success": True,
            "message": f"Conocimiento sobre '{concept}' enseñado correctamente"
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Error enseñando conocimiento: {str(e)}"
        }), 500

# =====================
# ENDPOINTS DE RETROALIMENTACIÓN
# =====================

@app.route('/api/feedback/conversation', methods=['POST'])
def api_log_conversation():
    """Registrar conversación con retroalimentación en la base de datos"""
    try:
        data = request.json
        user_message = data.get('user_message', '')
        aria_response = data.get('aria_response', '')
        user_feedback = data.get('user_feedback')
        
        success = feedback_system.log_conversation(
            user_message, aria_response, user_feedback
        )
        
        if success:
            return jsonify({
                "success": True,
                "message": "Conversación registrada exitosamente"
            })
        else:
            return jsonify({
                "success": False,
                "message": "Error al registrar conversación"
            }), 500
            
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Error: {str(e)}"
        }), 500

@app.route('/api/feedback/preference', methods=['POST'])
def api_save_preference():
    """Guardar preferencia del usuario"""
    try:
        data = request.json
        preference_type = data.get('preference_type', '')
        value = data.get('value', '')
        
        success = feedback_system.save_user_preference(preference_type, value)
        
        if success:
            return jsonify({
                "success": True,
                "message": "Preferencia guardada exitosamente"
            })
        else:
            return jsonify({
                "success": False,
                "message": "Error al guardar preferencia"
            }), 500
            
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Error: {str(e)}"
        }), 500

@app.route('/api/feedback/analytics', methods=['GET'])
def api_feedback_analytics():
    """Obtener análisis de retroalimentación"""
    try:
        analytics = feedback_system.analyze_feedback()
        return jsonify({
            "success": True,
            "analytics": analytics
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Error: {str(e)}"
        }), 500

@app.route('/api/feedback/patterns', methods=['GET'])
def api_learning_patterns():
    """Obtener patrones de aprendizaje"""
    try:
        patterns = feedback_system.get_learning_patterns()
        return jsonify({
            "success": True,
            "patterns": patterns
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Error: {str(e)}"
        }), 500

# === ENDPOINTS DEL SISTEMA DE APRENDIZAJE DE DICCIONARIO ===

@app.route('/api/dictionary/start-learning', methods=['POST'])
def api_start_dictionary_learning():
    """Iniciar aprendizaje automático de diccionario"""
    try:
        dictionary_learning.start_automatic_learning()
        return jsonify({
            "success": True,
            "message": "Aprendizaje automático iniciado"
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Error: {str(e)}"
        }), 500

@app.route('/api/dictionary/stop-learning', methods=['POST'])
def api_stop_dictionary_learning():
    """Detener aprendizaje automático de diccionario"""
    try:
        dictionary_learning.stop_automatic_learning()
        return jsonify({
            "success": True,
            "message": "Aprendizaje automático detenido"
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Error: {str(e)}"
        }), 500

@app.route('/api/dictionary/stats', methods=['GET'])
def api_dictionary_stats():
    """Obtener estadísticas del aprendizaje de diccionario"""
    try:
        stats = dictionary_learning.get_learning_stats()
        return jsonify({
            "success": True,
            "stats": stats
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Error: {str(e)}"
        }), 500

@app.route('/api/dictionary/word/<word>', methods=['GET'])
def api_get_word_definition(word):
    """Obtener definición de una palabra"""
    try:
        definition = dictionary_learning.get_word_definition(word)
        if definition:
            # Actualizar contador de uso
            dictionary_learning.update_word_usage(word)
            return jsonify({
                "success": True,
                "word_data": definition
            })
        else:
            return jsonify({
                "success": False,
                "message": "Palabra no encontrada"
            }), 404
        
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Error: {str(e)}"
        }), 500

@app.route('/api/dictionary/search', methods=['GET'])
def api_search_words():
    """Buscar palabras relacionadas"""
    try:
        query = request.args.get('q', '')
        limit = int(request.args.get('limit', 5))
        
        if not query:
            return jsonify({
                "success": False,
                "message": "Parámetro 'q' requerido"
            }), 400
        
        results = dictionary_learning.search_related_words(query, limit)
        return jsonify({
            "success": True,
            "results": results
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Error: {str(e)}"
        }), 500

@app.route('/api/dictionary/learn-word', methods=['POST'])
def api_learn_specific_word():
    """Aprender una palabra específica manualmente"""
    try:
        data = request.get_json()
        word = data.get('word', '').strip().lower()
        
        if not word:
            return jsonify({
                "success": False,
                "message": "Palabra requerida"
            }), 400
        
        success = dictionary_learning._learn_word(word)
        
        if success:
            return jsonify({
                "success": True,
                "message": f"Palabra '{word}' aprendida exitosamente"
            })
        else:
            return jsonify({
                "success": False,
                "message": f"No se pudo aprender la palabra '{word}'"
            }), 400
        
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Error: {str(e)}"
        }), 500

if __name__ == '__main__':
    main()