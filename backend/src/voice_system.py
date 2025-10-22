"""
ARIA - Sistema de Síntesis de Voz
Sistema completo de Text-to-Speech para Windows
"""

import win32com.client
import os
import tempfile
import threading
import time
from datetime import datetime

class ARIAVoiceSystem:
    def __init__(self):
        self.sapi_available = False
        self.current_voice = None
        self.voice_rate = 0  # -10 to 10
        self.voice_volume = 100  # 0 to 100
        self.available_voices = []
        
        # Intentar inicializar SAPI
        self.init_sapi()
    
    def init_sapi(self):
        """Inicializa el sistema SAPI de Windows"""
        try:
            # Inicializar COM
            import pythoncom
            pythoncom.CoInitialize()
            
            self.tts_engine = win32com.client.Dispatch("SAPI.SpVoice")
            self.sapi_available = True
            self.load_available_voices()
            self.select_best_spanish_voice()
            
            # Configurar velocidad y volumen iniciales
            self.set_rate(0)  # Velocidad normal
            self.set_volume(80)  # Volumen al 80%
            
            print("✅ Sistema de voz ARIA inicializado correctamente")
        except Exception as e:
            print(f"⚠️ Error inicializando SAPI: {e}")
            self.sapi_available = False
    
    def load_available_voices(self):
        """Carga las voces disponibles en el sistema"""
        if not self.sapi_available:
            return
        
        try:
            voices = self.tts_engine.GetVoices()
            self.available_voices = []
            
            for i in range(voices.Count):
                voice = voices.Item(i)
                voice_info = {
                    "id": i,
                    "name": voice.GetDescription(),
                    "language": voice.GetAttribute("Language"),
                    "gender": voice.GetAttribute("Gender") or "Unknown",
                    "age": voice.GetAttribute("Age") or "Adult"
                }
                self.available_voices.append(voice_info)
                print(f"🔊 Voz disponible: {voice_info['name']} ({voice_info['language']})")
        
        except Exception as e:
            print(f"Error cargando voces: {e}")
    
    def select_best_spanish_voice(self):
        """Selecciona la mejor voz en español disponible"""
        if not self.available_voices:
            return
        
        # Buscar voces en español
        spanish_voices = [v for v in self.available_voices if 'spanish' in v['name'].lower() or 'es-' in v.get('language', '').lower()]
        
        if spanish_voices:
            # Preferir voces femeninas para ARIA
            female_spanish = [v for v in spanish_voices if 'female' in v.get('gender', '').lower() or 'helena' in v['name'].lower() or 'sabina' in v['name'].lower()]
            
            if female_spanish:
                self.current_voice = female_spanish[0]
            else:
                self.current_voice = spanish_voices[0]
        else:
            # Si no hay voces en español, usar la primera disponible
            self.current_voice = self.available_voices[0] if self.available_voices else None
        
        if self.current_voice:
            self.set_voice(self.current_voice['id'])
            print(f"🎤 Voz seleccionada para ARIA: {self.current_voice['name']}")
    
    def set_voice(self, voice_id):
        """Establece una voz específica"""
        if not self.sapi_available:
            return False
        
        try:
            voices = self.tts_engine.GetVoices()
            if 0 <= voice_id < voices.Count:
                self.tts_engine.Voice = voices.Item(voice_id)
                return True
        except Exception as e:
            print(f"Error estableciendo voz: {e}")
        
        return False
    
    def set_rate(self, rate):
        """Establece la velocidad de habla (-10 a 10)"""
        if not self.sapi_available:
            return
        
        try:
            self.voice_rate = max(-10, min(10, rate))
            self.tts_engine.Rate = self.voice_rate
        except Exception as e:
            print(f"Error estableciendo velocidad: {e}")
    
    def set_volume(self, volume):
        """Establece el volumen (0 a 100)"""
        if not self.sapi_available:
            return
        
        try:
            self.voice_volume = max(0, min(100, volume))
            self.tts_engine.Volume = self.voice_volume
        except Exception as e:
            print(f"Error estableciendo volumen: {e}")
    
    def speak_text(self, text, async_mode=True):
        """Convierte texto a voz"""
        if not text or not text.strip():
            return False
        
        # Intentar con SAPI primero
        if self.sapi_available:
            try:
                return self._speak_with_sapi(text, async_mode)
            except Exception as e:
                print(f"Error en SAPI, probando PowerShell: {e}")
        
        # Usar PowerShell como respaldo
        return self.speak_with_powershell(text)
    
    def _speak_with_sapi(self, text, async_mode=True):
        """Método interno para hablar con SAPI"""
        try:
            # Limpiar el texto para mejorar la pronunciación
            cleaned_text = self.clean_text_for_speech(text)
            
            if async_mode:
                # Hablar de forma asíncrona
                def speak_async():
                    try:
                        import pythoncom
                        pythoncom.CoInitialize()
                        
                        # Crear nueva instancia para el hilo
                        tts = win32com.client.Dispatch("SAPI.SpVoice")
                        
                        # Configurar la misma voz
                        if self.current_voice:
                            voices = tts.GetVoices()
                            if self.current_voice['id'] < voices.Count:
                                tts.Voice = voices.Item(self.current_voice['id'])
                        
                        # Configurar velocidad y volumen
                        tts.Rate = self.voice_rate
                        tts.Volume = self.voice_volume
                        
                        # Hablar
                        tts.Speak(cleaned_text, 0)  # 0 = SVSFDefault (síncrono en el hilo)
                        
                        pythoncom.CoUninitialize()
                        
                    except Exception as e:
                        print(f"Error en síntesis de voz asíncrona: {e}")
                
                thread = threading.Thread(target=speak_async)
                thread.daemon = True
                thread.start()
            else:
                # Hablar de forma síncrona
                import pythoncom
                pythoncom.CoInitialize()
                self.tts_engine.Speak(cleaned_text, 0)  # 0 = SVSFDefault
                pythoncom.CoUninitialize()
            
            return True
            
        except Exception as e:
            print(f"Error en síntesis de voz SAPI: {e}")
            raise e
    
    def clean_text_for_speech(self, text):
        """Limpia el texto para mejorar la síntesis de voz"""
        # Remover caracteres especiales que pueden causar problemas
        text = text.replace("🤖", "")
        text = text.replace("✅", "")
        text = text.replace("❌", "")
        text = text.replace("🧠", "")
        text = text.replace("📊", "")
        text = text.replace("🎯", "")
        text = text.replace("⏱️", "")
        text = text.replace("💬", "")
        text = text.replace("🧩", "")
        text = text.replace("🏋️", "")
        text = text.replace("📅", "")
        text = text.replace("🏗️", "")
        
        # Reemplazar abreviaciones comunes
        text = text.replace("IA", "inteligencia artificial")
        text = text.replace("API", "a p i")
        text = text.replace("ARIA", "aria")
        
        return text.strip()
    
    def stop_speaking(self):
        """Detiene la síntesis de voz actual"""
        if not self.sapi_available:
            return
        
        try:
            self.tts_engine.Speak("", 2)  # 2 = SVSFPurgeBeforeSpeak
        except Exception as e:
            print(f"Error deteniendo voz: {e}")
    
    def get_voice_info(self):
        """Obtiene información del sistema de voz"""
        return {
            "available": self.sapi_available,
            "current_voice": self.current_voice['name'] if self.current_voice else None,
            "rate": self.voice_rate,
            "volume": self.voice_volume,
            "total_voices": len(self.available_voices),
            "available_voices": [v['name'] for v in self.available_voices]
        }
    
    def test_voice(self, test_text="¡Hola! Soy ARIA, tu asistente virtual inteligente."):
        """Prueba el sistema de voz"""
        print(f"🔊 Probando síntesis de voz...")
        
        # Método alternativo usando PowerShell si SAPI falla
        if not self.sapi_available:
            return self.speak_with_powershell(test_text)
        
        return self.speak_text(test_text)
    
    def speak_with_powershell(self, text):
        """Método alternativo usando PowerShell para síntesis de voz"""
        try:
            import subprocess
            import tempfile
            import os
            
            # Limpiar texto
            cleaned_text = self.clean_text_for_speech(text)
            
            # Crear archivo temporal PowerShell
            ps_script = f'''
Add-Type -AssemblyName System.Speech
$voice = New-Object System.Speech.Synthesis.SpeechSynthesizer
$voice.Rate = {self.voice_rate}
$voice.Volume = {self.voice_volume}
$voice.Speak("{cleaned_text}")
'''
            
            # Crear archivo temporal
            with tempfile.NamedTemporaryFile(mode='w', suffix='.ps1', delete=False, encoding='utf-8') as f:
                f.write(ps_script)
                ps_file = f.name
            
            try:
                # Ejecutar PowerShell
                result = subprocess.run([
                    "powershell", 
                    "-ExecutionPolicy", "Bypass",
                    "-File", 
                    ps_file
                ], 
                capture_output=True, 
                text=True,
                timeout=30
                )
                
                if result.returncode == 0:
                    print("✅ Síntesis de voz ejecutada con PowerShell")
                    return True
                else:
                    print(f"Error en PowerShell: {result.stderr}")
                    return False
                    
            finally:
                # Limpiar archivo temporal
                try:
                    os.unlink(ps_file)
                except:
                    pass
            
        except Exception as e:
            print(f"Error en síntesis con PowerShell: {e}")
            return False

# Instancia global del sistema de voz
try:
    voice_system = ARIAVoiceSystem()
except Exception as e:
    print(f"Error inicializando sistema de voz: {e}")
    voice_system = None