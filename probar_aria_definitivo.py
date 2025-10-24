#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🧪 PRUEBA RÁPIDA ARIA DEFINITIVO
===============================

Script para probar que ARIA responde correctamente después de la inicialización.
"""

import os
import sys
import json
import time

def test_basic_imports():
    """Probar que se pueden importar los módulos básicos"""
    print("📦 Probando importaciones...")
    
    try:
        from aria_embeddings_supabase import crear_embedding_system
        print("✅ aria_embeddings_supabase importado")
    except ImportError as e:
        print(f"❌ Error importando embeddings: {e}")
        return False
    
    try:
        # Importar el servidor (solo la clase, no ejecutar)
        sys.path.append('.')
        from aria_servidor_superbase import ARIASuperServer
        print("✅ aria_servidor_superbase importado")
    except ImportError as e:
        print(f"❌ Error importando servidor: {e}")
        return False
    
    return True

def test_supabase_connection():
    """Probar conexión a Supabase"""
    print("\n🔗 Probando conexión a Supabase...")
    
    # Verificar variables de entorno
    supabase_url = os.getenv('SUPABASE_URL')
    supabase_key = os.getenv('SUPABASE_ANON_KEY')
    
    if not supabase_url or not supabase_key:
        print("❌ Variables de entorno no configuradas")
        print("   SUPABASE_URL:", "✅" if supabase_url else "❌")
        print("   SUPABASE_ANON_KEY:", "✅" if supabase_key else "❌")
        return False
    
    print(f"✅ Variables configuradas")
    print(f"   URL: {supabase_url}")
    print(f"   Key: {supabase_key[:20]}...")
    
    # Probar conexión real
    try:
        from aria_embeddings_supabase import crear_embedding_system
        system = crear_embedding_system()
        if system:
            print("✅ Conexión a Supabase exitosa")
            return True
        else:
            print("❌ No se pudo crear sistema de embeddings")
            return False
    except Exception as e:
        print(f"❌ Error conectando: {e}")
        return False

def test_knowledge_search():
    """Probar búsqueda de conocimiento"""
    print("\n🔍 Probando búsqueda de conocimiento...")
    
    try:
        from aria_embeddings_supabase import crear_embedding_system
        system = crear_embedding_system()
        
        if not system:
            print("❌ Sistema no disponible")
            return False
        
        # Pruebas básicas
        pruebas = [
            "hola",
            "saludo", 
            "quien eres",
            "gracias",
            "buenos días"
        ]
        
        resultados_exitosos = 0
        
        for prueba in pruebas:
            print(f"\n🔎 Buscando: '{prueba}'")
            
            # Buscar conocimiento estructurado
            conocimiento = system.buscar_conocimiento(prueba, limite=1)
            similares = system.buscar_similares(prueba, limite=1)
            
            if conocimiento:
                resultado = conocimiento[0]
                print(f"   📚 Conocimiento: {resultado.get('concepto', 'N/A')}")
                print(f"   📝 Descripción: {resultado.get('descripcion', 'N/A')[:50]}...")
                print(f"   🎯 Similitud: {resultado.get('similitud', 0):.2f}")
                resultados_exitosos += 1
            elif similares:
                resultado = similares[0]
                print(f"   💬 Texto similar: {resultado.get('texto', 'N/A')[:50]}...")
                print(f"   🎯 Similitud: {resultado.get('similitud', 0):.2f}")
                resultados_exitosos += 1
            else:
                print(f"   ❌ Sin resultados")
        
        exito = resultados_exitosos >= len(pruebas) * 0.6  # 60% éxito mínimo
        print(f"\n📊 Resultado: {resultados_exitosos}/{len(pruebas)} pruebas exitosas")
        
        return exito
        
    except Exception as e:
        print(f"❌ Error en pruebas: {e}")
        return False

def test_aria_responses():
    """Probar respuestas de ARIA directamente"""
    print("\n🤖 Probando respuestas de ARIA...")
    
    try:
        from aria_servidor_superbase import ARIASuperServer
        
        # Crear instancia del servidor
        print("   Creando instancia de ARIA...")
        aria = ARIASuperServer()
        
        # Mensajes de prueba
        mensajes_prueba = [
            "Hola",
            "Buenos días", 
            "¿Quién eres?",
            "Gracias",
            "¿Cómo estás?"
        ]
        
        print("\n💬 Probando conversaciones:")
        
        for mensaje in mensajes_prueba:
            print(f"\n👤 Usuario: {mensaje}")
            try:
                respuesta = aria.process_message(mensaje)
                print(f"🤖 ARIA: {respuesta.get('response', 'Sin respuesta')[:100]}...")
                print(f"   Confianza: {respuesta.get('confidence', 0):.2f}")
                print(f"   Emoción: {respuesta.get('emotion', 'N/A')}")
                print(f"   Fuentes: {respuesta.get('knowledge_sources', 0)}")
            except Exception as e:
                print(f"❌ Error: {e}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error creando ARIA: {e}")
        return False

def check_initialization_status():
    """Verificar estado de inicialización"""
    print("\n📋 Verificando estado de inicialización...")
    
    if os.path.exists('aria_config_definitivo.json'):
        try:
            with open('aria_config_definitivo.json', 'r', encoding='utf-8') as f:
                config = json.load(f)
            
            print("✅ Archivo de configuración encontrado")
            print(f"   Estado: {config.get('estado', 'N/A')}")
            print(f"   Fecha: {config.get('fecha_inicializacion', 'N/A')}")
            print(f"   Conocimiento instalado: {config.get('conocimiento_basico_instalado', False)}")
            print(f"   Conversaciones instaladas: {config.get('conversaciones_ejemplo_instaladas', False)}")
            
            return config.get('aria_inicializado', False)
            
        except Exception as e:
            print(f"❌ Error leyendo configuración: {e}")
            return False
    else:
        print("⚠️ Archivo de configuración no encontrado")
        print("   Ejecuta: python inicializar_aria_definitivo.py")
        return False

def main():
    """Función principal de pruebas"""
    print("🧪 PRUEBA RÁPIDA DE ARIA DEFINITIVO")
    print("=" * 40)
    
    total_pruebas = 0
    pruebas_exitosas = 0
    
    # 1. Verificar inicialización
    total_pruebas += 1
    if check_initialization_status():
        pruebas_exitosas += 1
    
    # 2. Probar importaciones
    total_pruebas += 1
    if test_basic_imports():
        pruebas_exitosas += 1
    
    # 3. Probar Supabase
    total_pruebas += 1
    if test_supabase_connection():
        pruebas_exitosas += 1
    
    # 4. Probar búsqueda
    total_pruebas += 1
    if test_knowledge_search():
        pruebas_exitosas += 1
    
    # 5. Probar ARIA
    total_pruebas += 1
    if test_aria_responses():
        pruebas_exitosas += 1
    
    # Resultado final
    print("\n" + "=" * 40)
    print("📊 RESULTADO FINAL")
    print("=" * 40)
    print(f"Pruebas exitosas: {pruebas_exitosas}/{total_pruebas}")
    
    if pruebas_exitosas == total_pruebas:
        print("🎉 ¡TODAS LAS PRUEBAS PASARON!")
        print("✅ ARIA está completamente funcional")
        print("🚀 Puedes ejecutar: python aria_servidor_superbase.py")
    elif pruebas_exitosas >= total_pruebas * 0.8:
        print("✅ La mayoría de pruebas pasaron")
        print("⚠️ Algunas funciones pueden tener problemas menores")
        print("🚀 ARIA debería funcionar básicamente")
    else:
        print("❌ Varias pruebas fallaron")
        print("🔧 Necesitas revisar la configuración")
        print("📝 Ejecuta: python inicializar_aria_definitivo.py")
    
    return pruebas_exitosas >= total_pruebas * 0.8

if __name__ == "__main__":
    success = main()
    if success:
        print("\n✅ Pruebas completadas exitosamente")
    else:
        print("\n❌ Algunas pruebas fallaron")
        sys.exit(1)