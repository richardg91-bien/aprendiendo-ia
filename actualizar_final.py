"""
🤖 ARIA - Actualizador Final del Acceso Directo
==============================================

Actualiza con la versión mejorada y más robusta
"""

import os
import winshell
from win32com.client import Dispatch

def update_shortcut_final():
    """Actualiza el acceso directo con la versión final mejorada"""
    
    try:
        desktop = winshell.desktop()
        project_path = os.path.abspath(".")
        
        # Archivos
        premium_icon = os.path.join(project_path, "aria_icon_premium.ico")
        improved_script = os.path.join(project_path, "INICIAR_ARIA_NAVEGADOR_MEJORADO.bat")
        shortcut_path = os.path.join(desktop, 'ARIA Asistente IA.lnk')
        
        # Verificar archivos
        if not os.path.exists(improved_script):
            print("❌ Script mejorado no encontrado")
            return False
            
        if not os.path.exists(premium_icon):
            premium_icon = os.path.join(project_path, "aria_icon.ico")
        
        # Actualizar acceso directo
        shell = Dispatch('WScript.Shell')
        shortcut = shell.CreateShortCut(shortcut_path)
        
        shortcut.Targetpath = improved_script
        shortcut.WorkingDirectory = project_path
        shortcut.IconLocation = premium_icon
        shortcut.Description = "🤖 ARIA - Inicia IA y abre navegador automáticamente"
        shortcut.WindowStyle = 1
        
        shortcut.save()
        
        print("✅ ACCESO DIRECTO ACTUALIZADO CON VERSIÓN MEJORADA")
        print()
        print("🌟 CARACTERÍSTICAS FINALES:")
        print("   ✅ Codificación UTF-8 para caracteres especiales")
        print("   ✅ Colores en la interfaz de consola")
        print("   ✅ Limpieza automática de procesos anteriores")
        print("   ✅ Verificación robusta de servicios")
        print("   ✅ Detección automática de puertos") 
        print("   ✅ Apertura automática del navegador")
        print("   ✅ Minimización automática después del inicio")
        print("   ✅ Monitoreo continuo del sistema")
        print()
        print(f"📁 Acceso directo: {shortcut_path}")
        print(f"🎨 Icono: {premium_icon}")
        print(f"🚀 Script: {improved_script}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    print("🔄 ACTUALIZANDO ACCESO DIRECTO FINAL...")
    print("=" * 50)
    
    if update_shortcut_final():
        print()
        print("🎉 ¡CONFIGURACIÓN FINAL COMPLETADA!")
        print()
        print("🎯 INSTRUCCIONES DE USO:")
        print("   1. 🖱️  Doble clic en 'ARIA Asistente IA' (escritorio)")
        print("   2. ⏳ Espera que aparezca la ventana de inicio")
        print("   3. 🌐 El navegador se abrirá automáticamente")
        print("   4. ✨ ¡ARIA estará listo para usar!")
        print()
        print("💡 CARACTERÍSTICA PRINCIPAL:")
        print("   🌐 EL NAVEGADOR SE ABRE AUTOMÁTICAMENTE")
        print("   🚀 NO NECESITAS ABRIR NADA MANUALMENTE")
        
    else:
        print("❌ Error en la actualización")