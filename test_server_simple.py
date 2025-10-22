#!/usr/bin/env python3
"""
Servidor de prueba simplificado para probar las correcciones de ARIA
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
import sys
import os

# Agregar rutas
sys.path.append(os.path.dirname(__file__))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

app = Flask(__name__)
CORS(app)

# Intentar cargar el sistema avanzado
try:
    from auto_learning_advanced import aria_advanced_learning
    ADVANCED_AVAILABLE = True
    print("✅ Sistema avanzado cargado")
except ImportError as e:
    ADVANCED_AVAILABLE = False
    print(f"❌ Sistema avanzado no disponible: {e}")

@app.route('/api/status')
def status():
    return jsonify({"status": "ok", "advanced": ADVANCED_AVAILABLE})

@app.route('/api/chat', methods=['POST'])
def chat_test():
    data = request.get_json()
    message = data.get('message', '').strip()
    
    print(f"📩 Mensaje recibido: {message}")
    
    # Respuestas básicas simples
    basic_responses = {
        'hola': '¡Hola! Me alegra saludarte.',
        'adios': '¡Hasta luego!'
    }
    
    message_lower = message.lower()
    response = None
    confidence = 0.7
    
    # Buscar respuestas básicas
    for key, value in basic_responses.items():
        if message_lower == key:
            response = value
            confidence = 0.9
            break
    
    # Si no es básica, usar sistema avanzado
    if not response and ADVANCED_AVAILABLE:
        try:
            # Buscar conocimiento
            knowledge_results = aria_advanced_learning.search_knowledge(message, limit=1)
            
            if knowledge_results:
                best_result = knowledge_results[0]
                response = f"Tengo conocimiento sobre {best_result['topic']}: {best_result['content'][:200]}..."
                confidence = best_result['confidence_score']
                print(f"✅ Conocimiento encontrado: {best_result['topic']}")
            else:
                # Para preguntas sobre aprendizaje
                if any(word in message_lower for word in ['aprendido', 'aprender', 'conocimiento']):
                    status = aria_advanced_learning.get_status()
                    total = status.get('total_knowledge', 0)
                    if total > 0:
                        response = f"He aprendido {total} elementos de conocimiento real de fuentes científicas."
                        confidence = 0.95
                        print(f"✅ Resumen de aprendizaje: {total} elementos")
                    else:
                        response = "Aún no he aprendido elementos específicos."
        except Exception as e:
            print(f"❌ Error en sistema avanzado: {e}")
    
    # Fallback
    if not response:
        response = f"Interesante. Me dijiste: '{message}'. Estoy aprendiendo a responder mejor cada día."
        confidence = 0.65
    
    print(f"🤖 Respuesta: {response[:50]}...")
    
    return jsonify({
        "success": True,
        "response": response,
        "confidence": confidence
    })

if __name__ == '__main__':
    print("🧪 SERVIDOR DE PRUEBA ARIA")
    print("=" * 30)
    print(f"🌐 Iniciando en puerto 8001...")
    app.run(host='0.0.0.0', port=8001, debug=False)