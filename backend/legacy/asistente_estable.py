#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ARIA - Asistente Virtual Web con Red Neuronal (Versión Estable)
Sistema de IA avanzado con TensorFlow, Whisper y procesamiento de lenguaje natural
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

# Configuración básica de Flask
app = Flask(__name__)
CORS(app)

print("🤖 Iniciando ARIA - Sistema de IA Avanzado...")

class AsistenteWeb:
    def __init__(self):
        print("🔧 Inicializando componentes principales...")
        
        # Motor de voz
        self.engine = pyttsx3.init()
        self.configurar_voz()
        print("🗣️ Motor de voz configurado")
        
        # Whisper para transcripción
        print("📥 Cargando Whisper...")
        self.whisper_model = whisper.load_model("tiny")
        print("✅ Whisper listo")
        
        # Cola de respuestas y sistema de memoria
        self.cola_respuestas = queue.Queue()
        
        # Cargar sistema de memoria
        try:
            from memoria_aria import MemoriaARIA
            self.memoria = MemoriaARIA()
            print("🧠 Sistema de memoria cargado")
        except Exception as e:
            print(f"⚠️ Error cargando memoria: {e}")
            self.memoria = None
        
        # Red neuronal - cargar en segundo plano
        self.red_neuronal = None
        self.red_neuronal_ready = False
        self._inicializar_red_neuronal_async()
        
        print("✅ ARIA inicializado - Servidor listo!")
        
    def _inicializar_red_neuronal_async(self):
        """Carga la red neuronal en segundo plano"""
        def _cargar_red_neuronal():
            try:
                print("🧠 Cargando red neuronal TensorFlow en segundo plano...")
                from red_neuronal_aria import RedNeuronalARIA
                
                self.red_neuronal = RedNeuronalARIA()
                
                # Verificar si el modelo existe y está entrenado
                if not self.red_neuronal.is_trained:
                    print("🎓 Entrenando red neuronal...")
                    self.red_neuronal.entrenar_red_neuronal()
                
                self.red_neuronal_ready = True
                print("🎯 Red neuronal TensorFlow lista y funcionando!")
                
            except Exception as e:
                print(f"⚠️ Red neuronal no disponible: {e}")
                self.red_neuronal = None
                self.red_neuronal_ready = False
        
        # Ejecutar en hilo independiente
        hilo_neuronal = threading.Thread(target=_cargar_red_neuronal, daemon=True)
        hilo_neuronal.start()
        
    def configurar_voz(self):
        voices = self.engine.getProperty('voices')
        for voice in voices:
            if 'spanish' in voice.name.lower():
                self.engine.setProperty('voice', voice.id)
                break
        self.engine.setProperty('rate', 180)
        self.engine.setProperty('volume', 0.8)
    
    def hablar(self, texto):
        def _hablar():
            self.engine.say(texto)
            self.engine.runAndWait()
        
        hilo = threading.Thread(target=_hablar, daemon=True)
        hilo.start()
        return texto
    
    def procesar_comando(self, comando):
        """Procesa comando con o sin red neuronal según disponibilidad"""
        comando_original = comando
        comando = comando.lower().strip()
        
        # Respuesta base
        respuesta = ""
        categoria = "general"
        usa_red_neuronal = False
        
        # Intentar usar red neuronal si está disponible
        if self.red_neuronal_ready and self.red_neuronal:
            try:
                resultado_neuronal = self.red_neuronal.predecir_categoria(comando)
                categoria = resultado_neuronal['categoria']
                confianza = resultado_neuronal['confianza']
                usa_red_neuronal = True
                
                # Si la confianza es alta, mencionar la red neuronal
                if confianza > 0.7:
                    suffix_neuronal = f" [Red neuronal: {confianza*100:.1f}% confianza]"
                else:
                    suffix_neuronal = ""
                    
            except Exception as e:
                print(f"Error en predicción neuronal: {e}")
                suffix_neuronal = ""
        else:
            suffix_neuronal = ""
        
        # Generar respuesta basada en la categoría
        if 'hola' in comando or 'buenos días' in comando or 'hey' in comando:
            respuesta = f"¡Hola! 👋 Soy ARIA, tu asistente virtual con IA avanzada.{suffix_neuronal}"
            categoria = "saludo"
        elif 'hora' in comando:
            hora_actual = datetime.datetime.now().strftime('%H:%M:%S')
            respuesta = f"🕒 Son las {hora_actual}{suffix_neuronal}"
            categoria = "tiempo"
        elif 'fecha' in comando or 'día' in comando:
            fecha_actual = datetime.datetime.now().strftime('%d de %B de %Y')
            respuesta = f"📅 Hoy es {fecha_actual}{suffix_neuronal}"
            categoria = "fecha"
        elif 'chiste' in comando or 'gracioso' in comando:
            respuesta = f"🤣 ¿Por qué los programadores prefieren el modo oscuro? ¡Porque la luz atrae bugs!{suffix_neuronal}"
            categoria = "entretenimiento"
        elif 'python' in comando or 'programar' in comando or 'código' in comando:
            respuesta = f"💻 ¡Python es genial! ¿Necesitas ayuda con algún proyecto de programación?{suffix_neuronal}"
            categoria = "programacion"
        elif 'cómo estás' in comando or 'funcionando' in comando:
            estado_red = "con red neuronal TensorFlow activa 🧠" if self.red_neuronal_ready else "inicializando red neuronal 🔄"
            respuesta = f"🤖 ¡Funcionando perfectamente {estado_red}!{suffix_neuronal}"
            categoria = "estado"
        elif 'ayuda' in comando or 'asistencia' in comando:
            respuesta = f"🆘 ¡Estoy aquí para ayudarte! Puedo hablar, recordar conversaciones y usar IA para responder mejor.{suffix_neuronal}"
            categoria = "ayuda"
        else:
            respuesta = f"🤔 Interesante pregunta. Estoy procesándola con mis sistemas de IA.{suffix_neuronal}"
            categoria = "general"
        
        # Guardar en memoria si está disponible
        if self.memoria:
            try:
                self.memoria.guardar_conversacion(comando_original, respuesta, categoria)
            except Exception as e:
                print(f"Error guardando conversación: {e}")
        
        return {
            'respuesta': respuesta,
            'categoria': categoria,
            'usa_red_neuronal': usa_red_neuronal,
            'red_neuronal_ready': self.red_neuronal_ready
        }

# Crear instancia global del asistente
print("🚀 Creando instancia de ARIA...")
asistente = AsistenteWeb()

# =================== RUTAS WEB ===================

@app.route('/')
def index():
    return render_template('asistente.html')

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        mensaje = data.get('mensaje', '')
        
        if not mensaje:
            return jsonify({'error': 'Mensaje vacío'}), 400
        
        # Procesar con ARIA
        resultado = asistente.procesar_comando(mensaje)
        
        return jsonify({
            'respuesta': resultado['respuesta'],
            'categoria': resultado['categoria'],
            'timestamp': datetime.datetime.now().strftime('%H:%M:%S'),
            'usa_red_neuronal': resultado['usa_red_neuronal'],
            'red_neuronal_ready': resultado['red_neuronal_ready']
        })
        
    except Exception as e:
        print(f"Error en chat: {e}")
        return jsonify({'error': f'Error procesando mensaje: {str(e)}'}), 500

@app.route('/estado', methods=['GET'])
def estado():
    """Endpoint para verificar el estado del sistema"""
    return jsonify({
        'status': 'activo',
        'red_neuronal_ready': asistente.red_neuronal_ready,
        'timestamp': datetime.datetime.now().isoformat(),
        'version': 'ARIA v2.0 - Estable',
        'componentes': {
            'whisper': asistente.whisper_model is not None,
            'memoria': asistente.memoria is not None,
            'red_neuronal': asistente.red_neuronal_ready,
            'voz': asistente.engine is not None
        }
    })

@app.route('/entrenar_red_neuronal', methods=['POST'])
def entrenar_red_neuronal():
    """Endpoint para entrenar la red neuronal"""
    try:
        if not asistente.red_neuronal:
            return jsonify({'error': 'Red neuronal no disponible'}), 400
        
        print("🧠 Iniciando entrenamiento manual...")
        resultado = asistente.red_neuronal.entrenar_red_neuronal()
        
        return jsonify({
            'success': True,
            'mensaje': 'Red neuronal entrenada exitosamente',
            'resultado': resultado
        })
        
    except Exception as e:
        print(f"Error entrenando red neuronal: {e}")
        return jsonify({'error': f'Error entrenando: {str(e)}'}), 500

@app.route('/analizar_texto', methods=['POST'])
def analizar_texto():
    """Endpoint para análisis neuronal de texto"""
    try:
        if not asistente.red_neuronal_ready:
            return jsonify({'error': 'Red neuronal no está lista'}), 400
            
        data = request.json
        texto = data.get('texto', '')
        
        if not texto:
            return jsonify({'error': 'Texto vacío'}), 400
        
        resultado = asistente.red_neuronal.predecir_categoria(texto)
        
        return jsonify({
            'texto': texto,
            'categoria': resultado['categoria'],
            'confianza': resultado['confianza'],
            'timestamp': datetime.datetime.now().isoformat()
        })
        
    except Exception as e:
        print(f"Error analizando texto: {e}")
        return jsonify({'error': f'Error en análisis: {str(e)}'}), 500

@app.route('/feedback', methods=['POST'])
def feedback():
    """Endpoint para recibir feedback del usuario"""
    try:
        data = request.json
        pregunta = data.get('pregunta', '')
        respuesta = data.get('respuesta', '')
        calificacion = data.get('calificacion', 3)
        
        if not pregunta or not respuesta:
            return jsonify({'error': 'Datos incompletos'}), 400
        
        # Guardar feedback en la memoria
        if asistente.memoria:
            try:
                asistente.memoria.agregar_interaccion(pregunta, respuesta, calificacion)
                asistente.memoria.guardar_memoria()
                
                return jsonify({
                    'success': True,
                    'mensaje': 'Feedback guardado exitosamente',
                    'calificacion': calificacion,
                    'timestamp': datetime.datetime.now().isoformat()
                })
                
            except Exception as e:
                print(f"Error guardando feedback: {e}")
                return jsonify({'error': f'Error guardando feedback: {str(e)}'}), 500
        else:
            return jsonify({'error': 'Sistema de memoria no disponible'}), 500
            
    except Exception as e:
        print(f"Error procesando feedback: {e}")
        return jsonify({'error': f'Error procesando feedback: {str(e)}'}), 500

if __name__ == '__main__':
    print("🌐 Iniciando servidor web ARIA...")
    print(f"🔗 Accede a: http://localhost:5001")
    print("🧠 La red neuronal se cargará en segundo plano")
    
    try:
        app.run(host='127.0.0.1', port=5001, debug=True, threaded=True)
    except KeyboardInterrupt:
        print("\n👋 ARIA desconectado. ¡Hasta luego!")
    except Exception as e:
        print(f"❌ Error iniciando servidor: {e}")
        import traceback
        traceback.print_exc()