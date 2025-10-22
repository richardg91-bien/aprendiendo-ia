"""
🤖 ASISTENTE VIRTUAL ARIA - MENÚ PRINCIPAL
"""

import sys
import subprocess
import os

def mostrar_menu():
    print("🤖 ASISTENTE VIRTUAL ARIA")
    print("=" * 50)
    print("Elige cómo quieres usar el asistente:")
    print()
    print("1. 🌐 Asistente Web (Interfaz moderna)")
    print("2. 💻 Asistente por Voz (Línea de comandos)")
    print("3. 📋 Solo Transcripción (Web)")
    print("4. ⚙️  Configurar asistente")
    print("5. 📖 Ver ayuda")
    print("6. 🚪 Salir")
    print("=" * 50)

def iniciar_asistente_web():
    print("🌐 Iniciando Asistente Web...")
    print("📱 Se abrirá en: http://localhost:5001")
    print("💡 Presiona Ctrl+C para detener")
    print("-" * 30)
    
    try:
        subprocess.run([
            sys.executable, "asistente_web.py"
        ])
    except KeyboardInterrupt:
        print("\n🛑 Asistente web detenido")

def iniciar_asistente_voz():
    print("🎤 Iniciando Asistente por Voz...")
    print("💡 Di 'ARIA' para activar")
    print("💡 Presiona Ctrl+C para detener")
    print("-" * 30)
    
    try:
        subprocess.run([
            sys.executable, "asistente_virtual.py"
        ])
    except KeyboardInterrupt:
        print("\n🛑 Asistente por voz detenido")

def iniciar_transcripcion_web():
    print("📝 Iniciando Transcriptor Web...")
    print("📱 Se abrirá en: http://localhost:5000")
    print("💡 Presiona Ctrl+C para detener")
    print("-" * 30)
    
    try:
        subprocess.run([
            sys.executable, "web_app.py"
        ])
    except KeyboardInterrupt:
        print("\n🛑 Transcriptor web detenido")

def configurar_asistente():
    print("⚙️ CONFIGURACIÓN DEL ASISTENTE")
    print("-" * 30)
    
    config_file = "asistente_config.json"
    if os.path.exists(config_file):
        print(f"📄 Archivo de configuración: {config_file}")
        print("✅ Configuración existente encontrada")
        
        respuesta = input("¿Quieres editar la configuración? (s/n): ").lower()
        if respuesta in ['s', 'sí', 'si', 'yes', 'y']:
            print("📝 Abriendo archivo de configuración...")
            # En Windows, usar notepad
            if sys.platform == "win32":
                os.system(f"notepad {config_file}")
            else:
                os.system(f"nano {config_file}")
    else:
        print("📄 No se encontró configuración. Se creará al usar el asistente.")
    
    input("\nPresiona Enter para volver al menú...")

def mostrar_ayuda():
    print("📖 AYUDA DEL ASISTENTE VIRTUAL")
    print("-" * 40)
    print()
    print("🌐 ASISTENTE WEB:")
    print("   • Interfaz moderna con chat")
    print("   • Reconocimiento de voz en tiempo real")
    print("   • Subida de archivos de audio")
    print("   • Respuestas por texto y voz")
    print()
    print("💻 ASISTENTE POR VOZ:")
    print("   • Control total por voz")
    print("   • Di 'ARIA' para activar")
    print("   • Comandos naturales en español")
    print("   • Respuestas por altavoces")
    print()
    print("📝 SOLO TRANSCRIPCIÓN:")
    print("   • Convierte audio a texto")
    print("   • Múltiples formatos de audio")
    print("   • Descarga de resultados")
    print("   • Interfaz drag & drop")
    print()
    print("🎯 COMANDOS DISPONIBLES:")
    print("   • '¿Qué hora es?' - Hora actual")
    print("   • '¿Qué día es?' - Fecha de hoy")
    print("   • 'Cuéntame un chiste' - Humor")
    print("   • '¿Cómo estás?' - Conversación")
    print("   • 'Ayuda' - Lista de comandos")
    print("   • 'Transcribir' - Procesar audio")
    print()
    
    input("Presiona Enter para volver al menú...")

def main():
    while True:
        try:
            mostrar_menu()
            
            opcion = input("Selecciona una opción (1-6): ").strip()
            
            if opcion == "1":
                iniciar_asistente_web()
            elif opcion == "2":
                iniciar_asistente_voz()
            elif opcion == "3":
                iniciar_transcripcion_web()
            elif opcion == "4":
                configurar_asistente()
            elif opcion == "5":
                mostrar_ayuda()
            elif opcion == "6":
                print("👋 ¡Hasta luego! Gracias por usar ARIA")
                break
            else:
                print("❌ Opción no válida. Intenta de nuevo.")
                input("Presiona Enter para continuar...")
                
        except KeyboardInterrupt:
            print("\n\n👋 ¡Hasta luego!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")
            input("Presiona Enter para continuar...")

if __name__ == "__main__":
    main()