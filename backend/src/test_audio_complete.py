"""
Test de Audio del Sistema - Verificación Completa
"""

import subprocess
import tempfile
import os
import time

print("🔊 Verificación completa del sistema de audio...")

# Test 1: VBS directo sin captura
print("\n1️⃣ Test VBS directo...")
try:
    vbs_content = '''
    Set voice = CreateObject("SAPI.SpVoice")
    voice.Speak "Sistema de audio funcionando correctamente"
    '''
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.vbs', delete=False) as f:
        f.write(vbs_content)
        temp_file = f.name
    
    print("   🗣️ Reproduciendo audio directo...")
    # Sin capture_output para permitir audio
    result = subprocess.run(['cscript', '//nologo', temp_file], timeout=10)
    os.unlink(temp_file)
    
    if result.returncode == 0:
        print("   ✅ VBS directo completado")
    else:
        print("   ⚠️ VBS con código de salida:", result.returncode)
        
except Exception as e:
    print(f"   ❌ Error en VBS directo: {e}")

# Test 2: PowerShell TTS
print("\n2️⃣ Test PowerShell Speech...")
try:
    ps_command = '''
    Add-Type -AssemblyName System.speech
    $speak = New-Object System.Speech.Synthesis.SpeechSynthesizer
    $speak.Speak("PowerShell funcionando")
    '''
    
    print("   🗣️ Reproduciendo con PowerShell...")
    result = subprocess.run(['powershell', '-Command', ps_command], timeout=10)
    
    if result.returncode == 0:
        print("   ✅ PowerShell speech completado")
    else:
        print("   ⚠️ PowerShell con código:", result.returncode)
        
except Exception as e:
    print(f"   ❌ Error en PowerShell: {e}")

# Test 3: Verificar volumen
print("\n3️⃣ Verificando configuración de audio...")
try:
    # Verificar si hay dispositivos de audio
    result = subprocess.run(['powershell', '-Command', 
                           '''Get-WmiObject -Class Win32_SoundDevice | 
                           Select-Object Name, Status | Format-Table -AutoSize'''], 
                          capture_output=True, text=True, timeout=5)
    
    if result.stdout:
        print("   📢 Dispositivos de audio encontrados:")
        print(f"   {result.stdout}")
    else:
        print("   ⚠️ No se detectaron dispositivos de audio")
        
except Exception as e:
    print(f"   ⚠️ Error verificando dispositivos: {e}")

print("\n🎯 Tests completados.")
print("\n💡 Si no escuchaste nada:")
print("   1. Revisa el volumen del sistema (icono de altavoz)")
print("   2. Verifica que los altavoces estén conectados y encendidos")
print("   3. Prueba con auriculares")
print("   4. Ve a Configuración > Sistema > Sonido")
print("   5. Asegúrate que el dispositivo de salida sea correcto")

input("\nPresiona Enter para continuar...")