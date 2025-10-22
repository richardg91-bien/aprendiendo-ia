#!/usr/bin/env python3
"""
Servidor simplificado de ARIA para pruebas - sin aprendizaje automático
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
import sys
import os
import random

# Configurar rutas
sys.path.append(os.path.dirname(__file__))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

app = Flask(__name__)
CORS(app)

# Cargar sistema avanzado
try:
    from auto_learning_advanced import aria_advanced_learning
    ADVANCED_AVAILABLE = True
    print("✅ Sistema avanzado cargado")
    
    # Verificar base de conocimiento existente
    status = aria_advanced_learning.get_status()
    total_knowledge = status.get('total_knowledge', 0)
    print(f"📚 Conocimiento disponible: {total_knowledge} elementos")
    
except ImportError as e:
    ADVANCED_AVAILABLE = False
    print(f"❌ Sistema avanzado no disponible: {e}")

@app.route('/api/status')
def status():
    return jsonify({
        "status": "ok", 
        "advanced": ADVANCED_AVAILABLE,
        "mode": "test"
    })

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.get_json()
    message = data.get('message', '').strip()
    
    if not message:
        return jsonify({"success": False, "message": "Mensaje vacío"})
    
    print(f"📩 Mensaje: {message}")
    
    # Respuestas básicas
    basic_responses = {
        'hola': '¡Hola! Soy ARIA con conocimiento avanzado.',
        'como estas': 'Funcionando perfectamente con mi base de conocimiento científico.',
        'adios': '¡Hasta luego! Espero haberte ayudado.'
    }
    
    message_lower = message.lower()
    response = None
    confidence = 0.7
    
    # Verificar respuestas básicas
    for key, value in basic_responses.items():
        if message_lower == key:
            response = value
            confidence = 0.9
            break
    
    # Si no es básica, usar sistema avanzado
    if not response and ADVANCED_AVAILABLE:
        try:
            # Buscar conocimiento específico
            knowledge_results = aria_advanced_learning.search_knowledge(message, limit=1)
            
            if knowledge_results:
                best_result = knowledge_results[0]
                response = f"""Basándome en mi conocimiento real sobre {best_result['topic']}, puedo decirte que:

{best_result['content']}

Esta información proviene de {best_result['source_name']} (confianza: {best_result['confidence_score']:.0%})."""
                
                if best_result['source_url']:
                    response += f"\n\nPuedes verificar esta información en: {best_result['source_url']}"
                
                confidence = best_result['confidence_score']
                print(f"✅ Conocimiento encontrado: {best_result['topic']}")
            
            # Para preguntas sobre aprendizaje
            elif any(word in message_lower for word in ['aprendido', 'aprender', 'conocimiento', 'que has aprendido']):
                status = aria_advanced_learning.get_status()
                total = status.get('total_knowledge', 0)
                sources = status.get('top_sources', {})
                topics = status.get('top_topics', {})
                
                if total > 0:
                    response = f"He aprendido {total} elementos de conocimiento real de fuentes científicas verificadas."
                    if topics:
                        top_topics = list(topics.keys())[:3]
                        response += f" Mis temas principales son: {', '.join(top_topics)}."
                    if sources:
                        top_source = list(sources.keys())[0]
                        response += f" Mi fuente principal es {top_source}."
                    confidence = 0.95
                    print(f"✅ Resumen de aprendizaje: {total} elementos")
                else:
                    response = "Mi base de conocimiento está inicializándose. Pregúntame sobre tecnología, ciencia o computación."
                    confidence = 0.8
            
            # Buscar por palabras clave
            else:
                words = message.lower().split()
                for word in words:
                    if len(word) > 3:
                        keyword_results = aria_advanced_learning.search_knowledge(word, limit=1)
                        if keyword_results:
                            result = keyword_results[0]
                            response = f"Encontré información relacionada sobre {result['topic']}:\n\n{result['content'][:300]}...\n\n(Fuente: {result['source_name']}, {result['confidence_score']:.0%} confianza)"
                            confidence = result['confidence_score'] * 0.8
                            print(f"✅ Coincidencia por palabra clave '{word}': {result['topic']}")
                            break
                            
        except Exception as e:
            print(f"❌ Error en sistema avanzado: {e}")
    
    # Fallback
    if not response:
        if ADVANCED_AVAILABLE:
            response = "No tengo información específica sobre ese tema en mi base de conocimiento actual. ¿Podrías preguntarme sobre tecnología, ciencia, computación o seguridad?"
            confidence = 0.6
        else:
            response = f"Interesante. Me dijiste: '{message}'. Estoy aprendiendo a responder mejor cada día."
            confidence = 0.65
    
    print(f"🤖 Respuesta generada (confianza: {confidence:.0%})")
    
    return jsonify({
        "success": True,
        "response": response,
        "confidence": confidence,
        "timestamp": "2024-10-22T10:00:00",
        "advanced_mode": ADVANCED_AVAILABLE
    })

if __name__ == '__main__':
    print("🧪 ARIA - SERVIDOR DE PRUEBA")
    print("=" * 40)
    print("🌐 Iniciando en puerto 8000...")
    print("⚠️ Modo de prueba - sin aprendizaje automático")
    app.run(host='0.0.0.0', port=8000, debug=False)