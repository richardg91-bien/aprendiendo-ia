#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🎯 ARIA - Gestor de Iconos del Escritorio
==========================================

Script mejorado para gestionar los iconos de ARIA en el escritorio.
Limpia iconos antiguos y crea uno nuevo y actualizado.

Fecha: 23 de octubre de 2025
"""

import os
import sys
import glob
from pathlib import Path
import subprocess
import time

def limpiar_iconos_antiguos():
    """Limpiar iconos antiguos de ARIA del escritorio"""
    print("🧹 Limpiando iconos antiguos de ARIA...")
    
    desktop = Path.home() / "Desktop"
    
    # Patrones de iconos de ARIA
    patterns = [
        "ARIA*.lnk",
        "*ARIA*.lnk",
        "aria*.lnk",
        "*aria*.lnk"
    ]
    
    removed_count = 0
    for pattern in patterns:
        for icon_file in desktop.glob(pattern):
            try:
                print(f"   🗑️ Eliminando: {icon_file.name}")
                icon_file.unlink()
                removed_count += 1
            except Exception as e:
                print(f"   ⚠️ No se pudo eliminar {icon_file.name}: {e}")
    
    print(f"✅ {removed_count} iconos antiguos eliminados")
    return removed_count

def verificar_archivos_aria():
    """Verificar que existen los archivos necesarios de ARIA"""
    print("🔍 Verificando archivos de ARIA...")
    
    project_dir = Path(__file__).parent
    
    # Archivos launcher disponibles
    launchers = [
        ("ARIA_MENU_PRINCIPAL.bat", "🎯 ARIA - Menú Principal"),
        ("INICIAR_ARIA_FINAL.bat", "🚀 ARIA - Launcher Final"),
        ("INICIAR_ARIA_FINAL.ps1", "⚡ ARIA - PowerShell"),
        ("aria_integrated_server.py", "🤖 ARIA - Servidor Integrado")
    ]
    
    available_launchers = []
    for launcher_file, display_name in launchers:
        launcher_path = project_dir / launcher_file
        if launcher_path.exists():
            available_launchers.append((launcher_path, display_name))
            print(f"   ✅ {display_name}: {launcher_file}")
        else:
            print(f"   ❌ {display_name}: {launcher_file} (no encontrado)")
    
    # Verificar icono
    icon_paths = [
        project_dir / "assets" / "icons" / "aria_icon.ico",
        project_dir / "assets" / "icons" / "aria.ico",
        project_dir / "frontend" / "public" / "favicon.ico"
    ]
    
    icon_path = None
    for ico_path in icon_paths:
        if ico_path.exists():
            icon_path = ico_path
            print(f"   ✅ Icono encontrado: {ico_path}")
            break
    
    if not icon_path:
        print("   ⚠️ No se encontró icono personalizado, se usará el predeterminado")
    
    return available_launchers, icon_path

def crear_icono_moderno():
    """Crear icono moderno de ARIA usando PowerShell"""
    print("🎨 Creando icono moderno de ARIA...")
    
    # Obtener información
    available_launchers, icon_path = verificar_archivos_aria()
    
    if not available_launchers:
        print("❌ No se encontraron archivos launcher de ARIA")
        return False
    
    # Seleccionar el mejor launcher
    target_file, display_name = available_launchers[0]
    
    # Crear script PowerShell temporal
    ps_script = f'''
# Script temporal para crear icono de ARIA
$desktop = [Environment]::GetFolderPath("Desktop")
$projectPath = "{target_file.parent.as_posix()}"
$targetFile = "{target_file.as_posix()}"
$iconPath = "{icon_path.as_posix() if icon_path else ''}"

Write-Host "🎯 Creando icono de ARIA..." -ForegroundColor Cyan
Write-Host "Launcher: {display_name}" -ForegroundColor Green
Write-Host "Archivo: $targetFile" -ForegroundColor Yellow

# Crear objeto COM para accesos directos
$shell = New-Object -ComObject WScript.Shell

# Ruta del acceso directo
$shortcutPath = Join-Path $desktop "🤖 ARIA - Asistente IA.lnk"

# Crear acceso directo
$shortcut = $shell.CreateShortcut($shortcutPath)
$shortcut.TargetPath = $targetFile
$shortcut.WorkingDirectory = $projectPath
$shortcut.Description = "ARIA - Asistente de Inteligencia Artificial con Supabase y Google Cloud"
$shortcut.Arguments = ""

# Configurar icono si existe
if (Test-Path $iconPath) {{
    $shortcut.IconLocation = $iconPath
    Write-Host "Icono personalizado: $iconPath" -ForegroundColor Green
}}

# Guardar acceso directo
$shortcut.Save()

# Verificar creación
if (Test-Path $shortcutPath) {{
    Write-Host "✅ ICONO CREADO EXITOSAMENTE" -ForegroundColor Green
    Write-Host "Ubicación: $shortcutPath" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "🚀 ARIA está listo para usar:" -ForegroundColor Yellow
    Write-Host "  • Interfaz web: http://localhost:5000" -ForegroundColor White
    Write-Host "  • Chat inteligente con IA" -ForegroundColor White
    Write-Host "  • Conexión a Supabase y Google Cloud" -ForegroundColor White
    Write-Host "  • Sistema de aprendizaje continuo" -ForegroundColor White
    Write-Host ""
    Write-Host "Haz doble clic en el icono para iniciar ARIA" -ForegroundColor Cyan
}} else {{
    Write-Host "❌ Error creando el icono" -ForegroundColor Red
}}
'''
    
    # Escribir script temporal
    temp_script = Path(__file__).parent / "temp_icon_creator.ps1"
    with open(temp_script, 'w', encoding='utf-8') as f:
        f.write(ps_script)
    
    try:
        # Ejecutar script PowerShell
        result = subprocess.run([
            "powershell", "-ExecutionPolicy", "Bypass", "-File", str(temp_script)
        ], capture_output=True, text=True, encoding='utf-8')
        
        if result.returncode == 0:
            print("✅ Script PowerShell ejecutado exitosamente")
            print(result.stdout)
            return True
        else:
            print("❌ Error ejecutando script PowerShell:")
            print(result.stderr)
            return False
            
    except Exception as e:
        print(f"❌ Error ejecutando PowerShell: {e}")
        return False
    
    finally:
        # Limpiar script temporal
        try:
            temp_script.unlink()
        except:
            pass

def verificar_icono_final():
    """Verificar que el icono final se creó correctamente"""
    print("\\n🔍 Verificando icono final...")
    
    desktop = Path.home() / "Desktop"
    icon_patterns = ["*ARIA*.lnk", "aria*.lnk"]
    
    found_icons = []
    for pattern in icon_patterns:
        found_icons.extend(desktop.glob(pattern))
    
    if found_icons:
        print(f"✅ {len(found_icons)} icono(s) de ARIA encontrado(s):")
        for icon in found_icons:
            print(f"   📁 {icon.name}")
        return True
    else:
        print("❌ No se encontraron iconos de ARIA")
        return False

def main():
    """Función principal del gestor de iconos"""
    print("\\n" + "="*70)
    print("🎯 ARIA - GESTOR DE ICONOS DEL ESCRITORIO")
    print("="*70)
    print("Fecha: 23 de octubre de 2025")
    print("Estado: Gestión completa de iconos")
    print("="*70)
    
    try:
        # Paso 1: Limpiar iconos antiguos
        limpiar_iconos_antiguos()
        
        print("\\n" + "-"*50)
        
        # Paso 2: Crear icono nuevo
        if crear_icono_moderno():
            print("\\n" + "-"*50)
            
            # Paso 3: Verificar resultado
            verificar_icono_final()
            
            print("\\n" + "="*70)
            print("🎉 ¡ICONO DE ARIA RESTAURADO EXITOSAMENTE!")
            print("="*70)
            print("\\n🚀 Próximos pasos:")
            print("   1. Busca el icono '🤖 ARIA - Asistente IA' en tu escritorio")
            print("   2. Haz doble clic para iniciar ARIA")
            print("   3. Ve a http://localhost:5000 para usar la interfaz web")
            print("\\n💡 Características:")
            print("   • Chat inteligente con IA")
            print("   • Conexión a Supabase y Google Cloud")
            print("   • Sistema de aprendizaje continuo")
            print("   • Interfaz web moderna")
            
        else:
            print("\\n❌ Error creando el icono nuevo")
            return False
            
    except Exception as e:
        print(f"\\n❌ Error en el gestor de iconos: {e}")
        return False
    
    print("\\n" + "="*70)
    return True

if __name__ == "__main__":
    success = main()
    
    print("\\n⏸️ Presiona Enter para continuar...")
    input()
    
    sys.exit(0 if success else 1)