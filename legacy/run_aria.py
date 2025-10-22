#!/usr/bin/env python3
"""
ARIA v2.0 - Sistema de Inteligencia Artificial
Archivo de inicio principal del proyecto

Ejecuta este archivo para iniciar ARIA con la nueva estructura profesional
"""

import os
import sys
import subprocess
from pathlib import Path

def main():
    """Función principal de inicio"""
    print("🚀 Iniciando ARIA v2.0...")
    print("📁 Estructura profesional activada")
    print()
    
    # Verificar que estemos en el directorio correcto
    if not (Path("backend").exists() and Path("frontend").exists()):
        print("❌ Error: Ejecuta este script desde el directorio raíz de ARIA")
        return 1
    
    # Cambiar al directorio backend
    backend_dir = Path("backend/src")
    
    if not backend_dir.exists():
        print("❌ Error: No se encontró backend/src/")
        return 1
    
    print("🔄 Iniciando servidor backend...")
    
    try:
        # Ejecutar el servidor principal
        os.chdir("backend")
        subprocess.run([sys.executable, "src/main.py"])
    except KeyboardInterrupt:
        print("\n👋 ARIA detenido por el usuario")
    except Exception as e:
        print(f"❌ Error: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)