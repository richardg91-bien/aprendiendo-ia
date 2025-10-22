from flask import Flask
import sys

# Configuración simple para verificar Flask
app = Flask(__name__)

@app.route('/')
def home():
    return "<h1>🤖 ARIA - Test Server</h1><p>El servidor está funcionando correctamente!</p>"

@app.route('/test')
def test():
    return {"status": "ok", "message": "Servidor Flask funcionando"}

if __name__ == '__main__':
    print("🔧 Iniciando servidor de prueba...")
    print("🌐 Accede a: http://localhost:5001")
    
    try:
        app.run(debug=False, port=5001, host='127.0.0.1', threaded=True)
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)