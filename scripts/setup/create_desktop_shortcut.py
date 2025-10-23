"""
🤖 ARIA - Creador de Acceso Directo con Icono Personalizado
===========================================================

Crea un acceso directo en el escritorio con el icono de ARIA
"""

import os
import winshell
from win32com.client import Dispatch

def create_desktop_shortcut_with_icon():
    """Crea acceso directo en el escritorio con icono personalizado"""
    
    # Rutas
    desktop = winshell.desktop()
    project_path = os.path.abspath(".")
    icon_path = os.path.join(project_path, "aria_icon.ico")
    startup_script = os.path.join(project_path, "INICIAR_ARIA_COMPLETO.bat")
    
    # Verificar que existe el icono
    if not os.path.exists(icon_path):
        print("❌ No se encontró el icono de ARIA")
        return False
    
    # Verificar que existe el script de inicio
    if not os.path.exists(startup_script):
        print("❌ No se encontró el script de inicio")
        return False
    
    try:
        # Crear acceso directo
        shell = Dispatch('WScript.Shell')
        shortcut_path = os.path.join(desktop, 'ARIA Asistente IA.lnk')
        shortcut = shell.CreateShortCut(shortcut_path)
        
        # Configurar propiedades del acceso directo
        shortcut.Targetpath = startup_script
        shortcut.WorkingDirectory = project_path
        shortcut.IconLocation = icon_path
        shortcut.Description = "🤖 ARIA - Asistente de Inteligencia Artificial Avanzado"
        shortcut.WindowStyle = 1  # Ventana normal
        
        # Guardar acceso directo
        shortcut.save()
        
        print(f"✅ Acceso directo creado en el escritorio: 'ARIA Asistente IA'")
        print(f"📁 Ruta: {shortcut_path}")
        print(f"🎨 Icono: {icon_path}")
        print(f"🚀 Script: {startup_script}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error creando acceso directo: {e}")
        return False

def create_advanced_aria_icon():
    """Crea un icono más avanzado para ARIA"""
    try:
        from PIL import Image, ImageDraw, ImageFont
        
        # Crear imagen de alta resolución
        size = 256
        img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        center = size // 2
        
        # Fondo circular con gradiente
        for i in range(50):
            radius = int(size * 0.45) - i
            alpha = max(0, 255 - i * 5)
            color = (26 + i, 26 + i, 46 + i * 2, alpha)
            if radius > 0:
                draw.ellipse(
                    [(center - radius, center - radius), (center + radius, center + radius)],
                    fill=color
                )
        
        # Borde principal
        main_radius = int(size * 0.45)
        draw.ellipse(
            [(center - main_radius, center - main_radius), 
             (center + main_radius, center + main_radius)],
            outline=(0, 128, 255, 255),
            width=4
        )
        
        # Borde interior brillante
        inner_radius = int(main_radius * 0.85)
        draw.ellipse(
            [(center - inner_radius, center - inner_radius), 
             (center + inner_radius, center + inner_radius)],
            outline=(0, 255, 136, 255),
            width=2
        )
        
        # Texto ARIA con mejor fuente
        try:
            font_size = 48
            font = ImageFont.truetype("arial.ttf", font_size)
        except:
            try:
                font = ImageFont.truetype("calibri.ttf", font_size)
            except:
                font = ImageFont.load_default()
        
        text = "ARIA"
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        text_x = (size - text_width) // 2
        text_y = (size - text_height) // 2
        
        # Sombra múltiple para efecto de profundidad
        for offset in range(3, 0, -1):
            alpha = 100 - offset * 20
            draw.text((text_x + offset, text_y + offset), text, 
                     fill=(0, 0, 0, alpha), font=font)
        
        # Texto principal con gradiente simulado
        draw.text((text_x, text_y), text, fill=(255, 255, 255, 255), font=font)
        
        # Puntos de circuito futurista
        circuit_points = [
            (center - 60, center - 30),
            (center + 60, center - 30),
            (center - 60, center + 30),
            (center + 60, center + 30),
            (center - 80, center),
            (center + 80, center),
            (center, center - 70),
            (center, center + 70)
        ]
        
        for point in circuit_points:
            draw.ellipse(
                [(point[0] - 3, point[1] - 3), (point[0] + 3, point[1] + 3)],
                fill=(0, 255, 136, 200)
            )
            
            # Conexiones
            if abs(point[0] - center) > abs(point[1] - center):
                end_x = center + (30 if point[0] > center else -30)
                draw.line([(point[0], point[1]), (end_x, point[1])], 
                         fill=(0, 255, 136, 100), width=1)
            else:
                end_y = center + (25 if point[1] > center else -25)
                draw.line([(point[0], point[1]), (point[0], end_y)], 
                         fill=(0, 255, 136, 100), width=1)
        
        # Guardar como ICO
        img.save("aria_icon_advanced.ico", format='ICO')
        
        # También guardar como PNG para respaldo
        img.save("aria_icon_advanced.png", format='PNG')
        
        print("✅ Icono avanzado de ARIA creado")
        return True
        
    except Exception as e:
        print(f"⚠️ Error creando icono avanzado: {e}")
        return False

if __name__ == "__main__":
    print("🎨 Creando acceso directo de ARIA con icono personalizado...")
    print("=" * 60)
    
    # Crear icono avanzado
    create_advanced_aria_icon()
    
    # Instalar dependencias si es necesario
    try:
        import winshell
        from win32com.client import Dispatch
    except ImportError:
        print("📦 Instalando dependencias...")
        os.system("pip install pywin32 winshell")
        import winshell
        from win32com.client import Dispatch
    
    # Crear acceso directo
    if create_desktop_shortcut_with_icon():
        print("\n🎉 ¡Acceso directo creado exitosamente!")
        print("💡 Ahora puedes hacer doble clic en el icono de ARIA en tu escritorio")
        print("🤖 para iniciar todo el sistema automáticamente.")
    else:
        print("\n❌ No se pudo crear el acceso directo")
        print("💡 Puedes crear uno manualmente apuntando a INICIAR_ARIA_COMPLETO.bat")