#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🚀 ARIA SUPER BASE - LAUNCHER FINAL
===================================

Launcher definitivo para ARIA con Super Base completamente configurado.
Ejecuta el servidor con integración completa de Supabase para almacenamiento
de conocimiento y relaciones de APIs.

Características implementadas:
✅ Super Base (Supabase) completamente integrado
✅ Almacenamiento persistente de conversaciones
✅ Gestión de conocimiento con base de datos
✅ Relaciones inteligentes con APIs externas
✅ Sistema de aprendizaje continuo
✅ Interfaz moderna con React (opcional)

Fecha: 22 de octubre de 2025
"""

import os
import sys
import subprocess
import time
import webbrowser
from datetime import datetime

# Configurar codificación para Windows
if sys.platform == "win32":
    os.system("chcp 65001")

def check_environment():
    """Verificar que el entorno esté configurado"""
    print("Verificando configuración de ARIA Super Base...")
    
    # Verificar archivos esenciales
    required_files = [
        'aria_servidor_superbase.py',
        'backend/src/aria_superbase.py', 
        '.env',
        'aria_superbase_schema.sql'
    ]
    
    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print(f"[ERROR] Archivos faltantes: {', '.join(missing_files)}")
        return False
    
    print("[OK] Archivos principales encontrados")
    
    # Verificar entorno virtual
    venv_python = os.path.join('venv_new', 'Scripts', 'python.exe')
    if not os.path.exists(venv_python):
        print("[ERROR] Entorno virtual venv_new no encontrado")
        return False
    
    print("[OK] Entorno virtual encontrado")
    return True

def show_setup_instructions():
    """Mostrar instrucciones de configuración"""
    print("\n" + "="*60)
    print("📋 INSTRUCCIONES DE CONFIGURACIÓN")
    print("="*60)
    print("Para completar la configuración de ARIA Super Base:")
    print()
    print("1. 🌐 Ve a tu panel de Supabase:")
    print("   https://supabase.com/dashboard")
    print()
    print("2. 📂 Abre tu proyecto 'cggxjweagmeirqpdzypn'")
    print()
    print("3. 🛠️ Ve a SQL Editor")
    print()
    print("4. 📄 Copia y ejecuta el contenido de:")
    print("   aria_superbase_schema.sql")
    print()
    print("5. ✅ Las tablas se crearán automáticamente")
    print()
    print("6. 🔄 Vuelve a ejecutar este launcher")
    print("="*60)

def start_aria_superbase():
    """Iniciar ARIA con Super Base"""
    print("\n🚀 INICIANDO ARIA SUPER BASE...")
    print("="*50)
    
    try:
        # Comando para activar entorno virtual y ejecutar servidor
        cmd = [
            os.path.join('venv_new', 'Scripts', 'python.exe'),
            'aria_servidor_superbase.py'
        ]
        
        print(f"🖥️ Ejecutando: {' '.join(cmd)}")
        print("⏳ Iniciando servidor...")
        
        # Iniciar servidor
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
            universal_newlines=True
        )
        
        # Mostrar output del servidor en tiempo real
        print("\n📋 LOG DEL SERVIDOR:")
        print("-" * 30)
        
        backend_ready = False
        
        for line in iter(process.stdout.readline, ''):
            print(line.rstrip())
            
            # Detectar cuando el servidor está listo
            if "Servidor iniciado en http://localhost:8000" in line:
                backend_ready = True
                break
            elif "ARIA SUPER SERVER - Iniciando..." in line:
                print("✅ ARIA Super Server detectado")
            elif "Super Base: ✅ Conectado" in line:
                print("✅ Super Base conectado exitosamente")
            elif "Error" in line and "crítico" in line:
                print("❌ Error crítico detectado")
                break
        
        if backend_ready:
            print("\n🌐 ARIA Super Base está listo!")
            print(f"   📡 API: http://localhost:8000")
            print(f"   📊 Estado: http://localhost:8000/status")
            print(f"   🧠 Conocimiento: http://localhost:8000/knowledge")
            print(f"   🔍 Búsqueda: http://localhost:8000/search?q=inteligencia")
            
            # Abrir navegador automáticamente
            time.sleep(2)
            try:
                webbrowser.open("http://localhost:8000")
                print("   🌐 Navegador abierto automáticamente")
            except:
                print("   ⚠️ Abre manualmente: http://localhost:8000")
            
            print(f"\n💡 Comandos disponibles:")
            print("   Ctrl+C - Detener servidor")
            print("   POST /chat - Conversar con ARIA")
            print("   GET /knowledge - Ver conocimiento almacenado")
            
            # Mantener proceso activo
            try:
                process.wait()
            except KeyboardInterrupt:
                print("\n📡 Deteniendo ARIA Super Base...")
                process.terminate()
                process.wait()
                print("✅ ARIA detenido correctamente")
        else:
            print("❌ El servidor no pudo iniciarse correctamente")
            return False
            
    except FileNotFoundError:
        print("❌ Python no encontrado en el entorno virtual")
        print("💡 Ejecuta: python -m venv venv_new")
        return False
    except Exception as e:
        print(f"❌ Error iniciando ARIA: {e}")
        return False
    
    return True

def test_superbase_connection():
    """Probar conexión con Super Base"""
    print("\n🔗 Probando conexión con Super Base...")
    
    try:
        cmd = [
            os.path.join('venv_new', 'Scripts', 'python.exe'),
            '-c',
            'from backend.src.aria_superbase import aria_superbase; stats = aria_superbase.get_database_stats(); print(f"Conectado: {stats[\"connected\"]}"); print(f"Conocimiento: {stats[\"knowledge_count\"]} entradas")'
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        
        if result.returncode == 0:
            print("✅ Super Base respondió:")
            print(result.stdout)
            return "connected" in result.stdout.lower() and "true" in result.stdout.lower()
        else:
            print("⚠️ Respuesta de Super Base:")
            print(result.stderr)
            return False
            
    except subprocess.TimeoutExpired:
        print("⏰ Timeout conectando a Super Base")
        return False
    except Exception as e:
        print(f"❌ Error probando conexión: {e}")
        return False

def main():
    """Función principal"""
    print("🗄️ ARIA SUPER BASE - LAUNCHER FINAL")
    print("="*40)
    print("🤖 IA Avanzada con Base de Datos")
    print("🗄️ Powered by Supabase")
    print("="*40)
    
    # Cambiar al directorio del script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    # Verificar configuración
    if not check_environment():
        print("\n❌ Configuración incompleta")
        show_setup_instructions()
        return False
    
    # Probar conexión con Super Base
    connected = test_superbase_connection()
    
    if not connected:
        print("\n⚠️ Super Base no está completamente configurado")
        print("🔧 ARIA funcionará con almacenamiento local")
        response = input("\n¿Continuar de todos modos? (s/n): ").lower()
        if response != 's':
            show_setup_instructions()
            return False
    else:
        print("✅ Super Base conectado y funcionando")
    
    # Mostrar resumen antes de iniciar
    print("\n📋 RESUMEN DE CONFIGURACIÓN:")
    print(f"   🗄️ Super Base: {'✅ Conectado' if connected else '⚠️ Local'}")
    print(f"   🐍 Python: {os.path.join('venv_new', 'Scripts', 'python.exe')}")
    print(f"   🚀 Servidor: aria_servidor_superbase.py")
    print(f"   📡 Puerto: 8000")
    
    print(f"\n🚀 Iniciando en 3 segundos...")
    time.sleep(3)
    
    # Iniciar ARIA
    success = start_aria_superbase()
    
    if success:
        print("\n🎉 ¡ARIA Super Base ejecutado exitosamente!")
    else:
        print("\n⚠️ Revisa los errores anteriores")
        show_setup_instructions()
    
    return success

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n👋 ¡Hasta luego!")
        sys.exit(0)