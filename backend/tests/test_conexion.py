
from flask import Flask, render_template_string
app = Flask(__name__)

@app.route('/')
def home():
    return '''
    <html>
    <head><title>🔧 Test de Conexión</title></head>
    <body style="font-family: Arial; text-align: center; padding: 50px;">
        <h1>✅ ¡Conexión Exitosa!</h1>
        <p>Tu servidor Flask está funcionando correctamente.</p>
        <p>🕐 Hora actual: <span id="time"></span></p>
        <script>
            setInterval(() => {
                document.getElementById('time').textContent = new Date().toLocaleTimeString();
            }, 1000);
        </script>
    </body>
    </html>
    '''

@app.route('/test')
def test():
    return {'status': 'OK', 'message': 'Servidor funcionando'}

if __name__ == '__main__':
    print("🚀 Servidor de prueba iniciando...")
    print("🌐 Ve a: http://localhost:5002")
    app.run(debug=True, port=5002)
