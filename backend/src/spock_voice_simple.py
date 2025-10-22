"""
Sistema de Síntesis de Voz ARIA - Personalidad Spock (Windows SAPI)
Versión simplificada usando SAPI de Windows
"""

import threading
import time
import re
import random
import subprocess
import tempfile
import os

class SpockVoiceSystemSimple:
    def __init__(self):
        """Inicializa el sistema de voz con personalidad Spock"""
        self.voice_enabled = True
        self.voice_speed = 2  # Velocidad lenta (0-10)
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
        self.test_voice_availability()
        
    def test_voice_availability(self):
        """Prueba si el sistema de voz está disponible"""
        try:
            # Crear un archivo VBS temporal para probar
            with tempfile.NamedTemporaryFile(mode='w', suffix='.vbs', delete=False) as f:
                f.write('CreateObject("SAPI.SpVoice").Speak "Test"')
                test_file = f.name
            
            # Intentar ejecutar el comando
            result = subprocess.run(['cscript', '//nologo', test_file], 
                                  capture_output=True, timeout=5)
            os.unlink(test_file)
            
            if result.returncode == 0:
                print("🎙️ Sistema de voz Windows SAPI disponible")
                self.voice_enabled = True
            else:
                print("⚠️ Sistema de voz no disponible")
                self.voice_enabled = False
                
        except Exception as e:
            print(f"⚠️ Error probando voz: {e}")
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
        
        return spock_text
    
    def add_spock_introduction(self, text):
        """Agrega introducción estilo Spock ocasionalmente"""
        if random.random() < 0.3:  # 30% de probabilidad
            intro = random.choice(self.spock_phrases['conclusions'])
            return f"{intro} {text}"
        return text
    
    def speak_with_sapi(self, text):
        """Usa Windows SAPI para síntesis de voz"""
        try:
            # Escapar comillas en el texto
            clean_text = text.replace('"', "'").replace('\n', ' ')
            
            # Crear script VBS para SAPI
            vbs_script = f'''
            Set voice = CreateObject("SAPI.SpVoice")
            voice.Rate = {self.voice_speed}
            voice.Speak "{clean_text}"
            '''
            
            # Crear archivo temporal
            with tempfile.NamedTemporaryFile(mode='w', suffix='.vbs', delete=False) as f:
                f.write(vbs_script)
                temp_file = f.name
            
            # Ejecutar script
            subprocess.run(['cscript', '//nologo', temp_file], 
                         capture_output=True, timeout=30)
            
            # Limpiar archivo temporal
            os.unlink(temp_file)
            
        except Exception as e:
            print(f"⚠️ Error en síntesis SAPI: {e}")
    
    def speak_async(self, text):
        """Habla texto de forma asíncrona"""
        if not self.voice_enabled:
            return
            
        def speak_thread():
            try:
                # Transformar texto al estilo Spock
                spock_text = self.spock_transform_text(text)
                spock_text = self.add_spock_introduction(spock_text)
                
                print(f"🗣️ Spock: {spock_text}")
                
                # Síntesis de voz
                self.speak_with_sapi(spock_text)
                
            except Exception as e:
                print(f"⚠️ Error en síntesis de voz: {e}")
        
        # Ejecutar en hilo separado
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
    
    def test_voice(self):
        """Prueba el sistema de voz"""
        test_text = "Fascinante. El sistema de síntesis de voz está funcionando de manera lógica y eficiente."
        self.speak_async(test_text)

# Instancia global del sistema de voz
try:
    from spock_voice_system import SpockVoiceSystem
    spock_voice = SpockVoiceSystem()
    if not spock_voice.voice_enabled:
        # Fallback al sistema simple
        spock_voice = SpockVoiceSystemSimple()
except:
    spock_voice = SpockVoiceSystemSimple()

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
    print("🎙️ Probando sistema de voz Spock simple...")
    spock_voice_simple = SpockVoiceSystemSimple()
    spock_voice_simple.test_voice()
    time.sleep(3)
    spock_voice_simple.speak_greeting()
    time.sleep(2)
    spock_voice_simple.speak_farewell()