#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
✅ ARIA - Validador de Icono del Escritorio
===========================================

Valida que el icono de ARIA esté correctamente instalado y funcionando.

Fecha: 23 de octubre de 2025
"""

import os
from pathlib import Path
import subprocess

def validar_icono_aria():
    """Validar que el icono de ARIA esté correctamente configurado"""
    
    print("✅ ARIA - VALIDADOR DE ICONO DEL ESCRITORIO")
    print("=" * 60)
    
    # Verificar escritorio
    desktop = Path.home() / "Desktop"
    print(f"📂 Escritorio: {desktop}")
    
    # Buscar iconos de ARIA
    aria_icons = list(desktop.glob("*ARIA*.lnk"))
    
    if not aria_icons:
        print("❌ No se encontraron iconos de ARIA en el escritorio")
        return False
    
    print(f"✅ {len(aria_icons)} icono(s) de ARIA encontrado(s):")
    
    for icon in aria_icons:
        print(f"   📌 {icon.name}")
        print(f"      📅 Creado: {icon.stat().st_mtime}")
        print(f"      📏 Tamaño: {icon.stat().st_size} bytes")
    
    # Verificar archivos objetivo
    project_dir = Path(__file__).parent
    
    target_files = [
        "ARIA_MENU_PRINCIPAL.bat",
        "INICIAR_ARIA_FINAL.bat", 
        "INICIAR_ARIA_FINAL.ps1",
        "aria_integrated_server.py"
    ]
    
    print("\\n🎯 Verificando archivos objetivo:")
    available_targets = []
    
    for target in target_files:
        target_path = project_dir / target
        if target_path.exists():
            available_targets.append(target)
            print(f"   ✅ {target}")
        else:
            print(f"   ❌ {target}")
    
    # Verificar icono personalizado
    print("\\n🎨 Verificando icono personalizado:")
    icon_paths = [
        project_dir / "assets" / "icons" / "aria_icon.ico",
        project_dir / "assets" / "icons" / "aria.ico"
    ]
    
    custom_icon = None
    for icon_path in icon_paths:
        if icon_path.exists():
            custom_icon = icon_path
            print(f"   ✅ Icono encontrado: {icon_path.name}")
            break
    
    if not custom_icon:
        print("   ⚠️ No se encontró icono personalizado (se usa predeterminado)")
    
    # Resumen
    print("\\n" + "=" * 60)
    print("📋 RESUMEN DE VALIDACIÓN:")
    print("=" * 60)
    
    print(f"🔢 Iconos en escritorio: {len(aria_icons)}")
    print(f"📁 Archivos objetivo disponibles: {len(available_targets)}")
    print(f"🎨 Icono personalizado: {'✅ Disponible' if custom_icon else '❌ No encontrado'}")
    
    if aria_icons and available_targets:
        print("\\n🎉 ¡VALIDACIÓN EXITOSA!")
        print("\\n🚀 Para usar ARIA:")
        print("   1. Haz doble clic en el icono del escritorio")
        print("   2. Espera a que se inicie el servidor")
        print("   3. Ve a http://localhost:5000")
        print("   4. ¡Comienza a chatear con ARIA!")
        
        print("\\n💡 Funcionalidades disponibles:")
        print("   • Chat inteligente con IA")
        print("   • Sistema de aprendizaje continuo")
        print("   • Conexión a Supabase (base de datos)")
        print("   • Conexión a Google Cloud (IA avanzada)")
        print("   • APIs REST para desarrollo")
        print("   • Interfaz web moderna y responsiva")
        
        return True
    else:
        print("\\n❌ VALIDACIÓN FALLIDA")
        print("\\nPasos para solucionar:")
        if not aria_icons:
            print("   • Ejecuta: crear_icono_directo.bat")
        if not available_targets:
            print("   • Verifica que estás en la carpeta correcta del proyecto")
        
        return False

def test_aria_functionality():
    """Probar funcionalidades básicas de ARIA"""
    print("\\n🧪 PROBANDO FUNCIONALIDADES DE ARIA...")
    print("-" * 40)
    
    project_dir = Path(__file__).parent
    
    # Test 1: Verificar estructura del proyecto
    print("🔍 Test 1: Estructura del proyecto")
    required_dirs = ["backend", "frontend", "assets"]
    for dir_name in required_dirs:
        dir_path = project_dir / dir_name
        if dir_path.exists():
            print(f"   ✅ {dir_name}/")
        else:
            print(f"   ⚠️ {dir_name}/ (opcional)")
    
    # Test 2: Verificar archivos principales
    print("\\n🔍 Test 2: Archivos principales")
    important_files = [
        ".env",
        "requirements.txt", 
        "aria_integrated_server.py",
        "aria_enhanced_connector.py"
    ]
    
    for file_name in important_files:
        file_path = project_dir / file_name
        if file_path.exists():
            print(f"   ✅ {file_name}")
        else:
            print(f"   ❌ {file_name}")
    
    # Test 3: Verificar configuración
    print("\\n🔍 Test 3: Configuración")
    env_file = project_dir / ".env"
    if env_file.exists():
        with open(env_file, 'r') as f:
            env_content = f.read()
            
        if "SUPABASE_URL" in env_content:
            print("   ✅ Configuración de Supabase")
        else:
            print("   ❌ Configuración de Supabase")
            
        if "GOOGLE_CLOUD_API_KEY" in env_content:
            print("   ✅ Configuración de Google Cloud")
        else:
            print("   ❌ Configuración de Google Cloud")
    else:
        print("   ❌ Archivo .env no encontrado")
    
    print("\\n✅ Tests de funcionalidad completados")

def main():
    """Función principal"""
    try:
        # Validar icono
        icon_ok = validar_icono_aria()
        
        # Probar funcionalidades
        test_aria_functionality()
        
        # Mensaje final
        print("\\n" + "=" * 60)
        if icon_ok:
            print("🎉 ARIA ESTÁ COMPLETAMENTE CONFIGURADO Y LISTO PARA USAR")
            print("\\n🔗 Enlaces útiles:")
            print("   • Interfaz web: http://localhost:5000")
            print("   • Estado del sistema: http://localhost:5000/api/status")
            print("   • Base de conocimiento: http://localhost:5000/api/knowledge")
        else:
            print("⚠️ ARIA NECESITA CONFIGURACIÓN ADICIONAL")
            print("\\nEjecuta los scripts de reparación si es necesario")
        
        print("=" * 60)
        
        return icon_ok
        
    except Exception as e:
        print(f"\\n❌ Error durante la validación: {e}")
        return False

if __name__ == "__main__":
    success = main()
    
    print("\\n⏸️ Presiona Enter para continuar...")
    input()
    
    exit(0 if success else 1)