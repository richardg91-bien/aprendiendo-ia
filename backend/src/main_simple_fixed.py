"""
ARIA - Servidor Estable SIMPLIFICADO (Sin sistema de voz problemático)
"""

import sys
import os

# Configurar codificación UTF-8 para Windows
if sys.platform.startswith('win'):
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.detach())
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.detach())

from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime
import random

# Agregar el directorio src al path para importar neural_network
sys.path.append(os.path.join(os.path.dirname(__file__)))

print("🚀 Iniciando ARIA - Modo Simplificado")

try:
    from neural_network import neural_network
    NEURAL_NETWORK_AVAILABLE = True
    print("✅ Red neuronal cargada")
except ImportError as e:
    NEURAL_NETWORK_AVAILABLE = False
    print(f"⚠️ Red neuronal no disponible: {e}")

# DESHABILITAMOS EL SISTEMA DE VOZ PROBLEMÁTICO
VOICE_SYSTEM_AVAILABLE = False
print("⚠️ Sistema de voz deshabilitado (evitar error DLL)")

try:
    from auto_learning_simple import auto_learning
    AUTO_LEARNING_AVAILABLE = True
    print("🧠 Sistema de aprendizaje simple cargado")
except ImportError as e:
    AUTO_LEARNING_AVAILABLE = False
    print(f"⚠️ Sistema de aprendizaje no disponible: {e}")

try:
    from auto_learning_advanced import aria_advanced_learning
    ADVANCED_LEARNING_AVAILABLE = True
    print("🧠 Sistema de aprendizaje avanzado cargado")
except ImportError as e:
    ADVANCED_LEARNING_AVAILABLE = False
    print(f"⚠️ Sistema de aprendizaje avanzado no disponible: {e}")

# Configuración de Flask
app = Flask(__name__)
CORS(app)

print("🌐 Configurando servidor Flask...")

# Estado global de ARIA
aria_state = {
    "knowledge_base": {},
    "conversation_history": [],
    "learning_active": True,
    "total_knowledge": 0,
    "system_status": "running",
    "voice_enabled": False,  # Deshabilitado
    "neural_network_active": NEURAL_NETWORK_AVAILABLE,
    "auto_learning_active": AUTO_LEARNING_AVAILABLE
}

@app.route('/api/status', methods=['GET'])
def get_status():
    """Endpoint para verificar el estado del sistema"""
    status = {
        "status": "running",
        "timestamp": datetime.now().isoformat(),
        "components": {
            "neural_network": NEURAL_NETWORK_AVAILABLE,
            "voice_system": False,  # Deshabilitado
            "auto_learning": AUTO_LEARNING_AVAILABLE,
            "advanced_learning": ADVANCED_LEARNING_AVAILABLE
        },
        "aria_state": aria_state
    }
    return jsonify(status)

@app.route('/api/chat', methods=['POST'])
def chat():
    """Endpoint principal de chat con ARIA"""
    try:
        data = request.get_json()
        
        if not data or 'message' not in data:
            return jsonify({"error": "Mensaje requerido"}), 400
            
        user_message = data['message']
        
        print(f"👤 Usuario: {user_message}")
        
        # Procesar mensaje con red neuronal si está disponible
        if NEURAL_NETWORK_AVAILABLE:
            try:
                response = neural_network.process_message(user_message)
                print(f"🧠 Red neuronal: {response}")
            except Exception as e:
                print(f"❌ Error en red neuronal: {e}")
                response = generate_basic_response(user_message)
        else:
            response = generate_basic_response(user_message)
        
        # Guardar en historial
        aria_state["conversation_history"].append({
            "user": user_message,
            "aria": response,
            "timestamp": datetime.now().isoformat()
        })
        
        # Aprender del mensaje si el sistema está disponible
        if AUTO_LEARNING_AVAILABLE:
            try:
                auto_learning.learn_from_conversation(user_message, response)
                aria_state["total_knowledge"] = auto_learning.get_knowledge_count()
            except Exception as e:
                print(f"⚠️ Error en aprendizaje: {e}")
        
        return jsonify({
            "response": response,
            "timestamp": datetime.now().isoformat(),
            "knowledge_learned": aria_state["total_knowledge"]
        })
        
    except Exception as e:
        print(f"❌ Error en chat: {e}")
        return jsonify({"error": str(e)}), 500

def generate_basic_response(message):
    """Genera respuestas básicas cuando no hay red neuronal"""
    message_lower = message.lower()
    
    if "hola" in message_lower or "buenos" in message_lower:
        return "¡Hola! Soy ARIA, tu asistente de IA. ¿En qué puedo ayudarte hoy?"
    
    elif "¿qué has aprendido" in message_lower or "que has aprendido" in message_lower:
        knowledge_count = aria_state.get("total_knowledge", 0)
        return f"He aprendido {knowledge_count} conceptos hasta ahora. Cada conversación me ayuda a mejorar."
    
    elif "adiós" in message_lower or "adios" in message_lower:
        return "¡Hasta luego! Ha sido un placer ayudarte."
    
    elif "cómo estás" in message_lower or "como estas" in message_lower:
        return "¡Estoy funcionando perfectamente! Mi sistema está activo y listo para ayudarte."
    
    elif "ayuda" in message_lower:
        return "Puedo ayudarte con conversaciones, responder preguntas y aprender de nuestras interacciones. ¿Qué necesitas?"
    
    else:
        responses = [
            "Interesante. Dime más sobre eso.",
            "Entiendo. ¿Puedes explicarme más detalles?",
            "Esa es una buena pregunta. ¿Qué opinas tú?",
            "Déjame procesar esa información...",
            "Me parece fascinante. ¿Hay algo específico que quieras saber?"
        ]
        return random.choice(responses)

@app.route('/api/learn', methods=['POST'])
def learn():
    """Endpoint para aprendizaje manual"""
    try:
        data = request.get_json()
        
        if not data or 'topic' not in data:
            return jsonify({"error": "Topic requerido"}), 400
            
        topic = data['topic']
        
        if ADVANCED_LEARNING_AVAILABLE:
            try:
                result = aria_advanced_learning._learn_from_arxiv(topic)
                aria_state["total_knowledge"] = aria_advanced_learning.get_status().get('total_knowledge', 0)
                
                return jsonify({
                    "message": f"He aprendido sobre: {topic}",
                    "result": result,
                    "total_knowledge": aria_state["total_knowledge"]
                })
            except Exception as e:
                return jsonify({"error": f"Error en aprendizaje: {str(e)}"}), 500
        else:
            return jsonify({"error": "Sistema de aprendizaje avanzado no disponible"}), 503
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/knowledge', methods=['GET'])
def get_knowledge():
    """Endpoint para obtener el estado del conocimiento"""
    try:
        if ADVANCED_LEARNING_AVAILABLE:
            status = aria_advanced_learning.get_status()
            return jsonify(status)
        elif AUTO_LEARNING_AVAILABLE:
            return jsonify({
                "total_knowledge": auto_learning.get_knowledge_count(),
                "learning_active": True
            })
        else:
            return jsonify({
                "total_knowledge": 0,
                "learning_active": False,
                "message": "Sistema de aprendizaje no disponible"
            })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/history', methods=['GET'])
def get_history():
    """Endpoint para obtener el historial de conversación"""
    return jsonify({
        "history": aria_state["conversation_history"][-10:],  # Últimas 10 conversaciones
        "total_conversations": len(aria_state["conversation_history"])
    })

@app.route('/', methods=['GET'])
def index():
    """Página de inicio"""
    return jsonify({
        "message": "ARIA - Asistente IA Futurista",
        "status": "running",
        "endpoints": [
            "/api/status",
            "/api/chat",
            "/api/learn",
            "/api/knowledge", 
            "/api/history"
        ]
    })

if __name__ == '__main__':
    print("\n" + "="*50)
    print("🤖 ARIA - Servidor Estable SIMPLIFICADO")
    print("="*50)
    print(f"🧠 Red neuronal: {'✅ Activa' if NEURAL_NETWORK_AVAILABLE else '❌ No disponible'}")
    print(f"🔊 Sistema de voz: ❌ Deshabilitado (evitar error DLL)")
    print(f"📚 Aprendizaje simple: {'✅ Activo' if AUTO_LEARNING_AVAILABLE else '❌ No disponible'}")
    print(f"🚀 Aprendizaje avanzado: {'✅ Activo' if ADVANCED_LEARNING_AVAILABLE else '❌ No disponible'}")
    print("\n🌐 Iniciando servidor en http://localhost:8000")
    print("🔗 API disponible en http://localhost:8000/api/")
    print("\n⏹️ Presiona Ctrl+C para detener el servidor")
    print("="*50)
    
    try:
        app.run(host='0.0.0.0', port=8000, debug=False)
    except KeyboardInterrupt:
        print("\n\n👋 Servidor detenido por el usuario")
    except Exception as e:
        print(f"\n❌ Error iniciando servidor: {e}")
        sys.exit(1)