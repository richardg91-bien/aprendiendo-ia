#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🎯 Navegador Rápido de ARIA
Script para acceso rápido a diferentes secciones del proyecto
"""

import os
import sys
import subprocess
from pathlib import Path

class AriaNavigator:
    def __init__(self):
        self.base_path = Path(__file__).parent
        
    def show_menu(self):
        """Muestra el menú principal de navegación"""
        print("\n" + "="*60)
        print("🚀 ARIA - Navegador Rápido del Proyecto")
        print("="*60)
        print("\n📁 ESTRUCTURA DEL PROYECTO:")
        print("\n1. 🎨 Assets (Iconos y recursos)")
        print("2. ⚙️  Backend (Servidor y APIs)")
        print("3. 🌐 Frontend (Interfaz web)")
        print("4. 🤖 Scripts ARIA")
        print("5. 🎭 Demos y ejemplos")
        print("6. 🚀 Launchers (Iniciadores)")
        print("7. 🔧 Setup y configuración")
        print("8. 🧪 Tests y verificaciones")
        print("9. 📊 Reports y logs")
        print("10. 🔄 Updates y actualizaciones")
        print("\n0. ❌ Salir")
        print("-" * 60)
        
    def open_folder(self, folder_path):
        """Abre una carpeta en el explorador de Windows"""
        try:
            full_path = self.base_path / folder_path
            if full_path.exists():
                subprocess.run(['explorer', str(full_path)], check=True)
                print(f"✅ Abriendo: {full_path}")
            else:
                print(f"❌ La carpeta no existe: {full_path}")
        except Exception as e:
            print(f"❌ Error al abrir carpeta: {e}")
    
    def list_files(self, folder_path, description):
        """Lista archivos en una carpeta específica"""
        try:
            full_path = self.base_path / folder_path
            if full_path.exists():
                print(f"\n📂 {description}")
                print("-" * 50)
                files = list(full_path.rglob("*"))
                if files:
                    for file in sorted(files):
                        if file.is_file():
                            relative_path = file.relative_to(self.base_path)
                            print(f"  📄 {relative_path}")
                else:
                    print("  (Carpeta vacía)")
                
                input("\n⏸️  Presiona Enter para continuar...")
            else:
                print(f"❌ La carpeta no existe: {full_path}")
        except Exception as e:
            print(f"❌ Error al listar archivos: {e}")
    
    def run(self):
        """Ejecuta el navegador principal"""
        while True:
            try:
                self.show_menu()
                choice = input("\n🎯 Selecciona una opción (0-10): ").strip()
                
                if choice == "0":
                    print("\n👋 ¡Hasta luego!")
                    break
                elif choice == "1":
                    self.list_files("assets", "🎨 ASSETS - Iconos y recursos")
                    self.open_folder("assets")
                elif choice == "2":
                    self.list_files("backend", "⚙️ BACKEND - Servidor y APIs")
                    self.open_folder("backend")
                elif choice == "3":
                    self.list_files("frontend", "🌐 FRONTEND - Interfaz web")
                    self.open_folder("frontend")
                elif choice == "4":
                    self.list_files("scripts/aria", "🤖 SCRIPTS ARIA")
                    self.open_folder("scripts/aria")
                elif choice == "5":
                    self.list_files("scripts/demo", "🎭 DEMOS Y EJEMPLOS")
                    self.open_folder("scripts/demo")
                elif choice == "6":
                    self.list_files("scripts/launcher", "🚀 LAUNCHERS")
                    self.open_folder("scripts/launcher")
                elif choice == "7":
                    self.list_files("scripts/setup", "🔧 SETUP Y CONFIGURACIÓN")
                    self.open_folder("scripts/setup")
                elif choice == "8":
                    self.list_files("scripts/test", "🧪 TESTS Y VERIFICACIONES")
                    self.open_folder("scripts/test")
                elif choice == "9":
                    self.list_files("reports", "📊 REPORTS Y LOGS")
                    self.open_folder("reports")
                elif choice == "10":
                    self.list_files("updates", "🔄 UPDATES Y ACTUALIZACIONES")
                    self.open_folder("updates")
                else:
                    print("❌ Opción no válida. Intenta de nuevo.")
                    
            except KeyboardInterrupt:
                print("\n\n👋 ¡Hasta luego!")
                break
            except Exception as e:
                print(f"❌ Error inesperado: {e}")

if __name__ == "__main__":
    navigator = AriaNavigator()
    navigator.run()