#!/usr/bin/env python3
"""
Servidor de prueba simple para ARIA
Sin dependencias complejas
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
import json
import random
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Base de datos simple en memoria
conversaciones = []
contador_conversaciones = 0

@app.route('/')
def home():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>ARIA - Test Simple</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; background: #f0f2f5; }
            .container { max-width: 800px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; }
            .header { text-align: center; color: #333; margin-bottom: 30px; }
            .chat-container { border: 1px solid #ddd; border-radius: 8px; padding: 20px; margin-bottom: 20px; }
            .input-group { display: flex; gap: 10px; margin-bottom: 20px; }
            input { flex: 1; padding: 10px; border: 1px solid #ddd; border-radius: 5px; }
            button { padding: 10px 20px; background: #007bff; color: white; border: none; border-radius: 5px; cursor: pointer; }
            button:hover { background: #0056b3; }
            .response { background: #f8f9fa; padding: 15px; border-radius: 5px; margin-top: 10px; }
            .stats { background: #e7f3ff; padding: 15px; border-radius: 5px; margin-top: 20px; }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🤖 ARIA - Test Simple</h1>
                <p>Sistema básico funcionando correctamente</p>
            </div>
            
            <div class="chat-container">
                <h3>💬 Chat con ARIA</h3>
                <div class="input-group">
                    <input type="text" id="messageInput" placeholder="Escribe tu mensaje aquí..." />
                    <button onclick="sendMessage()">Enviar</button>
                </div>
                <div id="responses"></div>
            </div>
            
            <div class="stats">
                <h3>📊 Estadísticas</h3>
                <div id="stats">
                    <p>🔢 Conversaciones: <span id="convCount">0</span></p>
                    <p>⏰ Última actividad: <span id="lastActivity">-</span></p>
                    <p>✅ Estado del servidor: <span style="color: green;">Activo</span></p>
                </div>
            </div>
        </div>

        <script>
            let conversationCount = 0;
            
            function sendMessage() {
                const input = document.getElementById('messageInput');
                const message = input.value.trim();
                
                if (!message) return;
                
                input.value = '';
                
                fetch('/api/chat', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ message: message })
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        displayResponse(message, data.response);
                        updateStats();
                    } else {
                        displayResponse(message, 'Error: ' + data.message);
                    }
                })
                .catch(error => {
                    displayResponse(message, 'Error de conexión: ' + error);
                });
            }
            
            function displayResponse(message, response) {
                const responsesDiv = document.getElementById('responses');
                const time = new Date().toLocaleTimeString();
                
                responsesDiv.innerHTML = `
                    <div class="response">
                        <strong>Tú (${time}):</strong> ${message}<br>
                        <strong>🤖 ARIA:</strong> ${response}
                    </div>
                ` + responsesDiv.innerHTML;
                
                conversationCount++;
            }
            
            function updateStats() {
                document.getElementById('convCount').textContent = conversationCount;
                document.getElementById('lastActivity').textContent = new Date().toLocaleTimeString();
            }
            
            // Permitir envío con Enter
            document.getElementById('messageInput').addEventListener('keypress', function(e) {
                if (e.key === 'Enter') sendMessage();
            });
            
            // Actualizar estadísticas al cargar
            updateStats();
        </script>
    </body>
    </html>
    """

@app.route('/api/status')
def api_status():
    """Estado del servidor"""
    return jsonify({
        "status": "active",
        "message": "ARIA Test Server funcionando correctamente",
        "timestamp": datetime.now().isoformat(),
        "conversations": len(conversaciones),
        "servicios": {
            "chat": "activo",
            "api": "activo",
            "web": "activo"
        }
    })

@app.route('/api/chat', methods=['POST'])
def api_chat():
    """Chat simple con ARIA"""
    global contador_conversaciones
    
    try:
        data = request.json
        mensaje = data.get('message', '').strip().lower()
        
        # Respuestas simples predefinidas
        respuestas = {
            'hola': '¡Hola! 👋 Soy ARIA, tu asistente de IA. ¿En qué puedo ayudarte?',
            'como estas': '¡Estoy muy bien! 😊 Funcionando perfectamente y lista para ayudarte.',
            'que eres': 'Soy ARIA, una inteligencia artificial creada por Richard. Mi propósito es asistirte y conversar contigo.',
            'que haces': 'Puedo chatear contigo, responder preguntas y ayudarte con lo que necesites. ¡Pregúntame cualquier cosa!',
            'help': 'Puedes preguntarme sobre: mi identidad, el clima, matemáticas básicas, o simplemente conversar.',
            'gracias': '¡De nada! 😊 Siempre es un placer ayudarte.',
            'adios': '¡Hasta luego! 👋 Espero verte pronto.',
            'test': 'Test exitoso ✅ El sistema está funcionando correctamente.',
            'estado': f'Sistema operativo ✅ Conversaciones procesadas: {contador_conversaciones}'
        }
        
        # Buscar respuesta
        respuesta = None
        for clave, resp in respuestas.items():
            if clave in mensaje:
                respuesta = resp
                break
        
        # Respuesta por defecto
        if not respuesta:
            respuestas_genericas = [
                "Interesante pregunta. Aunque soy una IA simple, haré mi mejor esfuerzo para ayudarte.",
                "No tengo una respuesta específica para eso, pero estoy aquí para conversar contigo.",
                "Esa es una consulta muy buena. Como sistema básico, puedo ayudarte con conversaciones simples.",
                "Me parece una pregunta fascinante. ¿Podrías ser más específico?",
                "Aunque soy una versión simple de ARIA, intentaré ayudarte de la mejor manera."
            ]
            respuesta = random.choice(respuestas_genericas)
        
        # Guardar conversación
        contador_conversaciones += 1
        conversacion = {
            "id": contador_conversaciones,
            "mensaje": data.get('message', ''),
            "respuesta": respuesta,
            "timestamp": datetime.now().isoformat()
        }
        conversaciones.append(conversacion)
        
        print(f"💬 Chat {contador_conversaciones}: {data.get('message', '')}")
        print(f"🤖 ARIA: {respuesta}")
        
        return jsonify({
            "success": True,
            "response": respuesta,
            "conversation_id": contador_conversaciones,
            "timestamp": conversacion["timestamp"]
        })
        
    except Exception as e:
        print(f"❌ Error en chat: {e}")
        return jsonify({
            "success": False,
            "message": f"Error: {str(e)}"
        }), 500

@app.route('/api/stats')
def api_stats():
    """Estadísticas del sistema"""
    return jsonify({
        "total_conversations": len(conversaciones),
        "last_conversations": conversaciones[-5:] if conversaciones else [],
        "server_uptime": "Activo",
        "system_status": "Funcionando correctamente"
    })

if __name__ == '__main__':
    print("🚀 Iniciando servidor de prueba ARIA...")
    print("🌐 Accede a: http://127.0.0.1:5001")
    print("📡 API disponible en: http://127.0.0.1:5001/api/")
    print("=" * 50)
    
    try:
        app.run(
            host='127.0.0.1',
            port=5001,
            debug=True,
            use_reloader=False
        )
    except Exception as e:
        print(f"❌ Error: {e}")