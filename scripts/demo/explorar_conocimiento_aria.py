"""
🤖 ARIA - Explorador de Conocimiento Aprendido
==============================================

Muestra de dónde está aprendiendo ARIA
"""

import sqlite3
import json
from datetime import datetime

def explore_aria_knowledge():
    """Explora qué ha aprendido ARIA y de dónde"""
    
    print("🧠 ANÁLISIS DEL CONOCIMIENTO DE ARIA")
    print("=" * 50)
    
    try:
        conn = sqlite3.connect('data/aria_auto_learning.db')
        cursor = conn.cursor()
        
        # 1. Estadísticas generales
        print("📊 ESTADÍSTICAS GENERALES:")
        cursor.execute('SELECT COUNT(*) FROM auto_learned_knowledge')
        total_knowledge = cursor.fetchone()[0]
        print(f"   • Total de conocimientos: {total_knowledge}")
        
        cursor.execute('SELECT COUNT(DISTINCT topic) FROM auto_learned_knowledge')
        unique_topics = cursor.fetchone()[0]
        print(f"   • Temas únicos: {unique_topics}")
        
        cursor.execute('SELECT AVG(confidence_score) FROM auto_learned_knowledge')
        avg_confidence = cursor.fetchone()[0]
        print(f"   • Confianza promedio: {avg_confidence:.2%}")
        
        print()
        
        # 2. Temas por popularidad
        print("📚 TEMAS POR POPULARIDAD:")
        cursor.execute('''
            SELECT topic, COUNT(*) as count 
            FROM auto_learned_knowledge 
            GROUP BY topic 
            ORDER BY count DESC
        ''')
        
        topics = cursor.fetchall()
        for i, (topic, count) in enumerate(topics, 1):
            print(f"   {i}. {topic}: {count} conocimientos")
        
        print()
        
        # 3. Últimos conocimientos aprendidos
        print("🆕 ÚLTIMOS 5 CONOCIMIENTOS APRENDIDOS:")
        cursor.execute('''
            SELECT topic, content, confidence_score, learned_at 
            FROM auto_learned_knowledge 
            ORDER BY learned_at DESC 
            LIMIT 5
        ''')
        
        recent_knowledge = cursor.fetchall()
        for i, (topic, content_json, confidence, learned_at) in enumerate(recent_knowledge, 1):
            try:
                content_obj = json.loads(content_json)
                content_type = content_obj.get('type', 'unknown')
                content_text = content_obj.get('content', 'Sin contenido')
                
                print(f"\n   {i}. Tema: {topic}")
                print(f"      Tipo: {content_type}")
                print(f"      Contenido: {content_text}")
                print(f"      Confianza: {confidence:.1%}")
                print(f"      Aprendido: {learned_at}")
                
            except json.JSONDecodeError:
                print(f"   {i}. {topic} - Error decodificando contenido")
        
        print()
        
        # 4. Tipos de conocimiento
        print("🎯 TIPOS DE CONOCIMIENTO:")
        cursor.execute('''
            SELECT content FROM auto_learned_knowledge
        ''')
        
        all_content = cursor.fetchall()
        type_counts = {}
        
        for (content_json,) in all_content:
            try:
                content_obj = json.loads(content_json)
                content_type = content_obj.get('type', 'unknown')
                type_counts[content_type] = type_counts.get(content_type, 0) + 1
            except:
                type_counts['error'] = type_counts.get('error', 0) + 1
        
        for content_type, count in sorted(type_counts.items(), key=lambda x: x[1], reverse=True):
            print(f"   • {content_type}: {count} elementos")
        
        conn.close()
        
        print()
        print("🔍 FUENTE DEL CONOCIMIENTO:")
        print("   📝 ARIA está aprendiendo de:")
        print("   • Templates de conocimiento predefinidos")
        print("   • Temas tecnológicos específicos:")
        print("     - Inteligencia artificial")
        print("     - Machine learning")  
        print("     - Programación Python")
        print("     - Desarrollo web")
        print("     - Neurociencia")
        print("     - Robótica")
        print("     - Blockchain")
        print("     - Ciberseguridad")
        print()
        print("   🎲 Método de generación:")
        print("   • Selecciona temas aleatoriamente")
        print("   • Genera tipos de conocimiento:")
        print("     - Definiciones")
        print("     - Aplicaciones")
        print("     - Tendencias")
        print("     - Beneficios")
        print("   • Asigna confianza variable (50%-90%)")
        print("   • Almacena en base de datos SQLite")
        
    except Exception as e:
        print(f"❌ Error accediendo a la base de datos: {e}")

if __name__ == "__main__":
    explore_aria_knowledge()