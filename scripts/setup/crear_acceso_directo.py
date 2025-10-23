"""
🖥️ Creador de Acceso Directo para ARIA
=====================================
Este script crea un acceso directo en el escritorio para iniciar ARIA
"""

import os
import winshell
from win32com.client import Dispatch

def create_desktop_shortcut():
    print("🖥️ CREANDO ACCESO DIRECTO PARA ARIA")
    print("=" * 50)
    
    # Rutas
    project_path = r"C:\Users\richa\OneDrive\Desktop\aprendiendo-ia"
    desktop = winshell.desktop()
    
    # Opciones de accesos directos
    shortcuts = [
        {
            "name": "🚀 ARIA - Inicio Completo",
            "target": os.path.join(project_path, "INICIAR_ARIA_COMPLETO.bat"),
            "icon": "shell32.dll,137",  # Icono de estrella
            "description": "Inicia el sistema completo ARIA (Backend + Frontend + Supabase)"
        },
        {
            "name": "🤫 ARIA - Inicio Silencioso", 
            "target": os.path.join(project_path, "ARIA_INICIO_SILENCIOSO.vbs"),
            "icon": "shell32.dll,278",  # Icono de aplicación
            "description": "Inicia ARIA en segundo plano sin ventanas de comandos"
        },
        {
            "name": "🐍 ARIA - Inicio Python",
            "target": os.path.join(project_path, "venv", "Scripts", "python.exe"),
            "arguments": os.path.join(project_path, "INICIAR_ARIA_COMPLETO.py"),
            "icon": "shell32.dll,21",   # Icono de Python
            "description": "Inicia ARIA usando el script Python multiplataforma"
        }
    ]
    
    created_shortcuts = []
    
    for shortcut in shortcuts:
        try:
            shortcut_path = os.path.join(desktop, shortcut["name"] + ".lnk")
            
            shell = Dispatch('WScript.Shell')
            shortcut_obj = shell.CreateShortCut(shortcut_path)
            
            shortcut_obj.Targetpath = shortcut["target"]
            shortcut_obj.WorkingDirectory = project_path
            shortcut_obj.Description = shortcut["description"]
            
            if "arguments" in shortcut:
                shortcut_obj.Arguments = shortcut["arguments"]
            
            # Configurar icono
            if "icon" in shortcut:
                shortcut_obj.IconLocation = shortcut["icon"]
            
            shortcut_obj.save()
            
            print(f"✅ Creado: {shortcut['name']}")
            created_shortcuts.append(shortcut["name"])
            
        except Exception as e:
            print(f"❌ Error creando {shortcut['name']}: {e}")
    
    print()
    print("🎉 ACCESOS DIRECTOS CREADOS EN EL ESCRITORIO")
    print("=" * 50)
    
    for name in created_shortcuts:
        print(f"🔗 {name}")
    
    print()
    print("💡 RECOMENDACIONES:")
    print("   🚀 Usa 'ARIA - Inicio Completo' para desarrollo")
    print("   🤫 Usa 'ARIA - Inicio Silencioso' para uso diario")
    print("   🐍 Usa 'ARIA - Inicio Python' como alternativa")
    print()
    print("✨ ¡Ahora puedes iniciar ARIA con un solo clic!")

if __name__ == "__main__":
    try:
        create_desktop_shortcut()
    except ImportError:
        print("❌ Error: Necesitas instalar las dependencias:")
        print("   pip install pywin32 winshell")
        os.system("pip install pywin32 winshell")
        print("✅ Dependencias instaladas. Ejecuta el script nuevamente.")
    except Exception as e:
        print(f"❌ Error: {e}")
        input("Presiona Enter para continuar...")