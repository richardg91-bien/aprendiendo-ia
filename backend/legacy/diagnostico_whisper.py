import os
import sys
import subprocess
from pathlib import Path

def verificar_ffmpeg():
    """Verifica si FFmpeg está disponible"""
    try:
        resultado = subprocess.run(['ffmpeg', '-version'], 
                                 capture_output=True, text=True, timeout=10)
        if resultado.returncode == 0:
            print("✅ FFmpeg detectado correctamente")
            return True
        else:
            print("❌ FFmpeg no responde correctamente")
            return False
    except FileNotFoundError:
        print("❌ FFmpeg no encontrado en PATH")
        return False
    except subprocess.TimeoutExpired:
        print("❌ FFmpeg timeout")
        return False
    except Exception as e:
        print(f"❌ Error con FFmpeg: {e}")
        return False

def probar_whisper_simple():
    """Prueba Whisper con un método más simple"""
    try:
        import whisper
        print("✅ Whisper importado correctamente")
        
        # Verificar archivo
        archivo = "prueba.mp3"
        if not os.path.exists(archivo):
            print(f"❌ Archivo '{archivo}' no encontrado")
            return False
            
        print(f"✅ Archivo '{archivo}' encontrado")
        
        # Verificar FFmpeg
        if not verificar_ffmpeg():
            print("💡 Instala FFmpeg:")
            print("   1. winget install ffmpeg")
            print("   2. Reinicia VS Code")
            return False
        
        # Cargar modelo pequeño para prueba rápida
        print("🔄 Cargando modelo Whisper 'tiny' (más rápido)...")
        model = whisper.load_model("tiny")
        
        print("🎵 Transcribiendo (versión rápida)...")
        resultado = model.transcribe(archivo, fp16=False)
        
        print("✅ ¡TRANSCRIPCIÓN EXITOSA!")
        print("📝 Resultado:", resultado["text"])
        
        # Guardar resultado
        with open("transcripcion_resultado.txt", "w", encoding="utf-8") as f:
            f.write(resultado["text"])
        print("💾 Guardado en: transcripcion_resultado.txt")
        
        return True
        
    except ImportError as e:
        print(f"❌ Error importando Whisper: {e}")
        print("💡 Instala con: pip install openai-whisper")
        return False
    except Exception as e:
        print(f"❌ Error durante transcripción: {e}")
        print(f"📋 Tipo de error: {type(e).__name__}")
        return False

def main():
    print("🎙️ DIAGNÓSTICO Y TRANSCRIPCIÓN WHISPER LOCAL")
    print("=" * 50)
    
    # Verificar Python
    print(f"🐍 Python: {sys.version}")
    
    # Verificar directorio
    print(f"📁 Directorio: {os.getcwd()}")
    
    # Listar archivos de audio
    archivos_audio = [f for f in os.listdir(".") if f.endswith((".mp3", ".wav", ".m4a", ".webm"))]
    print(f"🎵 Archivos de audio encontrados: {archivos_audio}")
    
    # Intentar transcripción
    if probar_whisper_simple():
        print("\n🎉 ¡ÉXITO! Tu transcripción está completa.")
        print("🔧 Para usar el modelo más preciso, cambia 'tiny' por 'base' en el código")
    else:
        print("\n❌ Transcripción fallida. Revisa los mensajes de error arriba.")
        print("\n🛠️ SOLUCIONES POSIBLES:")
        print("1. Reiniciar VS Code completamente")
        print("2. Ejecutar en nuevo terminal:")
        print("   winget install ffmpeg")
        print("3. Verificar que el archivo de audio no esté corrupto")
        print("4. Usar herramientas online como alternativa")

if __name__ == "__main__":
    main()