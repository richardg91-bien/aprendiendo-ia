#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🚀 CONFIGURADOR AUTOMÁTICO DE ARIA DEFINITIVO
=============================================

Este script configura automáticamente todo el sistema ARIA:
1. Instala dependencias
2. Configura Supabase
3. Inicializa conocimiento básico
4. Prueba el sistema
5. Ejecuta ARIA

UN SOLO COMANDO PARA TENER ARIA COMPLETAMENTE FUNCIONAL
"""

import os
import sys
import subprocess
import time
import json

def print_banner():
    """Mostrar banner de inicio"""
    print("""
🤖 ARIA CONFIGURADOR AUTOMÁTICO DEFINITIVO
==========================================
    
    🧠 Inteligencia Artificial
    ☁️  Almacenamiento en Supabase  
    🔍 Búsqueda semántica
    💬 Conversación natural
    
Configurando todo automáticamente...
""")

def run_command(command, description="Ejecutando comando"):
    """Ejecutar comando con output"""
    print(f"\n🔄 {description}")
    print(f"   Comando: {command}")
    
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"✅ Éxito")
            if result.stdout.strip():
                # Mostrar solo las últimas líneas relevantes
                lines = result.stdout.strip().split('\n')
                for line in lines[-3:]:  # Últimas 3 líneas
                    if line.strip():
                        print(f"   📝 {line.strip()}")
        else:
            print(f"❌ Error")
            if result.stderr.strip():
                lines = result.stderr.strip().split('\n')
                for line in lines[-3:]:  # Últimas 3 líneas de error
                    if line.strip():
                        print(f"   ❌ {line.strip()}")
        
        return result.returncode == 0
        
    except Exception as e:
        print(f"❌ Excepción: {e}")
        return False

def check_python_version():
    """Verificar versión de Python"""
    print("🐍 Verificando Python...")
    version = sys.version_info
    
    if version.major >= 3 and version.minor >= 8:
        print(f"✅ Python {version.major}.{version.minor}.{version.micro} - Compatible")
        return True
    else:
        print(f"❌ Python {version.major}.{version.minor}.{version.micro} - Requiere 3.8+")
        return False

def install_dependencies():
    """Instalar dependencias automáticamente"""
    print("\n📦 PASO 1: Instalando dependencias...")
    
    # Verificar si existe el instalador
    if os.path.exists('instalar_embeddings_deps.py'):
        return run_command('python instalar_embeddings_deps.py', 'Ejecutando instalador de dependencias')
    else:
        # Instalar manualmente las dependencias básicas
        packages = [
            'sentence-transformers',
            'supabase',
            'numpy',
            'python-dotenv',
            'flask',
            'flask-cors'
        ]
        
        success_count = 0
        for package in packages:
            if run_command(f'pip install {package}', f'Instalando {package}'):
                success_count += 1
        
        return success_count >= len(packages) * 0.8  # 80% éxito mínimo

def check_environment_variables():
    """Verificar y configurar variables de entorno"""
    print("\n🔑 PASO 2: Verificando configuración de Supabase...")
    
    supabase_url = os.getenv('SUPABASE_URL')
    supabase_key = os.getenv('SUPABASE_ANON_KEY')
    
    if supabase_url and supabase_key:
        print(f"✅ Variables configuradas")
        print(f"   URL: {supabase_url}")
        print(f"   Key: {supabase_key[:20]}...")
        return True
    else:
        print("⚠️ Variables de entorno no encontradas")
        
        # Buscar archivo .env
        env_files = ['.env', '.env.local', '.env.embeddings']
        found_env = False
        
        for env_file in env_files:
            if os.path.exists(env_file):
                print(f"📄 Encontrado: {env_file}")
                try:
                    # Cargar variables del archivo
                    with open(env_file, 'r') as f:
                        lines = f.readlines()
                    
                    for line in lines:
                        if 'SUPABASE_URL=' in line and not line.strip().startswith('#'):
                            url = line.split('=', 1)[1].strip()
                            if url and url != 'https://tu-proyecto.supabase.co':
                                os.environ['SUPABASE_URL'] = url
                                found_env = True
                        
                        if 'SUPABASE_ANON_KEY=' in line and not line.strip().startswith('#'):
                            key = line.split('=', 1)[1].strip()
                            if key and key != 'tu_anon_key_aqui':
                                os.environ['SUPABASE_ANON_KEY'] = key
                                found_env = True
                
                except Exception as e:
                    print(f"❌ Error leyendo {env_file}: {e}")
        
        if found_env:
            print("✅ Variables cargadas desde archivo .env")
            return True
        else:
            print("❌ Configuración de Supabase requerida")
            print("\n📝 Para continuar, crea un archivo .env con:")
            print("   SUPABASE_URL=https://tu-proyecto.supabase.co")
            print("   SUPABASE_ANON_KEY=tu_anon_key_aqui")
            print("\n🌐 Obtén estas credenciales en supabase.com")
            return False

def run_database_schema():
    """Verificar/ejecutar esquema de base de datos"""
    print("\n🗄️ PASO 3: Verificando esquema de base de datos...")
    
    # Verificar si existe el archivo de esquema
    if os.path.exists('supabase_embeddings_schema.sql'):
        print("✅ Esquema SQL encontrado")
        print("📝 IMPORTANTE: Ejecuta este SQL en tu panel de Supabase:")
        print("   1. Ve a tu proyecto en supabase.com")
        print("   2. Abre el SQL Editor")
        print("   3. Copia y pega el contenido de: supabase_embeddings_schema.sql")
        print("   4. Ejecuta el script")
        
        # Esperar confirmación del usuario
        input("\n⏳ Presiona ENTER cuando hayas ejecutado el esquema SQL en Supabase...")
        return True
    else:
        print("❌ Archivo de esquema no encontrado")
        return False

def initialize_knowledge():
    """Inicializar conocimiento básico"""
    print("\n🧠 PASO 4: Inicializando conocimiento básico...")
    
    if os.path.exists('inicializar_aria_definitivo.py'):
        return run_command('python inicializar_aria_definitivo.py', 'Ejecutando inicializador definitivo')
    else:
        print("❌ Inicializador no encontrado")
        return False

def test_system():
    """Probar el sistema"""
    print("\n🧪 PASO 5: Probando el sistema...")
    
    if os.path.exists('probar_aria_definitivo.py'):
        return run_command('python probar_aria_definitivo.py', 'Ejecutando pruebas del sistema')
    else:
        print("⚠️ Script de pruebas no encontrado, continuando...")
        return True

def create_quick_start_script():
    """Crear script de inicio rápido"""
    print("\n📜 Creando script de inicio rápido...")
    
    script_content = '''@echo off
echo 🚀 Iniciando ARIA...
python aria_servidor_superbase.py
pause
'''
    
    try:
        with open('INICIAR_ARIA.bat', 'w') as f:
            f.write(script_content)
        print("✅ Creado: INICIAR_ARIA.bat")
        
        # También crear versión PowerShell
        ps_content = '''# 🚀 Iniciador ARIA PowerShell
Write-Host "🤖 Iniciando ARIA..." -ForegroundColor Green
python aria_servidor_superbase.py
Read-Host "Presiona ENTER para cerrar"
'''
        
        with open('INICIAR_ARIA.ps1', 'w', encoding='utf-8') as f:
            f.write(ps_content)
        print("✅ Creado: INICIAR_ARIA.ps1")
        
        return True
        
    except Exception as e:
        print(f"❌ Error creando scripts: {e}")
        return False

def start_aria():
    """Iniciar ARIA automáticamente"""
    print("\n🚀 PASO 6: Iniciando ARIA...")
    
    print("🎉 ¡Configuración completada!")
    print("\n¿Quieres iniciar ARIA ahora? (s/n): ", end="")
    
    try:
        respuesta = input().lower().strip()
        if respuesta in ['s', 'si', 'sí', 'y', 'yes']:
            print("\n🤖 Iniciando ARIA...")
            print("📝 Para detener el servidor, presiona Ctrl+C")
            time.sleep(2)
            
            # Iniciar servidor
            os.system('python aria_servidor_superbase.py')
            return True
        else:
            print("\n✅ Configuración completada")
            print("🚀 Para iniciar ARIA más tarde:")
            print("   • Windows: Doble clic en INICIAR_ARIA.bat")
            print("   • PowerShell: .\\INICIAR_ARIA.ps1") 
            print("   • Manual: python aria_servidor_superbase.py")
            return True
            
    except KeyboardInterrupt:
        print("\n⏹️ Cancelado por el usuario")
        return True

def main():
    """Función principal del configurador"""
    print_banner()
    
    # Verificar Python
    if not check_python_version():
        print("❌ Versión de Python incompatible")
        return False
    
    # Lista de pasos
    pasos = [
        ("Instalar dependencias", install_dependencies),
        ("Verificar Supabase", check_environment_variables),
        ("Configurar base de datos", run_database_schema),
        ("Inicializar conocimiento", initialize_knowledge),
        ("Probar sistema", test_system),
        ("Crear scripts de inicio", create_quick_start_script)
    ]
    
    pasos_exitosos = 0
    
    for nombre, funcion in pasos:
        try:
            if funcion():
                pasos_exitosos += 1
                print(f"✅ {nombre} - COMPLETADO")
            else:
                print(f"❌ {nombre} - FALLÓ")
                
                # Preguntar si continuar
                print(f"\n⚠️ {nombre} falló. ¿Continuar de todos modos? (s/n): ", end="")
                respuesta = input().lower().strip()
                if respuesta not in ['s', 'si', 'sí', 'y', 'yes']:
                    print("❌ Configuración cancelada")
                    return False
        except KeyboardInterrupt:
            print("\n⏹️ Configuración cancelada por el usuario")
            return False
        except Exception as e:
            print(f"❌ Error en {nombre}: {e}")
    
    # Resultado final
    print("\n" + "=" * 50)
    print("📊 RESUMEN DE CONFIGURACIÓN")
    print("=" * 50)
    print(f"Pasos completados: {pasos_exitosos}/{len(pasos)}")
    
    if pasos_exitosos >= len(pasos) * 0.8:  # 80% éxito
        print("🎉 ¡CONFIGURACIÓN EXITOSA!")
        print("✅ ARIA está listo para usar")
        
        # Intentar iniciar ARIA
        return start_aria()
    else:
        print("❌ Configuración incompleta")
        print("🔧 Revisa los errores arriba y vuelve a intentar")
        return False

if __name__ == "__main__":
    try:
        success = main()
        if success:
            print("\n🎉 ¡ARIA configurado exitosamente!")
        else:
            print("\n❌ Configuración falló")
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n⏹️ Configuración cancelada")
        sys.exit(1)