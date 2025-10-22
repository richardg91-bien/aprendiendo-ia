from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return jsonify({"message": "Servidor Flask funcionando correctamente", "status": "OK"})

@app.route('/test')
def test():
    return jsonify({"test": True, "message": "Endpoint de prueba funcionando"})

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        mensaje = data.get('mensaje', '')
        return jsonify({
            "success": True,
            "respuesta": f"Respuesta simulada para: {mensaje}",
            "timestamp": "2025-10-16T10:00:00Z"
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"Error en el chat: {str(e)}"
        }), 500

@app.route('/buscar_web', methods=['POST'])
def buscar_web():
    try:
        data = request.json
        consulta = data.get('consulta', '')
        return jsonify({
            "success": True,
            "resultados": [
                {
                    "titulo": f"Resultado simulado para: {consulta}",
                    "contenido": "Este es un contenido de ejemplo para la búsqueda web.",
                    "url": "https://ejemplo.com",
                    "fuente": "Simulador"
                }
            ],
            "total_resultados": 1
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"Error en la búsqueda: {str(e)}"
        }), 500

@app.route('/red_neuronal_info')
def red_neuronal_info():
    return jsonify({
        "success": True,
        "message": "Red neuronal disponible",
        "parametros": 4456,
        "accuracy": 33.3,
        "epochs": 50,
        "estado": "Lista"
    })

@app.route('/entrenar_red_neuronal', methods=['POST'])
def entrenar_red_neuronal():
    try:
        # Simular entrenamiento exitoso
        return jsonify({
            "success": True,
            "message": "Entrenamiento completado exitosamente",
            "accuracy": 35.5,
            "epochs": 50
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Error durante el entrenamiento: {str(e)}"
        }), 500

if __name__ == '__main__':
    print("🌐 Iniciando servidor Flask simple...")
    print("🔗 Accede a: http://localhost:5002")
    try:
        app.run(host='0.0.0.0', port=5002, debug=False, threaded=True)
    except Exception as e:
        print(f"Error iniciando servidor: {e}")
        input("Presiona Enter para continuar...")