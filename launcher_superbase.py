#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🚀 ARIA Super Base - Launcher Completo
=====================================

Launcher que inicializa y coordina todos los componentes de ARIA
con integración completa de Super Base (Supabase).

Características:
✅ Configuración automática de Super Base
✅ Verificación de dependencias
✅ Servidor backend con base de datos
✅ Frontend React moderno
✅ Gestión de procesos coordinada
✅ Monitoreo en tiempo real

Autor: ARIA Development Team
Fecha: 22 de octubre de 2025
"""

import os
import sys
import subprocess
import time
import json
import signal
import threading
from datetime import datetime
from typing import Dict, List, Optional
import webbrowser

class ARIASuperBaseLauncher:
    """Launcher completo para ARIA con Super Base"""
    
    def __init__(self):
        self.project_root = os.path.dirname(__file__)
        self.backend_process = None
        self.frontend_process = None
        self.processes = []
        self.running = False
        
        # Configuración
        self.config = {
            'backend_port': 8000,
            'frontend_port': 3000,
            'auto_open_browser': True,
            'enable_superbase': True,
            'enable_monitoring': True
        }
        
        print("🚀 ARIA Super Base Launcher inicializado")
    
    def check_dependencies(self) -> Dict[str, bool]:
        """Verificar dependencias del sistema"""
        print("🔍 Verificando dependencias...")
        
        deps = {
            'python': False,
            'node': False,
            'npm': False,
            'pip': False,
            'supabase': False,
            'react': False
        }
        
        try:
            # Verificar Python
            result = subprocess.run(['python', '--version'], capture_output=True, text=True)
            if result.returncode == 0:
                deps['python'] = True
                print(f"✅ Python: {result.stdout.strip()}")
            
            # Verificar pip
            result = subprocess.run(['pip', '--version'], capture_output=True, text=True)
            if result.returncode == 0:
                deps['pip'] = True
                print(f"✅ pip: {result.stdout.strip().split()[1]}")
            
            # Verificar Node.js
            result = subprocess.run(['node', '--version'], capture_output=True, text=True)
            if result.returncode == 0:
                deps['node'] = True
                print(f"✅ Node.js: {result.stdout.strip()}")
            
            # Verificar npm
            result = subprocess.run(['npm', '--version'], capture_output=True, text=True)
            if result.returncode == 0:
                deps['npm'] = True
                print(f"✅ npm: {result.stdout.strip()}")
            
            # Verificar Supabase
            try:
                import supabase
                deps['supabase'] = True
                print("✅ Supabase Python client instalado")
            except ImportError:
                print("❌ Supabase Python client no encontrado")
            
            # Verificar React (en frontend)
            frontend_path = os.path.join(self.project_root, 'frontend', 'package.json')
            if os.path.exists(frontend_path):
                deps['react'] = True
                print("✅ Frontend React encontrado")
            else:
                print("❌ Frontend React no encontrado")
                
        except Exception as e:
            print(f"⚠️ Error verificando dependencias: {e}")
        
        return deps
    
    def install_missing_dependencies(self, deps: Dict[str, bool]):
        """Instalar dependencias faltantes"""
        print("\n📦 Instalando dependencias faltantes...")
        
        # Instalar dependencias Python
        python_packages = []
        if not deps['supabase']:
            python_packages.extend(['supabase', 'python-dotenv'])
        
        if python_packages:
            print(f"📦 Instalando paquetes Python: {', '.join(python_packages)}")
            try:
                subprocess.run([
                    sys.executable, '-m', 'pip', 'install'
                ] + python_packages, check=True)
                print("✅ Paquetes Python instalados")
            except subprocess.CalledProcessError as e:
                print(f"❌ Error instalando paquetes Python: {e}")
                return False
        
        # Instalar dependencias Node.js
        if deps['node'] and deps['npm'] and deps['react']:
            frontend_path = os.path.join(self.project_root, 'frontend')
            if os.path.exists(frontend_path):
                print("📦 Instalando dependencias del frontend...")
                try:
                    subprocess.run([
                        'npm', 'install'
                    ], cwd=frontend_path, check=True)
                    print("✅ Dependencias del frontend instaladas")
                except subprocess.CalledProcessError as e:
                    print(f"❌ Error instalando dependencias del frontend: {e}")
        
        return True
    
    def setup_superbase(self):
        """Configurar Super Base"""
        print("\n🗄️ Configurando Super Base...")
        
        try:
            # Ejecutar configurador de Supabase
            configurator_script = os.path.join(self.project_root, 'configurar_superbase.py')
            if os.path.exists(configurator_script):
                print("🔧 Ejecutando configurador automático...")
                result = subprocess.run([
                    sys.executable, configurator_script
                ], capture_output=True, text=True)
                
                if result.returncode == 0:
                    print("✅ Super Base configurado correctamente")
                    return True
                else:
                    print(f"⚠️ Configuración parcial: {result.stderr}")
                    return False
            else:
                print("⚠️ Configurador de Super Base no encontrado")
                return False
                
        except Exception as e:
            print(f"❌ Error configurando Super Base: {e}")
            return False
    
    def start_backend(self):
        """Iniciar servidor backend con Super Base"""
        print(f"\n🖥️ Iniciando servidor backend en puerto {self.config['backend_port']}...")
        
        try:
            # Buscar el archivo del servidor
            server_files = [
                'aria_servidor_superbase.py',
                'backend/src/aria_servidor_multilingue.py',
                'scripts/aria/aria_servidor_multilingue.py'
            ]
            
            server_file = None
            for file in server_files:
                full_path = os.path.join(self.project_root, file)
                if os.path.exists(full_path):
                    server_file = full_path
                    break
            
            if not server_file:
                print("❌ Archivo del servidor no encontrado")
                return False
            
            # Iniciar servidor
            self.backend_process = subprocess.Popen([
                sys.executable, server_file
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            
            self.processes.append(self.backend_process)
            
            # Esperar a que el servidor inicie
            print("⏳ Esperando que el servidor backend inicie...")
            time.sleep(5)
            
            # Verificar que está funcionando
            if self.backend_process.poll() is None:
                print(f"✅ Servidor backend iniciado (PID: {self.backend_process.pid})")
                return True
            else:
                stdout, stderr = self.backend_process.communicate()
                print(f"❌ Error iniciando servidor: {stderr}")
                return False
                
        except Exception as e:
            print(f"❌ Error iniciando backend: {e}")
            return False
    
    def start_frontend(self):
        """Iniciar frontend React"""
        print(f"\n⚛️ Iniciando frontend React en puerto {self.config['frontend_port']}...")
        
        try:
            frontend_path = os.path.join(self.project_root, 'frontend')
            if not os.path.exists(frontend_path):
                print("⚠️ Directorio frontend no encontrado, saltando...")
                return True
            
            # Verificar package.json
            package_json = os.path.join(frontend_path, 'package.json')
            if not os.path.exists(package_json):
                print("⚠️ package.json no encontrado en frontend")
                return False
            
            # Iniciar servidor de desarrollo React
            env = os.environ.copy()
            env['PORT'] = str(self.config['frontend_port'])
            
            self.frontend_process = subprocess.Popen([
                'npm', 'start'
            ], cwd=frontend_path, env=env, 
               stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            
            self.processes.append(self.frontend_process)
            
            # Esperar a que inicie
            print("⏳ Esperando que el frontend React inicie...")
            time.sleep(10)
            
            if self.frontend_process.poll() is None:
                print(f"✅ Frontend React iniciado (PID: {self.frontend_process.pid})")
                return True
            else:
                stdout, stderr = self.frontend_process.communicate()
                print(f"❌ Error iniciando frontend: {stderr}")
                return False
                
        except Exception as e:
            print(f"❌ Error iniciando frontend: {e}")
            return False
    
    def open_browser(self):
        """Abrir navegador automáticamente"""
        if not self.config['auto_open_browser']:
            return
        
        print("\n🌐 Abriendo navegador...")
        
        urls_to_try = [
            f"http://localhost:{self.config['frontend_port']}",  # React frontend
            f"http://localhost:{self.config['backend_port']}"    # Backend directo
        ]
        
        for url in urls_to_try:
            try:
                webbrowser.open(url)
                print(f"✅ Navegador abierto: {url}")
                break
            except Exception as e:
                print(f"⚠️ Error abriendo {url}: {e}")
                continue
    
    def monitor_processes(self):
        """Monitorear procesos en background"""
        def monitor():
            while self.running:
                try:
                    # Verificar backend
                    if self.backend_process and self.backend_process.poll() is not None:
                        print("⚠️ Servidor backend se detuvo inesperadamente")
                    
                    # Verificar frontend
                    if self.frontend_process and self.frontend_process.poll() is not None:
                        print("⚠️ Frontend React se detuvo inesperadamente")
                    
                    time.sleep(10)  # Verificar cada 10 segundos
                    
                except Exception as e:
                    print(f"⚠️ Error en monitoreo: {e}")
                    break
        
        if self.config['enable_monitoring']:
            monitor_thread = threading.Thread(target=monitor, daemon=True)
            monitor_thread.start()
            print("📊 Monitoreo de procesos iniciado")
    
    def show_status(self):
        """Mostrar estado actual del sistema"""
        print("\n" + "="*50)
        print("📊 ESTADO DEL SISTEMA ARIA")
        print("="*50)
        
        # Estado de procesos
        backend_status = "🟢 Activo" if (self.backend_process and self.backend_process.poll() is None) else "🔴 Inactivo"
        frontend_status = "🟢 Activo" if (self.frontend_process and self.frontend_process.poll() is None) else "🔴 Inactivo"
        
        print(f"🖥️ Backend:  {backend_status}")
        print(f"⚛️ Frontend: {frontend_status}")
        
        # URLs disponibles
        print(f"\n🌐 URLs disponibles:")
        if self.backend_process and self.backend_process.poll() is None:
            print(f"   API Backend: http://localhost:{self.config['backend_port']}")
        if self.frontend_process and self.frontend_process.poll() is None:
            print(f"   Frontend:    http://localhost:{self.config['frontend_port']}")
        
        # Información adicional
        print(f"\n📋 Información:")
        print(f"   🗄️ Super Base: {'✅ Habilitado' if self.config['enable_superbase'] else '❌ Deshabilitado'}")
        print(f"   📊 Monitoreo: {'✅ Activo' if self.config['enable_monitoring'] else '❌ Inactivo'}")
        print(f"   🕐 Ejecutándose desde: {datetime.now().strftime('%H:%M:%S')}")
        
        print("="*50)
    
    def stop_all(self):
        """Detener todos los procesos"""
        print("\n🛑 Deteniendo ARIA Super Base...")
        
        self.running = False
        
        # Detener procesos
        for process in self.processes:
            if process and process.poll() is None:
                try:
                    process.terminate()
                    process.wait(timeout=5)
                    print(f"✅ Proceso {process.pid} detenido")
                except subprocess.TimeoutExpired:
                    process.kill()
                    print(f"🔨 Proceso {process.pid} forzado a detenerse")
                except Exception as e:
                    print(f"⚠️ Error deteniendo proceso: {e}")
        
        print("✅ Todos los procesos detenidos")
    
    def run_full_system(self):
        """Ejecutar sistema completo"""
        print("\n🚀 ARIA SUPER BASE - LAUNCHER COMPLETO")
        print("="*60)
        print("🤖 Sistema de IA con base de datos avanzada")
        print("🗄️ Powered by Supabase")
        print("⚛️ Modern React Interface")
        print("="*60)
        
        try:
            # Configurar handler para señales
            def signal_handler(signum, frame):
                print("\n📡 Señal de interrupción recibida")
                self.stop_all()
                sys.exit(0)
            
            signal.signal(signal.SIGINT, signal_handler)
            signal.signal(signal.SIGTERM, signal_handler)
            
            # Verificar dependencias
            deps = self.check_dependencies()
            missing_deps = [k for k, v in deps.items() if not v]
            
            if missing_deps:
                print(f"\n⚠️ Dependencias faltantes: {', '.join(missing_deps)}")
                if input("¿Desea instalar las dependencias faltantes? (s/n): ").lower() == 's':
                    if not self.install_missing_dependencies(deps):
                        print("❌ No se pudieron instalar todas las dependencias")
                        return False
                else:
                    print("⚠️ Continuando sin instalar dependencias...")
            
            # Configurar Super Base
            if self.config['enable_superbase']:
                self.setup_superbase()
            
            # Iniciar backend
            if not self.start_backend():
                print("❌ No se pudo iniciar el backend")
                return False
            
            # Iniciar frontend
            if not self.start_frontend():
                print("⚠️ Frontend no disponible, continuando solo con backend")
            
            # Configurar monitoreo
            self.running = True
            self.monitor_processes()
            
            # Abrir navegador
            self.open_browser()
            
            # Mostrar estado
            time.sleep(2)
            self.show_status()
            
            # Mantener activo
            print("\n💡 Comandos disponibles:")
            print("   'status' - Mostrar estado")
            print("   'restart' - Reiniciar servicios")
            print("   'stop' - Detener sistema")
            print("   'quit' o Ctrl+C - Salir")
            
            while self.running:
                try:
                    command = input("\n🤖 ARIA> ").strip().lower()
                    
                    if command in ['quit', 'exit', 'q']:
                        break
                    elif command == 'status':
                        self.show_status()
                    elif command == 'stop':
                        break
                    elif command == 'restart':
                        print("🔄 Reiniciando servicios...")
                        self.stop_all()
                        time.sleep(2)
                        self.start_backend()
                        self.start_frontend()
                        self.running = True
                        self.monitor_processes()
                    elif command == 'help':
                        print("💡 Comandos: status, restart, stop, quit")
                    elif command:
                        print("❓ Comando no reconocido. Escribe 'help' para ver comandos disponibles")
                        
                except KeyboardInterrupt:
                    print("\n📡 Interrupción detectada")
                    break
                except EOFError:
                    print("\n📡 EOF detectado")
                    break
            
            return True
            
        except Exception as e:
            print(f"❌ Error crítico: {e}")
            return False
            
        finally:
            self.stop_all()
    
    def run_backend_only(self):
        """Ejecutar solo el backend con Super Base"""
        print("\n🖥️ ARIA BACKEND CON SUPER BASE")
        print("="*40)
        
        try:
            # Configurar Super Base
            if self.config['enable_superbase']:
                self.setup_superbase()
            
            # Iniciar backend
            if self.start_backend():
                self.running = True
                self.monitor_processes()
                self.show_status()
                
                print(f"\n✅ Backend disponible en: http://localhost:{self.config['backend_port']}")
                print("💡 Presiona Ctrl+C para detener")
                
                try:
                    while self.running:
                        time.sleep(1)
                except KeyboardInterrupt:
                    print("\n📡 Deteniendo backend...")
                
                return True
            else:
                print("❌ No se pudo iniciar el backend")
                return False
                
        finally:
            self.stop_all()


def main():
    """Función principal"""
    launcher = ARIASuperBaseLauncher()
    
    # Verificar argumentos
    if len(sys.argv) > 1:
        mode = sys.argv[1].lower()
        if mode == 'backend':
            return launcher.run_backend_only()
        elif mode == 'full':
            return launcher.run_full_system()
        else:
            print("Uso: python launcher_superbase.py [backend|full]")
            return False
    
    # Modo interactivo
    print("\n🚀 ARIA SUPER BASE LAUNCHER")
    print("="*30)
    print("1. Sistema completo (Backend + Frontend)")
    print("2. Solo Backend con Super Base")
    print("3. Salir")
    
    try:
        choice = input("\nSelecciona una opción (1-3): ").strip()
        
        if choice == '1':
            return launcher.run_full_system()
        elif choice == '2':
            return launcher.run_backend_only()
        elif choice == '3':
            print("👋 ¡Hasta luego!")
            return True
        else:
            print("❌ Opción inválida")
            return False
            
    except KeyboardInterrupt:
        print("\n👋 ¡Hasta luego!")
        return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)