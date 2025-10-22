"""
🚀 ARIA - Inicio Automático con Sistema Avanzado
===============================================

Script mejorado que inicia ARIA con capacidades avanzadas de aprendizaje
"""

import os
import sys
import time
import subprocess
import threading
import requests
from pathlib import Path

def print_banner():
    """Muestra el banner de inicio"""
    print("\n" + "="*80)
    print("🚀 ARIA - SISTEMA DE APRENDIZAJE AUTÓNOMO AVANZADO")
    print("="*80)
    print("✨ NUEVAS CAPACIDADES:")
    print("   🌐 Acceso a internet en tiempo real")
    print("   📚 Fuentes científicas (ArXiv, Nature, IEEE)")
    print("   📰 Noticias tecnológicas en tiempo real")
    print("   🔍 Análisis inteligente de contenido")
    print("   📊 Estadísticas de aprendizaje")
    print("   🎯 Conocimiento verificado y puntuado")
    print("="*80)

def check_dependencies():
    """Verifica dependencias del sistema avanzado"""
    print("\n🔍 Verificando dependencias del sistema avanzado...")
    
    required_packages = [
        'feedparser',
        'beautifulsoup4',
        'lxml',
        'requests'
    ]
    
    missing = []
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
            print(f"   ✅ {package}")
        except ImportError:
            print(f"   ❌ {package} - FALTANTE")
            missing.append(package)
    
    if missing:
        print(f"\n⚠️ Dependencias faltantes: {', '.join(missing)}")
        print("💡 Instalando automáticamente...")
        
        try:
            subprocess.run([
                sys.executable, '-m', 'pip', 'install'
            ] + missing, check=True, capture_output=True)
            print("✅ Dependencias instaladas correctamente")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Error instalando dependencias: {e}")
            return False
    else:
        print("✅ Todas las dependencias están disponibles")
        return True

def start_backend():
    """Inicia el backend de ARIA"""
    print("\n🔧 Iniciando backend de ARIA...")
    
    backend_path = Path(__file__).parent / "backend"
    os.chdir(backend_path)
    
    # Comando para iniciar el backend
    cmd = [sys.executable, "src/main_stable.py"]
    
    try:
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            cwd=backend_path
        )
        
        print("✅ Backend iniciado correctamente")
        return process
        
    except Exception as e:
        print(f"❌ Error iniciando backend: {e}")
        return None

def start_frontend():
    """Inicia el frontend de ARIA"""
    print("\n🎨 Iniciando frontend de ARIA...")
    
    frontend_path = Path(__file__).parent / "frontend"
    
    try:
        process = subprocess.Popen(
            ["npm", "start"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            cwd=frontend_path,
            shell=True
        )
        
        print("✅ Frontend iniciado correctamente")
        return process
        
    except Exception as e:
        print(f"❌ Error iniciando frontend: {e}")
        return None

def wait_for_backend():
    """Espera a que el backend esté disponible"""
    print("\n⏳ Esperando a que el backend esté disponible...")
    
    max_attempts = 30
    for attempt in range(max_attempts):
        try:
            response = requests.get("http://localhost:8000/api/status", timeout=2)
            if response.status_code == 200:
                print("✅ Backend disponible")
                return True
        except:
            pass
        
        print(f"   🔄 Intento {attempt + 1}/{max_attempts}")
        time.sleep(2)
    
    print("❌ Backend no disponible después de 60 segundos")
    return False

def activate_advanced_learning():
    """Activa el sistema de aprendizaje avanzado"""
    print("\n🧠 Activando sistema de aprendizaje avanzado...")
    
    try:
        # Verificar capacidades
        response = requests.get("http://localhost:8000/api/advanced_learning/capabilities")
        
        if response.status_code == 200:
            capabilities = response.json()
            
            if capabilities.get("available"):
                print("✅ Sistema avanzado disponible")
                
                # Mostrar capacidades
                features = capabilities.get("features", {})
                available_features = [k for k, v in features.items() if v]
                print(f"   🔹 Características activas: {len(available_features)}")
                
                sources = capabilities.get("sources", [])
                print(f"   🔹 Fuentes de conocimiento: {len(sources)}")
                
                # Iniciar aprendizaje
                start_response = requests.post("http://localhost:8000/api/auto_learning/start")
                
                if start_response.status_code == 200:
                    result = start_response.json()
                    
                    if result.get("success"):
                        system_type = result.get("system", "unknown")
                        print(f"✅ Sistema {system_type} iniciado correctamente")
                        
                        if system_type == "advanced":
                            print("🚀 ¡SISTEMA AVANZADO ACTIVO!")
                            print("   ✨ Superando limitaciones anteriores:")
                            print("   ❌ ¡YA NO es simulado!")
                            print("   ✅ Acceso a internet en tiempo real")
                            print("   ✅ Lee fuentes externas verificadas")
                            print("   ✅ APIs científicas y noticias")
                            print("   ✅ Conocimiento real y actualizado")
                        
                        return True
                    else:
                        print(f"❌ Error iniciando: {result.get('message')}")
                        return False
                else:
                    print(f"❌ Error HTTP {start_response.status_code}")
                    return False
            else:
                print("⚠️ Sistema avanzado no disponible - usando sistema básico")
                return False
        else:
            print(f"❌ Error verificando capacidades: HTTP {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error activando sistema avanzado: {e}")
        return False

def open_browser():
    """Abre el navegador automáticamente"""
    print("\n🌐 Abriendo navegador...")
    
    try:
        import webbrowser
        webbrowser.open("http://localhost:3001")
        print("✅ Navegador abierto en http://localhost:3001")
        return True
    except Exception as e:
        print(f"❌ Error abriendo navegador: {e}")
        print("💡 Abre manualmente: http://localhost:3001")
        return False

def monitor_system():
    """Monitorea el estado del sistema"""
    print("\n📊 Iniciando monitoreo del sistema...")
    
    def monitor_loop():
        while True:
            try:
                time.sleep(30)  # Verificar cada 30 segundos
                
                # Verificar estado del aprendizaje
                response = requests.get("http://localhost:8000/api/auto_learning/status", timeout=5)
                
                if response.status_code == 200:
                    data = response.json()
                    
                    if data.get("success"):
                        status = data.get("status", {})
                        knowledge_count = status.get("total_knowledge", 0)
                        system_type = status.get("system_type", "unknown")
                        
                        print(f"📈 Sistema {system_type}: {knowledge_count} elementos de conocimiento")
                        
                        # Mostrar estadísticas si están disponibles
                        if "statistics" in status:
                            stats = status["statistics"]
                            sources = stats.get("sources_accessed", 0)
                            articles = stats.get("articles_processed", 0)
                            success = stats.get("successful_extractions", 0)
                            
                            if sources > 0:
                                print(f"   📊 Fuentes: {sources}, Artículos: {articles}, Éxitos: {success}")
                
            except Exception as e:
                print(f"⚠️ Error en monitoreo: {e}")
                time.sleep(60)  # Esperar más tiempo en caso de error
    
    # Iniciar monitoreo en hilo separado
    monitor_thread = threading.Thread(target=monitor_loop, daemon=True)
    monitor_thread.start()

def main():
    """Función principal"""
    print_banner()
    
    # Verificar dependencias
    if not check_dependencies():
        print("❌ No se pudieron instalar las dependencias necesarias")
        return False
    
    # Iniciar servicios
    backend_process = start_backend()
    if not backend_process:
        return False
    
    # Esperar a que el backend esté listo
    if not wait_for_backend():
        backend_process.terminate()
        return False
    
    # Activar sistema avanzado
    advanced_active = activate_advanced_learning()
    
    # Iniciar frontend
    frontend_process = start_frontend()
    if not frontend_process:
        backend_process.terminate()
        return False
    
    # Esperar a que el frontend esté listo
    print("\n⏳ Esperando a que el frontend esté listo...")
    time.sleep(10)
    
    # Abrir navegador
    open_browser()
    
    # Iniciar monitoreo
    monitor_system()
    
    # Mensaje final
    print("\n" + "="*80)
    print("🎉 ¡ARIA INICIADO CORRECTAMENTE!")
    print("="*80)
    
    if advanced_active:
        print("🚀 SISTEMA AVANZADO ACTIVO - Limitaciones superadas:")
        print("   ✅ Acceso a internet en tiempo real")
        print("   ✅ Fuentes científicas y noticias")
        print("   ✅ Conocimiento real y verificado")
    else:
        print("🔧 Sistema básico activo (sistema avanzado no disponible)")
    
    print("\n🌐 Interfaz web: http://localhost:3001")
    print("🔧 API backend: http://localhost:8000")
    print("\n💡 Presiona Ctrl+C para detener ARIA")
    print("="*80)
    
    try:
        # Mantener el script corriendo
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n\n🛑 Deteniendo ARIA...")
        
        # Detener procesos
        if frontend_process:
            frontend_process.terminate()
            print("✅ Frontend detenido")
        
        if backend_process:
            backend_process.terminate()
            print("✅ Backend detenido")
        
        print("👋 ¡Hasta luego!")
        return True

if __name__ == "__main__":
    success = main()
    
    if not success:
        print("\n❌ Error durante el inicio de ARIA")
        input("Presiona Enter para salir...")
    
    sys.exit(0 if success else 1)