"""
🔍 ARIA SYSTEM DIAGNOSTIC - Verificador de Sistema
==================================================
Este script verifica que todos los componentes de ARIA estén funcionando correctamente
"""

import os
import sys
import subprocess
import requests
import json
import time
from pathlib import Path

def print_header(title):
    print(f"\n{'='*60}")
    print(f"🔍 {title}")
    print(f"{'='*60}")

def print_status(message, status="info"):
    symbols = {
        "success": "✅",
        "error": "❌", 
        "warning": "⚠️",
        "info": "ℹ️"
    }
    print(f"{symbols.get(status, 'ℹ️')} {message}")

def check_python():
    """Verificar instalación de Python"""
    print_header("VERIFICACIÓN DE PYTHON")
    
    try:
        version = sys.version.split()[0]
        print_status(f"Python {version} encontrado", "success")
        
        # Verificar versión mínima
        major, minor = map(int, version.split('.')[:2])
        if major >= 3 and minor >= 7:
            print_status("Versión de Python compatible", "success")
        else:
            print_status("Se recomienda Python 3.7 o superior", "warning")
            
        return True
    except Exception as e:
        print_status(f"Error verificando Python: {e}", "error")
        return False

def check_dependencies():
    """Verificar dependencias de Python"""
    print_header("VERIFICACIÓN DE DEPENDENCIAS")
    
    required_packages = [
        "flask", "flask_cors", "requests", "aiohttp", 
        "asyncio", "python-dotenv", "datetime"
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace("-", "_"))
            print_status(f"{package} ✓", "success")
        except ImportError:
            print_status(f"{package} ✗", "error")
            missing_packages.append(package)
    
    if missing_packages:
        print_status(f"Paquetes faltantes: {', '.join(missing_packages)}", "warning")
        print_status("Ejecuta: pip install " + " ".join(missing_packages), "info")
        return False
    else:
        print_status("Todas las dependencias están instaladas", "success")
        return True

def check_files():
    """Verificar archivos necesarios"""
    print_header("VERIFICACIÓN DE ARCHIVOS")
    
    project_dir = Path(__file__).parent
    
    critical_files = [
        "backend/src/main_stable.py",
        "backend/src/cloud_database.py",
        "backend/requirements.txt",
        "frontend/src/components/FuturisticAriaInterface.jsx",
        ".env.example"
    ]
    
    optional_files = [
        ".env",
        "frontend/package.json",
        "venv/Scripts/activate.bat"
    ]
    
    print_status("Archivos críticos:", "info")
    all_critical_present = True
    
    for file_path in critical_files:
        full_path = project_dir / file_path
        if full_path.exists():
            print_status(f"  {file_path} ✓", "success")
        else:
            print_status(f"  {file_path} ✗", "error")
            all_critical_present = False
    
    print_status("\nArchivos opcionales:", "info")
    for file_path in optional_files:
        full_path = project_dir / file_path
        if full_path.exists():
            print_status(f"  {file_path} ✓", "success")
        else:
            print_status(f"  {file_path} ✗ (opcional)", "warning")
    
    return all_critical_present

def check_directories():
    """Verificar directorios necesarios"""
    print_header("VERIFICACIÓN DE DIRECTORIOS")
    
    project_dir = Path(__file__).parent
    
    required_dirs = [
        "backend",
        "backend/src", 
        "backend/data",
        "frontend",
        "frontend/src",
        "data",
        "data/logs"
    ]
    
    for dir_path in required_dirs:
        full_path = project_dir / dir_path
        if full_path.exists():
            print_status(f"{dir_path} ✓", "success")
        else:
            print_status(f"{dir_path} ✗ - Creando...", "warning")
            try:
                full_path.mkdir(parents=True, exist_ok=True)
                print_status(f"  {dir_path} creado", "success")
            except Exception as e:
                print_status(f"  Error creando {dir_path}: {e}", "error")
                return False
    
    return True

def check_ports():
    """Verificar puertos disponibles"""
    print_header("VERIFICACIÓN DE PUERTOS")
    
    import socket
    
    ports = [8000, 3000]
    
    for port in ports:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            result = sock.connect_ex(('127.0.0.1', port))
            if result == 0:
                print_status(f"Puerto {port} está en uso", "warning")
            else:
                print_status(f"Puerto {port} disponible", "success")
        except Exception as e:
            print_status(f"Error verificando puerto {port}: {e}", "error")
        finally:
            sock.close()
    
    return True

def test_server_startup():
    """Probar inicio del servidor"""
    print_header("PRUEBA DE INICIO DEL SERVIDOR")
    
    project_dir = Path(__file__).parent
    backend_dir = project_dir / "backend" / "src"
    main_file = backend_dir / "main_stable.py"
    
    if not main_file.exists():
        print_status("main_stable.py no encontrado", "error")
        return False
    
    print_status("Intentando iniciar servidor en modo prueba...", "info")
    
    try:
        # Cambiar al directorio del backend
        os.chdir(backend_dir)
        
        # Iniciar servidor en subprocess
        proc = subprocess.Popen(
            [sys.executable, "main_stable.py"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Esperar un poco para que inicie
        time.sleep(5)
        
        # Verificar si está corriendo
        if proc.poll() is None:
            print_status("Servidor iniciado exitosamente", "success")
            
            # Probar conexión
            try:
                response = requests.get("http://127.0.0.1:8000/api/status", timeout=5)
                if response.status_code == 200:
                    print_status("API responde correctamente", "success")
                    data = response.json()
                    print_status(f"Estado: {data.get('status', 'N/A')}", "info")
                else:
                    print_status(f"API responde con código {response.status_code}", "warning")
            except requests.exceptions.RequestException as e:
                print_status(f"Error conectando a API: {e}", "warning")
            
            # Terminar el proceso
            proc.terminate()
            time.sleep(2)
            if proc.poll() is None:
                proc.kill()
            
            return True
        else:
            # El proceso terminó, obtener error
            stdout, stderr = proc.communicate()
            print_status("Error iniciando servidor:", "error")
            if stderr:
                print_status(f"  {stderr.strip()}", "error")
            return False
            
    except Exception as e:
        print_status(f"Error en prueba de servidor: {e}", "error")
        return False

def check_configuration():
    """Verificar configuración"""
    print_header("VERIFICACIÓN DE CONFIGURACIÓN")
    
    project_dir = Path(__file__).parent
    env_file = project_dir / ".env"
    env_example = project_dir / ".env.example"
    
    if env_file.exists():
        print_status("Archivo .env encontrado", "success")
        # Leer y verificar variables básicas
        try:
            with open(env_file, 'r') as f:
                content = f.read()
                if "SUPABASE_URL" in content:
                    print_status("Configuración de base de datos encontrada", "success")
                else:
                    print_status("Configuración de base de datos no encontrada", "warning")
        except Exception as e:
            print_status(f"Error leyendo .env: {e}", "warning")
    else:
        print_status("Archivo .env no encontrado", "warning")
        if env_example.exists():
            print_status("Usa .env.example como plantilla", "info")
        
    return True

def generate_report():
    """Generar reporte de diagnóstico"""
    print_header("REPORTE DE DIAGNÓSTICO")
    
    results = {
        "Python": check_python(),
        "Dependencias": check_dependencies(), 
        "Archivos": check_files(),
        "Directorios": check_directories(),
        "Puertos": check_ports(),
        "Configuración": check_configuration(),
        "Servidor": test_server_startup()
    }
    
    print_status("RESUMEN:", "info")
    total_checks = len(results)
    passed_checks = sum(results.values())
    
    for check, result in results.items():
        status = "success" if result else "error"
        print_status(f"{check}: {'✓' if result else '✗'}", status)
    
    print_status(f"\nPruebas exitosas: {passed_checks}/{total_checks}", "info")
    
    if passed_checks == total_checks:
        print_status("🎉 ¡Sistema completamente funcional!", "success")
        print_status("Puedes ejecutar start_all_servers.bat", "info")
    elif passed_checks >= total_checks - 2:
        print_status("⚠️ Sistema mayormente funcional", "warning")
        print_status("Algunas características opcionales no están disponibles", "info")
    else:
        print_status("❌ Sistema requiere configuración adicional", "error")
        print_status("Revisa los errores anteriores", "info")
    
    return passed_checks == total_checks

def main():
    """Función principal"""
    print("🔍 ARIA SYSTEM DIAGNOSTIC")
    print("=" * 60)
    print("🤖 Verificando todos los componentes del sistema ARIA")
    print("=" * 60)
    
    try:
        success = generate_report()
        
        print_header("PRÓXIMOS PASOS")
        
        if success:
            print_status("1. Ejecuta start_all_servers.bat para iniciar ARIA", "info")
            print_status("2. Abre http://127.0.0.1:8000 en tu navegador", "info")
            print_status("3. ¡Disfruta tu asistente futurista!", "success")
        else:
            print_status("1. Instala las dependencias faltantes", "info")
            print_status("2. Ejecuta este diagnóstico nuevamente", "info")
            print_status("3. Consulta la documentación si persisten errores", "info")
        
    except KeyboardInterrupt:
        print_status("\nDiagnóstico interrumpido por el usuario", "warning")
    except Exception as e:
        print_status(f"Error durante el diagnóstico: {e}", "error")
    
    print("\n" + "=" * 60)
    print("🔍 Diagnóstico completado")
    input("Presiona Enter para salir...")

if __name__ == "__main__":
    main()