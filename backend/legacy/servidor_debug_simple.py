#!/usr/bin/env python3
"""
Servidor de debug simplificado para ARIA
"""

from flask import Flask, jsonify
from flask_cors import CORS
import sys
import traceback

print("🔧 Iniciando servidor de debug simplificado...")

app = Flask(__name__)
CORS(app)

@app.route('/api/status')
def api_status():
    return jsonify({
        "success": True,
        "message": "✅ Servidor de debug funcionando",
        "debug_info": {
            "python_version": sys.version,
            "flask_working": True
        }
    })

@app.route('/')
def home():
    return "<h1>🤖 ARIA Debug Server</h1><p>Servidor funcionando correctamente</p>"

if __name__ == '__main__':
    try:
        print("🚀 Iniciando servidor de debug en puerto 5000...")
        print("📡 Endpoints disponibles:")
        print("   - http://localhost:5000/")
        print("   - http://localhost:5000/api/status")
        print("=" * 50)
        
        app.run(
            host='0.0.0.0', 
            port=5000, 
            debug=True,
            use_reloader=False  # Evitar problemas con el reloader
        )
    except Exception as e:
        print(f"❌ Error iniciando servidor: {e}")
        traceback.print_exc()
        input("Presiona Enter para continuar...")