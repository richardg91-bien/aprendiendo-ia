import pyttsx3
import speech_recognition as sr
import whisper
import threading
import queue
import time
import os
import datetime
import json
from pathlib import Path

class AsistenteVirtual:
    def __init__(self):
        print("🤖 Inicializando Asistente Virtual...")
        
        # Inicializar Text-to-Speech
        self.engine = pyttsx3.init()
        self.configurar_voz()
        
        # Inicializar Speech Recognition
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        
        # Cargar modelo Whisper como respaldo
        print("🔄 Cargando Whisper para transcripción avanzada...")
        self.whisper_model = whisper.load_model("tiny")
        
        # Estado del asistente
        self.activo = False
        self.escuchando = False
        self.nombre = "ARIA"  # Asistente de Reconocimiento e Inteligencia Artificial
        
        # Cola de comandos
        self.cola_comandos = queue.Queue()
        
        # Configuración
        self.config = self.cargar_configuracion()
        
        print(f"✅ {self.nombre} listo para usar!")
        
    def configurar_voz(self):
        """Configura la voz del asistente"""
        voices = self.engine.getProperty('voices')
        
        # Buscar voz en español o femenina
        for voice in voices:
            if 'spanish' in voice.name.lower() or 'helena' in voice.name.lower():
                self.engine.setProperty('voice', voice.id)
                break
        
        # Configurar velocidad y volumen
        self.engine.setProperty('rate', 180)  # Velocidad de habla
        self.engine.setProperty('volume', 0.8)  # Volumen
        
    def cargar_configuracion(self):
        """Carga configuración del asistente"""
        config_file = "asistente_config.json"
        config_default = {
            "usuario": "Usuario",
            "idioma": "es",
            "comandos_personalizados": {},
            "recordatorios": [],
            "historial": []
        }
        
        if os.path.exists(config_file):
            with open(config_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            self.guardar_configuracion(config_default)
            return config_default
    
    def guardar_configuracion(self, config=None):
        """Guarda la configuración"""
        if config is None:
            config = self.config
        
        with open("asistente_config.json", 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
    
    def hablar(self, texto):
        """Convierte texto a voz"""
        print(f"🤖 {self.nombre}: {texto}")
        self.engine.say(texto)
        self.engine.runAndWait()
    
    def escuchar_microfono(self):
        """Escucha desde el micrófono"""
        with self.microphone as source:
            print("🎤 Calibrando micrófono...")
            self.recognizer.adjust_for_ambient_noise(source)
        
        print("👂 Escuchando... (di 'ARIA' para activar)")
        
        while self.escuchando:
            try:
                with self.microphone as source:
                    # Escuchar con timeout
                    audio = self.recognizer.listen(source, timeout=1, phrase_time_limit=5)
                
                # Reconocer usando Google Speech Recognition
                try:
                    texto = self.recognizer.recognize_google(audio, language="es-ES")
                    self.cola_comandos.put(("microfono", texto))
                except sr.UnknownValueError:
                    pass  # No se entendió el audio
                except sr.RequestError:
                    # Si Google no está disponible, usar Whisper
                    self.procesar_audio_whisper(audio)
                    
            except sr.WaitTimeoutError:
                pass  # Timeout normal, continuar escuchando
            except Exception as e:
                print(f"❌ Error en micrófono: {e}")
    
    def procesar_audio_whisper(self, audio_data):
        """Procesa audio usando Whisper como respaldo"""
        try:
            # Guardar audio temporal
            with open("temp_audio.wav", "wb") as f:
                f.write(audio_data.get_wav_data())
            
            # Transcribir con Whisper
            result = self.whisper_model.transcribe("temp_audio.wav")
            texto = result["text"].strip()
            
            if texto:
                self.cola_comandos.put(("whisper", texto))
            
            # Limpiar archivo temporal
            os.remove("temp_audio.wav")
            
        except Exception as e:
            print(f"❌ Error en Whisper: {e}")
    
    def procesar_comando(self, texto):
        """Procesa los comandos de voz"""
        texto = texto.lower().strip()
        
        # Activación del asistente
        if not self.activo:
            if "aria" in texto or "hey aria" in texto:
                self.activo = True
                self.hablar("¡Hola! ¿En qué puedo ayudarte?")
                return
            else:
                return
        
        # Comandos del asistente
        if "adiós" in texto or "hasta luego" in texto:
            self.hablar("¡Hasta luego! Que tengas un buen día.")
            self.activo = False
            
        elif "qué hora es" in texto or "hora" in texto:
            hora = datetime.datetime.now().strftime("%H:%M")
            self.hablar(f"Son las {hora}")
            
        elif "qué día es" in texto or "fecha" in texto:
            fecha = datetime.datetime.now().strftime("%d de %B del %Y")
            self.hablar(f"Hoy es {fecha}")
            
        elif "transcribir" in texto or "transcribe" in texto:
            self.hablar("Por favor, sube un archivo de audio para transcribir")
            # Aquí puedes integrar con tu aplicación web
            
        elif "clima" in texto or "tiempo" in texto:
            self.hablar("Lo siento, aún no tengo acceso a información del clima en tiempo real")
            
        elif "recordatorio" in texto:
            self.hablar("¿Qué quieres que recuerde?")
            # Implementar sistema de recordatorios
            
        elif "reproduce música" in texto or "música" in texto:
            self.hablar("Lo siento, aún no puedo reproducir música")
            
        elif "buscar" in texto:
            self.hablar("¿Qué quieres que busque?")
            
        elif "ayuda" in texto or "qué puedes hacer" in texto:
            self.mostrar_ayuda()
            
        elif "mi nombre es" in texto:
            nombre = texto.replace("mi nombre es", "").strip()
            self.config["usuario"] = nombre.title()
            self.guardar_configuracion()
            self.hablar(f"Hola {nombre}, es un placer conocerte")
            
        else:
            respuestas = [
                "Interesante, cuéntame más",
                "No estoy segura de entender, ¿puedes ser más específico?",
                "Eso suena interesante",
                "¿Podrías reformular la pregunta?",
                "Hmm, déjame pensar en eso"
            ]
            import random
            self.hablar(random.choice(respuestas))
    
    def mostrar_ayuda(self):
        """Muestra los comandos disponibles"""
        comandos = [
            "Puedo ayudarte con:",
            "- Decir la hora actual",
            "- Decir la fecha de hoy", 
            "- Transcribir archivos de audio",
            "- Crear recordatorios",
            "- Y mucho más por venir"
        ]
        
        for comando in comandos:
            self.hablar(comando)
            time.sleep(0.5)
    
    def iniciar(self):
        """Inicia el asistente virtual"""
        self.hablar(f"¡Hola! Soy {self.nombre}, tu asistente virtual")
        self.hablar("Di 'ARIA' para activarme o 'ayuda' para ver qué puedo hacer")
        
        self.escuchando = True
        
        # Iniciar hilo de escucha
        hilo_microfono = threading.Thread(target=self.escuchar_microfono)
        hilo_microfono.daemon = True
        hilo_microfono.start()
        
        # Bucle principal de procesamiento
        try:
            while True:
                try:
                    # Procesar comandos de la cola
                    if not self.cola_comandos.empty():
                        fuente, comando = self.cola_comandos.get(timeout=1)
                        print(f"📝 Comando ({fuente}): {comando}")
                        self.procesar_comando(comando)
                        
                        # Guardar en historial
                        self.config["historial"].append({
                            "timestamp": datetime.datetime.now().isoformat(),
                            "fuente": fuente,
                            "comando": comando
                        })
                        
                        # Mantener solo los últimos 50 comandos
                        if len(self.config["historial"]) > 50:
                            self.config["historial"] = self.config["historial"][-50:]
                        
                        self.guardar_configuracion()
                    
                    time.sleep(0.1)
                    
                except queue.Empty:
                    pass
                    
        except KeyboardInterrupt:
            self.detener()
    
    def detener(self):
        """Detiene el asistente"""
        self.escuchando = False
        self.hablar("¡Hasta pronto!")
        print("🤖 Asistente detenido")

def main():
    print("🚀 ASISTENTE VIRTUAL ARIA")
    print("=" * 40)
    print("💡 Controles:")
    print("   - Di 'ARIA' para activar")
    print("   - Di 'ayuda' para ver comandos")
    print("   - Ctrl+C para salir")
    print("=" * 40)
    
    asistente = AsistenteVirtual()
    asistente.iniciar()

if __name__ == "__main__":
    main()