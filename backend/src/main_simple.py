"""
Servidor ARIA Simplificado - Versión Estable
Solo funcionalidades esenciales para evitar conflictos
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

# Configuración de la aplicación
app = Flask(__name__, static_folder='../../frontend/build', static_url_path='/')
CORS(app)

# Variables globales simples
conversations = []
simple_responses = [
    "¡Hola! ¿Cómo puedo ayudarte?",
    "Entiendo tu pregunta. ¿Podrías ser más específico?",
    "Interesante. Cuéntame más sobre eso.",
    "Estoy aquí para ayudarte. ¿Qué necesitas?",
    "Gracias por conversar conmigo. ¿En qué más puedo asistirte?"
]

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

@app.route('/<path:path>')
def serve_static_files(path):
    """Servir archivos estáticos"""
    try:
        return send_from_directory(app.static_folder, path)
    except Exception as e:
        return send_from_directory(app.static_folder, 'index.html')

# =====================
# API ENDPOINTS BÁSICOS
# =====================

@app.route('/api/status', methods=['GET'])
def api_status():
    """Estado del sistema"""
    return jsonify({
        "status": "online",
        "version": "2.0.0-simple",
        "timestamp": datetime.now().isoformat(),
        "components": {
            "backend": "running",
            "frontend": "available",
            "mode": "simplified"
        }
    })

@app.route('/api/chat', methods=['POST'])
def api_chat():
    """Endpoint básico para chat"""
    try:
        data = request.json
        mensaje = data.get('message', '').strip()
        
        log_info(f"💬 Chat - Mensaje recibido: {mensaje}")
        
        if not mensaje:
            return jsonify({
                "success": False,
                "message": "Mensaje vacío"
            }), 400
        
        # Respuesta simple basada en palabras clave
        respuesta = generate_simple_response(mensaje)
        
        # Guardar conversación
        conversations.append({
            "user_input": mensaje,
            "aria_response": respuesta,
            "timestamp": datetime.now().isoformat()
        })
        
        log_info(f"   🧠 ARIA: {respuesta}")
        
        return jsonify({
            "success": True,
            "response": respuesta,
            "confidence": 0.8,
            "voice_enabled": False,
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        log_info(f"❌ Error en chat: {e}")
        return jsonify({
            "success": False,
            "message": f"Error en el chat: {str(e)}"
        }), 500

def generate_simple_response(mensaje):
    """Generar respuesta simple basada en palabras clave"""
    mensaje_lower = mensaje.lower()
    
    # Respuestas específicas
    if any(word in mensaje_lower for word in ['hola', 'hello', 'hi', 'buenos días', 'buenas tardes']):
        return "¡Hola! Me alegra verte. ¿En qué puedo ayudarte hoy?"
    
    elif any(word in mensaje_lower for word in ['cómo estás', 'how are you', 'qué tal']):
        return "Estoy funcionando perfectamente, gracias por preguntar. ¿Y tú cómo estás?"
    
    elif any(word in mensaje_lower for word in ['qué significa', 'define', 'definición']):
        return "Estoy trabajando en expandir mi conocimiento de definiciones. Por ahora, puedo ayudarte con conversaciones generales."
    
    elif any(word in mensaje_lower for word in ['ayuda', 'help', 'auxilio']):
        return "Estoy aquí para ayudarte. Puedes preguntarme cualquier cosa o simplemente conversar conmigo."
    
    elif any(word in mensaje_lower for word in ['gracias', 'thank you', 'thanks']):
        return "¡De nada! Me alegra poder ayudarte. ¿Hay algo más en lo que pueda asistirte?"
    
    elif any(word in mensaje_lower for word in ['adiós', 'bye', 'hasta luego', 'chau']):
        return "¡Hasta luego! Ha sido un placer conversar contigo. ¡Que tengas un excelente día!"
    
    else:
        # Respuesta general
        return random.choice(simple_responses)

@app.route('/api/learning/stats', methods=['GET'])
def api_learning_stats():
    """Estadísticas básicas"""
    return jsonify({
        "success": True,
        "stats": {
            "total_conversations": len(conversations),
            "server_uptime": "Running",
            "mode": "simplified",
            "last_conversation": conversations[-1]["timestamp"] if conversations else None
        }
    })

@app.route('/api/red_neuronal_info', methods=['GET'])
def api_red_neuronal_info():
    """Información de la red neuronal (simulada)"""
    return jsonify({
        "success": True,
        "model": {
            "name": "ARIA Neural Network",
            "version": "2.0",
            "status": "active",
            "training_data": "basic",
            "accuracy": 0.85
        }
    })

@app.route('/api/entrenar_red_neuronal', methods=['POST'])
def api_entrenar_red_neuronal():
    """Entrenamiento simulado"""
    return jsonify({
        "success": True,
        "message": "Entrenamiento completado",
        "accuracy": 0.87,
        "epochs": 50
    })

def main():
    """Función principal para iniciar el servidor"""
    print("=" * 50)
    print("🚀 Iniciando ARIA - Servidor Simplificado")
    print("=" * 50)
    print(f"🌐 Servidor: http://{HOST}:{PORT}")
    print(f"🔗 API Base: http://{HOST}:{PORT}/api/")
    print(f"📱 Modo: Simplificado (Estable)")
    print("=" * 50)
    
    # Verificar si el frontend está compilado
    build_path = Path(app.static_folder)
    if build_path.exists():
        print("✅ Frontend React encontrado")
    else:
        print("⚠️  Frontend React no compilado")
        print("   Ejecuta 'npm run build' en el directorio frontend")
    
    print("=" * 50)
    
    try:
        app.run(
            host='0.0.0.0',
            port=PORT,
            debug=False,  # Desactivar debug para mayor estabilidad
            use_reloader=False
        )
    except KeyboardInterrupt:
        print("\n🛑 Servidor detenido por el usuario")
    except Exception as e:
        print(f"\n❌ Error en el servidor: {e}")

if __name__ == '__main__':
    main()