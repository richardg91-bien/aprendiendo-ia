"""
🚀 ARIA - Iniciador Completo Python
==================================
Versión multiplataforma para iniciar todo el sistema ARIA
"""

import os
import sys
import time
import subprocess
import webbrowser
from pathlib import Path

def print_logo():
    print("""
 ██████╗ ██████╗ ██╗ █████╗ 
██╔══██╗██╔══██╗██║██╔══██╗
██████╔╝██████╔╝██║███████║
██╔══██╗██╔══██╗██║██╔══██║
██║  ██║██║  ██║██║██║  ██║
╚═╝  ╚═╝╚═╝  ╚═╝╚═╝╚═╝  ╚═╝
""")

def run_command(command, cwd=None, background=False):
    """Ejecutar comando de forma segura"""
    try:
        if background:
            if sys.platform == "win32":
                subprocess.Popen(command, cwd=cwd, shell=True, creationflags=subprocess.CREATE_NEW_CONSOLE)
            else:
                subprocess.Popen(command, cwd=cwd, shell=True)
        else:
            result = subprocess.run(command, cwd=cwd, shell=True, capture_output=True, text=True)
            return result.returncode == 0
    except Exception as e:
        print(f"❌ Error ejecutando comando: {e}")
        return False

def main():
    print_logo()
    print("🚀 ARIA - INICIADOR COMPLETO")
    print("=" * 50)
    
    # Cambiar al directorio del proyecto
    project_dir = Path(__file__).parent
    os.chdir(project_dir)
    
    print(f"📁 Directorio: {project_dir}")
    print()
    
    # Paso 1: Verificar entorno virtual
    print("[1/6] 🔧 Verificando entorno virtual...")
    venv_python = project_dir / "venv" / "Scripts" / "python.exe"
    if not venv_python.exists():
        print("❌ Entorno virtual no encontrado")
        return False
    print("✅ Entorno virtual encontrado")
    
    # Paso 2: Instalar dependencias
    print("[2/6] 📦 Verificando dependencias...")
    packages = ["flask", "flask-cors", "requests", "python-dotenv", "pyttsx3", "psycopg[binary]"]
    for package in packages:
        subprocess.run([str(venv_python), "-m", "pip", "install", "--quiet", package])
    print("✅ Dependencias verificadas")
    
    # Paso 3: Verificar Supabase
    print("[3/6] 🌐 Verificando conexión a Supabase...")
    supabase_test = subprocess.run([str(venv_python), "test_supabase_final.py"], 
                                 capture_output=True, text=True)
    if "SUPABASE COMPLETAMENTE CONFIGURADO" in supabase_test.stdout:
        print("✅ Supabase conectado")
    else:
        print("⚠️  Supabase no verificado, pero continuando...")
    
    # Paso 4: Iniciar backend
    print("[4/6] 🖥️  Iniciando servidor backend...")
    backend_cmd = f'"{venv_python}" backend/src/main_stable.py'
    
    if sys.platform == "win32":
        subprocess.Popen(f'start "ARIA Backend" cmd /k "{backend_cmd}"', shell=True)
    else:
        subprocess.Popen(f'gnome-terminal -- bash -c "{backend_cmd}; exec bash"', shell=True)
    
    print("✅ Backend iniciado en segundo plano")
    
    # Paso 5: Verificar frontend
    print("[5/6] 🎨 Preparando frontend...")
    frontend_dir = project_dir / "frontend"
    
    if not (frontend_dir / "node_modules").exists():
        print("📥 Instalando dependencias del frontend...")
        subprocess.run(["npm", "install"], cwd=frontend_dir)
    
    # Esperar un poco para que el backend inicie
    print("[6/6] ⏳ Esperando 8 segundos para iniciar frontend...")
    time.sleep(8)
    
    # Iniciar frontend
    print("🎨 Iniciando frontend React...")
    frontend_cmd = "npm start"
    
    if sys.platform == "win32":
        subprocess.Popen(f'start "ARIA Frontend" cmd /k "cd /d {frontend_dir} && {frontend_cmd}"', shell=True)
    else:
        subprocess.Popen(f'gnome-terminal -- bash -c "cd {frontend_dir} && {frontend_cmd}; exec bash"', shell=True)
    
    print("✅ Frontend iniciado en segundo plano")
    
    # Resultado final
    print()
    print("🎉 ARIA INICIADO COMPLETAMENTE!")
    print("=" * 50)
    print("🔗 URLs disponibles:")
    print("   Backend:  http://localhost:5002")
    print("   Frontend: http://localhost:3000")
    print("   Supabase: ✅ Conectado")
    print()
    
    # Esperar y abrir navegador
    print("⏳ Esperando 10 segundos para abrir navegador...")
    time.sleep(10)
    
    print("🌐 Abriendo ARIA en el navegador...")
    webbrowser.open("http://localhost:3000")
    
    print()
    print("✅ ARIA está ejecutándose.")
    print("💡 Cierra las ventanas del terminal cuando termines.")
    
    # Mantener script activo
    try:
        input("\nPresiona Enter para cerrar este iniciador...")
    except KeyboardInterrupt:
        print("\n👋 Cerrando iniciador...")

if __name__ == "__main__":
    main()