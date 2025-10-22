"""
🔧 DIAGNÓSTICO Y SOLUCIÓN DE PROBLEMAS DE CONEXIÓN
"""

import subprocess
import sys
import time
import requests
import threading
from pathlib import Path

class DiagnosticoConexion:
    def __init__(self):
        self.problemas = []
        self.soluciones = []
        
    def verificar_entorno_virtual(self):
        """Verifica si el entorno virtual está activo"""
        print("🔍 Verificando entorno virtual...")
        
        if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
            print("   ✅ Entorno virtual activado")
            return True
        else:
            print("   ❌ Entorno virtual NO activado")
            self.problemas.append("Entorno virtual no activado")
            self.soluciones.append("Ejecuta: .\\venv\\Scripts\\Activate.ps1")
            return False
    
    def verificar_dependencias(self):
        """Verifica que las dependencias estén instaladas"""
        print("🔍 Verificando dependencias...")
        
        dependencias = ['flask', 'whisper', 'pyttsx3', 'speech_recognition']
        dependencias_faltantes = []
        
        for dep in dependencias:
            try:
                __import__(dep)
                print(f"   ✅ {dep} instalado")
            except ImportError:
                print(f"   ❌ {dep} NO instalado")
                dependencias_faltantes.append(dep)
        
        if dependencias_faltantes:
            self.problemas.append(f"Dependencias faltantes: {', '.join(dependencias_faltantes)}")
            self.soluciones.append(f"Ejecuta: pip install {' '.join(dependencias_faltantes)}")
            return False
        return True
    
    def verificar_puertos(self):
        """Verifica si los puertos están disponibles"""
        print("🔍 Verificando puertos...")
        
        puertos = [5000, 5001]
        for puerto in puertos:
            try:
                import socket
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                resultado = sock.connect_ex(('127.0.0.1', puerto))
                sock.close()
                
                if resultado == 0:
                    print(f"   ⚠️  Puerto {puerto} ocupado")
                else:
                    print(f"   ✅ Puerto {puerto} disponible")
            except Exception as e:
                print(f"   ❌ Error verificando puerto {puerto}: {e}")
    
    def verificar_archivos(self):
        """Verifica que los archivos principales existan"""
        print("🔍 Verificando archivos principales...")
        
        archivos_requeridos = [
            'asistente_web.py',
            'web_app.py', 
            'templates/asistente.html',
            'templates/index.html'
        ]
        
        archivos_faltantes = []
        for archivo in archivos_requeridos:
            if Path(archivo).exists():
                print(f"   ✅ {archivo} existe")
            else:
                print(f"   ❌ {archivo} NO existe")
                archivos_faltantes.append(archivo)
        
        if archivos_faltantes:
            self.problemas.append(f"Archivos faltantes: {', '.join(archivos_faltantes)}")
            return False
        return True
    
    def iniciar_aplicacion_segura(self, archivo_app, puerto):
        """Inicia una aplicación con manejo de errores"""
        print(f"🚀 Iniciando {archivo_app} en puerto {puerto}...")
        
        try:
            # Verificar que el archivo existe
            if not Path(archivo_app).exists():
                print(f"   ❌ Archivo {archivo_app} no encontrado")
                return False
            
            # Iniciar la aplicación
            cmd = [sys.executable, archivo_app]
            proceso = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1,
                universal_newlines=True
            )
            
            # Esperar un poco para que la app inicie
            time.sleep(3)
            
            # Verificar si la aplicación está respondiendo
            try:
                response = requests.get(f'http://localhost:{puerto}', timeout=5)
                if response.status_code == 200:
                    print(f"   ✅ {archivo_app} iniciado correctamente")
                    print(f"   🌐 Accede a: http://localhost:{puerto}")
                    return proceso
                else:
                    print(f"   ❌ {archivo_app} no responde correctamente")
            except requests.RequestException as e:
                print(f"   ❌ Error conectando a la aplicación: {e}")
            
            # Si llegamos aquí, algo salió mal
            proceso.terminate()
            return False
            
        except Exception as e:
            print(f"   ❌ Error iniciando {archivo_app}: {e}")
            return False
    
    def crear_aplicacion_simple(self):
        """Crea una aplicación Flask simple para probar conexión"""
        print("🔧 Creando aplicación de prueba...")
        
        app_simple = """
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
"""
        
        with open('test_conexion.py', 'w', encoding='utf-8') as f:
            f.write(app_simple)
        
        print("   ✅ Aplicación de prueba creada: test_conexion.py")
        return True
    
    def generar_solucion_personalizada(self):
        """Genera una solución paso a paso"""
        print("\n🛠️ SOLUCIÓN PASO A PASO:")
        print("-" * 40)
        
        if self.problemas:
            print("❌ PROBLEMAS DETECTADOS:")
            for i, problema in enumerate(self.problemas, 1):
                print(f"   {i}. {problema}")
            
            print("\n✅ SOLUCIONES RECOMENDADAS:")
            for i, solucion in enumerate(self.soluciones, 1):
                print(f"   {i}. {solucion}")
        else:
            print("✅ No se detectaron problemas obvios")
        
        print("\n🔧 PASOS PARA RESOLVER:")
        print("1. Asegúrate de estar en el directorio correcto")
        print("2. Activa el entorno virtual: .\\venv\\Scripts\\Activate.ps1")
        print("3. Verifica dependencias: pip list")
        print("4. Prueba la aplicación simple: python test_conexion.py")
        print("5. Si funciona, prueba la app principal")
    
    def ejecutar_diagnostico_completo(self):
        """Ejecuta el diagnóstico completo"""
        print("🔍 DIAGNÓSTICO DE CONEXIÓN")
        print("=" * 50)
        
        # Verificaciones
        self.verificar_entorno_virtual()
        self.verificar_dependencias()
        self.verificar_puertos()
        self.verificar_archivos()
        
        # Crear app de prueba
        self.crear_aplicacion_simple()
        
        # Generar solución
        self.generar_solucion_personalizada()
        
        print("\n🎯 OPCIONES DISPONIBLES:")
        print("1. python test_conexion.py     # Probar conexión básica")
        print("2. python asistente_web.py     # Asistente completo")
        print("3. python web_app.py          # Solo transcripción")
        print("4. python menu_asistente.py    # Menú de opciones")

if __name__ == "__main__":
    diagnostico = DiagnosticoConexion()
    diagnostico.ejecutar_diagnostico_completo()