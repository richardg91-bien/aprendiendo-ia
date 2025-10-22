from flask import Flask, jsonify, request, send_from_directory, send_file
from flask_cors import CORS
import os
import json
import random

app = Flask(__name__, static_folder='aria-frontend/build')
CORS(app)

# =============================================================================
# RUTAS DE LA API BACKEND
# =============================================================================

@app.route('/api/test')
def api_test():
    return jsonify({"test": True, "message": "API funcionando correctamente"})

@app.route('/api/chat', methods=['POST'])
def api_chat():
    try:
        data = request.json
        mensaje = data.get('mensaje', '')
        
        # Simular respuesta del asistente
        respuesta = f"🤖 ARIA: He procesado tu mensaje '{mensaje}'. Esta es una respuesta simulada para demostrar la funcionalidad del chat."
        
        return jsonify({
            "success": True,
            "respuesta": respuesta,
            "timestamp": "2025-10-16T10:00:00Z"
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"Error en el chat: {str(e)}"
        }), 500

@app.route('/api/buscar_web', methods=['POST'])
def api_buscar_web():
    try:
        data = request.json or {}
        consulta = data.get('consulta', '').strip()
        
        if not consulta:
            return jsonify({
                "success": False,
                "error": "La consulta no puede estar vacía"
            }), 400
        
        if len(consulta) > 200:
            return jsonify({
                "success": False,
                "error": "La consulta es demasiado larga (máximo 200 caracteres)"
            }), 400
        
        # Simular resultados de búsqueda web mejorados
        import random
        num_resultados = random.randint(3, 6)
        
        resultados = []
        for i in range(num_resultados):
            resultados.append({
                "titulo": f"� {consulta} - Resultado {i+1}",
                "contenido": f"Información detallada sobre '{consulta}'. Este resultado proporciona una visión completa y actualizada del tema, incluyendo análisis experto y datos relevantes que te ayudarán a comprender mejor el concepto.",
                "url": f"https://aria-search.com/results/{consulta.replace(' ', '-').lower()}/{i+1}",
                "fuente": f"ARIA Knowledge Base #{i+1}",
                "relevancia": round(random.uniform(0.7, 1.0), 2),
                "fecha": "2025-10-16"
            })
        
        return jsonify({
            "success": True,
            "resultados": resultados,
            "total_resultados": len(resultados),
            "consulta": consulta,
            "tiempo_busqueda": f"{random.randint(50, 300)}ms",
            "sugerencias": [
                f"{consulta} tutorial",
                f"{consulta} ejemplos",
                f"qué es {consulta}",
                f"{consulta} vs alternativas"
            ]
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"❌ Error en la búsqueda: {str(e)}"
        }), 500

@app.route('/api/red_neuronal_info')
def api_red_neuronal_info():
    return jsonify({
        "success": True,
        "message": "Red neuronal ARIA disponible",
        "parametros": 4456,
        "accuracy": 78.5,
        "epochs": 100,
        "estado": "Entrenada y Lista",
        "modelo": "ARIA Neural Network v1.0",
        "ultima_actualizacion": "2025-10-16"
    })

@app.route('/api/entrenar_red_neuronal', methods=['POST'])
def api_entrenar_red_neuronal():
    try:
        # Log de debug
        print("🧠 Recibida solicitud de entrenamiento neural")
        
        data = request.json or {}
        epochs = data.get('epochs', 50)
        
        print(f"   Epochs solicitados: {epochs}")
        
        # Validar epochs
        if epochs <= 0 or epochs > 1000:
            error_msg = "El número de epochs debe estar entre 1 y 1000"
            print(f"   ❌ {error_msg}")
            return jsonify({
                "success": False,
                "message": error_msg
            }), 400
        
        # Simular proceso de entrenamiento con métricas más realistas
        accuracy_inicial = 33.3
        accuracy_final = min(95.0, accuracy_inicial + random.uniform(15, 45))
        loss_final = max(0.01, random.uniform(0.05, 0.3))
        
        resultado = {
            "success": True,
            "message": f"🧠 Entrenamiento completado exitosamente con {epochs} epochs",
            "accuracy_inicial": accuracy_inicial,
            "accuracy_final": round(accuracy_final, 2),
            "loss_final": round(loss_final, 3),
            "epochs_completados": epochs,
            "tiempo_entrenamiento": f"{random.randint(30, 120)} segundos",
            "mejoras": [
                "🎯 Precisión en respuestas mejorada",
                "⚡ Velocidad de procesamiento optimizada", 
                "🧠 Capacidad de comprensión ampliada",
                "📊 Mejor manejo de contexto"
            ],
            "metricas": {
                "accuracy_final": round(accuracy_final, 2),
                "loss_final": round(loss_final, 3),
                "epochs": epochs,
                "learning_rate": 0.001,
                "batch_size": 32
            }
        }
        
        print(f"   ✅ Entrenamiento simulado exitoso - Precisión: {resultado['accuracy_final']}%")
        return jsonify(resultado)
        
    except Exception as e:
        error_msg = f"❌ Error en entrenar_red_neuronal: {str(e)}"
        print(error_msg)
        import traceback
        traceback.print_exc()
        return jsonify({
            "success": False,
            "message": f"❌ Error durante el entrenamiento: {str(e)}"
        }), 500

@app.route('/api/status')
def api_status():
    return jsonify({
        "success": True,
        "message": "ARIA Sistema Completo Operativo",
        "servicios": {
            "backend": "✅ Funcionando",
            "frontend": "✅ Funcionando", 
            "api": "✅ Funcionando",
            "red_neuronal": "✅ Funcionando",
            "busqueda_web": "✅ Funcionando"
        },
        "version": "1.0.0",
        "timestamp": "2025-10-16T10:00:00Z"
    })

@app.route('/api/test_endpoints')
def api_test_endpoints():
    """Endpoint de prueba para verificar que todas las funciones estén disponibles"""
    endpoints = {
        "chat": "/api/chat",
        "buscar_web": "/api/buscar_web", 
        "red_neuronal_info": "/api/red_neuronal_info",
        "entrenar_red_neuronal": "/api/entrenar_red_neuronal",
        "status": "/api/status"
    }
    
    return jsonify({
        "success": True,
        "message": "Todos los endpoints están disponibles",
        "endpoints": endpoints,
        "total_endpoints": len(endpoints)
    })

# =============================================================================
# RUTAS DEL FRONTEND (SPA)
# =============================================================================

@app.route('/static/<path:filename>')
def static_files(filename):
    """Servir archivos estáticos del build"""
    return send_from_directory(os.path.join(app.static_folder, 'static'), filename)

@app.route('/manifest.json')
def manifest():
    """Servir manifest.json"""
    return send_from_directory(app.static_folder, 'manifest.json')

@app.route('/favicon.ico')
def favicon():
    """Servir favicon"""
    return send_from_directory(app.static_folder, 'favicon.ico')

@app.route('/')
@app.route('/<path:path>')
def serve_react_app(path=None):
    """Servir la aplicación React (SPA routing)"""
    try:
        # Si el archivo existe en el build, servirlo
        if path and os.path.exists(os.path.join(app.static_folder, path)):
            return send_from_directory(app.static_folder, path)
        
        # Si no, servir index.html (para SPA routing)
        return send_from_directory(app.static_folder, 'index.html')
    except Exception as e:
        # Fallback: servir página de error personalizada
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>ARIA - Error</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 50px; text-align: center; }}
                .error {{ color: #e74c3c; }}
                .info {{ color: #3498db; margin-top: 20px; }}
            </style>
        </head>
        <body>
            <h1>🤖 ARIA - Asistente IA</h1>
            <div class="error">
                <h2>Frontend no disponible</h2>
                <p>El frontend React no está compilado.</p>
            </div>
            <div class="info">
                <h3>API Backend Funcionando ✅</h3>
                <p>Endpoints disponibles:</p>
                <ul style="text-align: left; display: inline-block;">
                    <li><a href="/api/status">/api/status</a> - Estado del sistema</li>
                    <li><a href="/api/test">/api/test</a> - Prueba de API</li>
                    <li><a href="/api/red_neuronal_info">/api/red_neuronal_info</a> - Info red neuronal</li>
                </ul>
                <p><strong>Para compilar el frontend ejecuta:</strong></p>
                <code>cd aria-frontend && npm run build</code>
            </div>
        </body>
        </html>
        """, 200

if __name__ == '__main__':
    print("🚀 Iniciando ARIA - Sistema Completo Integrado")
    print("=" * 50)
    print("🌐 Frontend + Backend en: http://localhost:5000")
    print("🔗 API endpoints: http://localhost:5000/api/")
    print("🧠 Red Neuronal: Simulada y Lista")
    print("=" * 50)
    
    # Verificar si el frontend está compilado
    build_path = os.path.join('aria-frontend', 'build', 'index.html')
    if os.path.exists(build_path):
        print("✅ Frontend compilado encontrado")
    else:
        print("⚠️  Frontend no compilado - Solo API disponible")
        print("   Para compilar: cd aria-frontend && npm run build")
    
    print("=" * 50)
    
    try:
        # Iniciar el servidor en puerto 5000
        app.run(
            host='0.0.0.0', 
            port=5000, 
            debug=False, 
            threaded=True,
            use_reloader=False  # Evitar problemas con el reloader
        )
    except Exception as e:
        print(f"❌ Error iniciando servidor: {e}")
        import traceback
        traceback.print_exc()
        input("Presiona Enter para continuar...")