"""
Script de diagnóstico para ARIA
Verifica el estado de todos los componentes
"""

import requests
import json
import sys
from pathlib import Path

def test_server_connection():
    """Probar conexión al servidor"""
    try:
        response = requests.get("http://127.0.0.1:8000/api/status", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print("✅ Servidor conectado exitosamente")
            print(f"   Versión: {data.get('version', 'desconocida')}")
            print(f"   Componentes: {len(data.get('components', {}))}")
            return True
        else:
            print(f"❌ Servidor respondió con código: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error conectando al servidor: {e}")
        return False

def test_chat_functionality():
    """Probar funcionalidad de chat"""
    try:
        test_message = "Hola, ¿cómo estás?"
        response = requests.post(
            "http://127.0.0.1:8000/api/chat",
            json={"message": test_message, "voice_enabled": False},
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            if data.get("success"):
                print("✅ Sistema de chat funcionando")
                print(f"   Respuesta: {data.get('response', '')[:50]}...")
                print(f"   Confianza: {data.get('confidence', 0):.2f}")
                return True
            else:
                print(f"❌ Chat falló: {data.get('message', 'Error desconocido')}")
                return False
        else:
            print(f"❌ Chat respondió con código: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error en chat: {e}")
        return False

def test_dictionary_system():
    """Probar sistema de diccionario"""
    try:
        response = requests.get("http://127.0.0.1:8000/api/dictionary/stats", timeout=5)
        if response.status_code == 200:
            data = response.json()
            if data.get("success"):
                stats = data.get("stats", {})
                print("✅ Sistema de diccionario funcionando")
                print(f"   Palabras totales: {stats.get('total_words', 0)}")
                print(f"   Aprendidas hoy: {stats.get('words_learned_today', 0)}")
                print(f"   Estado: {'Activo' if stats.get('learning_enabled') else 'Inactivo'}")
                return True
            else:
                print(f"❌ Diccionario falló: {data.get('message', 'Error desconocido')}")
                return False
        else:
            print(f"❌ Diccionario respondió con código: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error en diccionario: {e}")
        return False

def test_word_definition():
    """Probar definición de palabras"""
    try:
        test_word = "inteligencia"
        response = requests.get(f"http://127.0.0.1:8000/api/dictionary/word/{test_word}", timeout=5)
        if response.status_code == 200:
            data = response.json()
            if data.get("success"):
                word_data = data.get("word_data", {})
                print("✅ Definición de palabras funcionando")
                print(f"   Palabra: {word_data.get('word', 'N/A')}")
                print(f"   Definición: {word_data.get('definition', 'N/A')[:50]}...")
                return True
            else:
                print(f"⚠️  Palabra '{test_word}' no encontrada en base de datos local")
                return False
        else:
            print(f"❌ Definición respondió con código: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error obteniendo definición: {e}")
        return False

def test_learning_stats():
    """Probar estadísticas de aprendizaje"""
    try:
        response = requests.get("http://127.0.0.1:8000/api/learning/stats", timeout=5)
        if response.status_code == 200:
            data = response.json()
            if data.get("success"):
                stats = data.get("stats", {})
                print("✅ Estadísticas de aprendizaje funcionando")
                print(f"   Conversaciones: {stats.get('total_conversations', 0)}")
                print(f"   Patrones aprendidos: {stats.get('learned_patterns', 0)}")
                return True
            else:
                print(f"❌ Estadísticas fallaron: {data.get('message', 'Error desconocido')}")
                return False
        else:
            print(f"❌ Estadísticas respondieron con código: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error en estadísticas: {e}")
        return False

def check_files_exist():
    """Verificar que los archivos críticos existan"""
    critical_files = [
        "backend/src/main.py",
        "backend/src/learning_system.py", 
        "backend/src/dictionary_learning.py",
        "backend/data/aria_knowledge.db"
    ]
    
    missing_files = []
    for file_path in critical_files:
        if not Path(file_path).exists():
            missing_files.append(file_path)
    
    if missing_files:
        print("❌ Archivos críticos faltantes:")
        for file in missing_files:
            print(f"   • {file}")
        return False
    else:
        print("✅ Todos los archivos críticos presentes")
        return True

def run_complete_diagnosis():
    """Ejecutar diagnóstico completo"""
    print("=" * 60)
    print("🔍 DIAGNÓSTICO COMPLETO DE ARIA")
    print("=" * 60)
    
    tests = [
        ("Archivos críticos", check_files_exist),
        ("Conexión al servidor", test_server_connection),
        ("Funcionalidad de chat", test_chat_functionality),
        ("Sistema de diccionario", test_dictionary_system),
        ("Definición de palabras", test_word_definition),
        ("Estadísticas de aprendizaje", test_learning_stats)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n🧪 Probando: {test_name}")
        print("-" * 40)
        success = test_func()
        results.append((test_name, success))
    
    print("\n" + "=" * 60)
    print("📊 RESUMEN DEL DIAGNÓSTICO")
    print("=" * 60)
    
    passed = 0
    total = len(results)
    
    for test_name, success in results:
        status = "✅ PASÓ" if success else "❌ FALLÓ"
        print(f"{status} {test_name}")
        if success:
            passed += 1
    
    print(f"\n📈 Resultado: {passed}/{total} pruebas pasaron")
    
    if passed == total:
        print("🎉 ¡ARIA está funcionando perfectamente!")
        print("\n🚀 Próximos pasos:")
        print("   1. Ir a http://127.0.0.1:8000")
        print("   2. Probar conversaciones")
        print("   3. Preguntar por definiciones")
    elif passed >= total * 0.8:
        print("⚠️  ARIA está funcionando con algunas limitaciones")
        print("   La mayoría de funcionalidades están operativas")
    else:
        print("❌ ARIA tiene problemas significativos")
        print("   Se requiere revisión técnica")
    
    return passed / total

if __name__ == "__main__":
    run_complete_diagnosis()