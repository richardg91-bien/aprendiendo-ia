"""
🤖 ARIA - Creador de Icono Personalizado
=======================================

Genera un icono futurista para ARIA
"""

from PIL import Image, ImageDraw, ImageFont
import os

def create_aria_icon():
    """Crea un icono futurista para ARIA"""
    
    # Tamaños de iconos estándar de Windows
    sizes = [16, 32, 48, 64, 128, 256]
    
    for size in sizes:
        # Crear imagen con fondo transparente
        img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        # Colores futuristas
        bg_color = (26, 26, 46, 255)  # Azul oscuro futurista
        border_color = (0, 128, 255, 255)  # Azul brillante
        glow_color = (0, 255, 136, 255)  # Verde neón
        text_color = (255, 255, 255, 255)  # Blanco
        
        # Crear fondo circular con gradiente
        center = size // 2
        radius = int(size * 0.45)
        
        # Fondo circular
        draw.ellipse(
            [(center - radius, center - radius), (center + radius, center + radius)],
            fill=bg_color,
            outline=border_color,
            width=max(1, size // 32)
        )
        
        # Efecto de brillo interior
        inner_radius = int(radius * 0.8)
        draw.ellipse(
            [(center - inner_radius, center - inner_radius), 
             (center + inner_radius, center + inner_radius)],
            outline=glow_color,
            width=max(1, size // 64)
        )
        
        # Texto ARIA
        try:
            # Intentar usar una fuente del sistema
            font_size = max(8, size // 6)
            try:
                font = ImageFont.truetype("arial.ttf", font_size)
            except:
                try:
                    font = ImageFont.truetype("calibri.ttf", font_size)
                except:
                    font = ImageFont.load_default()
            
            # Dibujar texto ARIA
            text = "ARIA"
            bbox = draw.textbbox((0, 0), text, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            
            text_x = (size - text_width) // 2
            text_y = (size - text_height) // 2
            
            # Sombra del texto
            draw.text((text_x + 1, text_y + 1), text, fill=(0, 0, 0, 128), font=font)
            # Texto principal
            draw.text((text_x, text_y), text, fill=text_color, font=font)
            
        except Exception as e:
            # Si falla el texto, usar un símbolo simple
            # Dibujar un símbolo de IA (circuito)
            circuit_size = size // 4
            draw.rectangle(
                [(center - circuit_size//2, center - circuit_size//2),
                 (center + circuit_size//2, center + circuit_size//2)],
                outline=glow_color,
                width=max(1, size // 32)
            )
            
            # Puntos de conexión
            dot_size = max(1, size // 16)
            positions = [
                (center - circuit_size//2, center),
                (center + circuit_size//2, center),
                (center, center - circuit_size//2),
                (center, center + circuit_size//2)
            ]
            
            for pos in positions:
                draw.ellipse(
                    [(pos[0] - dot_size, pos[1] - dot_size),
                     (pos[0] + dot_size, pos[1] + dot_size)],
                    fill=glow_color
                )
        
        # Guardar imagen
        filename = f"aria_icon_{size}x{size}.png"
        img.save(filename)
        print(f"✅ Icono creado: {filename}")
    
    # Crear el icono principal de 256x256 como .ico
    try:
        # Crear archivo .ico con múltiples tamaños
        images = []
        for size in [16, 32, 48, 64, 128, 256]:
            img = Image.open(f"aria_icon_{size}x{size}.png")
            images.append(img)
        
        # Guardar como .ico
        images[0].save(
            "aria_icon.ico",
            format='ICO',
            sizes=[(size, size) for size in [16, 32, 48, 64, 128, 256]]
        )
        print("✅ Archivo de icono principal creado: aria_icon.ico")
        
        # Limpiar archivos temporales
        for size in [16, 32, 48, 64, 128, 256]:
            try:
                os.remove(f"aria_icon_{size}x{size}.png")
            except:
                pass
                
    except Exception as e:
        print(f"⚠️ Error creando .ico: {e}")
        print("💡 Usando PNG de 256x256 como alternativa")
        
    print("\n🎨 Icono de ARIA creado exitosamente!")

if __name__ == "__main__":
    print("🎨 Creando icono futurista para ARIA...")
    create_aria_icon()