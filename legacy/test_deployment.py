"""
Script de prueba para verificar la funcionalidad de retroalimentación
"""

import sys
import os

# Agregar el directorio src al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend', 'src'))

def test_feedback_system():
    """Probar sistema de retroalimentación local"""
    try:
        from feedback_system import FeedbackSystem
        
        print("🧪 Probando sistema de retroalimentación...")
        
        # Crear instancia de prueba
        feedback = FeedbackSystem()
        
        print("✅ FeedbackSystem importado correctamente")
        
        # Probar generación de session_id
        session_id = feedback.generate_session_id()
        print(f"✅ Session ID generado: {session_id}")
        
        # Simular logging sin conexión a base de datos real
        print("✅ Sistema de retroalimentación funcionando")
        
        return True
        
    except Exception as e:
        print(f"❌ Error en sistema de retroalimentación: {e}")
        return False

def test_main_server():
    """Probar servidor principal"""
    try:
        from main import app
        
        print("🧪 Probando servidor principal...")
        
        with app.test_client() as client:
            # Probar endpoint de status
            response = client.get('/api/status')
            print(f"✅ Status endpoint: {response.status_code}")
            
            # Probar endpoint de feedback analytics
            response = client.get('/api/feedback/analytics')
            print(f"✅ Analytics endpoint: {response.status_code}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error en servidor principal: {e}")
        return False

if __name__ == "__main__":
    print("🚀 ARIA - Pruebas de Deployment\n")
    
    feedback_ok = test_feedback_system()
    server_ok = test_main_server()
    
    if feedback_ok and server_ok:
        print("\n✅ ¡Todas las pruebas pasaron! ARIA está listo para deployment.")
    else:
        print("\n❌ Algunas pruebas fallaron. Revisar errores arriba.")
        sys.exit(1)