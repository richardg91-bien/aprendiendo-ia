#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ARIA - Asistente Virtual (Versión de Diagnóstico)
"""

from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import pyttsx3
import threading
import queue
import json
import datetime
import whisper
import os

print("🚀 Iniciando ARIA - Versión de diagnóstico...")

# Configuración básica
app = Flask(__name__)
CORS(app)

class AsistenteWebDiagnostico:
    def __init__(self):
        print("🔧 Inicializando componentes básicos...")
        
        try:
            self.engine = pyttsx3.init()
            print("✅ Motor de voz inicializado")
        except Exception as e:
            print(f"⚠️ Error en motor de voz: {e}")
            self.engine = None
        
        try:
            print("📥 Cargando modelo Whisper...")
            self.whisper_model = whisper.load_model("tiny")
            print("✅ Whisper cargado")
        except Exception as e:
            print(f"⚠️ Error cargando Whisper: {e}")
            self.whisper_model = None
        
        self.cola_respuestas = queue.Queue()
        
        try:
            from memoria_aria import MemoriaARIA
            self.memoria = MemoriaARIA()
            print("✅ Sistema de memoria cargado")
        except Exception as e:
            print(f"⚠️ Error cargando memoria: {e}")
            self.memoria = None
        
        print("✅ Componentes básicos inicializados")

# Crear instancia global
print("🤖 Creando instancia del asistente...")
asistente = None

try:
    asistente = AsistenteWebDiagnostico()
    print("✅ Asistente creado exitosamente")
except Exception as e:
    print(f"❌ Error creando asistente: {e}")
    import traceback
    traceback.print_exc()

@app.route('/')
def index():
    return render_template('asistente.html')

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        mensaje = data.get('mensaje', '')
        
        # Respuesta simple para diagnóstico
        respuesta = f"🧪 ARIA Diagnóstico - Recibido: {mensaje}"
        
        return jsonify({
            'respuesta': respuesta,
            'timestamp': datetime.datetime.now().strftime('%H:%M:%S'),
            'tipo': 'diagnostico'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/test', methods=['GET'])
def test():
    return jsonify({
        'status': 'ok',
        'message': 'ARIA Diagnóstico funcionando',
        'timestamp': datetime.datetime.now().isoformat(),
        'components': {
            'whisper': asistente.whisper_model is not None if asistente else False,
            'engine': asistente.engine is not None if asistente else False,
            'memoria': asistente.memoria is not None if asistente else False
        }
    })

if __name__ == '__main__':
    print("🌐 Iniciando servidor web...")
    try:
        app.run(host='127.0.0.1', port=5001, debug=True, threaded=True)
    except Exception as e:
        print(f"❌ Error iniciando servidor: {e}")
        import traceback
        traceback.print_exc()