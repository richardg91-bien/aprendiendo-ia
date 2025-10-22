"""
🤖 ARIA - Generador de Icono Futurista Premium
=============================================

Crea iconos de alta calidad con efectos futuristas avanzados
"""

from PIL import Image, ImageDraw, ImageFont, ImageFilter
import math

def create_premium_aria_icon():
    """Crea un icono premium de ARIA con efectos futuristas avanzados"""
    
    size = 256
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    center = size // 2
    
    # === FONDO CON GRADIENTE RADIAL ===
    for radius in range(120, 0, -1):
        # Gradiente del exterior al interior
        intensity = (120 - radius) / 120
        
        # Colores de gradiente futurista
        if intensity < 0.3:
            # Exterior: azul oscuro
            r = int(20 + intensity * 30)
            g = int(25 + intensity * 35) 
            b = int(50 + intensity * 80)
        elif intensity < 0.7:
            # Medio: azul brillante
            r = int(30 + intensity * 50)
            g = int(40 + intensity * 60)
            b = int(100 + intensity * 100)
        else:
            # Interior: cyan brillante
            r = int(50 + intensity * 80)
            g = int(120 + intensity * 100)
            b = int(200 + intensity * 55)
        
        alpha = max(50, int(255 * intensity * 0.8))
        color = (r, g, b, alpha)
        
        draw.ellipse(
            [(center - radius, center - radius), (center + radius, center + radius)],
            fill=color
        )
    
    # === ANILLOS EXTERNOS ===
    ring_colors = [
        (0, 255, 255, 255),    # Cyan brillante
        (0, 200, 255, 200),    # Azul brillante
        (100, 150, 255, 150),  # Azul claro
    ]
    
    for i, color in enumerate(ring_colors):
        radius = 115 - i * 8
        width = 3 - i
        draw.ellipse(
            [(center - radius, center - radius), (center + radius, center + radius)],
            outline=color,
            width=width
        )
    
    # === PATRÓN DE CIRCUITO INTERNO ===
    circuit_radius = 80
    num_nodes = 8
    
    for i in range(num_nodes):
        angle = (2 * math.pi * i) / num_nodes
        x = center + int(circuit_radius * math.cos(angle))
        y = center + int(circuit_radius * math.sin(angle))
        
        # Nodos principales
        draw.ellipse(
            [(x-4, y-4), (x+4, y+4)],
            fill=(0, 255, 150, 255)
        )
        
        # Conexiones al centro
        draw.line(
            [(center, center), (x, y)],
            fill=(0, 255, 150, 100),
            width=2
        )
        
        # Conexiones entre nodos adyacentes
        next_i = (i + 1) % num_nodes
        next_angle = (2 * math.pi * next_i) / num_nodes
        next_x = center + int(circuit_radius * math.cos(next_angle))
        next_y = center + int(circuit_radius * math.sin(next_angle))
        
        draw.line(
            [(x, y), (next_x, next_y)],
            fill=(0, 200, 255, 80),
            width=1
        )
    
    # === NÚCLEO CENTRAL ===
    core_radius = 25
    # Efecto de brillo del núcleo
    for r in range(core_radius, 0, -1):
        alpha = int(255 * (core_radius - r) / core_radius)
        intensity = (core_radius - r) / core_radius
        
        if intensity < 0.5:
            color = (int(255 * intensity), int(255 * intensity), 255, alpha)
        else:
            color = (255, int(255 * intensity), int(255 * intensity), alpha)
        
        draw.ellipse(
            [(center - r, center - r), (center + r, center + r)],
            fill=color
        )
    
    # Borde del núcleo
    draw.ellipse(
        [(center - core_radius, center - core_radius), 
         (center + core_radius, center + core_radius)],
        outline=(255, 255, 255, 255),
        width=2
    )
    
    # === TEXTO ARIA ===
    try:
        font_size = 28
        try:
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
        
        # Efecto de resplandor del texto
        for offset in range(5, 0, -1):
            alpha = 50 + offset * 20
            draw.text(
                (text_x + offset//2, text_y + offset//2), 
                text, 
                fill=(0, 255, 255, alpha), 
                font=font
            )
        
        # Texto principal
        draw.text((text_x, text_y), text, fill=(255, 255, 255, 255), font=font)
        
    except Exception as e:
        # Si falla el texto, usar símbolo alternativo
        symbol_size = 20
        draw.rectangle(
            [(center - symbol_size//2, center - symbol_size//2),
             (center + symbol_size//2, center + symbol_size//2)],
            outline=(255, 255, 255, 255),
            width=3
        )
    
    # === EFECTOS DE LUZ ADICIONALES ===
    # Puntos de luz en posiciones estratégicas
    light_points = [
        (center - 40, center - 40),
        (center + 40, center - 40),
        (center - 40, center + 40),
        (center + 40, center + 40),
    ]
    
    for point in light_points:
        for r in range(8, 0, -1):
            alpha = int(100 * (8 - r) / 8)
            draw.ellipse(
                [(point[0] - r, point[1] - r), (point[0] + r, point[1] + r)],
                fill=(255, 255, 255, alpha)
            )
    
    # Guardar en múltiples formatos
    img.save("aria_icon_premium.png", format='PNG')
    img.save("aria_icon_premium.ico", format='ICO')
    
    # Crear versión para diferentes tamaños
    sizes = [16, 32, 48, 64, 128]
    images = [img]
    
    for target_size in sizes:
        resized = img.resize((target_size, target_size), Image.Resampling.LANCZOS)
        images.append(resized)
    
    # Crear ICO multi-tamaño
    images[0].save(
        "aria_icon_premium_multi.ico",
        format='ICO',
        sizes=[(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]
    )
    
    print("✅ Icono premium de ARIA creado")
    print("📁 Archivos generados:")
    print("   • aria_icon_premium.png (256x256)")
    print("   • aria_icon_premium.ico (256x256)")
    print("   • aria_icon_premium_multi.ico (multi-tamaño)")
    
    return True

def update_desktop_shortcut_with_premium_icon():
    """Actualiza el acceso directo con el icono premium"""
    
    try:
        import winshell
        from win32com.client import Dispatch
        import os
        
        desktop = winshell.desktop()
        project_path = os.path.abspath(".")
        
        # Usar el icono premium
        premium_icon = os.path.join(project_path, "aria_icon_premium.ico")
        if not os.path.exists(premium_icon):
            premium_icon = os.path.join(project_path, "aria_icon.ico")
        
        shortcut_path = os.path.join(desktop, 'ARIA Asistente IA.lnk')
        startup_script = os.path.join(project_path, "INICIAR_ARIA_COMPLETO.bat")
        
        if os.path.exists(shortcut_path):
            # Actualizar icono del acceso directo existente
            shell = Dispatch('WScript.Shell')
            shortcut = shell.CreateShortCut(shortcut_path)
            shortcut.IconLocation = premium_icon
            shortcut.save()
            
            print(f"✅ Icono del acceso directo actualizado")
            print(f"🎨 Nuevo icono: {premium_icon}")
            return True
        else:
            print("⚠️ No se encontró el acceso directo existente")
            return False
            
    except Exception as e:
        print(f"❌ Error actualizando icono: {e}")
        return False

if __name__ == "__main__":
    print("🎨 Creando icono premium de ARIA...")
    print("=" * 50)
    
    if create_premium_aria_icon():
        print("\n🔄 Actualizando acceso directo...")
        if update_desktop_shortcut_with_premium_icon():
            print("\n🎉 ¡Icono premium aplicado exitosamente!")
            print("💡 El acceso directo en el escritorio ahora tiene el icono futurista premium")
        else:
            print("\n💡 Icono premium creado. Puedes aplicarlo manualmente al acceso directo.")
    else:
        print("\n❌ Error creando icono premium")