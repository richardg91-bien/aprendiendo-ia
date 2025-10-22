import os
import whisper
from pathlib import Path

def transcribir_audio_local(archivo_audio):
    """
    Transcribe audio usando Whisper local (gratuito)
    No requiere API key ni conexión a internet
    """
    
    # Verificar que el archivo existe
    if not os.path.exists(archivo_audio):
        print(f"❌ Error: No se encontró el archivo '{archivo_audio}'")
        print("📁 Archivos disponibles en el directorio:")
        for file in os.listdir("."):
            if file.endswith((".mp3", ".wav", ".m4a", ".webm", ".mp4")):
                print(f"   - {file}")
        return None
    
    try:
        print("🔄 Cargando modelo Whisper (primera vez puede tardar)...")
        # Cargar modelo (base es un buen balance entre velocidad y precisión)
        model = whisper.load_model("base")
        
        print("🎵 Transcribiendo archivo de audio...")
        # Transcribir el audio
        resultado = model.transcribe(archivo_audio)
        
        print("✅ Transcripción completada:")
        print("📝 Resultado:", resultado["text"])
        
        # Guardar transcripción en archivo
        nombre_salida = f"transcripcion_{Path(archivo_audio).stem}.txt"
        with open(nombre_salida, "w", encoding="utf-8") as f:
            f.write(resultado["text"])
        print(f"💾 Transcripción guardada en: {nombre_salida}")
        
        return resultado["text"]
        
    except Exception as e:
        print(f"❌ Error durante la transcripción: {e}")
        print("💡 Asegúrate de que:")
        print("   1. Tienes instalado: pip install openai-whisper")
        print("   2. El archivo de audio sea válido")
        print("   3. Tienes espacio suficiente en disco")
        return None

if __name__ == "__main__":
    # Archivo a transcribir
    archivo_audio = "prueba.mp3"
    
    # Transcribir
    transcripcion = transcribir_audio_local(archivo_audio)