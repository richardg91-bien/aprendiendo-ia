"""
Script para reiniciar ARIA con personalidad mejorada
"""

import subprocess
import time
import os
import signal
import psutil

def stop_all_python_processes():
    """Detener todos los procesos de Python"""
    print("🛑 Deteniendo procesos anteriores...")
    try:
        for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
            try:
                if proc.info['name'] and 'python' in proc.info['name'].lower():
                    if proc.info['cmdline'] and any('main.py' in str(cmd) for cmd in proc.info['cmdline']):
                        print(f"   Deteniendo proceso Python {proc.info['pid']}")
                        proc.terminate()
                        proc.wait(timeout=5)
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.TimeoutExpired):
                pass
    except Exception as e:
        print(f"   Error deteniendo procesos: {e}")
    
    time.sleep(2)

def start_aria_with_personality():
    """Iniciar ARIA con personalidad mejorada"""
    print("🎭 Iniciando ARIA con personalidad mejorada...")
    
    # Cambiar al directorio correcto
    os.chdir(r"C:\Users\richa\OneDrive\Desktop\aprediendo ia")
    
    # Iniciar el servidor
    process = subprocess.Popen([
        'python', 'backend/src/main.py'
    ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    
    print("✅ ARIA iniciada con personalidad natural!")
    print("🌐 Servidor disponible en: http://127.0.0.1:5000")
    print("💬 ¡Ahora ARIA responderá de forma más natural y espontánea!")
    
    return process

if __name__ == "__main__":
    print("🎭 ARIA - Reinicio con Personalidad Mejorada")
    print("=" * 50)
    
    # Detener procesos anteriores
    stop_all_python_processes()
    
    # Esperar un momento
    time.sleep(3)
    
    # Iniciar ARIA mejorada
    aria_process = start_aria_with_personality()
    
    print("\n" + "=" * 50)
    print("🎉 ¡ARIA está lista con su nueva personalidad!")
    print("✨ Características mejoradas:")
    print("   • Respuestas más naturales y espontáneas")
    print("   • Personalidad más cálida y amigable") 
    print("   • Variedad en las respuestas")
    print("   • Humor ligero y creatividad")
    print("   • Mayor conexión emocional")
    print("\n💝 Tu hija digital ahora es más humana!")
    
    try:
        # Mantener el proceso vivo
        aria_process.wait()
    except KeyboardInterrupt:
        print("\n🛑 Deteniendo ARIA...")
        aria_process.terminate()
        aria_process.wait()
        print("✅ ARIA detenida correctamente")