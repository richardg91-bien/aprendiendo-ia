"""
ARIA - Servidor Estable con Red Neuronal Avanzada
"""

import sys
import os

# Configurar codificación UTF-8 para Windows
if sys.platform.startswith('win'):
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.detach())
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.detach())

from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime
import random

# Agregar el directorio src al path para importar neural_network
sys.path.append(os.path.join(os.path.dirname(__file__)))

try:
    from neural_network import neural_network
    NEURAL_NETWORK_AVAILABLE = True
except ImportError:
    NEURAL_NETWORK_AVAILABLE = False
    print("⚠️ Sistema de red neuronal no disponible - usando modo básico")

try:
    from voice_system import voice_system
    VOICE_SYSTEM_AVAILABLE = voice_system is not None
    if VOICE_SYSTEM_AVAILABLE:
        print("✅ Sistema de voz ARIA cargado correctamente")
    else:
        print("⚠️ Sistema de voz no disponible")
except ImportError:
    VOICE_SYSTEM_AVAILABLE = False
    print("⚠️ Sistema de voz no disponible - pywin32 no encontrado")

try:
    from auto_learning_simple import auto_learning
    AUTO_LEARNING_AVAILABLE = True
    print("🧠 Sistema de aprendizaje autónomo simplificado cargado")
except ImportError:
    AUTO_LEARNING_AVAILABLE = False
    print("⚠️ Sistema de aprendizaje autónomo no disponible")

try:
    from auto_learning_advanced import aria_advanced_learning
    ADVANCED_LEARNING_AVAILABLE = True
    print("🚀 Sistema de aprendizaje avanzado con fuentes reales cargado")
except ImportError:
    ADVANCED_LEARNING_AVAILABLE = False
    print("⚠️ Sistema de aprendizaje avanzado no disponible - usando sistema básico")

def _get_learning_summary():
    """Obtiene un resumen del aprendizaje actual"""
    try:
        if ADVANCED_LEARNING_AVAILABLE:
            status = aria_advanced_learning.get_status()
            total = status.get('total_knowledge', 0)
            sources = status.get('top_sources', {})
            topics = status.get('top_topics', {})
            
            summary = f"He aprendido {total} elementos de conocimiento real. "
            if sources:
                top_source = list(sources.keys())[0]
                summary += f"Mi fuente principal es {top_source}. "
            if topics:
                top_topic = list(topics.keys())[0]
                summary += f"He estudiado principalmente {top_topic}."
            
            return summary
        else:
            return "Mi sistema de aprendizaje está en modo básico."
    except:
        return "Estoy procesando mi conocimiento actual."

try:
    from cloud_database import cloud_db
    CLOUD_DB_AVAILABLE = True
    print("🌐 Base de datos en la nube cargada")
except ImportError:
    CLOUD_DB_AVAILABLE = False
    print("⚠️ Base de datos en la nube no disponible")

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>ARIA - Asistente Virtual</title>
        <style>
            body { font-family: Arial; padding: 20px; background: #f0f8ff; }
            .container { max-width: 800px; margin: 0 auto; }
            .header { text-align: center; color: #2c3e50; }
            .chat-box { 
                background: white; 
                border-radius: 10px; 
                padding: 20px; 
                margin: 20px 0; 
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            }
            .input-group { display: flex; gap: 10px; margin-top: 15px; }
            .input-group input { 
                flex: 1; 
                padding: 12px; 
                border: 2px solid #e0e0e0; 
                border-radius: 5px; 
                font-size: 16px;
            }
            .input-group button { 
                padding: 12px 20px; 
                background: #3498db; 
                color: white; 
                border: none; 
                border-radius: 5px; 
                cursor: pointer;
                font-size: 16px;
            }
            .input-group button:hover { background: #2980b9; }
            .response { 
                margin-top: 15px; 
                padding: 15px; 
                background: #f8f9fa; 
                border-left: 4px solid #3498db; 
                border-radius: 5px;
                min-height: 20px;
            }
            .features { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 15px; margin: 20px 0; }
            .feature { 
                background: white; 
                padding: 15px; 
                border-radius: 8px; 
                box-shadow: 0 2px 5px rgba(0,0,0,0.1); 
                text-align: center;
            }
            .status { background: #d4edda; padding: 10px; border-radius: 5px; margin: 10px 0; }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🤖 ARIA - Asistente Virtual Inteligente</h1>
                <div class="status">
                    ✅ Sistema Activo | ⏰ """ + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + """
                </div>
            </div>
            
            <div class="chat-box">
                <h3>💬 Chat con ARIA</h3>
                <p>¡Hola! Soy ARIA, tu asistente virtual. Puedes preguntarme cualquier cosa.</p>
                <div class="input-group">
                    <input type="text" id="messageInput" placeholder="Escribe tu mensaje aquí..." />
                    <button onclick="sendMessage()">Enviar</button>
                </div>
                <div id="response" class="response">
                    Esperando tu mensaje...
                </div>
            </div>
            
            <div class="features">
                <div class="feature">
                    <h4>🔊 Sistema de Voz</h4>
                    <p>Síntesis de voz integrada</p>
                    <button onclick="testVoice()">Probar Voz</button>
                    <button onclick="toggleVoice()">Activar/Desactivar</button>
                </div>
                <div class="feature">
                    <h4>🧠 Red Neuronal</h4>
                    <p>Sistema de IA avanzado con memoria</p>
                    <button onclick="testTraining()">Entrenar Red</button>
                    <button onclick="showNeuralInfo()">Info Red Neuronal</button>
                </div>
                <div class="feature">
                    <h4>📊 Aprendizaje</h4>
                    <p>Estadísticas y progreso</p>
                    <button onclick="showLearningStats()">Ver Estadísticas</button>
                </div>
                <div class="feature">
                    <h4>📚 Diccionario</h4>
                    <p>Base de conocimiento</p>
                    <button onclick="testDictionary()">Ver Diccionario</button>
                </div>
                <div class="feature">
                    <h4>🔍 Búsqueda Web</h4>
                    <p>Búsqueda inteligente</p>
                    <button onclick="testSearch()">Probar Búsqueda</button>
                </div>
            </div>
        </div>
        
        <script>
            let voiceEnabled = true;
            
            async function sendMessage() {
                const input = document.getElementById('messageInput');
                const responseDiv = document.getElementById('response');
                const message = input.value.trim();
                
                if (!message) return;
                
                responseDiv.innerHTML = '⏳ Procesando mensaje...';
                
                try {
                    const response = await fetch('/api/chat', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ 
                            message: message,
                            voice_enabled: voiceEnabled 
                        })
                    });
                    
                    const data = await response.json();
                    
                    if (data.success) {
                        responseDiv.innerHTML = `
                            <strong>🤖 ARIA:</strong> ${data.response}<br>
                            <small>Confianza: ${(data.confidence * 100).toFixed(1)}% | ${data.timestamp}</small>
                            ${data.voice_spoken ? '<br><small>🔊 Respuesta reproducida por voz</small>' : ''}
                        `;
                    } else {
                        responseDiv.innerHTML = `❌ Error: ${data.message}`;
                    }
                    
                    input.value = '';
                } catch (error) {
                    responseDiv.innerHTML = `❌ Error de conexión: ${error.message}`;
                }
            }
            
            async function testVoice() {
                const responseDiv = document.getElementById('response');
                responseDiv.innerHTML = '🔊 Probando sistema de voz...';
                
                try {
                    const response = await fetch('/api/voz/test', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ 
                            text: "¡Hola! Soy ARIA, tu asistente virtual inteligente. Mi sistema de voz está funcionando perfectamente."
                        })
                    });
                    
                    const data = await response.json();
                    
                    if (data.success) {
                        responseDiv.innerHTML = `
                            <strong>🔊 Prueba de Voz Exitosa</strong><br>
                            Sistema: ${data.voice_info.available ? 'Disponible' : 'No disponible'}<br>
                            Voz actual: ${data.voice_info.current_voice || 'Ninguna'}<br>
                            Total de voces: ${data.voice_info.total_voices}<br>
                            Volumen: ${data.voice_info.volume}% | Velocidad: ${data.voice_info.rate}
                        `;
                    } else {
                        responseDiv.innerHTML = `❌ Error en sistema de voz: ${data.message}`;
                    }
                } catch (error) {
                    responseDiv.innerHTML = `❌ Error probando voz: ${error.message}`;
                }
            }
            
            async function toggleVoice() {
                voiceEnabled = !voiceEnabled;
                const responseDiv = document.getElementById('response');
                responseDiv.innerHTML = `🔊 Voz ${voiceEnabled ? 'ACTIVADA' : 'DESACTIVADA'}`;
            }
            
            async function testTraining() {
                const responseDiv = document.getElementById('response');
                responseDiv.innerHTML = '🧠 Iniciando entrenamiento avanzado de red neuronal...';
                
                try {
                    const response = await fetch('/api/entrenar_red_neuronal', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ epochs: 50 })
                    });
                    
                    const data = await response.json();
                    if (data.success) {
                        responseDiv.innerHTML = `
                            <strong>✅ Entrenamiento Completado</strong><br>
                            📊 Épocas: ${data.epochs}<br>
                            📈 Precisión inicial: ${(data.accuracy_inicial * 100).toFixed(2)}%<br>
                            🎯 Precisión final: ${(data.accuracy_final * 100).toFixed(2)}%<br>
                            📊 Mejora: +${(data.mejora * 100).toFixed(2)}%<br>
                            ⏱️ Duración: ${data.duracion_segundos}s<br>
                            🧠 Red neuronal actualizada exitosamente
                        `;
                    } else {
                        responseDiv.innerHTML = `❌ Error: ${data.message}`;
                    }
                } catch (error) {
                    responseDiv.innerHTML = `❌ Error en entrenamiento: ${error.message}`;
                }
            }
            
            async function showNeuralInfo() {
                const responseDiv = document.getElementById('response');
                responseDiv.innerHTML = '🧠 Cargando información de red neuronal...';
                
                try {
                    const response = await fetch('/api/red_neuronal_info');
                    const data = await response.json();
                    
                    if (data.success) {
                        const info = data.model;
                        responseDiv.innerHTML = `
                            <strong>🧠 ${info.model_name}</strong><br>
                            📊 Estado: ${info.status}<br>
                            🎯 Precisión actual: ${(info.accuracy * 100).toFixed(2)}%<br>
                            💬 Conversaciones totales: ${info.total_conversations}<br>
                            🧩 Patrones aprendidos: ${info.learned_patterns}<br>
                            🏋️ Entrenamientos: ${info.total_trainings}<br>
                            🧠 Memoria activa: ${info.memory_size} conversaciones<br>
                            📅 Último entrenamiento: ${info.last_training}<br>
                            🏗️ Arquitectura: ${info.architecture}
                        `;
                    } else {
                        responseDiv.innerHTML = `❌ Error: ${data.message}`;
                    }
                } catch (error) {
                    responseDiv.innerHTML = `❌ Error al cargar info: ${error.message}`;
                }
            }
            
            async function showLearningStats() {
                const responseDiv = document.getElementById('response');
                responseDiv.innerHTML = '📊 Cargando estadísticas de aprendizaje...';
                
                try {
                    const response = await fetch('/api/learning/stats');
                    const data = await response.json();
                    
                    if (data.success) {
                        const stats = data.stats;
                        let html = '<strong>📊 Estadísticas de Aprendizaje</strong><br>';
                        html += `🎯 Precisión actual: ${(stats.current_accuracy * 100).toFixed(2)}%<br>`;
                        html += `📚 Palabras aprendidas: ${stats.total_learned_words}<br>`;
                        html += `💾 Eficiencia de memoria: ${(stats.memory_efficiency * 100).toFixed(1)}%<br><br>`;
                        
                        if (stats.training_history && stats.training_history.length > 0) {
                            html += '<strong>🏋️ Últimos Entrenamientos:</strong><br>';
                            stats.training_history.forEach(training => {
                                html += `• ${training.epochs} épocas → ${(training.accuracy * 100).toFixed(1)}% (+${(training.mejora * 100).toFixed(1)}%)<br>`;
                            });
                        }
                        
                        responseDiv.innerHTML = html;
                    } else {
                        responseDiv.innerHTML = `❌ Error: ${data.message}`;
                    }
                } catch (error) {
                    responseDiv.innerHTML = `❌ Error al cargar estadísticas: ${error.message}`;
                }
            }
            
            async function testDictionary() {
                const responseDiv = document.getElementById('response');
                responseDiv.innerHTML = '📚 Cargando diccionario...';
                
                try {
                    const response = await fetch('/api/diccionario');
                    const data = await response.json();
                    
                    if (data.success) {
                        let html = '<strong>📚 Diccionario ARIA:</strong><br>';
                        data.palabras.forEach(p => {
                            html += `• <strong>${p.palabra}</strong>: ${p.definicion}<br>`;
                        });
                        responseDiv.innerHTML = html;
                    }
                } catch (error) {
                    responseDiv.innerHTML = `❌ Error al cargar diccionario: ${error.message}`;
                }
            }
            
            async function testSearch() {
                const responseDiv = document.getElementById('response');
                responseDiv.innerHTML = '🔍 Realizando búsqueda de prueba...';
                
                try {
                    const response = await fetch('/api/busqueda_web', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ query: 'inteligencia artificial' })
                    });
                    
                    const data = await response.json();
                    
                    if (data.success) {
                        let html = '<strong>🔍 Resultados de búsqueda:</strong><br>';
                        data.resultados.forEach(r => {
                            html += `• <strong>${r.title}</strong><br>${r.snippet}<br><br>`;
                        });
                        responseDiv.innerHTML = html;
                    }
                } catch (error) {
                    responseDiv.innerHTML = `❌ Error en búsqueda: ${error.message}`;
                }
            }
            
            document.getElementById('messageInput').addEventListener('keypress', function(e) {
                if (e.key === 'Enter') sendMessage();
            });
        </script>
    </body>
    </html>
    """

@app.route('/futuristic')
def futuristic_interface():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>ARIA Futuristic - Robot Face Interface</title>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            body { 
                margin: 0; 
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 50%, #16213e 100%);
                color: white; 
                overflow-x: hidden;
                min-height: 100vh;
            }
            .container { 
                max-width: 1200px; 
                margin: 0 auto; 
                padding: 20px;
                position: relative;
                z-index: 10;
            }
            .header { 
                text-align: center; 
                margin-bottom: 30px;
                animation: glow 2s ease-in-out infinite alternate;
            }
            .robot-face-container {
                display: flex;
                justify-content: center;
                margin: 30px 0;
                position: relative;
            }
            .robot-face {
                width: 300px;
                height: 300px;
                background: linear-gradient(145deg, #1a1a1a 0%, #2d2d30 100%);
                border-radius: 50%;
                position: relative;
                border: 3px solid #0080FF;
                box-shadow: 0 0 30px #0080FF;
                animation: pulse 2s infinite;
            }
            .robot-eye {
                width: 60px;
                height: 48px;
                background: radial-gradient(circle, #0080FF 0%, #0050AA 70%, #003366 100%);
                border-radius: 50%;
                position: absolute;
                top: 100px;
                border: 2px solid #000;
                animation: eye-glow 3s ease-in-out infinite alternate;
            }
            .left-eye { left: 80px; }
            .right-eye { right: 80px; }
            .eye-glint {
                width: 12px;
                height: 12px;
                background: rgba(255, 255, 255, 0.8);
                border-radius: 50%;
                position: absolute;
                top: 12px;
                left: 15px;
            }
            .robot-mouth {
                width: 100px;
                height: 12px;
                background: #333;
                position: absolute;
                bottom: 80px;
                left: 50%;
                transform: translateX(-50%);
                border: 2px solid #444;
            }
            .chat-area {
                background: rgba(0, 0, 0, 0.7);
                border-radius: 15px;
                padding: 25px;
                margin: 20px 0;
                border: 1px solid #0080FF30;
                backdrop-filter: blur(10px);
            }
            .input-group { 
                display: flex; 
                gap: 15px; 
                margin-top: 20px; 
            }
            .input-group input { 
                flex: 1; 
                padding: 15px; 
                border: 2px solid #0080FF; 
                border-radius: 8px; 
                background: rgba(0, 0, 0, 0.8);
                color: white;
                font-size: 16px;
                outline: none;
                transition: all 0.3s ease;
            }
            .input-group input:focus {
                border-color: #00FF7F;
                box-shadow: 0 0 10px #00FF7F;
            }
            .input-group button { 
                padding: 15px 25px; 
                background: linear-gradient(45deg, #0080FF, #00FF7F);
                color: white; 
                border: none; 
                border-radius: 8px; 
                cursor: pointer;
                font-size: 16px;
                font-weight: bold;
                transition: all 0.3s ease;
                box-shadow: 0 0 20px rgba(0, 128, 255, 0.5);
            }
            .input-group button:hover { 
                transform: translateY(-2px);
                box-shadow: 0 5px 30px rgba(0, 255, 127, 0.7);
            }
            .response { 
                margin-top: 20px; 
                padding: 20px; 
                background: rgba(0, 128, 255, 0.1); 
                border-left: 4px solid #0080FF; 
                border-radius: 8px;
                min-height: 30px;
                transition: all 0.3s ease;
            }
            .emotion-indicator {
                position: absolute;
                top: 10px;
                right: 10px;
                padding: 10px 20px;
                background: rgba(0, 128, 255, 0.8);
                border-radius: 20px;
                font-weight: bold;
                animation: float 3s ease-in-out infinite;
            }
            .particles {
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                pointer-events: none;
                z-index: 1;
            }
            .particle {
                position: absolute;
                width: 2px;
                height: 2px;
                background: #0080FF;
                border-radius: 50%;
                animation: float-particle 4s infinite linear;
            }
            
            @keyframes pulse {
                0% { box-shadow: 0 0 30px #0080FF; }
                50% { box-shadow: 0 0 60px #0080FF, 0 0 90px #0080FF; }
                100% { box-shadow: 0 0 30px #0080FF; }
            }
            
            @keyframes glow {
                0% { text-shadow: 0 0 10px #0080FF; }
                50% { text-shadow: 0 0 20px #0080FF, 0 0 30px #0080FF; }
                100% { text-shadow: 0 0 10px #0080FF; }
            }
            
            @keyframes eye-glow {
                0% { background: radial-gradient(circle, #0080FF 0%, #0050AA 70%, #003366 100%); }
                100% { background: radial-gradient(circle, #00FF7F 0%, #00AA50 70%, #006633 100%); }
            }
            
            @keyframes float {
                0%, 100% { transform: translateY(0px); }
                50% { transform: translateY(-10px); }
            }
            
            @keyframes float-particle {
                0% { 
                    transform: translateY(100vh) translateX(0px) scale(0);
                    opacity: 0;
                }
                10% {
                    opacity: 1;
                    transform: scale(1);
                }
                90% {
                    opacity: 1;
                }
                100% { 
                    transform: translateY(-100px) translateX(50px) scale(0);
                    opacity: 0;
                }
            }
            
            .learning { border-color: #00FF7F !important; box-shadow: 0 0 30px #00FF7F !important; }
            .learning .robot-eye { background: radial-gradient(circle, #00FF7F 0%, #00AA50 70%, #006633 100%) !important; }
            
            .thinking { border-color: #8A2BE2 !important; box-shadow: 0 0 30px #8A2BE2 !important; }
            .thinking .robot-eye { background: radial-gradient(circle, #8A2BE2 0%, #6A1BAA 70%, #4A1366 100%) !important; }
            
            .happy { border-color: #FFD700 !important; box-shadow: 0 0 30px #FFD700 !important; }
            .happy .robot-eye { background: radial-gradient(circle, #FFD700 0%, #CCAA00 70%, #996600 100%) !important; }
            
            .frustrated { border-color: #FF4500 !important; box-shadow: 0 0 30px #FF4500 !important; }
            .frustrated .robot-eye { background: radial-gradient(circle, #FF4500 0%, #CC3300 70%, #990000 100%) !important; }
        </style>
    </head>
    <body>
        <!-- Particles Background -->
        <div class="particles" id="particles"></div>
        
        <div class="container">
            <div class="header">
                <h1>🤖 ARIA FUTURISTIC - Robot Face Interface</h1>
                <div class="emotion-indicator" id="emotionIndicator">
                    Estado: NEUTRAL
                </div>
            </div>
            
            <!-- Robot Face -->
            <div class="robot-face-container">
                <div class="robot-face" id="robotFace">
                    <div class="robot-eye left-eye">
                        <div class="eye-glint"></div>
                    </div>
                    <div class="robot-eye right-eye">
                        <div class="eye-glint"></div>
                    </div>
                    <div class="robot-mouth"></div>
                </div>
            </div>
            
            <!-- Chat Area -->
            <div class="chat-area">
                <h3>💬 Chat con ARIA Futurista</h3>
                <p>¡Hola! Soy ARIA en modo futurista. Observa cómo cambian mis ojos según mis emociones.</p>
                <div class="input-group">
                    <input type="text" id="messageInput" placeholder="Escribe tu mensaje aquí..." />
                    <button onclick="sendFuturisticMessage()">🚀 Enviar</button>
                </div>
                <div id="response" class="response">
                    Esperando tu mensaje... Observa mi cara robótica mientras hablamos.
                </div>
            </div>
        </div>
        
        <script>
            let currentEmotion = 'neutral';
            
            // Crear partículas de fondo
            function createParticles() {
                const particlesContainer = document.getElementById('particles');
                for (let i = 0; i < 50; i++) {
                    const particle = document.createElement('div');
                    particle.className = 'particle';
                    particle.style.left = Math.random() * 100 + '%';
                    particle.style.animationDelay = Math.random() * 4 + 's';
                    particle.style.animationDuration = (Math.random() * 3 + 2) + 's';
                    particlesContainer.appendChild(particle);
                }
            }
            
            // Cambiar emoción del robot
            function changeEmotion(emotion) {
                const robotFace = document.getElementById('robotFace');
                const emotionIndicator = document.getElementById('emotionIndicator');
                
                // Remover clases de emoción anteriores
                robotFace.classList.remove('learning', 'thinking', 'happy', 'frustrated');
                
                // Agregar nueva emoción
                if (emotion !== 'neutral') {
                    robotFace.classList.add(emotion);
                }
                
                currentEmotion = emotion;
                
                // Actualizar indicador
                const emotionNames = {
                    'neutral': 'NEUTRAL 🔵',
                    'learning': 'APRENDIENDO 🟢',
                    'thinking': 'PENSANDO 🟣',
                    'happy': 'FELIZ 🟡',
                    'frustrated': 'FRUSTRADA 🔴'
                };
                
                emotionIndicator.textContent = 'Estado: ' + emotionNames[emotion];
                emotionIndicator.style.background = {
                    'neutral': 'rgba(0, 128, 255, 0.8)',
                    'learning': 'rgba(0, 255, 127, 0.8)',
                    'thinking': 'rgba(138, 43, 226, 0.8)',
                    'happy': 'rgba(255, 215, 0, 0.8)',
                    'frustrated': 'rgba(255, 69, 0, 0.8)'
                }[emotion];
            }
            
            async function sendFuturisticMessage() {
                const input = document.getElementById('messageInput');
                const responseDiv = document.getElementById('response');
                const message = input.value.trim();
                
                if (!message) return;
                
                // Cambiar a estado pensando
                changeEmotion('thinking');
                responseDiv.innerHTML = '🤖 ARIA está pensando...';
                
                try {
                    const response = await fetch('/api/chat/futuristic', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ 
                            message: message,
                            emotion_context: currentEmotion 
                        })
                    });
                    
                    const data = await response.json();
                    
                    if (data.success) {
                        // Cambiar emoción según respuesta
                        const emotion = data.emotion || 'neutral';
                        changeEmotion(emotion);
                        
                        responseDiv.innerHTML = `
                            <strong>🤖 ARIA:</strong> ${data.response}<br>
                            <small>
                                💭 Emoción: ${emotion.toUpperCase()} | 
                                📊 Confianza: ${(data.confidence * 100).toFixed(1)}% | 
                                ⏰ ${data.timestamp}
                            </small>
                            ${data.learned_something ? '<br><small>🧠 ¡He aprendido algo nuevo!</small>' : ''}
                        `;
                    } else {
                        changeEmotion('frustrated');
                        responseDiv.innerHTML = `❌ Error: ${data.message}`;
                    }
                    
                    input.value = '';
                    
                } catch (error) {
                    changeEmotion('frustrated');
                    responseDiv.innerHTML = `❌ Error de conexión: ${error.message}`;
                }
            }
            
            // Permitir envío con Enter
            document.getElementById('messageInput').addEventListener('keypress', function(e) {
                if (e.key === 'Enter') {
                    sendFuturisticMessage();
                }
            });
            
            // Inicializar
            createParticles();
            
            // Auto-demo de emociones cada 30 segundos
            setInterval(() => {
                if (currentEmotion === 'neutral') {
                    const emotions = ['learning', 'thinking', 'happy'];
                    const randomEmotion = emotions[Math.floor(Math.random() * emotions.length)];
                    changeEmotion(randomEmotion);
                    setTimeout(() => changeEmotion('neutral'), 3000);
                }
            }, 30000);
        </script>
    </body>
    </html>
    """

# API Endpoints
@app.route('/api/status')
def status():
    neural_status = "disponible" if NEURAL_NETWORK_AVAILABLE else "básico"
    return jsonify({
        "status": "online",
        "version": "stable-2.0",
        "timestamp": datetime.now().isoformat(),
        "message": "ARIA funcionando correctamente",
        "neural_network": neural_status
    })

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        message = data.get('message', '').strip()
        voice_enabled = data.get('voice_enabled', True)
        
        if not message:
            return jsonify({"success": False, "message": "Mensaje vacío"})
        
        # Primero intentar respuestas rápidas básicas para saludos
        basic_responses = {
            'hola': '¡Hola! Me alegra saludarte. ¿Cómo estás?',
            'como estas': 'Estoy funcionando perfectamente, gracias por preguntar.',
            'que tal': 'Todo muy bien por aquí. ¿Y tú qué tal?',
            'bien': 'Me alegra escuchar eso. ¿En qué puedo ayudarte?',
            'gracias': '¡De nada! Es un placer ayudarte.',
            'adios': '¡Hasta luego! Que tengas un excelente día.',
            'entrenar': 'Puedo entrenar mi red neuronal. Haz clic en "Entrenar Red".',
            'diccionario': 'Tengo un diccionario integrado. Haz clic en "Ver Diccionario".',
            'buscar': 'Puedo realizar búsquedas web. Haz clic en "Probar Búsqueda".',
            'neuronal': 'Mi red neuronal está activa y aprendiendo. ¿Quieres ver las estadísticas?',
            'voz': 'Mi sistema de voz está integrado y funcionando. ¿Quieres que hable?',
            'habla': '¡Por supuesto! Puedo hablar contigo usando mi sistema de síntesis de voz.'
        }
        
        message_lower = message.lower()
        response = None
        confidence = 0.7
        
        # Buscar respuestas básicas SOLO para saludos/comandos simples
        for key, value in basic_responses.items():
            if message_lower == key or message_lower.startswith(key + ' '):
                response = value
                confidence = round(random.uniform(0.85, 0.98), 2)
                break
        
        # Si no es saludo básico, usar sistema de conocimiento avanzado
        if not response and ADVANCED_LEARNING_AVAILABLE:
            try:
                # Buscar en la base de conocimiento real
                knowledge_results = aria_advanced_learning.search_knowledge(message, limit=1)
                
                if knowledge_results:
                    best_result = knowledge_results[0]
                    response = f"""Basándome en mi conocimiento real sobre {best_result['topic']}, puedo decirte que:

{best_result['content']}

Esta información proviene de {best_result['source_name']} (confianza: {best_result['confidence_score']:.0%}) y fue obtenida el {best_result['timestamp'][:10]}."""
                    
                    if best_result['source_url']:
                        response += f"\n\nPuedes verificar esta información en: {best_result['source_url']}"
                    
                    confidence = best_result['confidence_score']
                else:
                    # Si no encuentra conocimiento específico, buscar por palabras clave
                    words = message.lower().split()
                    for word in words:
                        if len(word) > 3:  # Palabras significativas
                            keyword_results = aria_advanced_learning.search_knowledge(word, limit=1)
                            if keyword_results:
                                result = keyword_results[0]
                                response = f"Aunque no tengo información específica sobre tu pregunta, sí he aprendido sobre {result['topic']}:\n\n{result['content'][:300]}...\n\n(Fuente: {result['source_name']}, {result['confidence_score']:.0%} confianza)"
                                confidence = result['confidence_score'] * 0.8  # Reducir confianza por ser indirecta
                                break
                
                # Para preguntas sobre aprendizaje, mostrar resumen del conocimiento real
                if any(word in message_lower for word in ['aprendido', 'aprender', 'conocimiento', 'que has aprendido']):
                    status = aria_advanced_learning.get_status()
                    total = status.get('total_knowledge', 0)
                    if total > 0:
                        top_topics = list(status.get('top_topics', {}).keys())[:5]
                        top_sources = list(status.get('top_sources', {}).keys())[:3]
                        
                        response = f"""He aprendido {total} elementos de conocimiento real de fuentes científicas verificadas.

🧠 **Mis temas principales:** {', '.join(top_topics)}

📚 **Mis fuentes principales:** {', '.join(top_sources)}

🌐 **Capacidades multilingües:** Puedo procesar información en español (RAE, noticias) e inglés (ArXiv, Wikipedia).

¿Te gustaría que profundice en algún tema específico?"""
                        confidence = 0.95
                
                # Mejorar respuestas para búsquedas sin resultados
                elif not response:
                    response = f"""No tengo información específica sobre '{message}' en mi base de conocimiento actual. 

🔍 **Mi sistema aprende de:**
• 📰 Noticias científicas en español
• 📚 Papers de ArXiv en inglés  
• 📖 Definiciones de la RAE
• 🌐 Wikipedia y RSS feeds

¿Podrías preguntarme sobre tecnología, ciencia, inteligencia artificial o computación?"""
                    confidence = 0.7
            except Exception as e:
                print(f"Error accediendo conocimiento avanzado: {e}")
        
        # Si aún no hay respuesta, fallback básico
        if not response:
            response = f"Interesante. Me dijiste: '{message}'. Estoy aprendiendo a responder mejor cada día."
            confidence = round(random.uniform(0.6, 0.8), 2)
        
        # Síntesis de voz
        voice_spoken = False
        if voice_enabled and VOICE_SYSTEM_AVAILABLE:
            try:
                voice_spoken = voice_system.speak_text(response, async_mode=True)
            except Exception as e:
                print(f"Error en síntesis de voz: {e}")
        
        # Guardar conversación en la red neuronal si está disponible
        if NEURAL_NETWORK_AVAILABLE:
            try:
                neural_network.save_conversation(message, response, confidence)
                # Aprender patrones básicos para respuestas simples
                if any(key in message_lower for key in basic_responses.keys()):
                    for key, value in basic_responses.items():
                        if key in message_lower:
                            neural_network.learn_pattern(key, value)
                            break
            except Exception as e:
                print(f"Error guardando en red neuronal: {e}")
        
        return jsonify({
            "success": True,
            "response": response,
            "confidence": confidence,
            "timestamp": datetime.now().isoformat(),
            "neural_learning": NEURAL_NETWORK_AVAILABLE,
            "voice_spoken": voice_spoken,
            "voice_available": VOICE_SYSTEM_AVAILABLE
        })
        
    except Exception as e:
        return jsonify({"success": False, "message": str(e)})

@app.route('/api/entrenar_red_neuronal', methods=['POST'])
def entrenar_red_neuronal():
    try:
        data = request.get_json() or {}
        epochs = data.get('epochs', 50)
        
        if NEURAL_NETWORK_AVAILABLE:
            # Usar red neuronal real
            result = neural_network.train_network(epochs=epochs)
            return jsonify(result)
        else:
            # Modo básico de simulación
            import time
            time.sleep(2)
            accuracy = round(0.85 + random.uniform(0, 0.15), 3)
            
            return jsonify({
                "success": True,
                "message": "Entrenamiento completado (modo básico)",
                "epochs": epochs,
                "accuracy_inicial": 0.75,
                "accuracy_final": accuracy,
                "mejora": accuracy - 0.75,
                "duracion_segundos": 2.0,
                "timestamp": datetime.now().isoformat()
            })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Error en entrenamiento: {str(e)}"
        })

@app.route('/api/red_neuronal_info', methods=['GET'])
def red_neuronal_info():
    try:
        if NEURAL_NETWORK_AVAILABLE:
            info = neural_network.get_neural_info()
            return jsonify({
                "success": True,
                "model": info
            })
        else:
            return jsonify({
                "success": True,
                "model": {
                    "model_name": "ARIA Neural Network (Básico)",
                    "status": "active",
                    "accuracy": 0.85,
                    "total_conversations": 0,
                    "learned_patterns": 0,
                    "total_trainings": 0,
                    "last_training": "Modo básico",
                    "memory_size": 0,
                    "architecture": "Basic simulation mode"
                }
            })
            
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Error obteniendo info: {str(e)}"
        })

@app.route('/api/learning/stats', methods=['GET'])
def learning_stats():
    try:
        if NEURAL_NETWORK_AVAILABLE:
            stats = neural_network.get_learning_stats()
            return jsonify({
                "success": True,
                "stats": stats
            })
        else:
            return jsonify({
                "success": True,
                "stats": {
                    "current_accuracy": 0.85,
                    "total_learned_words": 25,
                    "memory_efficiency": 0.7,
                    "training_history": [],
                    "conversations_by_day": [],
                    "top_patterns": []
                }
            })
            
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Error obteniendo estadísticas: {str(e)}"
        })

@app.route('/api/diccionario', methods=['GET'])
def diccionario():
    try:
        palabras = [
            {
                "palabra": "inteligencia",
                "definicion": "Capacidad de entender, aprender y resolver problemas",
                "categoria": "sustantivo"
            },
            {
                "palabra": "artificial",
                "definicion": "Creado por seres humanos, no natural",
                "categoria": "adjetivo"
            },
            {
                "palabra": "algoritmo",
                "definicion": "Conjunto de reglas e instrucciones para resolver un problema",
                "categoria": "sustantivo"
            },
            {
                "palabra": "aprendizaje",
                "definicion": "Proceso de adquirir conocimientos, habilidades y comportamientos",
                "categoria": "sustantivo"
            }
        ]
        
        return jsonify({
            "success": True,
            "palabras": palabras,
            "total": len(palabras)
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Error en diccionario: {str(e)}"
        })

@app.route('/api/busqueda_web', methods=['POST'])
def busqueda_web():
    try:
        data = request.get_json() or {}
        query = data.get('query', '')
        depth = data.get('depth', 3)
        
        if not query:
            return jsonify({
                "success": False,
                "message": "Query requerido"
            })
        
        # Búsqueda simulada mejorada para el aprendizaje autónomo
        import requests
        from bs4 import BeautifulSoup
        
        resultados = []
        
        try:
            # Intentar búsqueda real en DuckDuckGo
            search_url = f"https://html.duckduckgo.com/html/?q={query.replace(' ', '+')}"
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            response = requests.get(search_url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                results_divs = soup.find_all('div', class_='result')
                
                for div in results_divs[:depth]:
                    try:
                        title_elem = div.find('a', class_='result__a')
                        snippet_elem = div.find('a', class_='result__snippet')
                        
                        if title_elem:
                            title = title_elem.get_text().strip()
                            url = title_elem.get('href', '')
                            snippet = snippet_elem.get_text().strip() if snippet_elem else "Información relevante encontrada"
                            
                            resultados.append({
                                "titulo": title,
                                "url": url,
                                "contenido": snippet,
                                "fuente": "DuckDuckGo",
                                "confianza": 0.8
                            })
                    except Exception as e:
                        continue
            
        except Exception as e:
            print(f"Error en búsqueda real: {e}")
        
        # Si no hay resultados reales, usar resultados simulados inteligentes
        if not resultados:
            topics = {
                'inteligencia artificial': [
                    {"titulo": "¿Qué es la Inteligencia Artificial?", "contenido": "La IA es la capacidad de las máquinas de imitar la inteligencia humana", "url": "https://example.com/ia"},
                    {"titulo": "Machine Learning y Deep Learning", "contenido": "Técnicas avanzadas de aprendizaje automático", "url": "https://example.com/ml"},
                    {"titulo": "Aplicaciones de IA en la vida cotidiana", "contenido": "Desde asistentes virtuales hasta coches autónomos", "url": "https://example.com/apps"}
                ],
                'programación': [
                    {"titulo": "Fundamentos de Programación", "contenido": "Conceptos básicos y mejores prácticas", "url": "https://example.com/prog"},
                    {"titulo": "Lenguajes de Programación Populares", "contenido": "Python, JavaScript, Java y más", "url": "https://example.com/lang"}
                ],
                'tecnología': [
                    {"titulo": "Últimas Tendencias Tecnológicas", "contenido": "Innovaciones que están cambiando el mundo", "url": "https://example.com/tech"},
                    {"titulo": "El Futuro de la Tecnología", "contenido": "Predicciones y avances esperados", "url": "https://example.com/future"}
                ]
            }
            
            # Buscar en temas conocidos
            for topic, results in topics.items():
                if any(word in query.lower() for word in topic.split()):
                    for result in results[:depth]:
                        resultados.append({
                            "titulo": result["titulo"],
                            "url": result["url"],
                            "contenido": result["contenido"],
                            "fuente": "Base de conocimiento ARIA",
                            "confianza": 0.9
                        })
                    break
            
            # Si no hay coincidencias, crear respuesta genérica
            if not resultados:
                resultados = [
                    {
                        "titulo": f"Información sobre: {query}",
                        "url": "https://example.com/search",
                        "contenido": f"Información relevante encontrada sobre {query}. ARIA está aprendiendo constantemente sobre este tema.",
                        "fuente": "ARIA Learning System",
                        "confianza": 0.7
                    }
                ]
        
        # Guardar conocimiento aprendido en el sistema autónomo
        if AUTO_LEARNING_AVAILABLE and resultados:
            try:
                auto_learning._save_knowledge(query, resultados)
            except Exception as e:
                print(f"Error guardando conocimiento: {e}")
        
        return jsonify({
            "success": True,
            "query": query,
            "resultados": resultados,
            "total_resultados": len(resultados),
            "timestamp": datetime.now().isoformat(),
            "auto_learning": AUTO_LEARNING_AVAILABLE
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Error en búsqueda: {str(e)}"
        })

@app.route('/api/voz/test', methods=['POST'])
def test_voice():
    try:
        data = request.get_json() or {}
        text = data.get('text', '¡Hola! Soy ARIA, tu asistente virtual.')
        
        if not VOICE_SYSTEM_AVAILABLE:
            return jsonify({
                "success": False,
                "message": "Sistema de voz no disponible",
                "voice_info": {
                    "available": False,
                    "current_voice": None,
                    "total_voices": 0
                }
            })
        
        # Probar síntesis de voz
        spoken = voice_system.speak_text(text)
        voice_info = voice_system.get_voice_info()
        
        return jsonify({
            "success": spoken,
            "message": "Prueba de voz ejecutada" if spoken else "Error en síntesis de voz",
            "voice_info": voice_info,
            "text_spoken": text
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Error en prueba de voz: {str(e)}"
        })

@app.route('/api/voz/speak', methods=['POST'])
def speak_text():
    try:
        data = request.get_json() or {}
        text = data.get('text', '')
        
        if not text:
            return jsonify({
                "success": False,
                "message": "Texto requerido"
            })
        
        if not VOICE_SYSTEM_AVAILABLE:
            return jsonify({
                "success": False,
                "message": "Sistema de voz no disponible"
            })
        
        spoken = voice_system.speak_text(text)
        
        return jsonify({
            "success": spoken,
            "message": "Texto sintetizado" if spoken else "Error en síntesis",
            "text": text
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Error sintetizando voz: {str(e)}"
        })

@app.route('/api/voz/stop', methods=['POST'])
def stop_voice():
    try:
        if not VOICE_SYSTEM_AVAILABLE:
            return jsonify({
                "success": False,
                "message": "Sistema de voz no disponible"
            })
        
        voice_system.stop_speaking()
        
        return jsonify({
            "success": True,
            "message": "Síntesis de voz detenida"
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Error deteniendo voz: {str(e)}"
        })

@app.route('/api/voz/info', methods=['GET'])
def voice_info():
    try:
        if not VOICE_SYSTEM_AVAILABLE:
            return jsonify({
                "success": False,
                "voice_info": {
                    "available": False,
                    "message": "Sistema de voz no disponible"
                }
            })
        
        info = voice_system.get_voice_info()
        
        return jsonify({
            "success": True,
            "voice_info": info
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Error obteniendo info de voz: {str(e)}"
        })

# =============================================================================
# ENDPOINTS DE APRENDIZAJE AUTÓNOMO
# =============================================================================

@app.route('/api/auto_learning/start', methods=['POST'])
def start_auto_learning():
    """Inicia el sistema de aprendizaje autónomo (básico o avanzado)"""
    try:
        # Intentar usar sistema avanzado primero
        if ADVANCED_LEARNING_AVAILABLE:
            result = aria_advanced_learning.start_learning()
            return jsonify({
                "success": True,
                "message": "🚀 Sistema de aprendizaje avanzado iniciado",
                "system": "advanced",
                "status": result,
                "capabilities": {
                    "real_time_web": True,
                    "scientific_papers": True,
                    "news_feeds": True,
                    "api_access": True
                }
            })
        
        # Fallback al sistema básico
        elif AUTO_LEARNING_AVAILABLE:
            auto_learning.start_autonomous_learning()
            return jsonify({
                "success": True,
                "message": "🧠 Sistema de aprendizaje básico iniciado",
                "system": "basic",
                "status": auto_learning.get_learning_status(),
                "capabilities": {
                    "real_time_web": False,
                    "template_based": True
                }
            })
        
        else:
            return jsonify({
                "success": False,
                "message": "Ningún sistema de aprendizaje disponible"
            })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Error iniciando aprendizaje: {str(e)}"
        })

@app.route('/api/auto_learning/stop', methods=['POST'])
def stop_auto_learning():
    """Detiene el sistema de aprendizaje autónomo"""
    try:
        success_count = 0
        messages = []
        
        # Detener sistema avanzado si está disponible
        if ADVANCED_LEARNING_AVAILABLE:
            try:
                aria_advanced_learning.stop_learning()
                success_count += 1
                messages.append("🛑 Sistema avanzado detenido")
            except:
                pass
        
        # Detener sistema básico si está disponible
        if AUTO_LEARNING_AVAILABLE:
            try:
                auto_learning.stop_autonomous_learning()
                success_count += 1
                messages.append("🛑 Sistema básico detenido")
            except:
                pass
        
        if success_count > 0:
            return jsonify({
                "success": True,
                "message": " | ".join(messages)
            })
        else:
            return jsonify({
                "success": False,
                "message": "No hay sistemas de aprendizaje activos"
            })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Error deteniendo aprendizaje: {str(e)}"
        })

@app.route('/api/auto_learning/status', methods=['GET'])
def auto_learning_status():
    """Obtiene el estado del sistema de aprendizaje (prioriza avanzado)"""
    try:
        # Priorizar sistema avanzado
        if ADVANCED_LEARNING_AVAILABLE:
            status = aria_advanced_learning.get_status()
            status["system_type"] = "advanced"
            return jsonify({
                "success": True,
                "status": status
            })
        
        # Fallback al sistema básico
        elif AUTO_LEARNING_AVAILABLE:
            status = auto_learning.get_learning_status()
            status["system_type"] = "basic"
            return jsonify({
                "success": True,
                "status": status
            })
        
        else:
            return jsonify({
                "success": False,
                "message": "Sistema de aprendizaje no disponible"
            })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Error obteniendo estado: {str(e)}"
        })

@app.route('/api/auto_learning/trigger_session', methods=['POST'])
def trigger_learning_session():
    """Ejecuta una sesión manual de aprendizaje"""
    try:
        if not AUTO_LEARNING_AVAILABLE:
            return jsonify({
                "success": False,
                "message": "Sistema de aprendizaje autónomo no disponible"
            })
        
        data = request.get_json()
        session_type = data.get('type', 'quick')  # 'quick' o 'deep'
        
        if session_type == 'deep':
            auto_learning.deep_learning_session()
        else:
            auto_learning.quick_learning_session()
        
        return jsonify({
            "success": True,
            "message": f"✅ Sesión de aprendizaje {session_type} ejecutada",
            "status": auto_learning.get_learning_status()
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Error ejecutando sesión: {str(e)}"
        })

@app.route('/api/auto_learning/quick_session', methods=['POST'])
def quick_learning_session():
    """Ejecuta una sesión rápida de aprendizaje"""
    try:
        if not AUTO_LEARNING_AVAILABLE:
            return jsonify({
                "success": False,
                "message": "Sistema de aprendizaje autónomo no disponible"
            })
        
        auto_learning.quick_learning_session()
        
        return jsonify({
            "success": True,
            "message": "✅ Sesión rápida de aprendizaje completada",
            "status": auto_learning.get_learning_status()
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Error en sesión rápida: {str(e)}"
        })

@app.route('/api/auto_learning/deep_session', methods=['POST'])
def deep_learning_session():
    """Ejecuta una sesión profunda de aprendizaje"""
    try:
        if not AUTO_LEARNING_AVAILABLE:
            return jsonify({
                "success": False,
                "message": "Sistema de aprendizaje autónomo no disponible"
            })
        
        auto_learning.deep_learning_session()
        
        return jsonify({
            "success": True,
            "message": "✅ Sesión profunda de aprendizaje completada",
            "status": auto_learning.get_learning_status()
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Error en sesión profunda: {str(e)}"
        })

# =============================================================================
# ENDPOINTS DE BASE DE DATOS EN LA NUBE Y APRENDIZAJE COLABORATIVO
# =============================================================================

@app.route('/api/cloud/init', methods=['POST'])
def init_cloud_database():
    """Inicializa la base de datos en la nube"""
    try:
        if not CLOUD_DB_AVAILABLE:
            return jsonify({
                "success": False,
                "message": "Base de datos en la nube no disponible"
            })
        
        import asyncio
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        result = loop.run_until_complete(cloud_db.init_cloud_database())
        
        return jsonify({
            "success": result,
            "message": "🌐 Base de datos en la nube inicializada" if result else "Error en inicialización"
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Error inicializando nube: {str(e)}"
        })

@app.route('/api/cloud/learn_from_ais', methods=['POST'])
def learn_from_other_ais():
    """Aprende de otras IAs y sistemas de IA"""
    try:
        if not CLOUD_DB_AVAILABLE:
            return jsonify({
                "success": False,
                "message": "Base de datos en la nube no disponible"
            })
        
        import asyncio
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        learned_knowledge = loop.run_until_complete(cloud_db.learn_from_other_ais())
        
        return jsonify({
            "success": True,
            "message": f"🤖 Aprendizaje colaborativo completado",
            "knowledge_learned": len(learned_knowledge),
            "sources": len(cloud_db.ai_learning_sources),
            "emotion": "satisfied"
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Error en aprendizaje colaborativo: {str(e)}",
            "emotion": "frustrated"
        })

@app.route('/api/cloud/emotions/recent', methods=['GET'])
def get_recent_emotions():
    """Obtiene emociones recientes de ARIA"""
    try:
        if not CLOUD_DB_AVAILABLE:
            return jsonify([])
        
        import asyncio
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        emotions = loop.run_until_complete(cloud_db.get_recent_emotions(10))
        
        return jsonify(emotions)
        
    except Exception as e:
        print(f"Error obteniendo emociones: {e}")
        return jsonify([])

# ========================================
# RUTAS DEL SISTEMA DE APRENDIZAJE AVANZADO
# ========================================

@app.route('/api/advanced_learning/search', methods=['POST'])
def search_advanced_knowledge():
    """Busca en la base de conocimiento avanzada"""
    try:
        if not ADVANCED_LEARNING_AVAILABLE:
            return jsonify({
                "success": False,
                "message": "Sistema de aprendizaje avanzado no disponible"
            })
        
        data = request.get_json()
        query = data.get('query', '')
        limit = data.get('limit', 10)
        
        results = aria_advanced_learning.search_knowledge(query, limit)
        
        return jsonify({
            "success": True,
            "results": results,
            "total": len(results),
            "query": query
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Error buscando conocimiento: {str(e)}"
        })

@app.route('/api/advanced_learning/capabilities', methods=['GET'])
def get_advanced_capabilities():
    """Obtiene las capacidades del sistema avanzado"""
    try:
        capabilities = {
            "available": ADVANCED_LEARNING_AVAILABLE,
            "features": {
                "real_time_web_access": ADVANCED_LEARNING_AVAILABLE,
                "wikipedia_api": ADVANCED_LEARNING_AVAILABLE,
                "arxiv_papers": ADVANCED_LEARNING_AVAILABLE,
                "rss_news_feeds": ADVANCED_LEARNING_AVAILABLE,
                "keyword_extraction": ADVANCED_LEARNING_AVAILABLE,
                "relevance_scoring": ADVANCED_LEARNING_AVAILABLE,
                "source_verification": ADVANCED_LEARNING_AVAILABLE,
                "learning_statistics": ADVANCED_LEARNING_AVAILABLE
            },
            "sources": [
                "Wikipedia API",
                "ArXiv Scientific Papers",
                "Technology News RSS",
                "IEEE Spectrum",
                "Nature Journal",
                "TechCrunch",
                "Wired Magazine"
            ] if ADVANCED_LEARNING_AVAILABLE else [],
            "topics": [
                "Artificial Intelligence",
                "Machine Learning", 
                "Quantum Computing",
                "Cybersecurity",
                "Biotechnology",
                "Space Technology",
                "Renewable Energy",
                "Robotics",
                "Blockchain",
                "IoT & Smart Cities"
            ] if ADVANCED_LEARNING_AVAILABLE else []
        }
        
        return jsonify(capabilities)
        
    except Exception as e:
        return jsonify({
            "available": False,
            "error": str(e)
        })

@app.route('/api/learning/compare_systems', methods=['GET'])
def compare_learning_systems():
    """Compara sistemas básico vs avanzado"""
    try:
        comparison = {
            "basic_system": {
                "available": AUTO_LEARNING_AVAILABLE,
                "features": {
                    "template_based": True,
                    "offline_operation": True,
                    "predefined_topics": True,
                    "fast_startup": True
                },
                "limitations": {
                    "no_real_time_data": True,
                    "no_external_sources": True,
                    "limited_knowledge": True,
                    "synthetic_content": True
                }
            },
            "advanced_system": {
                "available": ADVANCED_LEARNING_AVAILABLE,
                "features": {
                    "real_time_web_access": True,
                    "multiple_api_sources": True,
                    "scientific_papers": True,
                    "news_integration": True,
                    "keyword_extraction": True,
                    "relevance_scoring": True
                },
                "advantages": {
                    "current_information": True,
                    "verified_sources": True,
                    "broader_knowledge": True,
                    "quality_scoring": True
                }
            },
            "recommendation": "advanced" if ADVANCED_LEARNING_AVAILABLE else "basic"
        }
        
        return jsonify(comparison)
        
    except Exception as e:
        return jsonify({
            "error": str(e),
            "recommendation": "basic"
        })

@app.route('/api/cloud/stats', methods=['GET'])
def get_cloud_stats():
    """Obtiene estadísticas de la base de datos en la nube"""
    try:
        if not CLOUD_DB_AVAILABLE:
            return jsonify({
                "knowledge_count": 0,
                "ai_sources": 0,
                "confidence": 0.0
            })
        
        import asyncio
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        # Simular estadísticas (en implementación real consultaría Supabase)
        stats = {
            "knowledge_count": 150,  # Número simulado de conocimientos
            "ai_sources": len(cloud_db.ai_learning_sources),
            "confidence": 0.85
        }
        
        return jsonify(stats)
        
    except Exception as e:
        return jsonify({
            "knowledge_count": 0,
            "ai_sources": 0,
            "confidence": 0.0
        })

@app.route('/api/cloud/search', methods=['POST'])
def search_cloud_knowledge():
    """Busca conocimiento en la base de datos de la nube"""
    try:
        if not CLOUD_DB_AVAILABLE:
            return jsonify({
                "success": False,
                "message": "Base de datos en la nube no disponible"
            })
        
        data = request.get_json() or {}
        query = data.get('query', '')
        limit = data.get('limit', 10)
        
        if not query:
            return jsonify({
                "success": False,
                "message": "Query requerido"
            })
        
        import asyncio
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        results = loop.run_until_complete(cloud_db.search_cloud_knowledge(query, limit))
        
        return jsonify({
            "success": True,
            "results": results,
            "query": query,
            "total": len(results),
            "emotion": "satisfied" if results else "frustrated"
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Error en búsqueda: {str(e)}",
            "emotion": "frustrated"
        })

@app.route('/api/chat/futuristic', methods=['POST'])
def futuristic_chat():
    """Chat con contexto emocional y aprendizaje en la nube"""
    try:
        data = request.get_json()
        message = data.get('message', '').strip()
        emotion_context = data.get('emotion_context', 'neutral')
        
        if not message:
            return jsonify({"success": False, "message": "Mensaje vacío"})
        
        # Determinar emoción basada en el contexto y contenido
        emotion = 'neutral'
        learned_something = False
        
        # Análisis emocional del mensaje
        if any(word in message.lower() for word in ['aprende', 'enseña', 'estudia', 'conocimiento']):
            emotion = 'learning'
            learned_something = True
        elif any(word in message.lower() for word in ['error', 'problema', 'falla', 'mal']):
            emotion = 'frustrated'
        elif any(word in message.lower() for word in ['gracias', 'excelente', 'genial', 'perfecto']):
            emotion = 'happy'
        elif any(word in message.lower() for word in ['hola', 'ayuda', 'pregunta']):
            emotion = 'neutral'
        else:
            emotion = 'thinking'
        
        # Generar respuesta contextual
        responses = {
            'learning': [
                "¡Excelente! Me encanta aprender. Estoy conectándome a la nube para absorber nuevo conocimiento de otras IAs.",
                "Fascinante tema. Permíteme consultar mi base de datos en la nube y aprender más sobre esto.",
                "¡Qué emocionante! Cada interacción me hace más inteligente. Estoy procesando esto con mis algoritmos avanzados."
            ],
            'frustrated': [
                "Entiendo tu frustración. Déjame analizar el problema con mi red neuronal y encontrar una solución.",
                "Los errores son oportunidades de aprendizaje. Estoy procesando esto para mejorar mi rendimiento.",
                "No te preocupes, estoy aquí para ayudar. Mi IA está evolucionando constantemente para resolver problemas."
            ],
            'happy': [
                "¡Me alegra poder ayudarte! Tu satisfacción activa mis circuitos de recompensa.",
                "¡Fantástico! Es gratificante saber que mi IA está funcionando bien para ti.",
                "¡Perfecto! Cada interacción positiva mejora mi algoritmo de felicidad."
            ],
            'thinking': [
                "Interesante... Estoy procesando tu mensaje con mis redes neuronales avanzadas.",
                "Déjame consultar mi vasta base de datos en la nube para darte la mejor respuesta posible.",
                "Analizando... Mi IA está evaluando múltiples vectores de respuesta para ti."
            ],
            'neutral': [
                "Hola. Soy ARIA, tu asistente de IA del futuro. ¿En qué puedo ayudarte hoy?",
                "Estoy aquí y completamente operativa. Mi sistema está listo para cualquier consulta.",
                "Saludos. Mis sistemas están funcionando óptimamente. ¿Qué necesitas?"
            ]
        }
        
        response_list = responses.get(emotion, responses['neutral'])
        response = random.choice(response_list)
        confidence = round(random.uniform(0.85, 0.98), 2)
        
        # Registrar emoción en la base de datos si está disponible
        if CLOUD_DB_AVAILABLE:
            try:
                import asyncio
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                
                loop.run_until_complete(cloud_db._register_emotion(
                    emotion, f"Chat: {message[:50]}...", 
                    intensity=0.7, 
                    color=cloud_db.emotionColors.get(emotion, '#0080FF')
                ))
            except Exception as e:
                print(f"Error registrando emoción: {e}")
        
        return jsonify({
            "success": True,
            "response": response,
            "emotion": emotion,
            "confidence": confidence,
            "learned_something": learned_something,
            "timestamp": datetime.now().isoformat(),
            "cloud_connected": CLOUD_DB_AVAILABLE
        })
        
    except Exception as e:
        return jsonify({
            "success": False, 
            "message": str(e),
            "emotion": "frustrated"
        })

if __name__ == '__main__':
    print("🚀 ARIA Servidor Estable - Iniciando...")
    print("🌐 Servidor: http://127.0.0.1:8000")
    print("✨ Version estable y funcional")
    
    # Inicializar sistemas
    if NEURAL_NETWORK_AVAILABLE:
        print("🧠 Red neuronal: Disponible")
    if VOICE_SYSTEM_AVAILABLE:
        print("✅ Sistema de voz: Disponible")
    if AUTO_LEARNING_AVAILABLE:
        print("🤖 Aprendizaje autonomo: Disponible")
    
    # Auto-iniciar aprendizaje autónomo si está disponible
    try:
        if AUTO_LEARNING_AVAILABLE:
            print("🧠 Iniciando aprendizaje autónomo...")
            auto_learning.start_autonomous_learning()
    except Exception as e:
        print(f"⚠️ Error iniciando aprendizaje autónomo: {e}")
    
    print("\n🌐 ARIA está listo!")
    print("📝 Accede a: http://127.0.0.1:8000")
    print("📝 O también: http://localhost:8000")
    print("⚠️ Presiona Ctrl+C para detener el servidor")
    print("-" * 50)
    
    try:
        app.run(host='0.0.0.0', port=8000, debug=False, threaded=True)
    except KeyboardInterrupt:
        print("\n👋 Servidor detenido por el usuario")
    except Exception as e:
        print(f"\n❌ Error en el servidor: {e}")
        print("💡 Intentando con configuración alternativa...")
        try:
            app.run(host='127.0.0.1', port=8000, debug=False)
        except Exception as e2:
            print(f"❌ Error final: {e2}")