"""
Verificar conocimiento real de ARIA
"""
import sqlite3
import os

def verificar_conocimiento_aria():
    db_path = "data/aria_advanced_learning.db"
    
    if not os.path.exists(db_path):
        print("❌ Base de datos no existe")
        return
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Contar total de conocimiento
    cursor.execute("SELECT COUNT(*) FROM knowledge_base")
    total = cursor.fetchone()[0]
    print(f"📚 Total de conocimiento: {total} elementos")
    
    if total > 0:
        print("\n🧠 CONOCIMIENTO REAL QUE ARIA HA APRENDIDO:")
        print("=" * 60)
        
        cursor.execute('''
            SELECT title, content, source_name, confidence_score, timestamp 
            FROM knowledge_base 
            ORDER BY timestamp DESC 
            LIMIT 5
        ''')
        
        for i, (title, content, source, confidence, timestamp) in enumerate(cursor.fetchall(), 1):
            print(f"\n{i}. 📖 {title}")
            print(f"   🔗 Fuente: {source}")
            print(f"   📊 Confianza: {confidence:.0%}")
            print(f"   📅 Fecha: {timestamp}")
            print(f"   📄 Contenido: {content[:150]}...")
        
        print(f"\n🎯 ARIA DEBERÍA RESPONDER SOBRE ESTOS TEMAS:")
        cursor.execute("SELECT DISTINCT topic FROM knowledge_base")
        topics = [row[0] for row in cursor.fetchall()]
        for topic in topics:
            print(f"   • {topic}")
    else:
        print("⚠️ No hay conocimiento en la base de datos")
        print("💡 Necesitas ejecutar el sistema de aprendizaje primero")
    
    conn.close()

if __name__ == "__main__":
    verificar_conocimiento_aria()