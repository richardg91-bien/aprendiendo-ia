#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🧪 Script de Prueba de Retroalimentación ARIA
==============================================

Script para probar y demostrar cómo ARIA se retroalimenta
con cada consulta que se le hace.

Uso:
    python test_retroalimentacion.py
"""

import requests
import json
import time
from datetime import datetime

# Configuración
ARIA_URL = "http://localhost:8000"

def test_aria_connection():
    """Probar conexión con ARIA"""
    try:
        response = requests.get(f"{ARIA_URL}/status", timeout=5)
        return response.status_code == 200
    except:
        return False

def send_test_message(message):
    """Enviar mensaje de prueba y mostrar retroalimentación"""
    try:
        print(f"📤 Enviando: '{message}'")
        
        response = requests.post(f"{ARIA_URL}/chat", 
                               json={"message": message})
        
        if response.status_code == 200:
            data = response.json()
            
            print(f"📥 Respuesta: {data.get('response', 'Sin respuesta')[:100]}...")
            
            # Mostrar retroalimentación de aprendizaje
            if 'learning_feedback' in data:
                feedback = data['learning_feedback']
                print(f"🧠 RETROALIMENTACIÓN:")
                print(f"   📊 Conceptos antes: {feedback['concepts_before']}")
                print(f"   📊 Conceptos después: {feedback['concepts_after']}")
                print(f"   🆕 Nuevos conceptos: {feedback['new_concepts_learned']}")
                print(f"   🎯 Total en cache: {feedback['total_knowledge_cache']}")
                print(f"   🎭 Sesión: {feedback['session_id']}")
            
            # Mostrar insights de aprendizaje
            if 'learning_insights' in data and data['learning_insights']:
                print(f"💡 INSIGHTS DE APRENDIZAJE:")
                for insight in data['learning_insights']:
                    print(f"   • {insight}")
            
            return True
        else:
            print(f"❌ Error: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def get_learning_stats():
    """Obtener estadísticas de aprendizaje"""
    try:
        response = requests.get(f"{ARIA_URL}/learning/monitor")
        if response.status_code == 200:
            data = response.json()
            return data if data.get('success') else None
    except:
        return None

def show_learning_stats():
    """Mostrar estadísticas actuales de aprendizaje"""
    stats = get_learning_stats()
    if stats:
        print("\n📊 ESTADÍSTICAS ACTUALES DE APRENDIZAJE:")
        learning_stats = stats['learning_stats']
        print(f"   🧠 Sistema activo: {learning_stats['learning_system_active']}")
        print(f"   📚 Conceptos en cache: {learning_stats['knowledge_cache_size']}")
        print(f"   🌐 APIs españolas: {learning_stats['spanish_apis_available']}")
        
        recent = stats.get('recent_concepts', [])
        if recent:
            print(f"   🔥 Últimos conceptos: {len(recent)}")
            for concept in recent[-3:]:  # Últimos 3
                print(f"      • {concept['concept']} (conf: {concept['confidence']:.2f})")
    else:
        print("\n❌ No se pudieron obtener estadísticas")

def main():
    """Función principal"""
    print("🧪 ARIA - Test de Retroalimentación")
    print("=" * 50)
    
    # Verificar conexión
    if not test_aria_connection():
        print("❌ Error: No se puede conectar con ARIA")
        print("💡 Ejecuta primero: cd src && python aria_servidor_superbase.py")
        return
    
    print("✅ Conexión con ARIA establecida")
    
    # Mostrar estadísticas iniciales
    show_learning_stats()
    
    # Mensajes de prueba para demostrar retroalimentación
    test_messages = [
        "Hola ARIA, soy Ricardo y estoy probando tu sistema de aprendizaje",
        "¿Qué es la inteligencia artificial?",
        "Explícame sobre machine learning y deep learning",
        "¿Cómo funciona la programación en Python?",
        "Cuéntame sobre desarrollo web con JavaScript",
        "¿Qué sabes sobre bases de datos como Supabase?",
        "Háblame sobre sistemas de embeddings",
        "¿Cómo funciona el procesamiento de lenguaje natural?"
    ]
    
    print(f"\n🎯 Realizando {len(test_messages)} consultas de prueba...")
    print("🔍 Observa cómo ARIA aprende nuevos conceptos con cada pregunta:")
    print()
    
    for i, message in enumerate(test_messages, 1):
        print(f"\n{'=' * 60}")
        print(f"PRUEBA {i}/{len(test_messages)}")
        print(f"{'=' * 60}")
        
        # Estadísticas antes
        stats_before = get_learning_stats()
        cache_before = stats_before['learning_stats']['knowledge_cache_size'] if stats_before else 0
        
        # Enviar mensaje
        success = send_test_message(message)
        
        if success:
            time.sleep(1)  # Pequeña pausa
            
            # Estadísticas después
            stats_after = get_learning_stats()
            cache_after = stats_after['learning_stats']['knowledge_cache_size'] if stats_after else 0
            
            # Mostrar cambio
            if cache_after > cache_before:
                print(f"🎉 ¡APRENDIZAJE DETECTADO! Cache: {cache_before} → {cache_after}")
            else:
                print(f"🔄 Conocimiento usado (sin nuevos conceptos)")
        
        # Pausa entre pruebas
        if i < len(test_messages):
            time.sleep(2)
    
    # Estadísticas finales
    print(f"\n{'=' * 60}")
    print("📊 RESULTADOS FINALES")
    print(f"{'=' * 60}")
    show_learning_stats()
    
    print("\n🎊 ¡Prueba de retroalimentación completada!")
    print("💡 Puedes ver el monitor en tiempo real ejecutando:")
    print("   python monitor_retroalimentacion.py")
    print("\n🌐 O usar la interfaz web en:")
    print("   http://localhost:8000")
    print("   Usa el botón '🔍 Monitor de Retroalimentación'")

if __name__ == "__main__":
    main()