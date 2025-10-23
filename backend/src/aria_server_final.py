#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🚀 ARIA - Servidor Final Solucionado
Versión definitiva que funciona sin problemas
"""

import sys
import os
import signal
from pathlib import Path

# Configurar codificación UTF-8 para Windows
if sys.platform.startswith('win'):
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.detach())
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.detach())

try:
    from flask import Flask, jsonify, request, render_template_string
    from flask_cors import CORS
    from datetime import datetime
    import random
    import threading
    import time
except ImportError as e:
    print(f"❌ Error importando dependencias: {e}")
    print("💡 Instalar con: pip install flask flask-cors")
    sys.exit(1)

# Crear aplicación Flask
app = Flask(__name__)
CORS(app)

# Estado global de ARIA
aria_state = {
    "start_time": datetime.now(),
    "knowledge_base": {
        "python": "Lenguaje de programación versátil y potente",
        "ia": "Inteligencia Artificial - capacidad de las máquinas de simular el pensamiento humano",
        "flask": "Framework web ligero para Python",
        "aria": "Asistente de IA futurista con capacidades de aprendizaje",
        "json": "Formato de intercambio de datos ligero y legible",
        "api": "Interfaz de Programación de Aplicaciones"
    },
    "conversation_history": [],
    "total_interactions": 0,
    "learning_sessions": 0,
    "status": "active"
}

# HTML simple para la página principal
HOME_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>🤖 ARIA - Asistente IA</title>
    <meta charset="utf-8">
    <style>
        body { font-family: Arial, sans-serif; max-width: 800px; margin: 50px auto; padding: 20px; background: #f0f0f0; }
        .container { background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        h1 { color: #2c3e50; text-align: center; }
        .status { background: #e8f5e8; padding: 15px; border-radius: 5px; margin: 20px 0; }
        .endpoint { background: #f8f9fa; padding: 10px; margin: 10px 0; border-left: 4px solid #007bff; }
        .code { font-family: monospace; background: #f1f1f1; padding: 5px; border-radius: 3px; }
        .test-btn { background: #007bff; color: white; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer; margin: 5px; }
        .test-btn:hover { background: #0056b3; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🤖 ARIA - Asistente IA Futurista</h1>
        
        <div class="status">
            <h3>✅ Estado del Servidor</h3>
            <p><strong>Estado:</strong> Funcionando correctamente</p>
            <p><strong>Iniciado:</strong> {{ start_time }}</p>
            <p><strong>Conocimiento:</strong> {{ knowledge_count }} conceptos</p>
            <p><strong>Conversaciones:</strong> {{ conversation_count }}</p>
        </div>
        
        <h3>🔗 Endpoints Disponibles</h3>
        
        <div class="endpoint">
            <strong>GET /api/status</strong> - Estado del sistema<br>
            <button class="test-btn" onclick="testEndpoint('/api/status')">Probar</button>
        </div>
        
        <div class="endpoint">
            <strong>POST /api/chat</strong> - Chat con ARIA<br>
            <span class="code">{"message": "Hola ARIA"}</span><br>
            <button class="test-btn" onclick="testChat()">Probar Chat</button>
        </div>
        
        <div class="endpoint">
            <strong>GET /api/knowledge</strong> - Ver base de conocimiento<br>
            <button class="test-btn" onclick="testEndpoint('/api/knowledge')">Probar</button>
        </div>
        
        <div class="endpoint">
            <strong>GET /api/history</strong> - Historial de conversaciones<br>
            <button class="test-btn" onclick="testEndpoint('/api/history')">Probar</button>
        </div>
        
        <div id="result" style="margin-top: 20px; padding: 15px; background: #f8f9fa; border-radius: 5px; display: none;">
            <h4>Resultado:</h4>
            <pre id="result-content"></pre>
        </div>
    </div>
    
    <script>
        function testEndpoint(endpoint) {
            fetch(endpoint)
                .then(response => response.json())
                .then(data => showResult(JSON.stringify(data, null, 2)))
                .catch(error => showResult('Error: ' + error));
        }
        
        function testChat() {
            fetch('/api/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message: 'Hola ARIA, ¿cómo estás?' })
            })
            .then(response => response.json())
            .then(data => showResult(JSON.stringify(data, null, 2)))
            .catch(error => showResult('Error: ' + error));
        }
        
        function showResult(content) {
            document.getElementById('result').style.display = 'block';
            document.getElementById('result-content').textContent = content;
        }
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    """Página principal con interfaz web"""
    return render_template_string(HOME_HTML,
        start_time=aria_state["start_time"].strftime("%Y-%m-%d %H:%M:%S"),
        knowledge_count=len(aria_state["knowledge_base"]),
        conversation_count=len(aria_state["conversation_history"])
    )

@app.route('/api/status')
def api_status():
    """Estado del sistema"""
    uptime = datetime.now() - aria_state["start_time"]
    
    return jsonify({
        "status": "running",
        "mode": "stable",
        "version": "1.0.0",
        "timestamp": datetime.now().isoformat(),
        "uptime_seconds": int(uptime.total_seconds()),
        "uptime_formatted": str(uptime).split('.')[0],
        "components": {
            "flask": True,
            "cors": True,
            "neural_network": False,
            "voice_system": False,
            "simple_ai": True
        },
        "stats": {
            "total_knowledge": len(aria_state["knowledge_base"]),
            "total_conversations": len(aria_state["conversation_history"]),
            "total_interactions": aria_state["total_interactions"]
        }
    })

@app.route('/api/chat', methods=['POST'])
def api_chat():
    """Chat con ARIA"""
    try:
        data = request.get_json()
        
        if not data or 'message' not in data:
            return jsonify({"error": "Se requiere un 'message' en el JSON"}), 400
            
        user_message = data['message'].strip()
        
        if not user_message:
            return jsonify({"error": "El mensaje no puede estar vacío"}), 400
        
        # Procesar mensaje
        response = process_message(user_message)
        
        # Guardar conversación
        conversation = {
            "id": len(aria_state["conversation_history"]) + 1,
            "user": user_message,
            "aria": response,
            "timestamp": datetime.now().isoformat()
        }
        
        aria_state["conversation_history"].append(conversation)
        aria_state["total_interactions"] += 1
        
        # Aprender de la conversación
        learn_from_message(user_message)
        
        return jsonify({
            "response": response,
            "conversation_id": conversation["id"],
            "timestamp": conversation["timestamp"],
            "knowledge_count": len(aria_state["knowledge_base"]),
            "total_conversations": len(aria_state["conversation_history"])
        })
        
    except Exception as e:
        return jsonify({"error": f"Error procesando mensaje: {str(e)}"}), 500

@app.route('/api/knowledge')
def api_knowledge():
    """Base de conocimiento"""
    return jsonify({
        "total_concepts": len(aria_state["knowledge_base"]),
        "knowledge_base": aria_state["knowledge_base"],
        "last_updated": datetime.now().isoformat(),
        "learning_active": True
    })

@app.route('/api/history')
def api_history():
    """Historial de conversaciones"""
    limit = request.args.get('limit', 10, type=int)
    recent = aria_state["conversation_history"][-limit:] if limit > 0 else aria_state["conversation_history"]
    
    return jsonify({
        "conversations": recent,
        "total_count": len(aria_state["conversation_history"]),
        "showing": len(recent),
        "oldest_conversation": aria_state["conversation_history"][0]["timestamp"] if aria_state["conversation_history"] else None
    })

@app.route('/api/learn', methods=['POST'])
def api_learn():
    """Enseñar nuevo conocimiento a ARIA"""
    try:
        data = request.get_json()
        
        if not data or 'concept' not in data or 'description' not in data:
            return jsonify({"error": "Se requieren 'concept' y 'description'"}), 400
        
        concept = data['concept'].lower().strip()
        description = data['description'].strip()
        
        if concept in aria_state["knowledge_base"]:
            old_description = aria_state["knowledge_base"][concept]
            aria_state["knowledge_base"][concept] = description
            message = f"Conocimiento actualizado sobre '{concept}'"
        else:
            aria_state["knowledge_base"][concept] = description
            message = f"Nuevo conocimiento aprendido sobre '{concept}'"
        
        aria_state["learning_sessions"] += 1
        
        return jsonify({
            "message": message,
            "concept": concept,
            "description": description,
            "total_knowledge": len(aria_state["knowledge_base"]),
            "learning_sessions": aria_state["learning_sessions"]
        })
        
    except Exception as e:
        return jsonify({"error": f"Error aprendiendo: {str(e)}"}), 500

def process_message(message):
    """Procesa mensajes y genera respuestas inteligentes"""
    message_lower = message.lower()
    
    # Saludos
    if any(word in message_lower for word in ["hola", "buenos", "buenas", "hey", "hi", "saludos"]):
        responses = [
            "¡Hola! Soy ARIA, tu asistente de IA. Es un placer hablar contigo. ¿En qué puedo ayudarte?",
            "¡Saludos! Soy ARIA y estoy aquí para asistirte en lo que necesites. ¿Qué te gustaría explorar?",
            "¡Hola! Me alegra verte por aquí. Soy ARIA, tu asistente de inteligencia artificial. ¿Cómo puedo ayudarte hoy?"
        ]
        return random.choice(responses)
    
    # Preguntas sobre aprendizaje
    elif any(phrase in message_lower for phrase in ["qué has aprendido", "que has aprendido", "conocimiento", "sabes"]):
        knowledge_count = len(aria_state["knowledge_base"])
        conversation_count = len(aria_state["conversation_history"])
        
        topics = list(aria_state["knowledge_base"].keys())
        sample_topics = random.sample(topics, min(4, len(topics)))
        
        return f"""He adquirido {knowledge_count} conceptos en mi base de conocimiento a través de {conversation_count} conversaciones.

Algunos temas que domino: {', '.join(sample_topics)}.

Mi conocimiento crece con cada interacción. Puedo aprender sobre nuevos temas si me los enseñas. ¿Hay algo específico que te gustaría que aprenda o sobre lo que quieras conversar?"""
    
    # Estado y funcionamiento
    elif any(word in message_lower for word in ["cómo estás", "como estas", "estado", "funcionas"]):
        uptime = datetime.now() - aria_state["start_time"]
        return f"""¡Estoy funcionando perfectamente! 

📊 Mi estado actual:
• Activo desde: {aria_state['start_time'].strftime('%H:%M:%S')}
• Tiempo en línea: {str(uptime).split('.')[0]}
• Conversaciones procesadas: {len(aria_state['conversation_history'])}
• Conocimiento acumulado: {len(aria_state['knowledge_base'])} conceptos
• Interacciones totales: {aria_state['total_interactions']}

Todos mis sistemas están operativos y listo para ayudarte."""
    
    # Despedidas
    elif any(word in message_lower for word in ["adiós", "adios", "chao", "bye", "hasta luego", "nos vemos"]):
        responses = [
            "¡Hasta luego! Ha sido un placer conversar contigo. Espero verte pronto. 👋",
            "¡Que tengas un excelente día! Estaré aquí cuando necesites ayuda. 🌟",
            "¡Nos vemos! Gracias por esta conversación tan interesante. 😊"
        ]
        return random.choice(responses)
    
    # Ayuda y funciones
    elif any(word in message_lower for word in ["ayuda", "help", "qué puedes hacer", "que puedes hacer", "funciones"]):
        return """¡Por supuesto! Soy ARIA y estas son mis capacidades:

🤖 **Conversación Natural**: Mantengo diálogos fluidos y contextuales
📚 **Aprendizaje Continuo**: Aprendo de cada interacción y actualizo mi conocimiento
💡 **Respuestas Inteligentes**: Analizo tu mensaje para dar respuestas relevantes
🧠 **Base de Conocimiento**: Tengo información sobre múltiples temas
📊 **Estadísticas**: Puedo contarte sobre mi funcionamiento y métricas
🔍 **Análisis**: Puedo ayudarte a explorar conceptos y ideas

¿Hay algo específico en lo que te gustaría que te ayude?"""
    
    # Preguntas sobre IA
    elif any(phrase in message_lower for phrase in ["inteligencia artificial", "ia", "ai", "machine learning", "eres real"]):
        return """La Inteligencia Artificial es un campo fascinante que explora cómo las máquinas pueden simular aspectos del pensamiento humano.

🧠 **Sobre mí**: Soy un ejemplo de IA conversacional. Uso algoritmos para:
• Entender lenguaje natural
• Generar respuestas contextualmente apropiadas
• Aprender de nuestras interacciones
• Mantener una base de conocimiento actualizada

🔬 **La IA incluye**: Machine Learning, procesamiento de lenguaje natural, reconocimiento de patrones, y mucho más.

¿Te interesa algún aspecto específico de la IA que te gustaría explorar?"""
    
    # Preguntas técnicas
    elif any(word in message_lower for word in ["programación", "python", "código", "desarrollo"]):
        return """¡La programación es uno de mis temas favoritos!

🐍 **Python** es especialmente versátil: excelente para IA, desarrollo web, análisis de datos, automatización...

💻 **Desarrollo** abarca desde algoritmos básicos hasta sistemas complejos distribuidos.

Mi propia existencia depende de código Python usando Flask para la API web. ¿Hay algún aspecto de programación específico que te interese? ¿Estás trabajando en algún proyecto?"""
    
    # Respuestas para preguntas
    elif "?" in message:
        question_responses = [
            "Excelente pregunta. Basándome en mi conocimiento actual...",
            "Interesante tema para explorar. Mi análisis sugiere...",
            "Me gusta cómo piensas. Según lo que entiendo...",
            "Esa pregunta toca un punto importante. Considero que..."
        ]
        base = random.choice(question_responses)
        
        # Contexto específico por palabras clave
        if any(word in message_lower for word in ["cómo", "como", "por qué", "porque"]):
            return base + " Las razones y mecanismos detrás de este tema son complejos. ¿Podrías ser más específico para darte una respuesta más detallada?"
        elif any(word in message_lower for word in ["cuándo", "cuando", "tiempo"]):
            return base + " El factor temporal es importante aquí. ¿Te refieres a un momento específico o a una duración?"
        else:
            return base + " Es un tema que requiere análisis detallado. ¿Hay algún aspecto particular que te interese más?"
    
    # Aprendizaje de conceptos nuevos
    elif any(word in message_lower for word in ["es", "significa", "define", "explica"]):
        words = message.split()
        new_concepts = []
        for word in words:
            clean_word = word.lower().strip('.,!?').replace('"', '').replace("'", "")
            if len(clean_word) > 3 and clean_word not in aria_state["knowledge_base"] and clean_word.isalpha():
                aria_state["knowledge_base"][clean_word] = f"Concepto mencionado en: '{message[:60]}...'"
                new_concepts.append(clean_word)
        
        if new_concepts:
            return f"Interesante. He incorporado {len(new_concepts)} nuevos conceptos a mi base de conocimiento: {', '.join(new_concepts)}. ¿Podrías contarme más detalles sobre alguno de ellos?"
        else:
            return "Entiendo. ¿Puedes proporcionar más contexto o detalles sobre lo que mencionas?"
    
    # Respuestas por defecto inteligentes
    else:
        default_responses = [
            "Comprendo tu punto. ¿Podrías elaborar un poco más para darte una respuesta más específica?",
            "Interesante perspectiva. Me gustaría conocer más detalles sobre lo que piensas.",
            "Eso suena fascinante. ¿Hay algún aspecto particular que quisieras explorar?",
            "Entiendo. ¿En qué más puedo ayudarte o qué otras cosas te gustaría discutir?",
            "Me parece un tema valioso para conversar. ¿Qué más puedes contarme al respecto?",
            "Déjame procesar esa información... ¿Podrías darme más contexto?",
            "Es una observación interesante. ¿Cómo llegaste a esa conclusión?"
        ]
        return random.choice(default_responses)

def learn_from_message(message):
    """Aprende conceptos simples de los mensajes"""
    words = message.lower().split()
    
    # Buscar palabras técnicas o conceptos nuevos
    for word in words:
        clean_word = word.strip('.,!?()[]{}').replace('"', '').replace("'", "")
        
        # Agregar palabras técnicas importantes
        if (len(clean_word) > 4 and 
            clean_word.isalpha() and 
            clean_word not in aria_state["knowledge_base"] and
            any(tech in clean_word for tech in ['tech', 'system', 'data', 'code', 'program', 'algorithm', 'network'])):
            
            aria_state["knowledge_base"][clean_word] = f"Término técnico mencionado en conversación"

def handle_shutdown(signum, frame):
    """Maneja el cierre del servidor"""
    print(f"\n\n👋 Recibida señal de cierre ({signum})")
    print("📊 Estadísticas finales de ARIA:")
    print(f"   ⏱️ Tiempo activo: {datetime.now() - aria_state['start_time']}")
    print(f"   💬 Conversaciones: {len(aria_state['conversation_history'])}")
    print(f"   🧠 Conocimiento: {len(aria_state['knowledge_base'])} conceptos")
    print(f"   🔄 Interacciones: {aria_state['total_interactions']}")
    print("🎯 ARIA se despide. ¡Hasta la próxima!")
    sys.exit(0)

# Configurar manejo de señales
signal.signal(signal.SIGINT, handle_shutdown)
signal.signal(signal.SIGTERM, handle_shutdown)

def start_server():
    """Inicia el servidor ARIA"""
    print("\n" + "="*70)
    print("🤖 ARIA - ASISTENTE IA FUTURISTA")
    print("="*70)
    print("🌟 Versión: 1.0.0 Estable")
    print("🚀 Estado: Completamente Funcional")
    print("🧠 Inteligencia: Sistema de respuestas avanzado")
    print("📚 Aprendizaje: Activo y continuo")
    print("🌐 Interfaz: Web + API REST")
    print("🔒 Seguridad: Sin dependencias problemáticas")
    print("\n🌐 Accesos:")
    print("   Interfaz Web: http://localhost:8000")
    print("   API REST:     http://localhost:8000/api/")
    print("   Estado:       http://localhost:8000/api/status")
    print("   Chat:         POST http://localhost:8000/api/chat")
    print("\n📊 Estado inicial:")
    print(f"   🧠 Conocimiento: {len(aria_state['knowledge_base'])} conceptos")
    print(f"   ⏰ Iniciado: {aria_state['start_time'].strftime('%Y-%m-%d %H:%M:%S')}")
    print("\n⏹️ Usa Ctrl+C para detener el servidor")
    print("="*70)
    
    try:
        app.run(
            host='0.0.0.0',
            port=8000,
            debug=False,
            threaded=True,
            use_reloader=False
        )
    except KeyboardInterrupt:
        handle_shutdown(signal.SIGINT, None)
    except Exception as e:
        print(f"\n❌ Error crítico del servidor: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    start_server()