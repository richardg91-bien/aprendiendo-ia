"""
ARIA - Servidor de Diagnóstico para Entrenamiento Neural
Versión simplificada para debugging
"""
from flask import Flask, jsonify, request
from flask_cors import CORS
import random
import traceback
import sys

app = Flask(__name__)
CORS(app)

@app.route('/api/status')
def api_status():
    return jsonify({
        "success": True,
        "message": "ARIA Debug Server Funcionando",
        "puerto": 5001
    })

@app.route('/api/entrenar_red_neuronal', methods=['POST'])
def api_entrenar_red_neuronal():
    print("🧠 Recibida solicitud de entrenamiento")
    try:
        data = request.json or {}
        epochs = data.get('epochs', 50)
        
        print(f"   Epochs solicitados: {epochs}")
        
        # Validar epochs
        if epochs <= 0 or epochs > 1000:
            print(f"   ❌ Epochs inválidos: {epochs}")
            return jsonify({
                "success": False,
                "message": "El número de epochs debe estar entre 1 y 1000"
            }), 400
        
        # Simular entrenamiento
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
            "tiempo_entrenamiento": f"{random.randint(30, 120)} segundos"
        }
        
        print(f"   ✅ Entrenamiento simulado exitoso")
        print(f"   📊 Precisión final: {resultado['accuracy_final']}%")
        
        return jsonify(resultado)
        
    except Exception as e:
        print(f"❌ ERROR en entrenamiento: {str(e)}")
        traceback.print_exc()
        return jsonify({
            "success": False,
            "message": f"Error durante el entrenamiento: {str(e)}"
        }), 500

if __name__ == '__main__':
    print("🔍 ARIA - Servidor de Debug para Entrenamiento Neural")
    print("=" * 60)
    print("🌐 Ejecutándose en: http://localhost:5001")
    print("🧠 Endpoint de prueba: POST /api/entrenar_red_neuronal")
    print("=" * 60)
    
    try:
        app.run(host='127.0.0.1', port=5001, debug=True)
    except Exception as e:
        print(f"❌ Error iniciando servidor: {e}")
        sys.exit(1)