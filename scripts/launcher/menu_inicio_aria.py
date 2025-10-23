"""
📋 ARIA - Menú de Inicio Interactivo
===================================
"""

import os
import sys
import subprocess
import time

def print_menu():
    print("""
 ██████╗ ██████╗ ██╗ █████╗ 
██╔══██╗██╔══██╗██║██╔══██╗
██████╔╝██████╔╝██║███████║
██╔══██╗██╔══██╗██║██╔══██║
██║  ██║██║  ██║██║██║  ██║
╚═╝  ╚═╝╚═╝  ╚═╝╚═╝╚═╝  ╚═╝

🚀 ARIA - MENÚ DE INICIO
========================
""")
    print("Selecciona una opción:")
    print()
    print("1. 🚀 Inicio Completo (Backend + Frontend)")
    print("2. 🖥️  Solo Backend (Servidor)")
    print("3. 🎨 Solo Frontend (Interfaz)")
    print("4. 🔧 Verificar Sistema")
    print("5. 🌐 Probar Supabase")
    print("6. 📊 Estado del Sistema")
    print("0. ❌ Salir")
    print()

def main():
    project_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(project_dir)
    
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print_menu()
        
        choice = input("👉 Elige una opción (0-6): ").strip()
        
        if choice == "0":
            print("👋 ¡Hasta luego!")
            break
            
        elif choice == "1":
            print("🚀 Iniciando ARIA completo...")
            subprocess.run([sys.executable, "INICIAR_ARIA_COMPLETO.py"])
            
        elif choice == "2":
            print("🖥️  Iniciando solo backend...")
            subprocess.run([
                os.path.join("venv", "Scripts", "python.exe"),
                os.path.join("backend", "src", "main_stable.py")
            ])
            
        elif choice == "3":
            print("🎨 Iniciando solo frontend...")
            subprocess.run(["npm", "start"], cwd="frontend")
            
        elif choice == "4":
            print("🔧 Verificando sistema...")
            subprocess.run([sys.executable, "diagnose_system.py"])
            
        elif choice == "5":
            print("🌐 Probando Supabase...")
            subprocess.run([sys.executable, "test_supabase_final.py"])
            
        elif choice == "6":
            print("📊 Estado del sistema:")
            print("   ✅ Proyecto: ARIA")
            print("   📁 Directorio:", project_dir)
            print("   🐍 Python:", sys.executable)
            print("   🌐 Supabase: Configurado")
            
        else:
            print("❌ Opción no válida")
            
        if choice != "0":
            input("\nPresiona Enter para volver al menú...")

if __name__ == "__main__":
    main()