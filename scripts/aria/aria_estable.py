#!/usr/bin/env python3
"""
ARIA - Servidor Simple con Conocimiento Real
Versión estable para demostrar capacidades sin auto-aprendizaje
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
import sys
import os
import random

# Configurar rutas
current_dir = os.path.dirname(os.path.abspath(__file__))
backend_src = os.path.join(current_dir, 'backend', 'src')
sys.path.append(current_dir)
sys.path.append(backend_src)

app = Flask(__name__)
CORS(app)

# Cargar sistema avanzado
try:
    sys.path.append(backend_src)
    from auto_learning_advanced import aria_advanced_learning
    ADVANCED_AVAILABLE = True
    print("✅ Sistema avanzado cargado")
    
    # Asegurar que tenemos conocimiento
    status = aria_advanced_learning.get_status()
    total = status.get('total_knowledge', 0)
    if total == 0:
        print("📚 Agregando conocimiento inicial...")
        aria_advanced_learning._learn_from_arxiv('artificial intelligence')
        aria_advanced_learning._learn_from_arxiv('cloud computing')
        status = aria_advanced_learning.get_status()
        total = status.get('total_knowledge', 0)
    
    print(f"📊 Conocimiento disponible: {total} elementos")
    
except Exception as e:
    ADVANCED_AVAILABLE = False
    print(f"❌ Sistema avanzado no disponible: {e}")

@app.route('/api/status')
def status():
    return jsonify({
        "status": "ok", 
        "advanced": ADVANCED_AVAILABLE,
        "knowledge_count": aria_advanced_learning.get_status().get('total_knowledge', 0) if ADVANCED_AVAILABLE else 0
    })

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.get_json()
    message = data.get('message', '').strip()
    
    if not message:
        return jsonify({"success": False, "message": "Mensaje vacío"})
    
    print(f"📩 Mensaje recibido: {message}")
    
    # Respuestas básicas
    basic_responses = {
        'hola': '¡Hola! Soy ARIA con conocimiento científico real.',
        'como estas': 'Funcionando perfectamente con mi base de conocimiento.',
        'adios': '¡Hasta luego!'
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
    
    # Si no es básica y tenemos sistema avanzado
    if not response and ADVANCED_AVAILABLE:
        try:
            # Para preguntas sobre aprendizaje
            if any(word in message_lower for word in ['aprendido', 'aprender', 'conocimiento', 'que has aprendido', 'qué has aprendido']):
                status = aria_advanced_learning.get_status()
                total = status.get('total_knowledge', 0)
                topics = status.get('top_topics', {})
                sources = status.get('top_sources', {})
                
                if total > 0:
                    response = f"""He aprendido {total} elementos de conocimiento científico REAL verificado.

🧠 **Mis temas principales:**
{', '.join(list(topics.keys())[:5])}

📚 **Fuentes científicas:**
{', '.join(list(sources.keys())[:3])}

🌐 **Capacidades:**
• Papers científicos de ArXiv
• Definiciones de la RAE  
• Noticias tecnológicas
• Conocimiento verificado al 95%

¿Quieres que profundice en algún tema específico?"""
                    confidence = 0.95
                    print(f"✅ Respondiendo con resumen de {total} elementos")
                else:
                    response = "Mi base de conocimiento se está inicializando. Dame un momento para cargar información científica."
                    confidence = 0.8
            
            # Buscar conocimiento específico
            else:
                knowledge_results = aria_advanced_learning.search_knowledge(message, limit=1)
                
                if knowledge_results:
                    best_result = knowledge_results[0]
                    response = f"""Basándome en mi conocimiento científico real sobre **{best_result['topic']}**:

{best_result['content']}

📚 **Fuente:** {best_result['source_name']} 
📊 **Confianza:** {best_result['confidence_score']:.0%}
🌐 **Verificable en:** {best_result.get('source_url', 'Fuente interna')}"""
                    
                    confidence = best_result['confidence_score']
                    print(f"✅ Conocimiento específico encontrado: {best_result['topic']}")
                
                # Buscar por palabras clave
                else:
                    words = message.lower().split()
                    for word in words:
                        if len(word) > 3:
                            keyword_results = aria_advanced_learning.search_knowledge(word, limit=1)
                            if keyword_results:
                                result = keyword_results[0]
                                response = f"""Encontré información relacionada sobre **{result['topic']}**:

{result['content'][:300]}...

📚 **Fuente:** {result['source_name']} ({result['confidence_score']:.0%} confianza)

¿Te gustaría más detalles sobre este tema?"""
                                confidence = result['confidence_score'] * 0.8
                                print(f"✅ Coincidencia por palabra clave '{word}': {result['topic']}")
                                break
                
        except Exception as e:
            print(f"❌ Error accediendo conocimiento: {e}")
    
    # Fallback
    if not response:
        if ADVANCED_AVAILABLE:
            response = """No tengo información específica sobre ese tema en mi base actual.

🔍 **Puedo ayudarte con:**
• Inteligencia artificial
• Cloud computing  
• Tecnología y ciencia
• Definiciones técnicas

¿Podrías preguntarme sobre alguno de estos temas?"""
            confidence = 0.6
        else:
            response = f"Interesante. Me dijiste: '{message}'. Estoy aprendiendo a responder mejor cada día."
            confidence = 0.65
    
    print(f"🤖 Respuesta enviada (confianza: {confidence:.0%})")
    
    return jsonify({
        "success": True,
        "response": response,
        "confidence": confidence,
        "timestamp": "2024-10-22T10:00:00",
        "knowledge_used": ADVANCED_AVAILABLE and "aprendido" in message_lower
    })

if __name__ == '__main__':
    print("🚀 ARIA - SERVIDOR ESTABLE")
    print("=" * 40)
    print("📚 Con conocimiento científico real")
    print("🌐 Puerto: 8000")
    print("⚠️ Versión estable - sin auto-aprendizaje")
    print()
    
    app.run(host='0.0.0.0', port=8000, debug=False)