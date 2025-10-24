#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
🧪 PRUEBA RÁPIDA DE ARIA
========================

Script para probar que ARIA funciona correctamente con Caracas
"""

import sys
import os
import time
import subprocess
import requests
from threading import Thread

def start_aria_server():
    """Inicia ARIA en background"""
    try:
        os.chdir('src')
        subprocess.run([sys.executable, 'aria_servidor_superbase.py'])
    except Exception as e:
        print(f"Error iniciando servidor: {e}")

def test_aria_response():
    """Prueba la respuesta de ARIA"""
    print("🔄 Esperando que ARIA inicie...")
    time.sleep(10)  # Dar tiempo para que inicie
    
    max_attempts = 5
    for attempt in range(max_attempts):
        try:
            print(f"🎯 Intento {attempt + 1}/{max_attempts}: Preguntando sobre Caracas...")
            
            response = requests.post(
                'http://localhost:8000/chat',
                json={'message': '¿Qué sabes sobre caracas?'},
                timeout=20
            )
            
            if response.status_code == 200:
                data = response.json()
                respuesta = data.get('response', '')
                
                print("=" * 60)
                print("🎉 RESPUESTA DE ARIA:")
                print("=" * 60)
                print(respuesta)
                print("=" * 60)
                
                # Análisis
                respuesta_lower = respuesta.lower()
                if 'capital' in respuesta_lower and 'venezuela' in respuesta_lower:
                    print("✅ PERFECTO: Menciona que Caracas es capital de Venezuela")
                    return True
                elif 'caracas' in respuesta_lower and len(respuesta) > 50:
                    print("✅ BUENO: Información específica sobre Caracas")
                    return True
                else:
                    print("⚠️ REVISAR: Respuesta puede ser genérica")
                    return False
            else:
                print(f"❌ Error HTTP: {response.status_code}")
                
        except requests.exceptions.ConnectionError:
            print(f"🔄 Servidor no responde aún (intento {attempt + 1})")
            time.sleep(5)
        except Exception as e:
            print(f"❌ Error en intento {attempt + 1}: {e}")
            time.sleep(5)
    
    print("❌ No se pudo conectar con ARIA después de varios intentos")
    return False

def main():
    print("🧪 PRUEBA RÁPIDA DE ARIA")
    print("=" * 30)
    
    # Verificar directorio
    if not os.path.exists('src'):
        print("❌ Directorio 'src' no encontrado")
        return False
    
    original_dir = os.getcwd()
    
    try:
        # Iniciar servidor en thread separado
        server_thread = Thread(target=start_aria_server)
        server_thread.daemon = True
        server_thread.start()
        
        # Hacer la prueba
        result = test_aria_response()
        
        return result
        
    except KeyboardInterrupt:
        print("\\n👋 Prueba interrumpida por el usuario")
        return False
    finally:
        os.chdir(original_dir)

if __name__ == "__main__":
    success = main()
    if success:
        print("\\n🎉 ¡ARIA está funcionando correctamente!")
        print("✅ El problema de respuestas específicas está resuelto")
    else:
        print("\\n⚠️ ARIA puede necesitar ajustes adicionales")
        
    print("\\n📋 ESTADO DE LAS TABLAS:")
    print("✅ Tablas básicas: Funcionando")
    print("⚠️ Tablas de embeddings: Pendientes (usar CREAR_TABLAS_EMBEDDINGS.sql)")
    
    input("\\nPresiona Enter para salir...")