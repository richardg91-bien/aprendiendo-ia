"""
Script de inicio simple y robusto para ARIA
Maneja errores y reinicia automáticamente si es necesario
"""

import os
import sys
import time
import subprocess
from pathlib import Path

def check_server_status():
    """Verificar si el servidor está respondiendo"""
    try:
        import requests
        response = requests.get("http://127.0.0.1:8000/api/status", timeout=3)
        return response.status_code == 200
    except:
        return False

def start_server():
    """Iniciar servidor con manejo de errores"""
    print("🚀 Iniciando ARIA...")
    
    # Cambiar al directorio del proyecto
    project_dir = Path(__file__).parent.parent
    os.chdir(project_dir)
    
    # Activar entorno virtual y ejecutar servidor
    if sys.platform == "win32":
        activate_script = project_dir / "venv" / "Scripts" / "activate.bat"
        python_exe = project_dir / "venv" / "Scripts" / "python.exe"
    else:
        activate_script = project_dir / "venv" / "bin" / "activate"
        python_exe = project_dir / "venv" / "bin" / "python"
    
    # Verificar que el entorno virtual existe
    if not python_exe.exists():
        print("❌ Error: Entorno virtual no encontrado")
        print(f"   Buscando: {python_exe}")
        return False
    
    # Ejecutar servidor
    try:
        cmd = [str(python_exe), "backend/src/main.py"]
        print(f"📝 Ejecutando: {' '.join(cmd)}")
        
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
            universal_newlines=True
        )
        
        print("⏳ Esperando que el servidor inicie...")
        
        # Esperar y mostrar output
        for i in range(30):  # Esperar máximo 30 segundos
            if process.poll() is not None:
                print("❌ El servidor se cerró inesperadamente")
                output, _ = process.communicate()
                print("📋 Output:")
                print(output)
                return False
            
            if check_server_status():
                print("✅ ¡Servidor iniciado exitosamente!")
                print("🌐 Abre tu navegador en: http://127.0.0.1:8000")
                return True
            
            time.sleep(1)
            print(f"   Intentando conectar... {i+1}/30")
        
        print("❌ Timeout: El servidor no respondió en 30 segundos")
        process.terminate()
        return False
        
    except Exception as e:
        print(f"❌ Error iniciando servidor: {e}")
        return False

def main():
    """Función principal"""
    print("=" * 50)
    print("🤖 ARIA - Iniciador Robusto")
    print("=" * 50)
    
    # Verificar si ya hay un servidor ejecutándose
    if check_server_status():
        print("✅ Servidor ya está ejecutándose")
        print("🌐 Abre tu navegador en: http://127.0.0.1:8000")
        return
    
    # Intentar iniciar servidor
    success = start_server()
    
    if success:
        print("\n🎉 ARIA está listo!")
        print("💡 Consejos:")
        print("   • Pregunta: '¿Qué significa inteligencia?'")
        print("   • Conversa naturalmente")
        print("   • Usa el chat para probar las mejoras")
        
        # Mantener vivo
        try:
            while True:
                if not check_server_status():
                    print("\n⚠️  Servidor desconectado, intentando reiniciar...")
                    start_server()
                time.sleep(10)
        except KeyboardInterrupt:
            print("\n👋 Cerrando ARIA...")
    else:
        print("\n❌ No se pudo iniciar ARIA")
        print("🔧 Soluciones:")
        print("   1. Verificar que el entorno virtual esté creado")
        print("   2. Ejecutar: pip install -r backend/requirements.txt")
        print("   3. Revisar logs para errores específicos")

if __name__ == "__main__":
    main()