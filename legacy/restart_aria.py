#!/usr/bin/env python3
"""
ARIA - Script de Reinicio Completo
Automatiza el proceso completo de inicio del sistema ARIA
"""

import os
import sys
import subprocess
import time
import signal
import psutil
from pathlib import Path

def kill_processes_by_name(process_names):
    """Elimina procesos por nombre"""
    killed = []
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            if proc.info['name'].lower() in [name.lower() for name in process_names]:
                proc.kill()
                killed.append(f"{proc.info['name']} (PID: {proc.info['pid']})")
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    return killed

def kill_processes_by_port(ports):
    """Elimina procesos que usan puertos específicos"""
    killed = []
    for conn in psutil.net_connections():
        if conn.laddr.port in ports and conn.pid:
            try:
                proc = psutil.Process(conn.pid)
                proc.kill()
                killed.append(f"{proc.name()} en puerto {conn.laddr.port} (PID: {conn.pid})")
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
    return killed

def check_dependencies():
    """Verifica dependencias necesarias"""
    print("🔍 Verificando dependencias...")
    
    # Verificar estructura de directorios
    required_dirs = ["backend", "backend/src"]
    for dir_path in required_dirs:
        if not Path(dir_path).exists():
            print(f"❌ Error: Directorio {dir_path} no encontrado")
            return False
    
    # Verificar archivo principal
    if not Path("backend/src/main.py").exists():
        print("❌ Error: backend/src/main.py no encontrado")
        return False
    
    return True

def build_frontend():
    """Construye el frontend si existe"""
    if not Path("frontend").exists():
        print("ℹ️  Frontend no encontrado, omitiendo construcción")
        return True
    
    print("🏗️  Construyendo frontend...")
    frontend_dir = Path("frontend")
    
    if not (frontend_dir / "package.json").exists():
        print("⚠️  package.json no encontrado en frontend")
        return True
    
    try:
        os.chdir("frontend")
        result = subprocess.run(["npm", "run", "build"], 
                              capture_output=True, text=True, timeout=120)
        os.chdir("..")
        
        if result.returncode == 0:
            print("✅ Frontend construido exitosamente")
            return True
        else:
            print(f"⚠️  Error al construir frontend: {result.stderr}")
            return True  # No bloqueante
    except subprocess.TimeoutExpired:
        print("⚠️  Timeout al construir frontend")
        os.chdir("..")
        return True
    except Exception as e:
        print(f"⚠️  Error inesperado al construir frontend: {e}")
        os.chdir("..")
        return True

def start_server():
    """Inicia el servidor ARIA"""
    print("🚀 Iniciando servidor ARIA...")
    
    # Cambiar al directorio backend
    os.chdir("backend")
    
    # Ejecutar el servidor
    try:
        subprocess.run([sys.executable, "src/main.py"])
    except KeyboardInterrupt:
        print("\n👋 Servidor detenido por el usuario")
    except Exception as e:
        print(f"❌ Error al ejecutar servidor: {e}")
        return False
    
    return True

def main():
    """Función principal de reinicio"""
    print("╔══════════════════════════════════════════════════════════╗")
    print("║              🔄 REINICIO COMPLETO DE ARIA               ║")
    print("║              Sistema de Inteligencia Artificial         ║")
    print("╚══════════════════════════════════════════════════════════╝")
    print()
    
    # Verificar directorio correcto
    if not check_dependencies():
        print("💡 Asegúrate de ejecutar desde el directorio raíz de ARIA")
        return 1
    
    # Detener procesos anteriores
    print("🛑 Deteniendo procesos anteriores...")
    
    # Eliminar procesos Python y Node
    killed_by_name = kill_processes_by_name(['python.exe', 'python', 'node.exe', 'node'])
    if killed_by_name:
        print(f"✅ Procesos eliminados: {', '.join(killed_by_name)}")
    
    # Eliminar procesos en puertos específicos
    killed_by_port = kill_processes_by_port([8000, 5000, 3000])
    if killed_by_port:
        print(f"✅ Procesos en puertos eliminados: {', '.join(killed_by_port)}")
    
    if not killed_by_name and not killed_by_port:
        print("✅ No había procesos anteriores ejecutándose")
    
    # Esperar un momento para que los procesos terminen
    time.sleep(2)
    
    # Construir frontend
    if not build_frontend():
        print("⚠️  Problema con el frontend, pero continuando...")
    
    print()
    print("📡 Servidor disponible en: http://localhost:8000")
    print("🌐 Interfaz web en: http://localhost:8000")
    print("🔗 API disponible en: http://localhost:8000/api/")
    print()
    print("⚠️  Presiona Ctrl+C para detener el servidor")
    print()
    
    # Iniciar servidor
    success = start_server()
    
    print()
    print("👋 Proceso de reinicio completado")
    print("🔄 Para reiniciar, ejecuta este script nuevamente")
    
    return 0 if success else 1

if __name__ == "__main__":
    try:
        exit_code = main()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n👋 Reinicio cancelado por el usuario")
        sys.exit(0)