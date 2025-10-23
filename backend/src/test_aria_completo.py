#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🧪 ARIA - Script de Pruebas Completas
Valida que todas las funcionalidades del servidor ARIA funcionen correctamente
"""

import requests
import json
import time
import sys
from datetime import datetime

# Configuración
BASE_URL = "http://localhost:8000"
TEST_TIMEOUT = 5

def print_test_header(title):
    """Imprime cabecera de prueba"""
    print(f"\n{'='*60}")
    print(f"🧪 {title}")
    print('='*60)

def print_success(message):
    """Imprime mensaje de éxito"""
    print(f"✅ {message}")

def print_error(message):
    """Imprime mensaje de error"""
    print(f"❌ {message}")

def print_info(message):
    """Imprime información"""
    print(f"ℹ️ {message}")

def test_server_connection():
    """Prueba la conectividad básica del servidor"""
    print_test_header("CONECTIVIDAD DEL SERVIDOR")
    
    try:
        response = requests.get(f"{BASE_URL}/", timeout=TEST_TIMEOUT)
        if response.status_code == 200:
            print_success("Servidor accesible en puerto 8000")
            print_success("Interfaz web carga correctamente")
            return True
        else:
            print_error(f"Servidor responde con código: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print_error("No se puede conectar al servidor")
        print_info("Asegúrate de que ARIA esté ejecutándose en puerto 8000")
        return False
    except Exception as e:
        print_error(f"Error de conexión: {e}")
        return False

def test_api_status():
    """Prueba el endpoint de estado"""
    print_test_header("API DE ESTADO")
    
    try:
        response = requests.get(f"{BASE_URL}/api/status", timeout=TEST_TIMEOUT)
        
        if response.status_code == 200:
            data = response.json()
            print_success("Endpoint /api/status responde correctamente")
            
            # Verificar estructura de respuesta
            required_fields = ["status", "mode", "version", "timestamp", "components", "stats"]
            for field in required_fields:
                if field in data:
                    print_success(f"Campo '{field}' presente")
                else:
                    print_error(f"Campo '{field}' faltante")
            
            # Mostrar información del estado
            print_info(f"Estado: {data.get('status', 'N/A')}")
            print_info(f"Versión: {data.get('version', 'N/A')}")
            print_info(f"Modo: {data.get('mode', 'N/A')}")
            
            components = data.get('components', {})
            print_info(f"Flask: {'✅' if components.get('flask') else '❌'}")
            print_info(f"CORS: {'✅' if components.get('cors') else '❌'}")
            print_info(f"IA Simple: {'✅' if components.get('simple_ai') else '❌'}")
            
            return True
        else:
            print_error(f"API status responde con código: {response.status_code}")
            return False
            
    except Exception as e:
        print_error(f"Error probando API status: {e}")
        return False

def test_api_chat():
    """Prueba el endpoint de chat"""
    print_test_header("API DE CHAT")
    
    test_messages = [
        "Hola ARIA, ¿cómo estás?",
        "¿Qué puedes hacer?",
        "¿Qué has aprendido?",
        "Explícame sobre inteligencia artificial"
    ]
    
    successful_chats = 0
    
    for i, message in enumerate(test_messages, 1):
        try:
            payload = {"message": message}
            response = requests.post(
                f"{BASE_URL}/api/chat", 
                json=payload, 
                timeout=TEST_TIMEOUT
            )
            
            if response.status_code == 200:
                data = response.json()
                print_success(f"Chat {i}: '{message[:30]}...' → Respuesta recibida")
                
                # Verificar que hay respuesta
                if 'response' in data and data['response']:
                    print_info(f"Respuesta ({len(data['response'])} caracteres)")
                    successful_chats += 1
                else:
                    print_error(f"Chat {i}: Respuesta vacía")
            else:
                print_error(f"Chat {i}: Código de error {response.status_code}")
                
        except Exception as e:
            print_error(f"Chat {i}: Error - {e}")
    
    print_info(f"Conversaciones exitosas: {successful_chats}/{len(test_messages)}")
    return successful_chats > 0

def test_api_knowledge():
    """Prueba el endpoint de conocimiento"""
    print_test_header("API DE CONOCIMIENTO")
    
    try:
        response = requests.get(f"{BASE_URL}/api/knowledge", timeout=TEST_TIMEOUT)
        
        if response.status_code == 200:
            data = response.json()
            print_success("Endpoint /api/knowledge responde correctamente")
            
            if 'knowledge_base' in data:
                knowledge_count = len(data['knowledge_base'])
                print_success(f"Base de conocimiento contiene {knowledge_count} conceptos")
                
                if knowledge_count > 0:
                    sample_concepts = list(data['knowledge_base'].keys())[:3]
                    print_info(f"Conceptos de ejemplo: {', '.join(sample_concepts)}")
                
            return True
        else:
            print_error(f"Knowledge API error: {response.status_code}")
            return False
            
    except Exception as e:
        print_error(f"Error probando knowledge API: {e}")
        return False

def test_api_history():
    """Prueba el endpoint de historial"""
    print_test_header("API DE HISTORIAL")
    
    try:
        response = requests.get(f"{BASE_URL}/api/history", timeout=TEST_TIMEOUT)
        
        if response.status_code == 200:
            data = response.json()
            print_success("Endpoint /api/history responde correctamente")
            
            if 'conversations' in data:
                conversation_count = len(data['conversations'])
                total_count = data.get('total_count', 0)
                print_success(f"Mostrando {conversation_count} de {total_count} conversaciones")
                
                if conversation_count > 0:
                    print_info(f"Primera conversación: {data['conversations'][0].get('timestamp', 'N/A')}")
                
            return True
        else:
            print_error(f"History API error: {response.status_code}")
            return False
            
    except Exception as e:
        print_error(f"Error probando history API: {e}")
        return False

def test_api_learning():
    """Prueba el endpoint de aprendizaje"""
    print_test_header("API DE APRENDIZAJE")
    
    test_concept = {
        "concept": "testing",
        "description": "Proceso de verificar que el software funciona correctamente"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/learn", 
            json=test_concept, 
            timeout=TEST_TIMEOUT
        )
        
        if response.status_code == 200:
            data = response.json()
            print_success("Endpoint /api/learn funciona correctamente")
            print_success(f"Concepto 'testing' enseñado exitosamente")
            print_info(f"Total conocimiento: {data.get('total_knowledge', 'N/A')} conceptos")
            return True
        else:
            print_error(f"Learn API error: {response.status_code}")
            return False
            
    except Exception as e:
        print_error(f"Error probando learn API: {e}")
        return False

def run_performance_test():
    """Prueba de rendimiento básica"""
    print_test_header("PRUEBA DE RENDIMIENTO")
    
    start_time = time.time()
    successful_requests = 0
    total_requests = 10
    
    print_info(f"Enviando {total_requests} requests al endpoint /api/status...")
    
    for i in range(total_requests):
        try:
            response = requests.get(f"{BASE_URL}/api/status", timeout=TEST_TIMEOUT)
            if response.status_code == 200:
                successful_requests += 1
        except:
            pass
    
    end_time = time.time()
    duration = end_time - start_time
    
    print_success(f"Requests exitosos: {successful_requests}/{total_requests}")
    print_info(f"Tiempo total: {duration:.2f} segundos")
    print_info(f"Promedio: {duration/total_requests:.2f} segundos por request")
    
    if successful_requests == total_requests and duration < 10:
        print_success("Rendimiento satisfactorio")
        return True
    else:
        print_error("Rendimiento por debajo de lo esperado")
        return False

def main():
    """Función principal de pruebas"""
    print("🧪 ARIA - SUITE DE PRUEBAS COMPLETAS")
    print("="*60)
    print(f"⏰ Iniciado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🎯 Objetivo: {BASE_URL}")
    
    # Lista de pruebas
    tests = [
        ("Conectividad", test_server_connection),
        ("API Estado", test_api_status),
        ("API Chat", test_api_chat),
        ("API Conocimiento", test_api_knowledge),
        ("API Historial", test_api_history),
        ("API Aprendizaje", test_api_learning),
        ("Rendimiento", run_performance_test)
    ]
    
    # Ejecutar pruebas
    results = []
    
    for test_name, test_function in tests:
        try:
            result = test_function()
            results.append((test_name, result))
        except Exception as e:
            print_error(f"Error ejecutando {test_name}: {e}")
            results.append((test_name, False))
    
    # Resumen final
    print_test_header("RESUMEN DE RESULTADOS")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {test_name}")
    
    print(f"\n📊 Resultado Final: {passed}/{total} pruebas pasaron")
    
    if passed == total:
        print_success("🎉 ¡TODAS LAS PRUEBAS EXITOSAS!")
        print_success("🚀 ARIA está funcionando perfectamente")
    else:
        print_error(f"⚠️ {total - passed} pruebas fallaron")
        print_error("🔧 Revisa los errores arriba para más detalles")
    
    print(f"\n⏰ Pruebas completadas: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    return passed == total

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⏹️ Pruebas interrumpidas por el usuario")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Error fatal en las pruebas: {e}")
        sys.exit(1)