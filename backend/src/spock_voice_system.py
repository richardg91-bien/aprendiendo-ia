"""
Sistema de Síntesis de Voz ARIA - Personalidad Spock
Implementa Text-to-Speech con estilo lógico y tranquilo
"""

import threading
import time
import re
import random
from pathlib import Path

try:
    import pyttsx3
    PYTTSX3_AVAILABLE = True
except ImportError:
    PYTTSX3_AVAILABLE = False
    print("⚠️ pyttsx3 no disponible. Sistema de voz deshabilitado.")

class SpockVoiceSystem:
    def __init__(self):
        """Inicializa el sistema de voz con personalidad Spock"""
        self.engine = None
        self.voice_enabled = True
        self.voice_speed = 150  # Velocidad lenta y medida
        self.voice_volume = 0.8
        self.current_voice = None
        self.spock_phrases = {
            'greetings': [
                "Saludo, humano.",
                "Fascinante. ¿En qué puedo asistirle?",
                "La lógica dicta que debo responder a su consulta."
            ],
            'thinking': [
                "Procesando datos...",
                "Analizando información disponible...",
                "Consultando base de conocimientos..."
            ],
            'conclusions': [
                "La respuesta lógica es:",
                "Basándome en los datos disponibles:",
                "Mi análisis indica que:"
            ],
            'farewell': [
                "Vida larga y próspera.",
                "Que la lógica les acompañe.",
                "Fin de la transmisión."
            ]
        }
        self.initialize_voice_engine()
        
    def initialize_voice_engine(self):
        """Inicializa el motor de síntesis de voz"""
        if not PYTTSX3_AVAILABLE:
            print("⚠️ pyttsx3 no disponible. Sistema de voz deshabilitado.")
            self.voice_enabled = False
            return
            
        try:
            self.engine = pyttsx3.init()
            
            # Configurar velocidad (Spock habla pausadamente)
            self.engine.setProperty('rate', self.voice_speed)
            
            # Configurar volumen
            self.engine.setProperty('volume', self.voice_volume)
            
            # Buscar voz masculina profunda
            voices = self.engine.getProperty('voices')
            selected_voice = None
            
            # Preferir voces masculinas en inglés o español
            for voice in voices:
                voice_info = voice.name.lower()
                if any(keyword in voice_info for keyword in ['male', 'man', 'masculine', 'david', 'mark']):
                    selected_voice = voice.id
                    break
            
            if selected_voice:
                self.engine.setProperty('voice', selected_voice)
                self.current_voice = selected_voice
                
            print(f"🎙️ Sistema de voz Spock inicializado")
            print(f"   Velocidad: {self.voice_speed} WPM")
            print(f"   Voz: {selected_voice if selected_voice else 'Default'}")
            
        except Exception as e:
            print(f"⚠️ Error inicializando síntesis de voz: {e}")
            self.voice_enabled = False
    
    def spock_transform_text(self, text):
        """Transforma el texto para que suene más como Spock"""
        # Frases de reemplazo para sonar más lógico y formal
        transformations = {
            r'\bno sé\b': 'no poseo esa información',
            r'\bno estoy seguro\b': 'los datos son insuficientes',
            r'\bcreo que\b': 'mi análisis sugiere que',
            r'\bpienso que\b': 'la lógica indica que',
            r'\btal vez\b': 'existe una probabilidad de que',
            r'\bprobablemente\b': 'es altamente probable que',
            r'\bhola\b': 'saludo',
            r'\badiós\b': 'vida larga y próspera',
            r'\binteresante\b': 'fascinante',
            r'\bimpresionante\b': 'lógicamente satisfactorio',
            r'\bgenial\b': 'eficiente',
            r'\bestupendo\b': 'altamente satisfactorio'
        }
        
        spock_text = text
        for pattern, replacement in transformations.items():
            spock_text = re.sub(pattern, replacement, spock_text, flags=re.IGNORECASE)
        
        # Agregar pausas lógicas
        spock_text = spock_text.replace('.', '. ')
        spock_text = spock_text.replace(',', ', ')
        
        return spock_text
    
    def add_spock_introduction(self, text):
        """Agrega introducción estilo Spock ocasionalmente"""
        
        if random.random() < 0.3:  # 30% de probabilidad
            intro = random.choice(self.spock_phrases['conclusions'])
            return f"{intro} {text}"
        
        return text
    
    def speak_async(self, text):
        """Habla texto de forma asíncrona"""
        if not self.voice_enabled or not self.engine:
            return
            
        def speak_thread():
            try:
                # Transformar texto al estilo Spock
                spock_text = self.spock_transform_text(text)
                spock_text = self.add_spock_introduction(spock_text)
                
                print(f"🗣️ Spock: {spock_text}")
                
                # Sintetizar voz
                self.engine.say(spock_text)
                self.engine.runAndWait()
                
            except Exception as e:
                print(f"⚠️ Error en síntesis de voz: {e}")
        
        # Ejecutar en hilo separado para no bloquear
        thread = threading.Thread(target=speak_thread, daemon=True)
        thread.start()
    
    def speak_greeting(self):
        """Pronuncia un saludo estilo Spock"""
        greeting = random.choice(self.spock_phrases['greetings'])
        self.speak_async(greeting)
    
    def speak_thinking(self):
        """Indica que está procesando"""
        thinking = random.choice(self.spock_phrases['thinking'])
        self.speak_async(thinking)
    
    def speak_farewell(self):
        """Pronuncia una despedida estilo Spock"""
        farewell = random.choice(self.spock_phrases['farewell'])
        self.speak_async(farewell)
    
    def set_voice_enabled(self, enabled):
        """Habilita o deshabilita la síntesis de voz"""
        self.voice_enabled = enabled
        print(f"🎙️ Síntesis de voz: {'Habilitada' if enabled else 'Deshabilitada'}")
    
    def adjust_speed(self, speed):
        """Ajusta la velocidad de la voz (50-300 WPM)"""
        if self.engine and 50 <= speed <= 300:
            self.voice_speed = speed
            self.engine.setProperty('rate', speed)
            print(f"🎙️ Velocidad de voz ajustada a: {speed} WPM")
    
    def test_voice(self):
        """Prueba el sistema de voz"""
        test_text = "Fascinante. El sistema de síntesis de voz está funcionando de manera lógica y eficiente."
        self.speak_async(test_text)

# Instancia global del sistema de voz
spock_voice = SpockVoiceSystem()

def speak_response(text):
    """Función helper para que ARIA hable con voz de Spock"""
    spock_voice.speak_async(text)

def speak_greeting():
    """Función helper para saludo"""
    spock_voice.speak_greeting()

def speak_thinking():
    """Función helper para indicar procesamiento"""
    spock_voice.speak_thinking()

def toggle_voice(enabled=None):
    """Activa/desactiva la síntesis de voz"""
    if enabled is None:
        enabled = not spock_voice.voice_enabled
    spock_voice.set_voice_enabled(enabled)
    return enabled

if __name__ == "__main__":
    print("🎙️ Probando sistema de voz Spock...")
    spock_voice.test_voice()
    time.sleep(3)
    spock_voice.speak_greeting()
    time.sleep(2)
    spock_voice.speak_farewell()