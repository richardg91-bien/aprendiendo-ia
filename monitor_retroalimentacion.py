#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔍 Monitor de Retroalimentación ARIA en Tiempo Real
====================================================

Script para monitorear cómo ARIA se retroalimenta con cada consulta.
Muestra en tiempo real el aprendizaje y los nuevos conceptos.

Uso:
    python monitor_retroalimentacion.py
"""

import requests
import time
import json
from datetime import datetime
import sys
import os

# Configuración
ARIA_URL = "http://localhost:8000"
REFRESH_INTERVAL = 2  # segundos

def clear_screen():
    """Limpiar pantalla"""
    os.system('cls' if os.name == 'nt' else 'clear')

def get_learning_stats():
    """Obtener estadísticas de aprendizaje"""
    try:
        response = requests.get(f"{ARIA_URL}/learning/monitor")
        return response.json() if response.status_code == 200 else None
    except:
        return None

def get_system_status():
    """Obtener estado del sistema"""
    try:
        response = requests.get(f"{ARIA_URL}/status")
        return response.json() if response.status_code == 200 else None
    except:
        return None

def format_timestamp():
    """Formatear timestamp actual"""
    return datetime.now().strftime("%H:%M:%S")

def display_monitor(stats, status):
    """Mostrar información del monitor"""
    clear_screen()
    
    print("=" * 80)
    print("🔍 ARIA - MONITOR DE RETROALIMENTACIÓN EN TIEMPO REAL")
    print("=" * 80)
    print(f"⏰ Última actualización: {format_timestamp()}")
    print()
    
    if not stats or not status:
        print("❌ Error: No se puede conectar con ARIA")
        print("💡 Asegúrate de que el servidor esté ejecutándose en http://localhost:8000")
        return
    
    # Estado del sistema
    print("📊 ESTADO DEL SISTEMA:")
    print(f"   🗄️  Super Base: {'✅ Conectado' if status.get('supabase') else '❌ Desconectado'}")
    print(f"   🧠 Sistema de Aprendizaje: {'✅ Activo' if stats['learning_stats']['learning_system_active'] else '❌ Inactivo'}")
    print(f"   🌐 APIs Españolas: {'✅ Activas' if stats['learning_stats']['spanish_apis_available'] else '❌ Inactivas'}")
    print(f"   🎭 Sesión ID: {stats['learning_stats']['session_id']}")
    print()
    
    # Estadísticas de aprendizaje
    print("🧠 ESTADÍSTICAS DE APRENDIZAJE:")
    print(f"   📚 Conceptos en Cache: {stats['learning_stats']['knowledge_cache_size']}")
    
    db_stats = stats.get('database_stats', {})
    if 'total_knowledge' in db_stats:
        print(f"   🗄️  Total en Base de Datos: {db_stats['total_knowledge']}")
    
    print()
    
    # Conceptos recientes
    recent = stats.get('recent_concepts', [])
    if recent:
        print("🔥 ÚLTIMOS CONCEPTOS APRENDIDOS:")
        for i, concept in enumerate(recent[-5:], 1):  # Últimos 5
            confidence = concept.get('confidence', 0)
            confidence_icon = "🟢" if confidence > 0.7 else "🟡" if confidence > 0.4 else "🔴"
            print(f"   {i}. {concept['concept']} {confidence_icon}")
            print(f"      📂 Categoría: {concept.get('category', 'N/A')}")
            print(f"      📈 Confianza: {confidence:.2f}")
            print(f"      🔗 Fuente: {concept.get('source', 'N/A')}")
            print()
    else:
        print("📝 No hay conceptos recientes en cache")
        print()
    
    # Adiciones recientes a BD
    if 'recent_additions' in db_stats and db_stats['recent_additions']:
        print("📊 ÚLTIMAS ADICIONES A BASE DE DATOS:")
        for i, item in enumerate(db_stats['recent_additions'][:3], 1):
            print(f"   {i}. {item.get('concept', 'N/A')}")
            print(f"      📝 {item.get('description', 'Sin descripción')[:60]}...")
            print()
    
    print("=" * 80)
    print("💡 CÓMO INTERPRETAR:")
    print("   🟢 Alta confianza (>0.7)  🟡 Media confianza (0.4-0.7)  🔴 Baja confianza (<0.4)")
    print("   📚 Cache = Conceptos temporales de la sesión")
    print("   🗄️  BD = Conocimiento persistente almacenado")
    print()
    print("🔄 Actualizando cada 2 segundos... Presiona Ctrl+C para salir")

def test_aria_connection():
    """Probar conexión con ARIA"""
    try:
        response = requests.get(f"{ARIA_URL}/status", timeout=5)
        return response.status_code == 200
    except:
        return False

def main():
    """Función principal"""
    print("🔍 Iniciando Monitor de Retroalimentación ARIA...")
    
    # Verificar conexión
    if not test_aria_connection():
        print("❌ Error: No se puede conectar con ARIA")
        print("💡 Ejecuta primero el servidor ARIA:")
        print("   cd src && python aria_servidor_superbase.py")
        sys.exit(1)
    
    print("✅ Conexión establecida")
    time.sleep(1)
    
    try:
        while True:
            stats = get_learning_stats()
            status = get_system_status()
            display_monitor(stats, status)
            time.sleep(REFRESH_INTERVAL)
            
    except KeyboardInterrupt:
        clear_screen()
        print("👋 Monitor de retroalimentación detenido")
        print("📊 Gracias por usar el monitor de ARIA")

if __name__ == "__main__":
    main()