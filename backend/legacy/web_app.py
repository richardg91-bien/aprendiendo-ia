from flask import Flask, request, jsonify, render_template, send_file
from flask_cors import CORS
import os
import whisper
import tempfile
import uuid
from pathlib import Path
import time

app = Flask(__name__)
CORS(app)

# Configuración
UPLOAD_FOLDER = 'uploads'
RESULTS_FOLDER = 'results'

# Crear directorios si no existen
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULTS_FOLDER, exist_ok=True)

# Cargar modelo Whisper (solo una vez al iniciar)
print("🔄 Cargando modelo Whisper...")
model = whisper.load_model("base")  # Modelo balanceado entre velocidad y precisión
print("✅ Modelo Whisper cargado")

@app.route('/')
def index():
    """Página principal"""
    return render_template('index.html')

@app.route('/transcribe', methods=['POST'])
def transcribe_audio():
    """Endpoint para transcribir audio"""
    try:
        # Verificar si se subió un archivo
        if 'audio' not in request.files:
            return jsonify({'error': 'No se encontró archivo de audio'}), 400
        
        file = request.files['audio']
        if file.filename == '':
            return jsonify({'error': 'No se seleccionó archivo'}), 400
        
        # Generar nombre único para el archivo
        unique_id = str(uuid.uuid4())
        file_extension = Path(file.filename).suffix
        temp_filename = f"{unique_id}{file_extension}"
        temp_path = os.path.join(UPLOAD_FOLDER, temp_filename)
        
        # Guardar archivo temporalmente
        file.save(temp_path)
        
        # Transcribir el audio
        print(f"🎵 Transcribiendo: {file.filename}")
        start_time = time.time()
        
        result = model.transcribe(temp_path, fp16=False)
        
        end_time = time.time()
        processing_time = round(end_time - start_time, 2)
        
        # Guardar resultado
        result_filename = f"transcripcion_{unique_id}.txt"
        result_path = os.path.join(RESULTS_FOLDER, result_filename)
        
        with open(result_path, 'w', encoding='utf-8') as f:
            f.write(result["text"])
        
        # Limpiar archivo temporal
        os.remove(temp_path)
        
        print(f"✅ Transcripción completada en {processing_time}s")
        
        return jsonify({
            'success': True,
            'transcription': result["text"],
            'filename': file.filename,
            'processing_time': processing_time,
            'result_file': result_filename
        })
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return jsonify({'error': f'Error durante la transcripción: {str(e)}'}), 500

@app.route('/download/<filename>')
def download_result(filename):
    """Descargar archivo de resultado"""
    try:
        file_path = os.path.join(RESULTS_FOLDER, filename)
        if os.path.exists(file_path):
            return send_file(file_path, as_attachment=True)
        else:
            return jsonify({'error': 'Archivo no encontrado'}), 404
    except Exception as e:
        return jsonify({'error': f'Error al descargar: {str(e)}'}), 500

@app.route('/health')
def health_check():
    """Verificar estado de la aplicación"""
    return jsonify({
        'status': 'OK',
        'whisper_model': 'base',
        'upload_folder': UPLOAD_FOLDER,
        'results_folder': RESULTS_FOLDER
    })

if __name__ == '__main__':
    print("🚀 Iniciando servidor de transcripción...")
    print("📂 Uploads: uploads/")
    print("📁 Results: results/")
    print("🌐 Accede a: http://localhost:5000")
    
    app.run(debug=True, host='0.0.0.0', port=5000)