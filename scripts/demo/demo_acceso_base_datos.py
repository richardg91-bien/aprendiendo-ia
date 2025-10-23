"""
🗄️ ARIA - ACCESO A BASE DE DATOS PARA RESPUESTAS
=================================================

Explicación completa de cómo ARIA accede a su base de datos SQLite
para responder preguntas con conocimiento real
"""

import sqlite3
import json
import os
from datetime import datetime
from typing import List, Dict, Any

class AriaKnowledgeExplorer:
    """Explorador de la base de conocimiento de ARIA"""
    
    def __init__(self):
        self.db_path = "data/aria_advanced_learning.db"
        self.ensure_database_exists()
    
    def ensure_database_exists(self):
        """Verifica que la base de datos existe"""
        if not os.path.exists(self.db_path):
            print(f"⚠️ Base de datos no encontrada en: {self.db_path}")
            print("💡 Ejecuta primero el sistema de aprendizaje para crear datos")
            return False
        return True
    
    def show_database_structure(self):
        """Muestra la estructura de la base de datos"""
        print("=" * 80)
        print("🗄️ ESTRUCTURA DE LA BASE DE DATOS DE ARIA")
        print("=" * 80)
        
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Obtener todas las tablas
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = cursor.fetchall()
            
            print(f"📁 Archivo: {self.db_path}")
            print(f"📊 Tamaño: {os.path.getsize(self.db_path)} bytes")
            print(f"🗂️ Tablas encontradas: {len(tables)}")
            
            for table in tables:
                table_name = table[0]
                print(f"\n📋 TABLA: {table_name}")
                print("-" * 50)
                
                # Obtener estructura de la tabla
                cursor.execute(f"PRAGMA table_info({table_name})")
                columns = cursor.fetchall()
                
                for col in columns:
                    col_id, col_name, col_type, not_null, default, pk = col
                    print(f"   📝 {col_name:<20} {col_type:<15} {'(PK)' if pk else ''}")
                
                # Contar registros
                cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
                count = cursor.fetchone()[0]
                print(f"   📊 Registros: {count}")
            
            conn.close()
            return True
            
        except Exception as e:
            print(f"❌ Error accediendo a base de datos: {e}")
            return False
    
    def search_knowledge_demo(self, query: str):
        """Demuestra cómo ARIA busca conocimiento"""
        print(f"\n🔍 BÚSQUEDA EN BASE DE DATOS: '{query}'")
        print("=" * 60)
        
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # La misma consulta que usa ARIA
            print("📋 Consulta SQL ejecutada:")
            sql_query = '''
                SELECT topic, title, content, source_name, source_url, 
                       confidence_score, relevance_score, timestamp
                FROM knowledge_base 
                WHERE title LIKE ? OR content LIKE ? OR keywords LIKE ?
                ORDER BY relevance_score DESC, confidence_score DESC
                LIMIT 10
            '''
            print(sql_query)
            
            # Parámetros de búsqueda
            search_params = (f'%{query}%', f'%{query}%', f'%{query}%')
            print(f"🎯 Parámetros: {search_params}")
            
            # Ejecutar búsqueda
            cursor.execute(sql_query, search_params)
            results = cursor.fetchall()
            
            print(f"\n📊 Resultados encontrados: {len(results)}")
            
            if results:
                print("\n📚 CONOCIMIENTO ENCONTRADO:")
                print("-" * 60)
                
                for i, row in enumerate(results[:5], 1):  # Mostrar máximo 5
                    topic, title, content, source_name, source_url, confidence, relevance, timestamp = row
                    
                    print(f"\n{i}. 📖 {title}")
                    print(f"   🏷️ Tema: {topic}")
                    print(f"   🔗 Fuente: {source_name}")
                    print(f"   📊 Confianza: {confidence:.2f} | Relevancia: {relevance:.2f}")
                    print(f"   📅 Fecha: {timestamp}")
                    print(f"   📄 Contenido: {content[:200]}...")
                    if source_url:
                        print(f"   🌐 URL: {source_url}")
                
                # Mostrar cómo ARIA construiría la respuesta
                self.demonstrate_response_generation(results, query)
            else:
                print("❌ No se encontró conocimiento sobre este tema")
                print("💡 El sistema de aprendizaje necesita más tiempo para adquirir información")
            
            conn.close()
            
        except Exception as e:
            print(f"❌ Error en búsqueda: {e}")
    
    def demonstrate_response_generation(self, results, query):
        """Demuestra cómo ARIA genera respuestas basadas en su conocimiento"""
        print(f"\n🤖 CÓMO ARIA GENERARÍA UNA RESPUESTA SOBRE '{query}'")
        print("=" * 60)
        
        if not results:
            response = f"Lo siento, no tengo información suficiente sobre '{query}' en mi base de conocimiento actual."
            print(f"📝 Respuesta: {response}")
            return
        
        # Tomar los resultados más relevantes
        best_result = results[0]
        topic, title, content, source_name, source_url, confidence, relevance, timestamp = best_result
        
        print("🧠 PROCESO DE GENERACIÓN:")
        print("1️⃣ Buscar en base de conocimiento ✅")
        print("2️⃣ Ordenar por relevancia y confianza ✅")
        print("3️⃣ Seleccionar mejor resultado ✅")
        print("4️⃣ Construir respuesta contextual ✅")
        
        # Generar respuesta como lo haría ARIA
        response = f"""Basándome en mi conocimiento actualizado sobre {topic}, puedo decirte que:

{content[:300]}{'...' if len(content) > 300 else ''}

Esta información proviene de {source_name} (confianza: {confidence:.0%}) y fue obtenida el {timestamp[:10]}.
"""
        
        if source_url:
            response += f"\nPuedes verificar esta información en: {source_url}"
        
        print(f"\n💬 RESPUESTA GENERADA:")
        print("-" * 40)
        print(response)
        
        print(f"\n📊 METADATOS DE LA RESPUESTA:")
        print(f"   🎯 Nivel de confianza: {confidence:.0%}")
        print(f"   📈 Relevancia: {relevance:.0%}")
        print(f"   📚 Fuente: {source_name}")
        print(f"   📅 Actualización: {timestamp[:10]}")
    
    def show_learning_statistics(self):
        """Muestra estadísticas de aprendizaje"""
        print("\n📊 ESTADÍSTICAS DE APRENDIZAJE DE ARIA")
        print("=" * 60)
        
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Estadísticas generales
            cursor.execute("SELECT COUNT(*) FROM knowledge_base")
            total_knowledge = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(DISTINCT topic) FROM knowledge_base")
            unique_topics = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(DISTINCT source_name) FROM knowledge_base")
            unique_sources = cursor.fetchone()[0]
            
            cursor.execute("SELECT AVG(confidence_score) FROM knowledge_base")
            avg_confidence = cursor.fetchone()[0] or 0
            
            print(f"📚 Total de conocimiento: {total_knowledge} elementos")
            print(f"🏷️ Temas únicos: {unique_topics}")
            print(f"🔗 Fuentes únicas: {unique_sources}")
            print(f"📊 Confianza promedio: {avg_confidence:.2%}")
            
            # Top temas
            print(f"\n🔝 TEMAS MÁS ESTUDIADOS:")
            cursor.execute('''
                SELECT topic, COUNT(*) as count 
                FROM knowledge_base 
                GROUP BY topic 
                ORDER BY count DESC 
                LIMIT 5
            ''')
            
            for topic, count in cursor.fetchall():
                print(f"   📖 {topic}: {count} elementos")
            
            # Top fuentes
            print(f"\n🔝 FUENTES MÁS UTILIZADAS:")
            cursor.execute('''
                SELECT source_name, COUNT(*) as count 
                FROM knowledge_base 
                GROUP BY source_name 
                ORDER BY count DESC 
                LIMIT 5
            ''')
            
            for source, count in cursor.fetchall():
                print(f"   🌐 {source}: {count} elementos")
            
            # Conocimiento reciente
            print(f"\n🆕 CONOCIMIENTO MÁS RECIENTE:")
            cursor.execute('''
                SELECT title, source_name, timestamp 
                FROM knowledge_base 
                ORDER BY timestamp DESC 
                LIMIT 3
            ''')
            
            for title, source, timestamp in cursor.fetchall():
                print(f"   📰 {title[:50]}... ({source}, {timestamp[:10]})")
            
            conn.close()
            
        except Exception as e:
            print(f"❌ Error obteniendo estadísticas: {e}")
    
    def simulate_conversation(self):
        """Simula una conversación con ARIA usando su base de datos"""
        print("\n💬 SIMULACIÓN DE CONVERSACIÓN CON ARIA")
        print("=" * 60)
        
        conversations = [
            "¿Qué sabes sobre inteligencia artificial?",
            "Háblame sobre machine learning",
            "¿Cuáles son las últimas noticias de tecnología?",
            "¿Qué papers científicos has leído recientemente?"
        ]
        
        for question in conversations:
            print(f"\n👤 Usuario: {question}")
            print(f"🤖 ARIA: ", end="")
            
            # Extraer palabras clave de la pregunta
            keywords = question.lower().replace("¿", "").replace("?", "")
            for word in ["sobre", "de", "qué", "cuáles", "son", "las", "los", "me", "te"]:
                keywords = keywords.replace(word, "")
            
            main_keywords = [w.strip() for w in keywords.split() if len(w.strip()) > 3]
            
            if main_keywords:
                search_term = main_keywords[0]  # Tomar primera palabra clave
                
                try:
                    conn = sqlite3.connect(self.db_path)
                    cursor = conn.cursor()
                    
                    cursor.execute('''
                        SELECT title, content, source_name, confidence_score
                        FROM knowledge_base 
                        WHERE title LIKE ? OR content LIKE ? OR keywords LIKE ?
                        ORDER BY confidence_score DESC, relevance_score DESC
                        LIMIT 1
                    ''', (f'%{search_term}%', f'%{search_term}%', f'%{search_term}%'))
                    
                    result = cursor.fetchone()
                    
                    if result:
                        title, content, source, confidence = result
                        
                        # Generar respuesta contextual
                        if "últimas noticias" in question.lower():
                            response = f"Según mi base de conocimiento actualizada, una noticia reciente es: '{title}'. {content[:150]}... (Fuente: {source}, confianza: {confidence:.0%})"
                        elif "papers" in question.lower() or "científicos" in question.lower():
                            response = f"He procesado información científica reciente, incluyendo: '{title}'. {content[:150]}... Esta información tiene alta confianza ({confidence:.0%}) al provenir de {source}."
                        else:
                            response = f"Basándome en mi conocimiento actual: {content[:200]}... Esta información proviene de {source} con {confidence:.0%} de confianza."
                        
                        print(response)
                    else:
                        print(f"No tengo información específica sobre '{search_term}' en mi base de conocimiento actual. Necesito aprender más sobre este tema.")
                    
                    conn.close()
                    
                except Exception as e:
                    print(f"Error accediendo a mi base de conocimiento: {e}")
            else:
                print("No pude identificar el tema específico de tu pregunta. ¿Podrías ser más específico?")

def main():
    """Función principal de demostración"""
    print("🤖 ARIA - CÓMO ACCEDE A SU BASE DE DATOS PARA RESPONDER")
    print("=" * 80)
    print("📅 Demostración ejecutada:", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    
    explorer = AriaKnowledgeExplorer()
    
    # 1. Mostrar estructura de base de datos
    if not explorer.show_database_structure():
        return
    
    # 2. Demostrar búsquedas
    search_terms = ["artificial intelligence", "machine learning", "technology"]
    
    for term in search_terms:
        explorer.search_knowledge_demo(term)
    
    # 3. Mostrar estadísticas
    explorer.show_learning_statistics()
    
    # 4. Simular conversación
    explorer.simulate_conversation()
    
    print("\n" + "=" * 80)
    print("🎯 RESUMEN: CÓMO ARIA RESPONDE CON SU BASE DE DATOS")
    print("=" * 80)
    print("✅ 1. Recibe pregunta del usuario")
    print("✅ 2. Extrae palabras clave de la pregunta")
    print("✅ 3. Busca en SQLite con consulta LIKE")
    print("✅ 4. Ordena por relevancia y confianza")
    print("✅ 5. Selecciona mejor resultado")
    print("✅ 6. Genera respuesta contextual")
    print("✅ 7. Incluye metadatos (fuente, confianza)")
    print("✅ 8. Proporciona URL para verificación")
    print("\n🚀 ¡ARIA responde con conocimiento REAL de su base de datos!")

if __name__ == "__main__":
    main()