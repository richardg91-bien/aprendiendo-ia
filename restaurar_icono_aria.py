#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🎯 ARIA - Restaurador de Ícono del Escritorio
Recrear el acceso directo de ARIA en el escritorio
"""

import os
import sys
import winshell
from win32com.client import Dispatch
from pathlib import Path

def crear_icono_aria():
    """Crear ícono de ARIA en el escritorio"""
    print("🎯 ARIA - Restaurador de Ícono del Escritorio")
    print("=" * 60)
    
    try:
        # Rutas importantes
        project_dir = Path(__file__).parent.absolute()
        desktop = winshell.desktop()
        
        # Archivo launcher principal
        launcher_bat = project_dir / "INICIAR_ARIA_FINAL.bat"
        launcher_ps1 = project_dir / "INICIAR_ARIA_FINAL.ps1"
        menu_principal = project_dir / "ARIA_MENU_PRINCIPAL.bat"
        
        # Verificar que existen los launchers
        if not launcher_bat.exists() and not launcher_ps1.exists() and not menu_principal.exists():
            print("❌ No se encontraron archivos launcher de ARIA")
            return False
        
        # Crear acceso directo para el menú principal (preferido)
        if menu_principal.exists():
            target_file = str(menu_principal)
            shortcut_name = "🤖 ARIA - Asistente IA"
            description = "ARIA - Asistente de Inteligencia Artificial Futurista"
        elif launcher_bat.exists():
            target_file = str(launcher_bat)
            shortcut_name = "🤖 ARIA - Launcher"
            description = "ARIA - Iniciar Asistente de IA"
        else:
            target_file = str(launcher_ps1)
            shortcut_name = "🤖 ARIA - PowerShell"
            description = "ARIA - Iniciar con PowerShell"
        
        # Ruta del acceso directo
        shortcut_path = os.path.join(desktop, f"{shortcut_name}.lnk")
        
        print(f"📁 Directorio proyecto: {project_dir}")
        print(f"🖥️ Escritorio: {desktop}")
        print(f"🎯 Archivo objetivo: {target_file}")
        print(f"🔗 Acceso directo: {shortcut_path}")
        
        # Crear el acceso directo
        shell = Dispatch('WScript.Shell')
        shortcut = shell.CreateShortCut(shortcut_path)
        shortcut.Targetpath = target_file
        shortcut.WorkingDirectory = str(project_dir)
        shortcut.Description = description
        
        # Buscar un ícono personalizado
        icon_paths = [
            project_dir / "assets" / "icons" / "aria_icon.ico",
            project_dir / "assets" / "aria.ico",
            project_dir / "aria_icon.ico",
            project_dir / "icon.ico"
        ]
        
        icon_found = False
        for icon_path in icon_paths:
            if icon_path.exists():
                shortcut.IconLocation = str(icon_path)
                icon_found = True
                print(f"🎨 Ícono encontrado: {icon_path}")
                break
        
        if not icon_found:
            # Usar ícono del sistema para aplicaciones
            shortcut.IconLocation = "shell32.dll,1"  # Ícono de aplicación
            print("🎨 Usando ícono del sistema")
        
        # Guardar el acceso directo
        shortcut.save()
        
        print("✅ Acceso directo creado exitosamente")
        print(f"🔗 Ubicación: {shortcut_path}")
        
        # Verificar que se creó
        if os.path.exists(shortcut_path):
            print("✅ Ícono de ARIA restaurado en el escritorio")
            return True
        else:
            print("❌ Error: No se pudo crear el acceso directo")
            return False
            
    except Exception as e:
        print(f"❌ Error creando ícono: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def crear_icono_personalizado():
    """Crear un ícono personalizado para ARIA si no existe"""
    try:
        from PIL import Image, ImageDraw, ImageFont
        
        project_dir = Path(__file__).parent.absolute()
        assets_dir = project_dir / "assets" / "icons"
        assets_dir.mkdir(parents=True, exist_ok=True)
        
        icon_path = assets_dir / "aria_icon.ico"
        
        if icon_path.exists():
            print(f"✅ Ícono personalizado ya existe: {icon_path}")
            return str(icon_path)
        
        print("🎨 Creando ícono personalizado para ARIA...")
        
        # Crear imagen 256x256 para el ícono
        size = 256
        image = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(image)
        
        # Fondo circular azul futurista
        center = size // 2
        radius = size // 2 - 10
        draw.ellipse([center-radius, center-radius, center+radius, center+radius], 
                    fill=(0, 120, 255, 255), outline=(0, 80, 200, 255), width=4)
        
        # Círculo interno
        inner_radius = radius - 30
        draw.ellipse([center-inner_radius, center-inner_radius, center+inner_radius, center+inner_radius], 
                    fill=(20, 140, 255, 180))
        
        # Texto "AI" en el centro
        try:
            font_size = 80
            # Intentar usar una fuente del sistema
            try:
                font = ImageFont.truetype("arial.ttf", font_size)
            except:
                font = ImageFont.load_default()
        except:
            font = ImageFont.load_default()
        
        text = "AI"
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        text_x = center - text_width // 2
        text_y = center - text_height // 2
        
        # Sombra del texto
        draw.text((text_x + 2, text_y + 2), text, font=font, fill=(0, 0, 0, 128))
        # Texto principal
        draw.text((text_x, text_y), text, font=font, fill=(255, 255, 255, 255))
        
        # Efectos futuristas (líneas)
        for i in range(8):
            angle = i * 45
            import math
            x1 = center + int((radius - 20) * math.cos(math.radians(angle)))
            y1 = center + int((radius - 20) * math.sin(math.radians(angle)))
            x2 = center + int((radius - 5) * math.cos(math.radians(angle)))
            y2 = center + int((radius - 5) * math.sin(math.radians(angle)))
            draw.line([x1, y1, x2, y2], fill=(255, 255, 255, 200), width=3)
        
        # Guardar como ICO
        # Para ICO necesitamos varios tamaños
        sizes = [16, 32, 48, 64, 128, 256]
        images = []
        
        for s in sizes:
            resized = image.resize((s, s), Image.Resampling.LANCZOS)
            images.append(resized)
        
        # Guardar como ICO
        images[0].save(str(icon_path), format='ICO', sizes=[(s, s) for s in sizes])
        
        print(f"✅ Ícono personalizado creado: {icon_path}")
        return str(icon_path)
        
    except ImportError:
        print("⚠️ PIL no disponible, usando ícono del sistema")
        return None
    except Exception as e:
        print(f"⚠️ Error creando ícono personalizado: {e}")
        return None

def main():
    """Función principal"""
    print("🎯 ARIA - Restauración de Ícono del Escritorio")
    print("=" * 60)
    
    # Verificar dependencias
    try:
        import winshell
        import win32com.client
    except ImportError as e:
        print(f"❌ Falta dependencia: {e}")
        print("💡 Instalando dependencias necesarias...")
        os.system("pip install pywin32 winshell")
        try:
            import winshell
            import win32com.client
            print("✅ Dependencias instaladas")
        except ImportError:
            print("❌ No se pudieron instalar las dependencias")
            print("💡 Ejecuta manualmente: pip install pywin32 winshell")
            return False
    
    # Crear ícono personalizado si es posible
    try:
        crear_icono_personalizado()
    except:
        pass
    
    # Crear acceso directo
    success = crear_icono_aria()
    
    if success:
        print("\n🎉 ¡Ícono de ARIA restaurado exitosamente!")
        print("✅ Ahora puedes ver el ícono de ARIA en tu escritorio")
        print("🚀 Haz doble clic para iniciar ARIA")
    else:
        print("\n❌ No se pudo restaurar el ícono")
        print("💡 Intenta ejecutar como administrador")
    
    return success

if __name__ == "__main__":
    try:
        success = main()
        input("\nPresiona Enter para continuar...")
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⏹️ Cancelado por el usuario")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Error fatal: {e}")
        import traceback
        traceback.print_exc()
        input("\nPresiona Enter para salir...")
        sys.exit(1)