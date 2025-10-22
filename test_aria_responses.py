"""
🧪 PRUEBA DE RESPUESTAS DE ARIA CON CONOCIMIENTO REAL
===================================================

Script para probar que ARIA use su conocimiento real en lugar de respuestas genéricas
"""

import requests
import json
import sys
import os

# Agregar el path del backend
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend', 'src'))

def test_aria_responses():
    """Prueba las respuestas de ARIA"""
    
    print("🧪 PROBANDO RESPUESTAS DE ARIA CON CONOCIMIENTO REAL")
    print("=" * 60)
    
    # URL del endpoint
    url = "http://localhost:8000/api/chat"
    
    # Preguntas para probar
    test_questions = [
        "¿Qué has aprendido?",
        "¿Qué sabes sobre cloud computing?",
        "¿Qué conocimiento tienes?", 
        "Háblame sobre tecnología",
        "¿Qué papers científicos has leído?",
        "¿De qué fuentes aprendes?"
    ]
    
    print("📡 Probando conexión con ARIA...")
    
    for i, question in enumerate(test_questions, 1):
        print(f"\n{i}. 👤 Usuario: {question}")
        
        try:
            response = requests.post(url, json={
                "message": question,
                "voice_enabled": False
            }, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                if data.get("success"):
                    aria_response = data.get("response", "")
                    confidence = data.get("confidence", 0)
                    
                    print(f"🤖 ARIA: {aria_response}")
                    print(f"📊 Confianza: {confidence:.0%}")
                    
                    # Verificar si es una respuesta real o genérica
                    if "Interesante. Me dijiste:" in aria_response:
                        print("⚠️ RESPUESTA GENÉRICA - Sistema básico")
                    elif "base de conocimiento" in aria_response.lower() or "arxiv" in aria_response.lower():
                        print("✅ RESPUESTA CON CONOCIMIENTO REAL - Sistema avanzado")
                    else:
                        print("🔄 RESPUESTA BÁSICA MEJORADA")
                else:
                    print(f"❌ Error: {data.get('message', 'Error desconocido')}")
            else:
                print(f"❌ Error HTTP: {response.status_code}")
                
        except requests.exceptions.ConnectionError:
            print("❌ No se pudo conectar a ARIA")
            print("💡 Asegúrate de que el backend esté ejecutándose en http://localhost:8000")
            return False
        except Exception as e:
            print(f"❌ Error: {e}")
    
    return True

def test_specific_knowledge():
    """Prueba conocimiento específico que ARIA debería tener"""
    
    print(f"\n🎯 PROBANDO CONOCIMIENTO ESPECÍFICO")
    print("=" * 60)
    
    # ARIA debería saber sobre cloud computing porque tiene ese paper
    url = "http://localhost:8000/api/chat"
    
    specific_questions = [
        "cloud computing",
        "FPGA",
        "ArXiv",
        "security",
        "technology"
    ]
    
    for question in specific_questions:
        print(f"\n🔍 Probando: '{question}'")
        
        try:
            response = requests.post(url, json={
                "message": question,
                "voice_enabled": False
            }, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                aria_response = data.get("response", "")
                confidence = data.get("confidence", 0)
                
                if "Security of Cloud FPGAs" in aria_response or "ArXiv" in aria_response:
                    print(f"✅ CONOCIMIENTO REAL ENCONTRADO")
                    print(f"📄 Respuesta: {aria_response[:200]}...")
                    print(f"📊 Confianza: {confidence:.0%}")
                else:
                    print(f"⚠️ No usó conocimiento específico")
                    print(f"📄 Respuesta: {aria_response}")
            
        except Exception as e:
            print(f"❌ Error: {e}")

def test_learning_summary():
    """Prueba el resumen de aprendizaje"""
    
    print(f"\n📚 PROBANDO RESUMEN DE APRENDIZAJE")
    print("=" * 60)
    
    # Importar directamente para probar
    try:
        from backend.src.auto_learning_advanced import aria_advanced_learning
        
        print("🧠 Probando función de resumen...")
        status = aria_advanced_learning.get_status()
        
        print(f"📊 Estado del sistema:")
        print(f"   Total de conocimiento: {status.get('total_knowledge', 0)}")
        print(f"   Sistema ejecutándose: {status.get('running', False)}")
        print(f"   Fuentes principales: {status.get('top_sources', {})}")
        print(f"   Temas principales: {status.get('top_topics', {})}")
        
        return True
        
    except ImportError:
        print("⚠️ Sistema avanzado no disponible")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    """Función principal"""
    
    print("🤖 PRUEBA COMPLETA DE ARIA - RESPUESTAS CON CONOCIMIENTO REAL")
    print("=" * 80)
    
    # 1. Probar resumen de aprendizaje
    learning_available = test_learning_summary()
    
    # 2. Probar respuestas generales
    if test_aria_responses():
        # 3. Probar conocimiento específico
        test_specific_knowledge()
        
        print(f"\n🎯 RESULTADO FINAL")
        print("=" * 40)
        
        if learning_available:
            print("✅ Sistema de aprendizaje avanzado disponible")
            print("✅ ARIA debería usar conocimiento real")
            print("📚 Conocimiento: Paper científico sobre Cloud FPGAs")
            print("🔗 Fuente: ArXiv (95% confianza)")
        else:
            print("⚠️ Sistema avanzado no disponible")
            print("🔄 ARIA usará respuestas básicas mejoradas")
        
        print(f"\n💡 PARA ACTIVAR CONOCIMIENTO REAL:")
        print("1. Asegúrate de que el backend use el sistema avanzado")
        print("2. Verifica que la base de datos tenga contenido")
        print("3. Pregunta sobre 'cloud computing' o 'tecnología'")
    
if __name__ == "__main__":
    main()