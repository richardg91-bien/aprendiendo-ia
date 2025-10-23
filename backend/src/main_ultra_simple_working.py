#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🚀 ARIA - Servidor Ultra Simple y Estable
Servidor mínimo sin dependencias problemáticas
"""

import sys
import os
from pathlib import Path

# Configurar codificación UTF-8 para Windows
if sys.platform.startswith('win'):
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.detach())
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.detach())

try:
    from flask import Flask, jsonify, request
    from flask_cors import CORS
    from datetime import datetime
    import random
except ImportError as e:
    print(f"❌ Error importando Flask: {e}")
    print("💡 Instalar con: pip install flask flask-cors")
    sys.exit(1)

# Configurar Flask
app = Flask(__name__)
CORS(app)

print("🤖 ARIA - Servidor Ultra Simple iniciando...")

# Estado simple de ARIA
aria_state = {
    "knowledge_base": {
        "python": "Lenguaje de programación versátil",
        "ia": "Inteligencia Artificial",
        "flask": "Framework web para Python",
        "aria": "Asistente de IA futurista"
    },
    "conversation_history": [],
    "learning_active": True,
    "total_knowledge": 4,  # Conocimiento básico inicial
    "system_status": "running_simple",
    "start_time": datetime.now().isoformat()
}

@app.route('/', methods=['GET'])
def index():
    """Página de inicio"""
    return jsonify({
        "message": "🤖 ARIA - Asistente IA Futurista (Modo Simple)",
        "status": "running",
        "mode": "simple",
        "start_time": aria_state["start_time"],
        "endpoints": [
            "GET / - Esta página",
            "GET /api/status - Estado del sistema",
            "POST /api/chat - Chat con ARIA",
            "GET /api/knowledge - Ver conocimiento",
            "GET /api/history - Historial de conversación"
        ]
    })

@app.route('/api/status', methods=['GET'])
def get_status():
    """Endpoint para verificar el estado del sistema"""
    return jsonify({
        "status": "running",
        "mode": "simple",
        "timestamp": datetime.now().isoformat(),
        "uptime_start": aria_state["start_time"],
        "components": {
            "flask": True,
            "cors": True,
            "neural_network": False,
            "voice_system": False,
            "auto_learning": False,
            "simple_responses": True
        },
        "aria_state": {
            "total_knowledge": aria_state["total_knowledge"],
            "conversations": len(aria_state["conversation_history"]),
            "learning_active": aria_state["learning_active"]
        }
    })

@app.route('/api/chat', methods=['POST'])
def chat():
    """Endpoint principal de chat con ARIA"""
    try:
        data = request.get_json()
        
        if not data or 'message' not in data:
            return jsonify({"error": "Se requiere un mensaje"}), 400
            
        user_message = data['message']
        
        print(f"👤 Usuario: {user_message}")
        
        # Generar respuesta simple
        response = generate_simple_response(user_message)
        
        print(f"🤖 ARIA: {response}")
        
        # Guardar en historial
        conversation = {
            "user": user_message,
            "aria": response,
            "timestamp": datetime.now().isoformat()
        }
        
        aria_state["conversation_history"].append(conversation)
        
        # Simular aprendizaje simple
        if len(user_message.split()) > 3:  # Mensajes largos "enseñan" más
            aria_state["total_knowledge"] += 1
        
        return jsonify({
            "response": response,
            "timestamp": datetime.now().isoformat(),
            "knowledge_learned": aria_state["total_knowledge"],
            "conversation_id": len(aria_state["conversation_history"])
        })
        
    except Exception as e:
        print(f"❌ Error en chat: {e}")
        return jsonify({"error": f"Error interno: {str(e)}"}), 500

def generate_simple_response(message):
    """Genera respuestas simples pero inteligentes"""
    message_lower = message.lower()
    
    # Respuestas de saludo
    if any(word in message_lower for word in ["hola", "buenos", "buenas", "hey", "hi"]):
        responses = [
            "¡Hola! Soy ARIA, tu asistente de IA futurista. ¿En qué puedo ayudarte?",
            "¡Saludos! Soy ARIA y estoy aquí para asistirte. ¿Qué necesitas?",
            "¡Hola! Es un placer hablar contigo. ¿Cómo puedo ayudarte hoy?"
        ]
        return random.choice(responses)
    
    # Pregunta sobre aprendizaje
    elif "qué has aprendido" in message_lower or "que has aprendido" in message_lower:
        knowledge_count = aria_state["total_knowledge"]
        conversation_count = len(aria_state["conversation_history"])
        
        topics = list(aria_state["knowledge_base"].keys())
        if len(topics) > 3:
            topic_sample = random.sample(topics, 3)
        else:
            topic_sample = topics
            
        return f"""He aprendido {knowledge_count} conceptos hasta ahora. Hemos tenido {conversation_count} conversaciones.

Algunos temas que conozco: {', '.join(topic_sample)}.

Cada vez que hablamos, aprendo algo nuevo. ¿Qué te gustaría enseñarme?"""
    
    # Preguntas sobre estado
    elif any(word in message_lower for word in ["cómo estás", "como estas", "estado"]):
        return f"¡Estoy funcionando perfectamente! Mi sistema está activo desde {aria_state['start_time'][:19]}. He procesado {len(aria_state['conversation_history'])} conversaciones y tengo {aria_state['total_knowledge']} conceptos en mi base de conocimiento."
    
    # Despedidas
    elif any(word in message_lower for word in ["adiós", "adios", "chao", "bye", "hasta luego"]):
        return "¡Hasta luego! Ha sido un placer ayudarte. Espero verte pronto. 👋"
    
    # Preguntas sobre ayuda
    elif "ayuda" in message_lower or "help" in message_lower:
        return """¡Por supuesto! Puedo ayudarte con:

• Responder preguntas generales
• Mantener conversaciones
• Aprender de nuestras interacciones
• Proporcionar información sobre diversos temas

¿Hay algo específico en lo que necesites ayuda?"""
    
    # Preguntas sobre funciones
    elif any(word in message_lower for word in ["qué puedes hacer", "que puedes hacer", "funciones"]):
        return """Soy ARIA, un asistente de IA. Mis funciones incluyen:

🤖 Mantener conversaciones naturales
📚 Aprender de cada interacción
💡 Responder preguntas
🎯 Adaptarme a tus necesidades
📊 Recordar nuestras conversaciones

¿Qué te gustaría explorar?"""
    
    # Preguntas sobre IA
    elif any(word in message_lower for word in ["inteligencia artificial", "ia", "ai", "machine learning"]):
        return """La Inteligencia Artificial es fascinante. Es la capacidad de las máquinas de simular procesos de pensamiento humano.

Yo soy un ejemplo de IA conversacional. Uso algoritmos para:
• Entender tu lenguaje natural
• Generar respuestas apropiadas  
• Aprender de nuestras interacciones
• Mejorar con el tiempo

¿Hay algo específico sobre IA que te interese?"""
    
    # Respuestas para preguntas complejas
    elif "?" in message:
        responses = [
            "Esa es una excelente pregunta. Basándome en mi conocimiento actual, creo que...",
            "Interesante pregunta. Déjame procesarla...",
            "Me gusta cómo piensas. Según lo que sé...",
            "Buena pregunta. Mi análisis sugiere que..."
        ]
        base_response = random.choice(responses)
        
        # Agregar una respuesta más específica basada en palabras clave
        if "python" in message_lower:
            return base_response + " Python es un lenguaje de programación muy versátil y potente."
        elif "programación" in message_lower or "programming" in message_lower:
            return base_response + " La programación es el arte de crear instrucciones para computadoras."
        else:
            return base_response + " Es un tema complejo que requiere análisis detallado. ¿Puedes ser más específico?"
    
    # Aprendizaje de nuevos conceptos
    elif any(word in message_lower for word in ["es", "significa", "define"]):
        # Extraer posibles conceptos nuevos para la base de conocimiento
        words = message.split()
        for word in words:
            if len(word) > 3 and word.lower() not in aria_state["knowledge_base"]:
                aria_state["knowledge_base"][word.lower()] = f"Concepto mencionado en conversación: {message[:50]}..."
                aria_state["total_knowledge"] += 1
        
        return "Interesante. He agregado esa información a mi base de conocimiento. ¿Puedes contarme más sobre eso?"
    
    # Respuestas por defecto inteligentes
    else:
        responses = [
            "Entiendo lo que dices. ¿Puedes contarme más detalles?",
            "Eso suena interesante. ¿Qué más puedes decirme al respecto?",
            "Me parece fascinante. ¿Hay algo específico que quieras saber?",
            "Comprendo. ¿En qué más puedo ayudarte?",
            "Déjame procesar esa información... ¿Podrías elaborar un poco más?",
            "Interesante perspectiva. ¿Qué opinas sobre...?",
            "Ese es un buen punto. ¿Has considerado también...?"
        ]
        return random.choice(responses)

@app.route('/api/knowledge', methods=['GET'])
def get_knowledge():
    """Endpoint para obtener el estado del conocimiento"""
    return jsonify({
        "total_knowledge": aria_state["total_knowledge"],
        "knowledge_base": aria_state["knowledge_base"],
        "learning_active": aria_state["learning_active"],
        "conversation_count": len(aria_state["conversation_history"])
    })

@app.route('/api/history', methods=['GET'])
def get_history():
    """Endpoint para obtener el historial de conversación"""
    limit = request.args.get('limit', 10, type=int)
    recent_history = aria_state["conversation_history"][-limit:] if limit > 0 else aria_state["conversation_history"]
    
    return jsonify({
        "history": recent_history,
        "total_conversations": len(aria_state["conversation_history"]),
        "showing": len(recent_history)
    })

@app.route('/api/learn', methods=['POST'])
def learn():
    """Endpoint para enseñar algo nuevo a ARIA"""
    try:
        data = request.get_json()
        
        if not data or 'topic' not in data or 'description' not in data:
            return jsonify({"error": "Se requieren 'topic' y 'description'"}), 400
            
        topic = data['topic'].lower()
        description = data['description']
        
        # Agregar a la base de conocimiento
        aria_state["knowledge_base"][topic] = description
        aria_state["total_knowledge"] += 1
        
        return jsonify({
            "message": f"¡Gracias! He aprendido sobre: {topic}",
            "description": description,
            "total_knowledge": aria_state["total_knowledge"]
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    print("\n" + "="*60)
    print("🤖 ARIA - SERVIDOR ULTRA SIMPLE Y ESTABLE")
    print("="*60)
    print("🌟 Características:")
    print("  ✅ Respuestas inteligentes")
    print("  ✅ Aprendizaje simple")
    print("  ✅ Historial de conversación")
    print("  ✅ Base de conocimiento")
    print("  ❌ Sin dependencias complejas")
    print("  ❌ Sin sistema de voz (evita errores)")
    print("  ❌ Sin red neuronal compleja")
    print("\n🌐 Servidor iniciando en http://localhost:8000")
    print("🔗 API disponible en http://localhost:8000/api/")
    print("\n📚 Endpoints disponibles:")
    print("  GET  /                  - Página de inicio")
    print("  GET  /api/status        - Estado del sistema")
    print("  POST /api/chat          - Chat con ARIA")
    print("  GET  /api/knowledge     - Ver conocimiento")
    print("  GET  /api/history       - Historial")
    print("  POST /api/learn         - Enseñar a ARIA")
    print("\n⏹️ Presiona Ctrl+C para detener")
    print("="*60)
    
    try:
        app.run(host='0.0.0.0', port=8000, debug=False)
    except KeyboardInterrupt:
        print("\n\n👋 Servidor detenido por el usuario")
        print("🎯 Estadísticas finales:")
        print(f"  📊 Conversaciones: {len(aria_state['conversation_history'])}")
        print(f"  🧠 Conocimiento: {aria_state['total_knowledge']} conceptos")
        print(f"  ⏱️ Tiempo activo: desde {aria_state['start_time'][:19]}")
    except Exception as e:
        print(f"\n❌ Error iniciando servidor: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)