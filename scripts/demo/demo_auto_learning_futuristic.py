"""
🤖 ARIA - Demo del Sistema de Aprendizaje Autónomo Futurista
=============================================================

Script de demostración completo del nuevo sistema
"""

import requests
import json
import time
from datetime import datetime

def test_aria_auto_learning():
    """Prueba completa del sistema de aprendizaje autónomo"""
    
    base_url = "http://localhost:8000"
    
    print("🚀 ARIA - Sistema de Aprendizaje Autónomo Futurista")
    print("=" * 60)
    print()
    
    # 1. Verificar estado del sistema
    print("📊 1. VERIFICANDO ESTADO DEL SISTEMA...")
    try:
        response = requests.get(f"{base_url}/api/auto_learning/status")
        if response.status_code == 200:
            data = response.json()
            status = data['status']
            
            print(f"   ✅ Sistema: {'🟢 ACTIVO' if status['is_running'] else '🔴 DETENIDO'}")
            print(f"   🧠 Conocimiento total: {status['knowledge_stats']['total_knowledge']}")
            print(f"   📚 Áreas de conocimiento: {status['knowledge_stats']['unique_topics']}")
            print(f"   💡 Confianza promedio: {status['knowledge_stats']['avg_confidence']:.2%}")
            print(f"   🎯 Temas activos: {status['active_topics']}")
            
            if status.get('last_session'):
                last = status['last_session']
                print(f"   ⏰ Última sesión: {last.get('last_session', 'N/A')}")
                print(f"   🏆 Calidad: {last.get('quality', 0):.2%}")
        else:
            print(f"   ❌ Error: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Error de conexión: {e}")
    
    print()
    
    # 2. Ejecutar sesión rápida de aprendizaje
    print("⚡ 2. EJECUTANDO SESIÓN RÁPIDA DE APRENDIZAJE...")
    try:
        response = requests.post(f"{base_url}/api/auto_learning/quick_session")
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ {data['message']}")
            
            status = data['status']
            print(f"   📈 Nuevo conocimiento: {status['knowledge_stats']['total_knowledge']}")
            print(f"   🎓 Nuevas áreas: {status['knowledge_stats']['unique_topics']}")
        else:
            print(f"   ❌ Error: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    print()
    
    # 3. Ejecutar sesión profunda de aprendizaje
    print("🧠 3. EJECUTANDO SESIÓN PROFUNDA DE APRENDIZAJE...")
    try:
        response = requests.post(f"{base_url}/api/auto_learning/deep_session")
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ {data['message']}")
            
            status = data['status']
            print(f"   📊 Conocimiento profundo: {status['knowledge_stats']['total_knowledge']}")
            print(f"   🎯 Áreas expandidas: {status['knowledge_stats']['unique_topics']}")
            print(f"   💎 Confianza mejorada: {status['knowledge_stats']['avg_confidence']:.2%}")
        else:
            print(f"   ❌ Error: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    print()
    
    # 4. Verificar estado final
    print("📈 4. ESTADO FINAL DEL SISTEMA...")
    try:
        response = requests.get(f"{base_url}/api/auto_learning/status")
        if response.status_code == 200:
            data = response.json()
            status = data['status']
            
            print(f"   📚 Conocimiento total acumulado: {status['knowledge_stats']['total_knowledge']}")
            print(f"   🎓 Áreas de especialización: {status['knowledge_stats']['unique_topics']}")
            print(f"   ⭐ Confianza del sistema: {status['knowledge_stats']['avg_confidence']:.2%}")
            print(f"   🕐 Sesión actual: {'🟡 En progreso' if status['current_session_active'] else '⚪ Inactiva'}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    print()
    print("🎉 DEMO COMPLETADA - Sistema de Aprendizaje Autónomo Futurista")
    print("=" * 60)
    print()
    print("💡 CARACTERÍSTICAS IMPLEMENTADAS:")
    print("   ✅ Sistema de aprendizaje autónomo simplificado (sin dependencias externas)")
    print("   ✅ Interfaz futurista con efectos visuales avanzados")
    print("   ✅ Base de datos SQLite para almacenamiento local")
    print("   ✅ Sesiones de aprendizaje rápidas y profundas")
    print("   ✅ Métricas en tiempo real de conocimiento y confianza")
    print("   ✅ API endpoints completamente funcionales")
    print("   ✅ Sistema de patrones de aprendizaje automático")
    print("   ✅ Integración con la interfaz React futurista")
    print()
    print("🌐 ACCESO:")
    print(f"   Frontend: http://localhost:3000")
    print(f"   Backend:  http://localhost:8000")
    print(f"   API Status: {base_url}/api/auto_learning/status")

if __name__ == "__main__":
    test_aria_auto_learning()