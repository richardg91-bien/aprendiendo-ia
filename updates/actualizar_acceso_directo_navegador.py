"""
🤖 ARIA - Actualizador de Acceso Directo con Navegador Automático
================================================================

Actualiza el acceso directo para abrir directamente el navegador
"""

import os
import winshell
from win32com.client import Dispatch

def update_desktop_shortcut_with_browser():
    """Actualiza el acceso directo para abrir automáticamente el navegador"""
    
    try:
        desktop = winshell.desktop()
        project_path = os.path.abspath(".")
        
        # Rutas de archivos
        premium_icon = os.path.join(project_path, "aria_icon_premium.ico")
        new_startup_script = os.path.join(project_path, "INICIAR_ARIA_Y_ABRIR_NAVEGADOR.bat")
        shortcut_path = os.path.join(desktop, 'ARIA Asistente IA.lnk')
        
        # Verificar que existe el nuevo script
        if not os.path.exists(new_startup_script):
            print("❌ No se encontró el script de inicio con navegador")
            return False
        
        # Verificar que existe el icono
        if not os.path.exists(premium_icon):
            premium_icon = os.path.join(project_path, "aria_icon.ico")
        
        # Actualizar o crear acceso directo
        shell = Dispatch('WScript.Shell')
        shortcut = shell.CreateShortCut(shortcut_path)
        
        # Configurar propiedades del acceso directo
        shortcut.Targetpath = new_startup_script
        shortcut.WorkingDirectory = project_path
        shortcut.IconLocation = premium_icon
        shortcut.Description = "🤖 ARIA - Inicia la IA y abre el navegador automáticamente"
        shortcut.WindowStyle = 1  # Ventana normal
        
        # Guardar acceso directo
        shortcut.save()
        
        print("✅ Acceso directo actualizado con éxito")
        print(f"📁 Ruta: {shortcut_path}")
        print(f"🎨 Icono: {premium_icon}")
        print(f"🚀 Script: {new_startup_script}")
        print()
        print("🌟 NUEVAS CARACTERÍSTICAS:")
        print("   • ✅ Inicia backend automáticamente")
        print("   • ✅ Inicia frontend automáticamente") 
        print("   • ✅ Espera que ambos estén listos")
        print("   • ✅ Abre el navegador automáticamente")
        print("   • ✅ Verifica puertos disponibles (3000/3001)")
        print("   • ✅ Minimiza ventanas después del inicio")
        print("   • ✅ Mantiene ARIA ejecutándose")
        
        return True
        
    except Exception as e:
        print(f"❌ Error actualizando acceso directo: {e}")
        return False

def create_quick_test_script():
    """Crea un script rápido para probar el sistema"""
    
    test_script = """@echo off
title ARIA - Prueba Rápida
echo.
echo 🧪 Probando ARIA - Inicio con Navegador
echo ========================================
echo.
echo 🚀 Ejecutando script de inicio...
call "%~dp0INICIAR_ARIA_Y_ABRIR_NAVEGADOR.bat"
"""
    
    with open("PROBAR_ARIA_NAVEGADOR.bat", "w", encoding="utf-8") as f:
        f.write(test_script)
    
    print("✅ Script de prueba creado: PROBAR_ARIA_NAVEGADOR.bat")

if __name__ == "__main__":
    print("🔄 Actualizando acceso directo de ARIA...")
    print("=" * 50)
    print()
    
    # Crear script de prueba
    create_quick_test_script()
    
    # Actualizar acceso directo
    if update_desktop_shortcut_with_browser():
        print()
        print("🎉 ¡ACCESO DIRECTO ACTUALIZADO EXITOSAMENTE!")
        print()
        print("💡 CÓMO FUNCIONA AHORA:")
        print("   1. 🖱️  Doble clic en 'ARIA Asistente IA' del escritorio")
        print("   2. ⏳ El sistema inicia backend y frontend automáticamente")
        print("   3. 🌐 Se abre el navegador con ARIA cuando esté listo")
        print("   4. ✨ ¡Listo para usar!")
        print()
        print("🧪 PARA PROBAR:")
        print("   • Ejecuta: PROBAR_ARIA_NAVEGADOR.bat")
        print("   • O usa el acceso directo del escritorio")
        
    else:
        print()
        print("❌ No se pudo actualizar el acceso directo")
        print("💡 Puedes ejecutar manualmente: INICIAR_ARIA_Y_ABRIR_NAVEGADOR.bat")