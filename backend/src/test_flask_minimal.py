#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🚀 ARIA - Servidor de Prueba Minimalista
Solo para probar que Flask funciona
"""

try:
    from flask import Flask, jsonify
    from datetime import datetime
except ImportError as e:
    print(f"Error importando Flask: {e}")
    exit(1)

print("🚀 Creando aplicación Flask...")
app = Flask(__name__)

print("✅ Flask creado correctamente")

@app.route('/')
def home():
    return jsonify({
        "message": "🤖 ARIA - Servidor de Prueba",
        "status": "OK",
        "timestamp": datetime.now().isoformat()
    })

@app.route('/test')
def test():
    return jsonify({"test": "OK", "server": "running"})

if __name__ == '__main__':
    print("🌐 Intentando iniciar servidor en puerto 8001...")
    try:
        app.run(host='localhost', port=8001, debug=True)
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()