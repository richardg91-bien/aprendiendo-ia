"""
Diagnóstico del Sistema de Voz - Prueba Simple
"""

print("🔍 Iniciando diagnóstico del sistema de voz...")

# Prueba 1: Windows SAPI directo
print("\n1️⃣ Probando Windows SAPI...")
import subprocess
import tempfile
import os

try:
    # Crear script VBS simple
    vbs_content = '''
    Set voice = CreateObject("SAPI.SpVoice")
    voice.Speak "Hola. Este es una prueba de voz."
    '''
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.vbs', delete=False) as f:
        f.write(vbs_content)
        temp_file = f.name
    
    print("   Ejecutando script VBS...")
    result = subprocess.run(['cscript', '//nologo', temp_file], 
                          capture_output=True, timeout=10)
    
    os.unlink(temp_file)
    
    if result.returncode == 0:
        print("   ✅ Windows SAPI funciona correctamente")
    else:
        print(f"   ❌ Error en SAPI: {result.stderr.decode()}")
        
except Exception as e:
    print(f"   ❌ Error probando SAPI: {e}")

# Prueba 2: pyttsx3
print("\n2️⃣ Probando pyttsx3...")
try:
    import pyttsx3
    
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    
    print(f"   📊 Voces disponibles: {len(voices)}")
    for i, voice in enumerate(voices[:3]):  # Mostrar solo las primeras 3
        print(f"   {i+1}. {voice.name}")
    
    print("   🗣️ Probando síntesis...")
    engine.say("Hola. Este es pyttsx3 funcionando.")
    engine.runAndWait()
    print("   ✅ pyttsx3 funciona correctamente")
    
except Exception as e:
    print(f"   ❌ Error con pyttsx3: {e}")

# Prueba 3: Volumen del sistema
print("\n3️⃣ Verificando configuración de audio...")
try:
    # Verificar si el volumen está habilitado
    result = subprocess.run(['powershell', '-Command', 
                           'Get-AudioDevice | Select-Object Name, Default'], 
                          capture_output=True, text=True, timeout=5)
    
    if result.returncode == 0:
        print("   📢 Dispositivos de audio:")
        print(f"   {result.stdout}")
    else:
        print("   ⚠️ No se pudo verificar dispositivos de audio")
        
except Exception as e:
    print(f"   ⚠️ Error verificando audio: {e}")

print("\n🎯 Diagnóstico completado.")
print("\n💡 Soluciones posibles:")
print("   - Verifica que el volumen del sistema esté activado")
print("   - Asegúrate de que los altavoces estén conectados")
print("   - Prueba con auriculares si tienes")
print("   - Verifica que Windows Speech Platform esté instalado")

input("\nPresiona Enter para continuar...")