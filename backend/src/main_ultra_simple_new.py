"""
ARIA - Servidor Ultra Simple
Version minima para debugging
"""

from flask import Flask, jsonify, send_from_directory, request
from flask_cors import CORS
from datetime import datetime
import json

app = Flask(__name__, static_folder='../../frontend/build', static_url_path='/')
CORS(app)

@app.route('/')
def home():
    try:
        return send_from_directory(app.static_folder, 'index.html')
    except:
        return """
        <!DOCTYPE html>
        <html>
        <head>
            <title>ARIA - Funcionando</title>
            <style>
                body { font-family: Arial; padding: 20px; text-align: center; }
                .container { max-width: 600px; margin: 0 auto; }
                .success { color: green; }
                .info { background: #e7f3ff; padding: 15px; margin: 10px; border-radius: 5px; }
            </style>
        </head>
        <body>
            <div class="container">
                <h1 class="success">✅ ARIA esta funcionando!</h1>
                <div class="info">
                    <h3>🎯 Estado del Servidor</h3>
                    <p>✅ Backend: Activo</p>
                    <p>✅ APIs: Disponibles</p>
                    <p>⏰ Tiempo: """ + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + """</p>
                </div>
                <div class="info">
                    <h3>🧪 Prueba el Chat</h3>
                    <p>Escribe un mensaje y presiona enviar:</p>
                    <input type="text" id="messageInput" placeholder="Escribe tu mensaje aqui..." style="width: 300px; padding: 8px;">
                    <button onclick="sendMessage()" style="padding: 8px 15px; margin-left: 5px;">Enviar</button>
                    <div id="response" style="margin-top: 15px; padding: 10px; background: #f0f0f0; border-radius: 5px; min-height: 40px;"></div>
                </div>
            </div>
            
            <script>
                async function sendMessage() {
                    const input = document.getElementById('messageInput');
                    const responseDiv = document.getElementById('response');
                    const message = input.value.trim();
                    
                    if (!message) return;
                    
                    responseDiv.innerHTML = '⏳ Enviando mensaje...';
                    
                    try {
                        const response = await fetch('/api/chat', {
                            method: 'POST',
                            headers: {
                                'Content-Type': 'application/json'
                            },
                            body: JSON.stringify({ message: message })
                        });
                        
                        const data = await response.json();
                        
                        if (data.success) {
                            responseDiv.innerHTML = `
                                <strong>🧠 ARIA:</strong> ${data.response}<br>
                                <small>Confianza: ${(data.confidence * 100).toFixed(1)}%</small>
                            `;
                        } else {
                            responseDiv.innerHTML = `❌ Error: ${data.message}`;
                        }
                        
                        input.value = '';
                    } catch (error) {
                        responseDiv.innerHTML = `❌ Error de conexion: ${error.message}`;
                    }
                }
                
                document.getElementById('messageInput').addEventListener('keypress', function(e) {
                    if (e.key === 'Enter') {
                        sendMessage();
                    }
                });
            </script>
        </body>
        </html>
        """

@app.route('/api/status')
def status():
    return jsonify({
        "status": "online",
        "version": "ultra-simple",
        "timestamp": datetime.now().isoformat(),
        "message": "ARIA funcionando correctamente",
        "components": {
            "backend": "running",
            "neural_network": "active",
            "web_search": "available",
            "voice_system": "unavailable"
        }
    })

@app.route('/api/learning/stats')
def learning_stats():
    return jsonify({
        "success": True,
        "stats": {
            "total_conversations": 10,
            "learned_patterns": 5,
            "confidence_average": 0.85,
            "last_training": datetime.now().isoformat(),
            "training_accuracy": 0.92
        }
    })

@app.route('/api/red_neuronal_info')
def red_neuronal_info():
    return jsonify({
        "success": True,
        "model": {
            "name": "ARIA Neural Network",
            "version": "2.0",
            "status": "active",
            "training_data": "basic_conversations",
            "accuracy": 0.92,
            "last_training": datetime.now().isoformat(),
            "total_parameters": 1000,
            "epochs_completed": 50
        }
    })

@app.route('/api/entrenar_red_neuronal', methods=['POST'])
def entrenar_red_neuronal():
    try:
        data = request.get_json() or {}
        epochs = data.get('epochs', 50)
        
        # Simular entrenamiento
        import time
        time.sleep(2)  # Simular tiempo de entrenamiento
        
        # Calcular una precision simulada
        import random
        accuracy = round(0.85 + random.uniform(0, 0.15), 3)
        
        return jsonify({
            "success": True,
            "message": "Entrenamiento completado exitosamente",
            "result": {
                "epochs": epochs,
                "final_accuracy": accuracy,
                "training_time": "2.1 segundos",
                "status": "completed",
                "improvement": "0.05"
            }
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Error en entrenamiento: {str(e)}"
        })

@app.route('/api/busqueda_web', methods=['POST'])
@app.route('/api/buscar_web', methods=['POST'])
def busqueda_web():
    try:
        data = request.get_json() or {}
        query = data.get('query', '')
        
        if not query:
            return jsonify({
                "success": False,
                "message": "Query requerido"
            })
        
        # Resultados simulados
        resultados = [
            {
                "title": f"Resultado sobre: {query}",
                "url": "https://example.com",
                "snippet": f"Informacion relevante sobre {query}. Esta es una busqueda simulada.",
                "source": "Wikipedia"
            },
            {
                "title": f"Mas informacion: {query}",
                "url": "https://example2.com", 
                "snippet": f"Detalles adicionales sobre {query}. Contenido educativo.",
                "source": "Enciclopedia"
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
            "message": f"Error en busqueda: {str(e)}"
        })

@app.route('/api/diccionario', methods=['GET', 'POST'])
def diccionario():
    try:
        if request.method == 'GET':
            # Devolver palabras del diccionario
            palabras_ejemplo = [
                {
                    "palabra": "inteligencia",
                    "definicion": "Capacidad de entender, aprender y resolver problemas",
                    "categoria": "sustantivo",
                    "aprendida": "2025-10-20",
                    "uso_frecuente": True
                },
                {
                    "palabra": "artificial",
                    "definicion": "Creado por seres humanos, no natural",
                    "categoria": "adjetivo",
                    "aprendida": "2025-10-20",
                    "uso_frecuente": True
                },
                {
                    "palabra": "algoritmo",
                    "definicion": "Conjunto de reglas e instrucciones para resolver un problema",
                    "categoria": "sustantivo",
                    "aprendida": "2025-10-20",
                    "uso_frecuente": False
                },
                {
                    "palabra": "diccionario",
                    "definicion": "Libro o conjunto de palabras ordenadas alfabeticamente con sus significados",
                    "categoria": "sustantivo",
                    "aprendida": "2025-10-20",
                    "uso_frecuente": True
                }
            ]
            
            return jsonify({
                "success": True,
                "palabras": palabras_ejemplo,
                "total": len(palabras_ejemplo)
            })
            
        elif request.method == 'POST':
            # Agregar nueva palabra al diccionario
            data = request.get_json() or {}
            palabra = data.get('palabra', '').strip()
            
            if not palabra:
                return jsonify({
                    "success": False,
                    "message": "Palabra requerida"
                })
            
            # Simular definicion de diccionario
            definicion_simulada = f"Definicion de '{palabra}': termino aprendido automaticamente por ARIA."
            
            return jsonify({
                "success": True,
                "message": f"Palabra '{palabra}' agregada al diccionario",
                "palabra_agregada": {
                    "palabra": palabra,
                    "definicion": definicion_simulada,
                    "categoria": "general",
                    "aprendida": datetime.now().isoformat(),
                    "uso_frecuente": False
                }
            })
            
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Error en diccionario: {str(e)}"
        })

@app.route('/api/diccionario/buscar', methods=['POST'])
def buscar_diccionario():
    try:
        data = request.get_json() or {}
        termino = data.get('termino', '').strip().lower()
        
        if not termino:
            return jsonify({
                "success": False,
                "message": "Termino de busqueda requerido"
            })
        
        # Diccionario simulado
        diccionario_simulado = {
            "inteligencia": {
                "definicion": "Capacidad de entender, aprender y resolver problemas",
                "sinonimos": ["intelecto", "razon", "entendimiento"],
                "categoria": "sustantivo"
            },
            "artificial": {
                "definicion": "Creado por seres humanos, no natural",
                "sinonimos": ["sintetico", "fabricado", "creado"],
                "categoria": "adjetivo"
            },
            "algoritmo": {
                "definicion": "Conjunto de reglas e instrucciones para resolver un problema",
                "sinonimos": ["procedimiento", "metodo", "proceso"],
                "categoria": "sustantivo"
            },
            "diccionario": {
                "definicion": "Libro o conjunto de palabras ordenadas alfabeticamente con sus significados",
                "sinonimos": ["vocabulario", "glosario", "lexicon"],
                "categoria": "sustantivo"
            }
        }
        
        # Buscar termino
        resultado = diccionario_simulado.get(termino)
        
        if resultado:
            return jsonify({
                "success": True,
                "encontrado": True,
                "termino": termino,
                "resultado": resultado
            })
        else:
            return jsonify({
                "success": True,
                "encontrado": False,
                "termino": termino,
                "mensaje": f"No se encontro definicion para '{termino}'. Te gustaria que la aprenda?"
            })
            
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Error en busqueda de diccionario: {str(e)}"
        })

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        message = data.get('message', '').strip()
        
        if not message:
            return jsonify({"success": False, "message": "Mensaje vacio"})
        
        # Respuesta simple
        responses = {
            'hola': 'Hola! Me alegra saludarte. Como estas?',
            'como estas': 'Estoy funcionando perfectamente, gracias por preguntar.',
            'que tal': 'Todo muy bien por aqui. Y tu que tal?',
            'bien': 'Me alegra escuchar eso. En que puedo ayudarte?',
            'gracias': 'De nada! Es un placer ayudarte.',
            'adios': 'Hasta luego! Que tengas un excelente dia.',
            'diccionario': 'Puedo ayudarte con el diccionario. Usa /api/diccionario para ver palabras o /api/diccionario/buscar para buscar terminos especificos.'
        }
        
        message_lower = message.lower()
        response = None
        
        for key, value in responses.items():
            if key in message_lower:
                response = value
                break
        
        if not response:
            response = f"Interesante. Me dijiste: '{message}'. Estoy aprendiendo a responder mejor cada dia."
        
        return jsonify({
            "success": True,
            "response": response,
            "confidence": 0.9,
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({"success": False, "message": str(e)})

@app.route('/api/test_simple')
def test_simple():
    return jsonify({
        "success": True,
        "message": "API funcionando correctamente",
        "timestamp": datetime.now().isoformat()
    })

if __name__ == '__main__':
    print("🚀 ARIA Ultra Simple - Iniciando...")
    print("🌐 Servidor: http://127.0.0.1:8000")
    print("✨ Version ultra estable")
    
    app.run(
        host='0.0.0.0',
        port=8000,
        debug=False,
        use_reloader=False
    )