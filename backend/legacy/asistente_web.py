from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import pyttsx3
import threading
import queue
import json
import datetime
import whisper
import os
from memoria_aria import MemoriaARIA
from red_neuronal_aria import RedNeuronalARIA
from buscador_web_aria import buscador_web_aria

app = Flask(__name__)
CORS(app)

class AsistenteWeb:
    def __init__(self):
        self.engine = pyttsx3.init()
        self.configurar_voz()
        self.whisper_model = whisper.load_model("tiny")
        self.cola_respuestas = queue.Queue()
        self.memoria = MemoriaARIA()  # Sistema de memoria y aprendizaje
        
        # 🧠 RED NEURONAL AVANZADA - Inicialización diferida
        print("🧠 Preparando Red Neuronal ARIA...")
        self.red_neuronal = None
        self._inicializar_red_neuronal_async()
        
    def configurar_voz(self):
        voices = self.engine.getProperty('voices')
        for voice in voices:
            if 'spanish' in voice.name.lower():
                self.engine.setProperty('voice', voice.id)
                break
        self.engine.setProperty('rate', 180)
        self.engine.setProperty('volume', 0.8)
    
    def _inicializar_red_neuronal_async(self):
        """Inicializa la red neuronal en segundo plano para no bloquear el servidor"""
        def _init_red_neuronal():
            try:
                print("🧠 Cargando Red Neuronal en segundo plano...")
                from red_neuronal_aria import RedNeuronalARIA
                self.red_neuronal = RedNeuronalARIA()
                if not self.red_neuronal.is_trained:
                    print("🎓 Entrenando red neuronal por primera vez...")
                    self.red_neuronal.entrenar_red_neuronal()
                print("✅ Red neuronal lista y funcionando!")
            except Exception as e:
                print(f"⚠️ Error inicializando red neuronal: {e}")
                self.red_neuronal = None
        
        # Ejecutar en hilo separado para no bloquear
        hilo_red_neuronal = threading.Thread(target=_init_red_neuronal)
        hilo_red_neuronal.daemon = True
        hilo_red_neuronal.start()
    
    def hablar(self, texto):
        def _hablar():
            self.engine.say(texto)
            self.engine.runAndWait()
        
        hilo = threading.Thread(target=_hablar)
        hilo.daemon = True
        hilo.start()
        return texto
    
    def procesar_comando(self, comando):
        comando_original = comando
        comando = comando.lower().strip()
        
        # 🧠 SISTEMA NEURONAL AVANZADO: Análisis con Deep Learning
        if self.red_neuronal and self.red_neuronal.is_trained:
            try:
                prediccion = self.red_neuronal.predecir_categoria(comando)
                categoria = prediccion['categoria']
                confianza = prediccion['confianza']
                
                # Si la red neuronal tiene alta confianza, usar su respuesta
                if confianza > 0.7:
                    respuesta_neural = self.red_neuronal.generar_respuesta_inteligente(
                        comando, categoria, confianza
                    )
                    
                    # Registrar en memoria
                    self.memoria.agregar_interaccion(comando_original, respuesta_neural, int(confianza * 5))
                    
                    return f"🧠 {respuesta_neural}"
            except Exception as e:
                print(f"Error en red neuronal: {e}")
        
        # 🧠 SISTEMA DE MEMORIA: Verificar respuestas aprendidas
        respuesta_aprendida = self.memoria.obtener_respuesta_mejorada(comando)
        if respuesta_aprendida:
            respuesta_final = f"💾 {respuesta_aprendida['respuesta']}\n\n💡 {respuesta_aprendida['contexto']}"
            self.memoria.agregar_interaccion(comando_original, respuesta_final, respuesta_aprendida['confianza'])
            return respuesta_final
        
        # 📊 Obtener contexto de la conversación
        contexto = self.memoria.obtener_contexto_conversacion()
        
        # 🎯 Procesar comandos específicos
        if "estadisticas" in comando or "aprendizaje" in comando:
            stats = self.memoria.obtener_estadisticas()
            respuesta = f"""📊 **Estadísticas de Aprendizaje ARIA**
            
🔢 **Conversaciones totales:** {stats['total_conversaciones']}
👍 **Feedback positivo:** {stats['feedback_positivo']}
👎 **Feedback negativo:** {stats['feedback_negativo']}
📈 **Satisfacción:** {stats['ratio_satisfaccion']:.1%}
🧠 **Respuestas aprendidas:** {stats['respuestas_aprendidas']}

🔥 **Top preguntas:**
{chr(10).join([f"• {q}: {c} veces" for q, c in stats['top_preguntas'][:3]])}"""
        
        # Manejar saludos
        elif any(saludo in comando for saludo in ["hola", "buenos días", "buenas tardes", "buenas noches", "hey", "hi"]):
            saludos = [
                f"¡Hola! 👋 Soy ARIA, tu asistente virtual con aprendizaje. {contexto}",
                f"¡Hola! ¿Cómo estás? Soy ARIA y cada conversación me hace más inteligente 😊",
                f"¡Saludos! Soy ARIA, aprendo contigo en cada interacción. {contexto}",
                f"¡Hola! Me alegra verte de nuevo. He aprendido de {self.memoria.obtener_estadisticas()['total_conversaciones']} conversaciones."
            ]
            import random
            respuesta = random.choice(saludos)
        
        elif "qué hora es" in comando or "hora" in comando:
            hora = datetime.datetime.now().strftime("%H:%M")
            respuesta = f"Son las {hora}"
            
        elif "qué día es" in comando or "fecha" in comando:
            fecha = datetime.datetime.now().strftime("%d de %B del %Y")
            respuesta = f"Hoy es {fecha}"
            
        elif "clima" in comando or "tiempo" in comando:
            respuesta = "El clima está perfecto para usar el asistente virtual"
            
        elif "cómo estás" in comando:
            respuesta = "¡Estoy funcionando perfectamente! Gracias por preguntar"
            
        elif "chiste" in comando:
            chistes = [
                "¿Por qué los programadores prefieren el modo oscuro? Porque la luz atrae a los bugs",
                "¿Cuál es el colmo de un informático? Que su mujer tenga un chip en el hombro",
                "¿Por qué los robots nunca entran en pánico? Porque tienen buenos algoritmos"
            ]
            import random
            respuesta = random.choice(chistes)
            
        elif "ayuda" in comando:
            respuesta = "Puedo ayudarte con la hora, fecha, chistes, transcribir audio y mucho más. ¿Qué necesitas?"
            
        elif "transcribir" in comando:
            respuesta = "Perfecto, usa la función de transcripción de audio para subir tus archivos"
            
        # 🌐 BÚSQUEDA WEB INTELIGENTE: Para preguntas que requieren información actualizada
        elif any(palabra in comando for palabra in ["buscar", "qué es", "quién es", "dónde está", "cuándo", "cómo", "noticias", "actual", "último"]):
            print("🌐 Activando búsqueda web inteligente")
            try:
                respuesta_web = buscador_web_aria.responder_con_web(comando)
                respuesta = f"🌐 **Información actualizada:**\n\n{respuesta_web}\n\n💡 *Esta información ha sido obtenida de fuentes web confiables y agregada a mi conocimiento.*"
            except Exception as e:
                print(f"Error en búsqueda web: {e}")
                respuesta = "🌐 Intenté buscar información actualizada, pero no pude acceder a recursos web en este momento. ¿Puedes reformular tu pregunta?"
            
        else:
            # Respuestas inteligentes basadas en aprendizaje previo
            respuestas_genericas = [
                f"Interesante tema. {contexto} ¿puedes contarme más?",
                f"Entiendo, ¿hay algo específico en lo que pueda ayudarte? 🤔",
                f"Hmm, eso suena intrigante. Estoy aprendiendo sobre este tipo de consultas.",
                f"¿Podrías ser más específico? Me ayuda a mejorar mis respuestas 🧠",
                f"🌐 ¿Te gustaría que busque información actualizada sobre este tema en web?"
            ]
            import random
            respuesta = random.choice(respuestas_genericas)
        
        # 📝 IMPORTANTE: Registrar la interacción en memoria para aprendizaje
        self.memoria.agregar_interaccion(comando_original, respuesta)
        
        return respuesta

# Instancia global del asistente
asistente = AsistenteWeb()

@app.route('/')
def index():
    return render_template('asistente.html')

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        mensaje = data.get('mensaje', '')
        
        if not mensaje:
            return jsonify({'error': 'No se proporcionó mensaje'}), 400
        
        # Procesar comando
        respuesta = asistente.procesar_comando(mensaje)
        
        # Hablar la respuesta
        asistente.hablar(respuesta)
        
        return jsonify({
            'success': True,
            'respuesta': respuesta,
            'timestamp': datetime.datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({'error': f'Error procesando comando: {str(e)}'}), 500

@app.route('/transcribir_audio', methods=['POST'])
def transcribir_audio_asistente():
    try:
        if 'audio' not in request.files:
            return jsonify({'error': 'No se encontró archivo de audio'}), 400
        
        file = request.files['audio']
        if file.filename == '':
            return jsonify({'error': 'No se seleccionó archivo'}), 400
        
        # Guardar archivo temporal
        temp_path = f"temp_{datetime.datetime.now().timestamp()}.wav"
        file.save(temp_path)
        
        # Transcribir con Whisper
        resultado = asistente.whisper_model.transcribe(temp_path)
        texto = resultado["text"]
        
        # Procesar como comando
        respuesta = asistente.procesar_comando(texto)
        asistente.hablar(respuesta)
        
        # Limpiar archivo temporal
        os.remove(temp_path)
        
        return jsonify({
            'success': True,
            'transcripcion': texto,
            'respuesta': respuesta
        })
        
    except Exception as e:
        return jsonify({'error': f'Error transcribiendo audio: {str(e)}'}), 500

@app.route('/feedback', methods=['POST'])
def agregar_feedback():
    """Endpoint para que el usuario califique respuestas"""
    try:
        data = request.get_json()
        pregunta = data.get('pregunta')
        respuesta = data.get('respuesta')
        calificacion = data.get('calificacion')  # 1-5
        comentario = data.get('comentario', '')
        
        if not pregunta or not respuesta or calificacion is None:
            return jsonify({'error': 'Datos incompletos'}), 400
        
        # Agregar feedback al sistema de memoria
        es_positivo = calificacion >= 4
        asistente.memoria.agregar_feedback(pregunta, respuesta, es_positivo, comentario)
        
        # Actualizar la interacción con la calificación
        asistente.memoria.agregar_interaccion(pregunta, respuesta, calificacion)
        
        return jsonify({
            'success': True,
            'mensaje': '¡Gracias por tu feedback! Me ayuda a mejorar 🧠✨'
        })
        
    except Exception as e:
        return jsonify({'error': f'Error guardando feedback: {str(e)}'}), 500

@app.route('/estadisticas', methods=['GET'])
def obtener_estadisticas():
    """Endpoint para obtener estadísticas de aprendizaje"""
    try:
        stats = asistente.memoria.obtener_estadisticas()
        return jsonify({
            'success': True,
            'estadisticas': stats
        })
    except Exception as e:
        return jsonify({'error': f'Error obteniendo estadísticas: {str(e)}'}), 500

@app.route('/nueva_sesion', methods=['POST'])
def nueva_sesion():
    """Inicia una nueva sesión de conversación"""
    try:
        asistente.memoria.nueva_sesion()
        return jsonify({
            'success': True,
            'mensaje': 'Nueva sesión iniciada. ¡Listo para aprender más! 🚀'
        })
    except Exception as e:
        return jsonify({'error': f'Error iniciando sesión: {str(e)}'}), 500

@app.route('/entrenar_red_neuronal', methods=['POST'])
def entrenar_red_neuronal():
    """Entrena la red neuronal con los datos actuales"""
    try:
        if asistente.red_neuronal:
            exito = asistente.red_neuronal.entrenar_red_neuronal()
            
            if exito:
                try:
                    metricas = asistente.red_neuronal.obtener_metricas_entrenamiento()
                    # Convertir numpy.float32 a float nativo de Python para JSON
                    if metricas:
                        metricas_json = {
                            'epochs': int(metricas.get('epochs', 0)),
                            'loss_final': float(metricas.get('loss_final', 0)),
                            'accuracy_final': float(metricas.get('accuracy_final', 0)),
                            'val_loss_final': float(metricas.get('val_loss_final', 0)) if metricas.get('val_loss_final') else None,
                            'val_accuracy_final': float(metricas.get('val_accuracy_final', 0)) if metricas.get('val_accuracy_final') else None,
                            'mejor_epoch': int(metricas.get('mejor_epoch', 0))
                        }
                    else:
                        metricas_json = {'mensaje': 'Entrenamiento completado sin métricas detalladas'}
                except Exception as e:
                    print(f"Error procesando métricas: {e}")
                    metricas_json = {'mensaje': 'Entrenamiento completado'}
                
                return jsonify({
                    'success': True,
                    'mensaje': '🧠 Red neuronal entrenada exitosamente!',
                    'metricas': metricas_json
                })
            else:
                return jsonify({
                    'success': False,
                    'mensaje': 'No hay suficientes datos para entrenar'
                })
        else:
            return jsonify({
                'success': False,
                'mensaje': 'Red neuronal no disponible'
            })
    except Exception as e:
        print(f"Error en entrenamiento: {e}")
        return jsonify({'error': f'Error entrenando red neuronal: {str(e)}'}), 500

@app.route('/analisis_neuronal', methods=['POST'])
def analisis_neuronal():
    """Analiza texto con la red neuronal"""
    try:
        data = request.get_json()
        texto = data.get('texto', '')
        
        if not texto:
            return jsonify({'error': 'Texto requerido'}), 400
        
        if asistente.red_neuronal and asistente.red_neuronal.is_trained:
            prediccion = asistente.red_neuronal.predecir_categoria(texto)
            categoria = prediccion['categoria']
            confianza = prediccion['confianza']
            respuesta_sugerida = asistente.red_neuronal.generar_respuesta_inteligente(texto, categoria, confianza)
            
            return jsonify({
                'success': True,
                'categoria': categoria,
                'confianza': f"{confianza:.1%}",
                'respuesta_sugerida': respuesta_sugerida
            })
        else:
            return jsonify({
                'success': False,
                'mensaje': 'Red neuronal no entrenada'
            })
            
    except Exception as e:
        return jsonify({'error': f'Error en análisis neuronal: {str(e)}'}), 500

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

@app.route('/buscar_web', methods=['POST'])
def buscar_web():
    """Endpoint para búsqueda web explícita"""
    try:
        data = request.get_json()
        consulta = data.get('consulta', '').strip()
        profundidad = data.get('profundidad', 3)
        
        if not consulta:
            return jsonify({'error': 'Consulta requerida'}), 400
        
        print(f"🌐 Búsqueda web solicitada: {consulta}")
        resultado = buscador_web_aria.buscar_y_aprender(consulta, profundidad)
        
        return jsonify({
            'success': resultado['exito'],
            'consulta': consulta,
            'resultados': resultado.get('resultados_encontrados', 0),
            'contenido_procesado': resultado.get('contenido_procesado', 0),
            'resumen': resultado.get('resumen', ''),
            'conocimiento': resultado.get('conocimiento', []),
            'timestamp': datetime.datetime.now().isoformat()
        })
        
    except Exception as e:
        print(f"Error en búsqueda web: {e}")
        return jsonify({'error': f'Error en búsqueda web: {str(e)}'}), 500

@app.route('/conocimiento_web', methods=['GET'])
def obtener_conocimiento_web():
    """Obtiene estadísticas del conocimiento web adquirido"""
    try:
        stats = buscador_web_aria.obtener_estadisticas()
        conocimiento_reciente = buscador_web_aria.obtener_conocimiento_reciente(5)
        
        return jsonify({
            'success': True,
            'estadisticas': stats,
            'conocimiento_reciente': conocimiento_reciente,
            'timestamp': datetime.datetime.now().isoformat()
        })
        
    except Exception as e:
        print(f"Error obteniendo conocimiento web: {e}")
        return jsonify({'error': f'Error obteniendo conocimiento web: {str(e)}'}), 500

@app.route('/test', methods=['GET'])
def test_connection():
    """Endpoint para verificar conectividad"""
    return jsonify({
        'status': 'connected',
        'message': 'Servidor ARIA funcionando correctamente',
        'timestamp': datetime.datetime.now().isoformat(),
        'version': '1.0.0'
    })

@app.route('/red_neuronal_info', methods=['GET'])
def get_neural_network_info():
    """Obtener información de la red neuronal"""
    try:
        if asistente.red_neuronal and hasattr(asistente.red_neuronal, 'modelo') and asistente.red_neuronal.modelo:
            parametros = asistente.red_neuronal.modelo.count_params()
            estado = 'activa'
            
            # Intentar obtener métricas reales
            try:
                metricas = asistente.red_neuronal.obtener_metricas_entrenamiento()
                precision = float(metricas.get('accuracy_final', 0.33)) if metricas else 0.33
            except:
                precision = 0.33  # Valor por defecto
        else:
            parametros = 4456  # Valor por defecto
            estado = 'no_disponible'
            precision = 0.0
            
        return jsonify({
            'parametros': int(parametros),
            'precision': precision,
            'ultima_actualizacion': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'estado': estado
        })
    except Exception as e:
        print(f"Error en red_neuronal_info: {e}")
        return jsonify({
            'parametros': 4456,
            'precision': 0.0,
            'ultima_actualizacion': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'estado': 'error',
            'error': str(e)
        })

if __name__ == '__main__':
    print("🤖 Iniciando Asistente Virtual Web...")
    print("🌐 Accede a: http://localhost:5001")
    
    try:
        app.run(debug=False, port=5001, host='127.0.0.1')
    except KeyboardInterrupt:
        print("\n🛑 Servidor detenido por el usuario")
    except Exception as e:
        print(f"❌ Error en el servidor: {e}")
        print("🔄 Reintentando en modo debug...")
        app.run(debug=True, port=5001, host='127.0.0.1')