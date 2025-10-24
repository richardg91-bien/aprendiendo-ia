#!/usr/bin/env python3
"""
🧪 SCRIPT DE PRUEBA PARA VERIFICAR EL SISTEMA RAG
================================================

Prueba directa del sistema RAG sin depender del servidor web.
"""

import os
import sys
from datetime import datetime

# Agregar el directorio del proyecto al path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_rag_directly():
    """Probar el sistema RAG directamente"""
    
    print("🧪 PROBANDO SISTEMA RAG DIRECTAMENTE")
    print("=" * 50)
    
    try:
        # Importar los módulos necesarios
        from aria_rag_system import create_rag_system
        from aria_enhanced_connector import get_enhanced_connector
        
        print("✅ Módulos importados correctamente")
        
        # Crear conexiones
        cloud_connector = get_enhanced_connector()
        print("✅ Conector cloud inicializado")
        
        # Crear sistema RAG
        rag_system = create_rag_system(cloud_connector=cloud_connector)
        print("✅ Sistema RAG inicializado")
        
        # Consultas de prueba
        test_queries = [
            "la ciudad de roma",
            "roma",
            "imperio romano",
            "italia",
            "coliseo",
            "¿qué es la inteligencia artificial?",
            "explícame el amor",
            "programación en python"
        ]
        
        print(f"\n🔍 Probando {len(test_queries)} consultas...")
        
        for i, query in enumerate(test_queries, 1):
            print(f"\n--- PRUEBA {i}/8: '{query}' ---")
            
            try:
                # Generar respuesta RAG
                start_time = datetime.now()
                rag_response = rag_system.generate_rag_response(query)
                elapsed_time = (datetime.now() - start_time).total_seconds()
                
                print(f"⏱️  Tiempo: {elapsed_time:.2f}s")
                print(f"🎯 Confianza: {rag_response.confidence:.2f}")
                print(f"📊 Fuentes: {len(rag_response.sources)}")
                print(f"🔧 Método: {rag_response.generation_method}")
                print(f"📝 Respuesta:")
                print(f"   {rag_response.answer[:200]}...")
                
                if rag_response.sources:
                    print("📚 Fuentes utilizadas:")
                    for source in rag_response.sources[:3]:
                        print(f"   • {source.get('source', 'unknown')} (conf: {source.get('confidence', 0):.2f})")
                
                print("✅ Prueba exitosa")
                
            except Exception as e:
                print(f"❌ Error en prueba: {e}")
                import traceback
                traceback.print_exc()
        
        print(f"\n🎉 PRUEBAS COMPLETADAS")
        
    except Exception as e:
        print(f"❌ Error general: {e}")
        import traceback
        traceback.print_exc()

def test_local_database():
    """Probar la base de datos local directamente"""
    
    print("\n🗄️ PROBANDO BASE DE DATOS LOCAL")
    print("=" * 40)
    
    try:
        import sqlite3
        from pathlib import Path
        
        db_path = Path("config/knowledge_base.db")
        
        if not db_path.exists():
            print("❌ Base de datos no encontrada")
            return
        
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Contar registros
        cursor.execute("SELECT COUNT(*) FROM knowledge")
        total_count = cursor.fetchone()[0]
        print(f"📊 Total registros: {total_count}")
        
        # Buscar sobre Roma
        cursor.execute("""
            SELECT concept, description, category 
            FROM knowledge 
            WHERE concept LIKE '%roma%' OR description LIKE '%roma%'
        """)
        
        roma_results = cursor.fetchall()
        print(f"\n🏛️ Resultados sobre Roma: {len(roma_results)}")
        
        for concept, description, category in roma_results:
            print(f"   • {concept} ({category})")
            print(f"     {description[:100]}...")
        
        # Listar todas las categorías
        cursor.execute("SELECT DISTINCT category FROM knowledge")
        categories = [row[0] for row in cursor.fetchall()]
        print(f"\n📑 Categorías disponibles: {', '.join(categories)}")
        
        conn.close()
        print("✅ Base de datos funcionando correctamente")
        
    except Exception as e:
        print(f"❌ Error con base de datos: {e}")

def main():
    """Función principal"""
    print("🚀 VERIFICACIÓN COMPLETA DEL SISTEMA RAG")
    print("=" * 60)
    
    # Probar base de datos local
    test_local_database()
    
    # Probar sistema RAG completo
    test_rag_directly()
    
    print("\n" + "=" * 60)
    print("🎯 DIAGNÓSTICO COMPLETADO")

if __name__ == "__main__":
    main()