#!/usr/bin/env python3
"""
🌍 MEJORAR CONOCIMIENTO GEOGRÁFICO E HISTÓRICO PARA ARIA
======================================================

Agregar información específica sobre ciudades, países, historia
para que ARIA pueda responder mejor sobre consultas geográficas.
"""

import os
import sys
import sqlite3
from datetime import datetime
from pathlib import Path

# Agregar el directorio del proyecto al path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def expand_geographic_knowledge():
    """Expandir base de conocimiento con información geográfica"""
    
    print("🌍 Expandiendo conocimiento geográfico...")
    
    # Conectar a la base de conocimiento local
    db_path = Path("config/knowledge_base.db")
    
    if not db_path.exists():
        print("❌ Base de datos de conocimiento no encontrada")
        return False
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Conocimiento geográfico e histórico
    geographic_knowledge = [
        # CIUDADES IMPORTANTES
        ("Roma", "Roma es la capital de Italia y una de las ciudades más importantes de la historia. Fundada según la leyenda en 753 a.C., fue el centro del Imperio Romano. Conocida como 'La Ciudad Eterna', alberga el Vaticano, el Coliseo, el Foro Romano y numerosos sitios arqueológicos. Tiene una población de aproximadamente 2.9 millones de habitantes y es un importante centro político, cultural y religioso.", "geografia", "roma,italia,ciudad,historia,imperio_romano"),
        
        ("París", "París es la capital de Francia, conocida como 'La Ciudad de la Luz'. Con una población metropolitana de más de 12 millones, es un centro mundial de arte, moda, gastronomía y cultura. Alberga monumentos icónicos como la Torre Eiffel, el Louvre, Notre-Dame y los Campos Elíseos.", "geografia", "paris,francia,ciudad,cultura,arte"),
        
        ("Londres", "Londres es la capital del Reino Unido y una de las ciudades más influyentes del mundo. Con una historia de más de 2000 años, es un centro financiero global y cultural. Famosa por el Big Ben, el Parlamento, el Palacio de Buckingham y sus museos de clase mundial.", "geografia", "londres,reino_unido,ciudad,historia,cultura"),
        
        ("Madrid", "Madrid es la capital de España, ubicada en el centro de la península ibérica. Es el centro político, económico y cultural del país, conocida por sus museos (Prado, Reina Sofía), parques (Retiro), y vida nocturna vibrante.", "geografia", "madrid,españa,ciudad,cultura,museos"),
        
        ("Nueva York", "Nueva York es la ciudad más poblada de Estados Unidos, conocida como 'La Gran Manzana'. Es un centro global de finanzas, arte, moda, investigación, tecnología y entretenimiento. Famosa por Manhattan, la Estatua de la Libertad, Central Park y Broadway.", "geografia", "nueva_york,estados_unidos,ciudad,finanzas,cultura"),
        
        # PAÍSES
        ("Italia", "Italia es un país europeo en forma de bota en el Mediterráneo. Cuna del Imperio Romano y el Renacimiento, es famosa por su arte, arquitectura, gastronomía y cultura. Capital: Roma. Ciudades importantes: Milán, Nápoles, Florencia, Venecia.", "geografia", "italia,pais,europa,mediterraneo,cultura"),
        
        ("Francia", "Francia es un país de Europa Occidental, conocido por su cultura, gastronomía, moda y arte. Es una república con una rica historia que incluye la Revolución Francesa. Capital: París. Regiones famosas: Provenza, Normandía, Riviera Francesa.", "geografia", "francia,pais,europa,cultura,historia"),
        
        ("España", "España es un país en la península ibérica, conocido por su diversidad cultural, historia, arquitectura y gastronomía. Comprende diferentes regiones con lenguas y tradiciones propias. Capital: Madrid. Ciudades importantes: Barcelona, Sevilla, Valencia.", "geografia", "españa,pais,europa,cultura,historia"),
        
        # HISTORIA ANTIGUA
        ("Imperio Romano", "El Imperio Romano fue una de las civilizaciones más poderosas de la historia, que se extendió desde Gran Bretaña hasta el Medio Oriente entre los siglos I a.C. y V d.C. Su capital era Roma, y su legado incluye el derecho, la arquitectura, el idioma latín y la organización política.", "historia", "imperio_romano,roma,historia_antigua,civilizacion"),
        
        ("Antigua Roma", "La Antigua Roma abarca desde la fundación de la ciudad (753 a.C.) hasta la caída del Imperio Romano de Occidente (476 d.C.). Pasó por tres períodos: Monarquía, República e Imperio. Sus contribuciones incluyen el derecho romano, la ingeniería, la arquitectura y la organización militar.", "historia", "roma,historia_antigua,republica,imperio"),
        
        # ARQUITECTURA E HISTORIA
        ("Coliseo", "El Coliseo de Roma es un anfiteatro de la época del Imperio Romano, construido entre 72-80 d.C. Es uno de los monumentos más famosos del mundo, donde se celebraban combates de gladiadores y espectáculos públicos. Puede albergar entre 50,000 y 80,000 espectadores.", "arquitectura", "coliseo,roma,anfiteatro,gladiadores,monumento"),
        
        ("Foro Romano", "El Foro Romano era el centro de la vida política, comercial y judicial de la antigua Roma. Contiene ruinas de varios edificios gubernamentales importantes de la época del Imperio Romano, incluyendo templos, basilicas y arcos triunfales.", "arquitectura", "foro_romano,roma,ruinas,politica,comercio"),
        
        ("Vaticano", "El Vaticano es el estado soberano más pequeño del mundo, ubicado en Roma. Es la sede de la Iglesia Católica y residencia del Papa. Alberga la Capilla Sixtina, los Museos Vaticanos y la Basílica de San Pedro, con obras de arte de Miguel Ángel, Rafael y Bernini.", "religion", "vaticano,roma,papa,iglesia_catolica,arte"),
        
        # CULTURA Y GASTRONOMÍA
        ("Gastronomía Italiana", "La gastronomía italiana es una de las más influyentes del mundo, conocida por la pasta, pizza, risotto, gelato y vinos. Cada región tiene especialidades únicas. Es Patrimonio Cultural Inmaterial de la UNESCO.", "cultura", "italia,gastronomia,pasta,pizza,cocina"),
        
        ("Renacimiento", "El Renacimiento fue un movimiento cultural que se originó en Italia en el siglo XIV y se extendió por Europa. Marcó la transición de la Edad Media a la Edad Moderna, caracterizado por el resurgimiento del arte, la ciencia y la cultura clásica.", "historia", "renacimiento,italia,arte,cultura,historia"),
        
        # GEOGRAFÍA FÍSICA
        ("Mediterráneo", "El Mar Mediterráneo es un mar interior conectado al Océano Atlántico, rodeado por Europa, África y Asia. Ha sido crucial para el comercio, la cultura y la historia de las civilizaciones que lo rodean, incluyendo griegos, romanos y árabes.", "geografia", "mediterraneo,mar,europa,africa,comercio"),
        
        ("Península Ibérica", "La Península Ibérica está ubicada en el suroeste de Europa, ocupada principalmente por España y Portugal. Separada del resto de Europa por los Pirineos y rodeada por el Atlántico y el Mediterráneo.", "geografia", "peninsula_iberica,españa,portugal,europa"),
        
        # ARTE Y MONUMENTOS
        ("Torre Eiffel", "La Torre Eiffel es una torre de hierro de 330 metros en París, construida por Gustave Eiffel para la Exposición Universal de 1889. Es el símbolo más reconocible de Francia y uno de los monumentos más visitados del mundo.", "arquitectura", "torre_eiffel,paris,francia,monumento,hierro"),
        
        ("Sagrada Familia", "La Sagrada Familia es una basílica católica en Barcelona, diseñada por Antoni Gaudí. Su construcción comenzó en 1882 y continúa hasta hoy. Es famosa por su arquitectura modernista única y es Patrimonio de la Humanidad de la UNESCO.", "arquitectura", "sagrada_familia,barcelona,gaudi,basilica,modernismo"),
        
        # CIENCIA E HISTORIA
        ("Astronomía Antigua", "La astronomía en la antigüedad fue desarrollada por civilizaciones como los babilonios, egipcios, griegos y romanos. Contribuyeron al desarrollo de calendarios, navegación y comprensión del cosmos.", "ciencia", "astronomia,historia,antiguedad,calendario,cosmos")
    ]
    
    # Insertar el nuevo conocimiento
    inserted_count = 0
    for concept, description, category, tags in geographic_knowledge:
        try:
            # Verificar si ya existe
            cursor.execute("SELECT id FROM knowledge WHERE concept = ?", (concept,))
            if cursor.fetchone() is None:
                cursor.execute("""
                    INSERT INTO knowledge (concept, description, category, tags, updated_at)
                    VALUES (?, ?, ?, ?, ?)
                """, (concept, description, category, tags, datetime.now().isoformat()))
                inserted_count += 1
                print(f"  ✅ Agregado: {concept}")
            else:
                print(f"  ⚠️ Ya existe: {concept}")
        except Exception as e:
            print(f"  ❌ Error con {concept}: {e}")
    
    conn.commit()
    
    # Verificar total
    cursor.execute("SELECT COUNT(*) FROM knowledge")
    total_count = cursor.fetchone()[0]
    
    conn.close()
    
    print(f"\n📊 Resumen:")
    print(f"   📈 Conceptos agregados: {inserted_count}")
    print(f"   📚 Total en base de datos: {total_count}")
    
    return inserted_count > 0

def improve_rag_response_for_geographic_queries():
    """Mejorar las respuestas RAG para consultas geográficas"""
    
    print("\n🔧 Mejorando sistema RAG para consultas geográficas...")
    
    # Crear archivo de configuración específica para geografía
    geographic_config = {
        "geographic_query_patterns": [
            # Patrones de ciudades
            {"pattern": r"\b(ciudad|municipio|urbe)\s+de\s+(\w+)", "type": "city"},
            {"pattern": r"\b(la\s+ciudad\s+de|en\s+la\s+ciudad)\s+(\w+)", "type": "city"},
            {"pattern": r"\b(\w+)\s+(ciudad|capital)", "type": "city"},
            
            # Patrones de países
            {"pattern": r"\b(país|nación|estado)\s+de\s+(\w+)", "type": "country"},
            {"pattern": r"\b(en|de)\s+(\w+)\s+(país|nación)", "type": "country"},
            
            # Patrones históricos
            {"pattern": r"\b(historia|origen|fundación)\s+de\s+(\w+)", "type": "history"},
            {"pattern": r"\b(antiguo|antigua)\s+(\w+)", "type": "ancient"},
            
            # Patrones geográficos
            {"pattern": r"\b(geografía|ubicación|localización)\s+de\s+(\w+)", "type": "geography"},
            {"pattern": r"\b(dónde\s+está|dónde\s+se\s+encuentra)\s+(\w+)", "type": "location"},
        ],
        
        "city_synonyms": {
            "roma": ["rome", "capital italiana", "ciudad eterna"],
            "paris": ["parís", "ciudad de la luz", "capital francesa"],
            "madrid": ["capital española", "capital de españa"],
            "barcelona": ["ciudad condal", "barcelona"],
            "londres": ["london", "capital británica"]
        },
        
        "enhanced_search_terms": {
            "roma": ["roma", "imperio romano", "coliseo", "foro romano", "vaticano", "italia"],
            "paris": ["paris", "francia", "torre eiffel", "louvre", "ciudad luz"],
            "madrid": ["madrid", "españa", "capital", "península ibérica"],
            "londres": ["londres", "reino unido", "big ben", "parlamento"],
            "barcelona": ["barcelona", "cataluña", "sagrada familia", "gaudí"]
        }
    }
    
    config_path = Path("config/geographic_enhancement.json")
    with open(config_path, 'w', encoding='utf-8') as f:
        import json
        json.dump(geographic_config, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Configuración geográfica guardada: {config_path}")
    return True

def test_geographic_knowledge():
    """Probar el conocimiento geográfico expandido"""
    
    print("\n🧪 Probando conocimiento geográfico...")
    
    db_path = Path("config/knowledge_base.db")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Consultas de prueba
    test_queries = [
        "roma",
        "ciudad de roma",
        "imperio romano",
        "italia",
        "coliseo"
    ]
    
    for query in test_queries:
        cursor.execute("""
            SELECT concept, description 
            FROM knowledge 
            WHERE concept LIKE ? OR description LIKE ? OR tags LIKE ?
            LIMIT 3
        """, (f"%{query}%", f"%{query}%", f"%{query}%"))
        
        results = cursor.fetchall()
        print(f"\n🔍 Consulta: '{query}'")
        print(f"   📊 Resultados: {len(results)}")
        
        for concept, description in results:
            print(f"   ✅ {concept}: {description[:100]}...")
    
    conn.close()
    
def main():
    """Función principal para expandir conocimiento geográfico"""
    
    print("🌍 EXPANDIENDO CONOCIMIENTO GEOGRÁFICO DE ARIA")
    print("=" * 60)
    
    try:
        # 1. Expandir base de conocimiento
        success1 = expand_geographic_knowledge()
        
        # 2. Mejorar configuración RAG
        success2 = improve_rag_response_for_geographic_queries()
        
        # 3. Probar conocimiento
        test_geographic_knowledge()
        
        if success1 and success2:
            print("\n🎉 CONOCIMIENTO GEOGRÁFICO EXPANDIDO EXITOSAMENTE")
            print("=" * 60)
            print("✅ Ahora ARIA puede responder sobre:")
            print("   🏛️ Roma y el Imperio Romano")
            print("   🌍 Ciudades europeas importantes")
            print("   🗺️ Geografía e historia")
            print("   🎨 Arte y arquitectura")
            print("   🍝 Cultura y gastronomía")
            
        else:
            print("\n⚠️ Algunas operaciones fallaron")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()