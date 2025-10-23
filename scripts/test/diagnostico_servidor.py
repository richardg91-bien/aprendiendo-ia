#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔍 Diagnóstico Rápido del Servidor ARIA
Script para identificar problemas de inicio del servidor
"""

import sys
import os
import traceback
from pathlib import Path

def test_imports():
    """Prueba todas las importaciones críticas"""
    print("🔍 Probando importaciones críticas...")
    
    results = {}
    
    # Cambiar al directorio src
    src_dir = Path(__file__).parent
    sys.path.insert(0, str(src_dir))
    
    # Probar importaciones básicas
    try:
        from flask import Flask
        results['flask'] = True
        print("✅ Flask: OK")
    except Exception as e:
        results['flask'] = False
        print(f"❌ Flask: {e}")
    
    try:
        from flask_cors import CORS
        results['cors'] = True
        print("✅ CORS: OK")
    except Exception as e:
        results['cors'] = False
        print(f"❌ CORS: {e}")
    
    # Probar importaciones de ARIA
    try:
        from neural_network import neural_network
        results['neural_network'] = True
        print("✅ Neural Network: OK")
    except Exception as e:
        results['neural_network'] = False
        print(f"❌ Neural Network: {e}")
    
    try:
        from auto_learning_simple import auto_learning
        results['auto_learning'] = True
        print("✅ Auto Learning Simple: OK")
    except Exception as e:
        results['auto_learning'] = False
        print(f"❌ Auto Learning Simple: {e}")
    
    try:
        from auto_learning_advanced import aria_advanced_learning
        results['advanced_learning'] = True
        print("✅ Advanced Learning: OK")
    except Exception as e:
        results['advanced_learning'] = False
        print(f"❌ Advanced Learning: {e}")
    
    # Probar sistema de voz (que sabemos que falla)
    try:
        from voice_system import voice_system
        results['voice_system'] = True
        print("✅ Voice System: OK")
    except Exception as e:
        results['voice_system'] = False
        print(f"⚠️ Voice System: {e} (ESPERADO)")
    
    return results

def test_server_startup():
    """Prueba el inicio del servidor Flask"""
    print("\n🚀 Probando inicio del servidor Flask...")
    
    try:
        from flask import Flask
        app = Flask(__name__)
        
        @app.route('/test')
        def test():
            return "OK"
        
        print("✅ Aplicación Flask creada correctamente")
        
        # Probar si podemos vincular al puerto
        import socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex(('localhost', 8000))
        sock.close()
        
        if result == 0:
            print("⚠️ Puerto 8000 ya está en uso")
        else:
            print("✅ Puerto 8000 disponible")
            
        return True
        
    except Exception as e:
        print(f"❌ Error en servidor Flask: {e}")
        traceback.print_exc()
        return False

def test_minimal_server():
    """Crea un servidor mínimo para probar"""
    print("\n🧪 Creando servidor de prueba mínimo...")
    
    try:
        from flask import Flask, jsonify
        app = Flask(__name__)
        
        @app.route('/test')
        def test():
            return jsonify({"status": "OK", "message": "Servidor de prueba funcionando"})
        
        print("✅ Servidor de prueba creado")
        print("🌐 Iniciando en puerto 8001...")
        
        app.run(host='localhost', port=8001, debug=False)
        
    except Exception as e:
        print(f"❌ Error en servidor de prueba: {e}")
        traceback.print_exc()

def main():
    """Función principal de diagnóstico"""
    print("🔍 DIAGNÓSTICO DEL SERVIDOR ARIA")
    print("=" * 50)
    
    # Verificar directorio actual
    print(f"📁 Directorio actual: {os.getcwd()}")
    print(f"🐍 Python: {sys.executable}")
    print(f"📦 Python path: {sys.path[:3]}...")  # Primeros 3 elementos
    
    # Probar importaciones
    results = test_imports()
    
    # Contar éxitos
    success_count = sum(1 for v in results.values() if v)
    total_count = len(results)
    
    print(f"\n📊 Resultado de importaciones: {success_count}/{total_count} exitosas")
    
    if success_count >= 4:  # Flask, CORS, neural_network, auto_learning mínimo
        print("✅ Suficientes componentes para servidor básico")
        
        # Probar inicio de servidor
        if test_server_startup():
            print("\n🎯 RECOMENDACIÓN: El servidor debería funcionar")
            
            choice = input("\n¿Quieres probar un servidor mínimo en puerto 8001? (s/N): ")
            if choice.lower() == 's':
                test_minimal_server()
        else:
            print("\n❌ PROBLEMA: Servidor Flask no puede iniciarse")
    else:
        print("❌ PROBLEMA: Faltan componentes críticos")
        
        print("\n🔧 SOLUCIONES RECOMENDADAS:")
        
        if not results.get('flask'):
            print("  - Instalar Flask: pip install flask")
        if not results.get('cors'):
            print("  - Instalar CORS: pip install flask-cors")
        if not results.get('neural_network'):
            print("  - Verificar archivo neural_network.py")
        if not results.get('auto_learning'):
            print("  - Verificar archivo auto_learning_simple.py")

if __name__ == "__main__":
    main()