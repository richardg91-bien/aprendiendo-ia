"""
ARIA - Servidor Ultra Simple - Version de Diagnostico
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>ARIA - Test</title>
    </head>
    <body>
        <h1>ARIA Server Test</h1>
        <p>Servidor funcionando correctamente!</p>
        <p>Tiempo: """ + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + """</p>
    </body>
    </html>
    """

@app.route('/api/status')
def status():
    return jsonify({
        "status": "online",
        "timestamp": datetime.now().isoformat(),
        "message": "Server running"
    })

@app.route('/api/test')
def test():
    return jsonify({
        "success": True,
        "message": "Test endpoint working",
        "timestamp": datetime.now().isoformat()
    })

if __name__ == '__main__':
    print("🚀 ARIA Test Server - Starting...")
    print("🌐 Server: http://127.0.0.1:8000")
    
    app.run(
        host='127.0.0.1',
        port=8000,
        debug=True
    )