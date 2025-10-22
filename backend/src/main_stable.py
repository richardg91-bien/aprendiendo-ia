"""
ARIA - Servidor Estable con Red Neuronal Avanzada
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime
import random
import sys
import os

# Agregar el directorio src al path para importar neural_network
sys.path.append(os.path.join(os.path.dirname(__file__)))

try:
    from neural_network import neural_network
    NEURAL_NETWORK_AVAILABLE = True
except ImportError:
    NEURAL_NETWORK_AVAILABLE = False
    print("⚠️ Sistema de red neuronal no disponible - usando modo básico")

try:
    from voice_system import voice_system
    VOICE_SYSTEM_AVAILABLE = voice_system is not None
    if VOICE_SYSTEM_AVAILABLE:
        print("🔊 Sistema de voz ARIA cargado correctamente")
    else:
        print("⚠️ Sistema de voz no disponible")
except ImportError:
    VOICE_SYSTEM_AVAILABLE = False
    print("⚠️ Sistema de voz no disponible - pywin32 no encontrado")

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>ARIA - Asistente Virtual</title>
        <style>
            body { font-family: Arial; padding: 20px; background: #f0f8ff; }
            .container { max-width: 800px; margin: 0 auto; }
            .header { text-align: center; color: #2c3e50; }
            .chat-box { 
                background: white; 
                border-radius: 10px; 
                padding: 20px; 
                margin: 20px 0; 
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            }
            .input-group { display: flex; gap: 10px; margin-top: 15px; }
            .input-group input { 
                flex: 1; 
                padding: 12px; 
                border: 2px solid #e0e0e0; 
                border-radius: 5px; 
                font-size: 16px;
            }
            .input-group button { 
                padding: 12px 20px; 
                background: #3498db; 
                color: white; 
                border: none; 
                border-radius: 5px; 
                cursor: pointer;
                font-size: 16px;
            }
            .input-group button:hover { background: #2980b9; }
            .response { 
                margin-top: 15px; 
                padding: 15px; 
                background: #f8f9fa; 
                border-left: 4px solid #3498db; 
                border-radius: 5px;
                min-height: 20px;
            }
            .features { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 15px; margin: 20px 0; }
            .feature { 
                background: white; 
                padding: 15px; 
                border-radius: 8px; 
                box-shadow: 0 2px 5px rgba(0,0,0,0.1); 
                text-align: center;
            }
            .status { background: #d4edda; padding: 10px; border-radius: 5px; margin: 10px 0; }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🤖 ARIA - Asistente Virtual Inteligente</h1>
                <div class="status">
                    ✅ Sistema Activo | ⏰ """ + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + """
                </div>
            </div>
            
            <div class="chat-box">
                <h3>💬 Chat con ARIA</h3>
                <p>¡Hola! Soy ARIA, tu asistente virtual. Puedes preguntarme cualquier cosa.</p>
                <div class="input-group">
                    <input type="text" id="messageInput" placeholder="Escribe tu mensaje aquí..." />
                    <button onclick="sendMessage()">Enviar</button>
                </div>
                <div id="response" class="response">
                    Esperando tu mensaje...
                </div>
            </div>
            
            <div class="features">
                <div class="feature">
                    <h4>🔊 Sistema de Voz</h4>
                    <p>Síntesis de voz integrada</p>
                    <button onclick="testVoice()">Probar Voz</button>
                    <button onclick="toggleVoice()">Activar/Desactivar</button>
                </div>
                <div class="feature">
                    <h4>🧠 Red Neuronal</h4>
                    <p>Sistema de IA avanzado con memoria</p>
                    <button onclick="testTraining()">Entrenar Red</button>
                    <button onclick="showNeuralInfo()">Info Red Neuronal</button>
                </div>
                <div class="feature">
                    <h4>📊 Aprendizaje</h4>
                    <p>Estadísticas y progreso</p>
                    <button onclick="showLearningStats()">Ver Estadísticas</button>
                </div>
                <div class="feature">
                    <h4>📚 Diccionario</h4>
                    <p>Base de conocimiento</p>
                    <button onclick="testDictionary()">Ver Diccionario</button>
                </div>
                <div class="feature">
                    <h4>🔍 Búsqueda Web</h4>
                    <p>Búsqueda inteligente</p>
                    <button onclick="testSearch()">Probar Búsqueda</button>
                </div>
            </div>
        </div>
        
        <script>
            let voiceEnabled = true;
            
            async function sendMessage() {
                const input = document.getElementById('messageInput');
                const responseDiv = document.getElementById('response');
                const message = input.value.trim();
                
                if (!message) return;
                
                responseDiv.innerHTML = '⏳ Procesando mensaje...';
                
                try {
                    const response = await fetch('/api/chat', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ 
                            message: message,
                            voice_enabled: voiceEnabled 
                        })
                    });
                    
                    const data = await response.json();
                    
                    if (data.success) {
                        responseDiv.innerHTML = `
                            <strong>🤖 ARIA:</strong> ${data.response}<br>
                            <small>Confianza: ${(data.confidence * 100).toFixed(1)}% | ${data.timestamp}</small>
                            ${data.voice_spoken ? '<br><small>🔊 Respuesta reproducida por voz</small>' : ''}
                        `;
                    } else {
                        responseDiv.innerHTML = `❌ Error: ${data.message}`;
                    }
                    
                    input.value = '';
                } catch (error) {
                    responseDiv.innerHTML = `❌ Error de conexión: ${error.message}`;
                }
            }
            
            async function testVoice() {
                const responseDiv = document.getElementById('response');
                responseDiv.innerHTML = '🔊 Probando sistema de voz...';
                
                try {
                    const response = await fetch('/api/voz/test', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ 
                            text: "¡Hola! Soy ARIA, tu asistente virtual inteligente. Mi sistema de voz está funcionando perfectamente."
                        })
                    });
                    
                    const data = await response.json();
                    
                    if (data.success) {
                        responseDiv.innerHTML = `
                            <strong>🔊 Prueba de Voz Exitosa</strong><br>
                            Sistema: ${data.voice_info.available ? 'Disponible' : 'No disponible'}<br>
                            Voz actual: ${data.voice_info.current_voice || 'Ninguna'}<br>
                            Total de voces: ${data.voice_info.total_voices}<br>
                            Volumen: ${data.voice_info.volume}% | Velocidad: ${data.voice_info.rate}
                        `;
                    } else {
                        responseDiv.innerHTML = `❌ Error en sistema de voz: ${data.message}`;
                    }
                } catch (error) {
                    responseDiv.innerHTML = `❌ Error probando voz: ${error.message}`;
                }
            }
            
            async function toggleVoice() {
                voiceEnabled = !voiceEnabled;
                const responseDiv = document.getElementById('response');
                responseDiv.innerHTML = `🔊 Voz ${voiceEnabled ? 'ACTIVADA' : 'DESACTIVADA'}`;
            }
            
            async function testTraining() {
                const responseDiv = document.getElementById('response');
                responseDiv.innerHTML = '🧠 Iniciando entrenamiento avanzado de red neuronal...';
                
                try {
                    const response = await fetch('/api/entrenar_red_neuronal', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ epochs: 50 })
                    });
                    
                    const data = await response.json();
                    if (data.success) {
                        responseDiv.innerHTML = `
                            <strong>✅ Entrenamiento Completado</strong><br>
                            📊 Épocas: ${data.epochs}<br>
                            📈 Precisión inicial: ${(data.accuracy_inicial * 100).toFixed(2)}%<br>
                            🎯 Precisión final: ${(data.accuracy_final * 100).toFixed(2)}%<br>
                            📊 Mejora: +${(data.mejora * 100).toFixed(2)}%<br>
                            ⏱️ Duración: ${data.duracion_segundos}s<br>
                            🧠 Red neuronal actualizada exitosamente
                        `;
                    } else {
                        responseDiv.innerHTML = `❌ Error: ${data.message}`;
                    }
                } catch (error) {
                    responseDiv.innerHTML = `❌ Error en entrenamiento: ${error.message}`;
                }
            }
            
            async function showNeuralInfo() {
                const responseDiv = document.getElementById('response');
                responseDiv.innerHTML = '🧠 Cargando información de red neuronal...';
                
                try {
                    const response = await fetch('/api/red_neuronal_info');
                    const data = await response.json();
                    
                    if (data.success) {
                        const info = data.model;
                        responseDiv.innerHTML = `
                            <strong>🧠 ${info.model_name}</strong><br>
                            📊 Estado: ${info.status}<br>
                            🎯 Precisión actual: ${(info.accuracy * 100).toFixed(2)}%<br>
                            💬 Conversaciones totales: ${info.total_conversations}<br>
                            🧩 Patrones aprendidos: ${info.learned_patterns}<br>
                            🏋️ Entrenamientos: ${info.total_trainings}<br>
                            🧠 Memoria activa: ${info.memory_size} conversaciones<br>
                            📅 Último entrenamiento: ${info.last_training}<br>
                            🏗️ Arquitectura: ${info.architecture}
                        `;
                    } else {
                        responseDiv.innerHTML = `❌ Error: ${data.message}`;
                    }
                } catch (error) {
                    responseDiv.innerHTML = `❌ Error al cargar info: ${error.message}`;
                }
            }
            
            async function showLearningStats() {
                const responseDiv = document.getElementById('response');
                responseDiv.innerHTML = '📊 Cargando estadísticas de aprendizaje...';
                
                try {
                    const response = await fetch('/api/learning/stats');
                    const data = await response.json();
                    
                    if (data.success) {
                        const stats = data.stats;
                        let html = '<strong>📊 Estadísticas de Aprendizaje</strong><br>';
                        html += `🎯 Precisión actual: ${(stats.current_accuracy * 100).toFixed(2)}%<br>`;
                        html += `📚 Palabras aprendidas: ${stats.total_learned_words}<br>`;
                        html += `💾 Eficiencia de memoria: ${(stats.memory_efficiency * 100).toFixed(1)}%<br><br>`;
                        
                        if (stats.training_history && stats.training_history.length > 0) {
                            html += '<strong>🏋️ Últimos Entrenamientos:</strong><br>';
                            stats.training_history.forEach(training => {
                                html += `• ${training.epochs} épocas → ${(training.accuracy * 100).toFixed(1)}% (+${(training.mejora * 100).toFixed(1)}%)<br>`;
                            });
                        }
                        
                        responseDiv.innerHTML = html;
                    } else {
                        responseDiv.innerHTML = `❌ Error: ${data.message}`;
                    }
                } catch (error) {
                    responseDiv.innerHTML = `❌ Error al cargar estadísticas: ${error.message}`;
                }
            }
            
            async function testDictionary() {
                const responseDiv = document.getElementById('response');
                responseDiv.innerHTML = '📚 Cargando diccionario...';
                
                try {
                    const response = await fetch('/api/diccionario');
                    const data = await response.json();
                    
                    if (data.success) {
                        let html = '<strong>📚 Diccionario ARIA:</strong><br>';
                        data.palabras.forEach(p => {
                            html += `• <strong>${p.palabra}</strong>: ${p.definicion}<br>`;
                        });
                        responseDiv.innerHTML = html;
                    }
                } catch (error) {
                    responseDiv.innerHTML = `❌ Error al cargar diccionario: ${error.message}`;
                }
            }
            
            async function testSearch() {
                const responseDiv = document.getElementById('response');
                responseDiv.innerHTML = '🔍 Realizando búsqueda de prueba...';
                
                try {
                    const response = await fetch('/api/busqueda_web', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ query: 'inteligencia artificial' })
                    });
                    
                    const data = await response.json();
                    
                    if (data.success) {
                        let html = '<strong>🔍 Resultados de búsqueda:</strong><br>';
                        data.resultados.forEach(r => {
                            html += `• <strong>${r.title}</strong><br>${r.snippet}<br><br>`;
                        });
                        responseDiv.innerHTML = html;
                    }
                } catch (error) {
                    responseDiv.innerHTML = `❌ Error en búsqueda: ${error.message}`;
                }
            }
            
            document.getElementById('messageInput').addEventListener('keypress', function(e) {
                if (e.key === 'Enter') sendMessage();
            });
        </script>
    </body>
    </html>
    """

# API Endpoints
@app.route('/api/status')
def status():
    neural_status = "disponible" if NEURAL_NETWORK_AVAILABLE else "básico"
    return jsonify({
        "status": "online",
        "version": "stable-2.0",
        "timestamp": datetime.now().isoformat(),
        "message": "ARIA funcionando correctamente",
        "neural_network": neural_status
    })

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        message = data.get('message', '').strip()
        voice_enabled = data.get('voice_enabled', True)
        
        if not message:
            return jsonify({"success": False, "message": "Mensaje vacío"})
        
        responses = {
            'hola': '¡Hola! Me alegra saludarte. ¿Cómo estás?',
            'como estas': 'Estoy funcionando perfectamente, gracias por preguntar.',
            'que tal': 'Todo muy bien por aquí. ¿Y tú qué tal?',
            'bien': 'Me alegra escuchar eso. ¿En qué puedo ayudarte?',
            'gracias': '¡De nada! Es un placer ayudarte.',
            'adios': '¡Hasta luego! Que tengas un excelente día.',
            'entrenar': 'Puedo entrenar mi red neuronal. Haz clic en "Entrenar Red".',
            'diccionario': 'Tengo un diccionario integrado. Haz clic en "Ver Diccionario".',
            'buscar': 'Puedo realizar búsquedas web. Haz clic en "Probar Búsqueda".',
            'aprender': 'Estoy aprendiendo constantemente de nuestras conversaciones.',
            'neuronal': 'Mi red neuronal está activa y aprendiendo. ¿Quieres ver las estadísticas?',
            'voz': 'Mi sistema de voz está integrado y funcionando. ¿Quieres que hable?',
            'habla': '¡Por supuesto! Puedo hablar contigo usando mi sistema de síntesis de voz.'
        }
        
        message_lower = message.lower()
        response = None
        confidence = round(random.uniform(0.8, 0.95), 2)
        
        for key, value in responses.items():
            if key in message_lower:
                response = value
                confidence = round(random.uniform(0.85, 0.98), 2)
                break
        
        if not response:
            response = f"Interesante. Me dijiste: '{message}'. Estoy aprendiendo a responder mejor cada día."
            confidence = round(random.uniform(0.6, 0.8), 2)
        
        # Síntesis de voz
        voice_spoken = False
        if voice_enabled and VOICE_SYSTEM_AVAILABLE:
            try:
                voice_spoken = voice_system.speak_text(response, async_mode=True)
            except Exception as e:
                print(f"Error en síntesis de voz: {e}")
        
        # Guardar conversación en la red neuronal si está disponible
        if NEURAL_NETWORK_AVAILABLE:
            try:
                neural_network.save_conversation(message, response, confidence)
                # Aprender patrones básicos
                if any(key in message_lower for key in responses.keys()):
                    for key, value in responses.items():
                        if key in message_lower:
                            neural_network.learn_pattern(key, value)
                            break
            except Exception as e:
                print(f"Error guardando en red neuronal: {e}")
        
        return jsonify({
            "success": True,
            "response": response,
            "confidence": confidence,
            "timestamp": datetime.now().isoformat(),
            "neural_learning": NEURAL_NETWORK_AVAILABLE,
            "voice_spoken": voice_spoken,
            "voice_available": VOICE_SYSTEM_AVAILABLE
        })
        
    except Exception as e:
        return jsonify({"success": False, "message": str(e)})

@app.route('/api/entrenar_red_neuronal', methods=['POST'])
def entrenar_red_neuronal():
    try:
        data = request.get_json() or {}
        epochs = data.get('epochs', 50)
        
        if NEURAL_NETWORK_AVAILABLE:
            # Usar red neuronal real
            result = neural_network.train_network(epochs=epochs)
            return jsonify(result)
        else:
            # Modo básico de simulación
            import time
            time.sleep(2)
            accuracy = round(0.85 + random.uniform(0, 0.15), 3)
            
            return jsonify({
                "success": True,
                "message": "Entrenamiento completado (modo básico)",
                "epochs": epochs,
                "accuracy_inicial": 0.75,
                "accuracy_final": accuracy,
                "mejora": accuracy - 0.75,
                "duracion_segundos": 2.0,
                "timestamp": datetime.now().isoformat()
            })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Error en entrenamiento: {str(e)}"
        })

@app.route('/api/red_neuronal_info', methods=['GET'])
def red_neuronal_info():
    try:
        if NEURAL_NETWORK_AVAILABLE:
            info = neural_network.get_neural_info()
            return jsonify({
                "success": True,
                "model": info
            })
        else:
            return jsonify({
                "success": True,
                "model": {
                    "model_name": "ARIA Neural Network (Básico)",
                    "status": "active",
                    "accuracy": 0.85,
                    "total_conversations": 0,
                    "learned_patterns": 0,
                    "total_trainings": 0,
                    "last_training": "Modo básico",
                    "memory_size": 0,
                    "architecture": "Basic simulation mode"
                }
            })
            
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Error obteniendo info: {str(e)}"
        })

@app.route('/api/learning/stats', methods=['GET'])
def learning_stats():
    try:
        if NEURAL_NETWORK_AVAILABLE:
            stats = neural_network.get_learning_stats()
            return jsonify({
                "success": True,
                "stats": stats
            })
        else:
            return jsonify({
                "success": True,
                "stats": {
                    "current_accuracy": 0.85,
                    "total_learned_words": 25,
                    "memory_efficiency": 0.7,
                    "training_history": [],
                    "conversations_by_day": [],
                    "top_patterns": []
                }
            })
            
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Error obteniendo estadísticas: {str(e)}"
        })

@app.route('/api/diccionario', methods=['GET'])
def diccionario():
    try:
        palabras = [
            {
                "palabra": "inteligencia",
                "definicion": "Capacidad de entender, aprender y resolver problemas",
                "categoria": "sustantivo"
            },
            {
                "palabra": "artificial",
                "definicion": "Creado por seres humanos, no natural",
                "categoria": "adjetivo"
            },
            {
                "palabra": "algoritmo",
                "definicion": "Conjunto de reglas e instrucciones para resolver un problema",
                "categoria": "sustantivo"
            },
            {
                "palabra": "aprendizaje",
                "definicion": "Proceso de adquirir conocimientos, habilidades y comportamientos",
                "categoria": "sustantivo"
            }
        ]
        
        return jsonify({
            "success": True,
            "palabras": palabras,
            "total": len(palabras)
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Error en diccionario: {str(e)}"
        })

@app.route('/api/busqueda_web', methods=['POST'])
def busqueda_web():
    try:
        data = request.get_json() or {}
        query = data.get('query', '')
        
        if not query:
            return jsonify({
                "success": False,
                "message": "Query requerido"
            })
        
        resultados = [
            {
                "title": f"Todo sobre {query}",
                "snippet": f"Información completa y actualizada sobre {query}. Contenido educativo de alta calidad.",
                "source": "Wikipedia"
            },
            {
                "title": f"Guía de {query}",
                "snippet": f"Guía práctica y tutorial completo sobre {query}. Ideal para principiantes y expertos.",
                "source": "Education.com"
            }
        ]
        
        return jsonify({
            "success": True,
            "resultados": resultados,
            "total": len(resultados),
            "query": query
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Error en búsqueda: {str(e)}"
        })

@app.route('/api/voz/test', methods=['POST'])
def test_voice():
    try:
        data = request.get_json() or {}
        text = data.get('text', '¡Hola! Soy ARIA, tu asistente virtual.')
        
        if not VOICE_SYSTEM_AVAILABLE:
            return jsonify({
                "success": False,
                "message": "Sistema de voz no disponible",
                "voice_info": {
                    "available": False,
                    "current_voice": None,
                    "total_voices": 0
                }
            })
        
        # Probar síntesis de voz
        spoken = voice_system.speak_text(text)
        voice_info = voice_system.get_voice_info()
        
        return jsonify({
            "success": spoken,
            "message": "Prueba de voz ejecutada" if spoken else "Error en síntesis de voz",
            "voice_info": voice_info,
            "text_spoken": text
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Error en prueba de voz: {str(e)}"
        })

@app.route('/api/voz/speak', methods=['POST'])
def speak_text():
    try:
        data = request.get_json() or {}
        text = data.get('text', '')
        
        if not text:
            return jsonify({
                "success": False,
                "message": "Texto requerido"
            })
        
        if not VOICE_SYSTEM_AVAILABLE:
            return jsonify({
                "success": False,
                "message": "Sistema de voz no disponible"
            })
        
        spoken = voice_system.speak_text(text)
        
        return jsonify({
            "success": spoken,
            "message": "Texto sintetizado" if spoken else "Error en síntesis",
            "text": text
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Error sintetizando voz: {str(e)}"
        })

@app.route('/api/voz/stop', methods=['POST'])
def stop_voice():
    try:
        if not VOICE_SYSTEM_AVAILABLE:
            return jsonify({
                "success": False,
                "message": "Sistema de voz no disponible"
            })
        
        voice_system.stop_speaking()
        
        return jsonify({
            "success": True,
            "message": "Síntesis de voz detenida"
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Error deteniendo voz: {str(e)}"
        })

@app.route('/api/voz/info', methods=['GET'])
def voice_info():
    try:
        if not VOICE_SYSTEM_AVAILABLE:
            return jsonify({
                "success": False,
                "voice_info": {
                    "available": False,
                    "message": "Sistema de voz no disponible"
                }
            })
        
        info = voice_system.get_voice_info()
        
        return jsonify({
            "success": True,
            "voice_info": info
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Error obteniendo info de voz: {str(e)}"
        })

if __name__ == '__main__':
    print("🚀 ARIA Servidor Estable - Iniciando...")
    print("🌐 Servidor: http://127.0.0.1:8000")
    print("✨ Versión estable y funcional")
    print(f"🧠 Red neuronal: {'Disponible' if NEURAL_NETWORK_AVAILABLE else 'Modo básico'}")
    print(f"🔊 Sistema de voz: {'Disponible' if VOICE_SYSTEM_AVAILABLE else 'No disponible'}")
    
    app.run(
        host='127.0.0.1',
        port=8000,
        debug=False
    )