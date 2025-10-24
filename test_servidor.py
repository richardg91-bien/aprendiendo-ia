#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🧪 Servidor de Prueba ARIA
==========================
Script simple para probar si el servidor Flask funciona correctamente
sin todas las importaciones complejas.
"""

import sys
import os
from flask import Flask, jsonify

# Configurar Flask
app = Flask(__name__)

@app.route('/')
def home():
    """Página de inicio básica"""
    return jsonify({
        "status": "ok",
        "message": "🤖 ARIA Test Server funcionando",
        "version": "test",
        "timestamp": "2025-10-24"
    })

@app.route('/test')
def test():
    """Endpoint de prueba"""
    return jsonify({
        "test": "successful",
        "python_version": sys.version,
        "working_directory": os.getcwd()
    })

if __name__ == '__main__':
    print("🧪 Iniciando servidor de prueba...")
    print("📍 URL: http://localhost:8000")
    print("🔗 Prueba: http://localhost:8000/test")
    print("🛑 Presiona Ctrl+C para detener")
    print("-" * 40)
    
    try:
        app.run(
            host='localhost',
            port=8000,
            debug=False,
            threaded=True,
            use_reloader=False
        )
    except Exception as e:
        print(f"❌ Error: {e}")
    except KeyboardInterrupt:
        print("\n👋 Servidor detenido")