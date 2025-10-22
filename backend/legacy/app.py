import os
from openai import OpenAI
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Inicializar el cliente de OpenAI
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Verificar que el archivo de audio existe
audio_file_path = "prueba.mp3"
if not os.path.exists(audio_file_path):
    print(f"❌ Error: No se encontró el archivo '{audio_file_path}'")
    print("📁 Archivos disponibles en el directorio:")
    for file in os.listdir("."):
        if file.endswith((".mp3", ".wav", ".m4a", ".webm")):
            print(f"   - {file}")
    exit(1)

try:
    # Abrir y transcribir el archivo de audio
    with open(audio_file_path, "rb") as audio_file:
        transcribed = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file
        )
    
    print("✅ Transcripción completada:")
    print("📝 Resultado:", transcribed.text)
    
except Exception as e:
    print(f"❌ Error durante la transcripción: {e}")
    print("💡 Asegúrate de que:")
    print("   1. El archivo OPENAI_API_KEY esté en el archivo .env")
    print("   2. Tu API key sea válida")
    print("   3. El archivo de audio sea válido")