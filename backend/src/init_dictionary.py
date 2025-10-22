"""
Script de inicialización para la base de datos de diccionario de ARIA
Carga palabras básicas para comenzar el aprendizaje
"""

import sys
from pathlib import Path

# Agregar el directorio src al path para imports
backend_src = Path(__file__).parent
sys.path.insert(0, str(backend_src))

from dictionary_learning import DictionaryLearningSystem
import sqlite3
import json
from datetime import datetime

def init_dictionary_with_basic_words(db_path="backend/data/aria_knowledge.db"):
    """Inicializar diccionario con palabras básicas en español"""
    
    # Primero inicializar el sistema para crear las tablas
    print("📚 Inicializando sistema de aprendizaje de diccionario...")
    dictionary_system = DictionaryLearningSystem(db_path)
    print("✅ Sistema inicializado correctamente")
    
    # Palabras básicas en español con definiciones
    basic_words = [
        {
            "word": "aprender",
            "definition": "Adquirir conocimiento, habilidades o actitudes mediante estudio, experiencia o enseñanza",
            "part_of_speech": "verbo",
            "example": "Los niños aprenden jugando",
            "synonyms": "estudiar, asimilar, memorizar"
        },
        {
            "word": "inteligencia",
            "definition": "Capacidad de entender, comprender, resolver problemas y adaptarse a nuevas situaciones",
            "part_of_speech": "sustantivo",
            "example": "La inteligencia artificial está transformando el mundo",
            "synonyms": "intelecto, ingenio, sabiduría"
        },
        {
            "word": "conocimiento",
            "definition": "Información, comprensión y habilidades que se adquieren a través de la experiencia o educación",
            "part_of_speech": "sustantivo",
            "example": "El conocimiento es poder",
            "synonyms": "saber, sabiduría, erudición"
        },
        {
            "word": "artificial",
            "definition": "Hecho por el ser humano en lugar de ocurrir naturalmente",
            "part_of_speech": "adjetivo",
            "example": "Las flores artificiales no necesitan agua",
            "synonyms": "sintético, fabricado, simulado",
            "antonyms": "natural, orgánico"
        },
        {
            "word": "sistema",
            "definition": "Conjunto de elementos relacionados que funcionan como un todo organizado",
            "part_of_speech": "sustantivo",
            "example": "El sistema nervioso controla el cuerpo",
            "synonyms": "conjunto, estructura, organización"
        },
        {
            "word": "respuesta",
            "definition": "Reacción o contestación a una pregunta, situación o estímulo",
            "part_of_speech": "sustantivo",
            "example": "La respuesta fue inmediata",
            "synonyms": "contestación, replica, reacción"
        },
        {
            "word": "pregunta",
            "definition": "Expresión que busca obtener información o una respuesta",
            "part_of_speech": "sustantivo",
            "example": "Hizo una pregunta muy interesante",
            "synonyms": "cuestión, interrogante, consulta"
        },
        {
            "word": "conversación",
            "definition": "Intercambio de ideas, opiniones o sentimientos mediante el habla",
            "part_of_speech": "sustantivo",
            "example": "Tuvieron una conversación muy amena",
            "synonyms": "diálogo, charla, plática"
        },
        {
            "word": "memoria",
            "definition": "Capacidad de retener y recordar información, experiencias o conocimientos",
            "part_of_speech": "sustantivo",
            "example": "Tiene una memoria excepcional",
            "synonyms": "recuerdo, retentiva, reminiscencia"
        },
        {
            "word": "algoritmo",
            "definition": "Conjunto de reglas o instrucciones definidas para resolver un problema",
            "part_of_speech": "sustantivo",
            "example": "El algoritmo resuelve el problema eficientemente",
            "synonyms": "procedimiento, método, proceso"
        },
        {
            "word": "datos",
            "definition": "Información que puede ser procesada o transmitida por un sistema",
            "part_of_speech": "sustantivo",
            "example": "Los datos muestran una tendencia clara",
            "synonyms": "información, registros, hechos"
        },
        {
            "word": "tecnología",
            "definition": "Aplicación de conocimientos científicos para crear herramientas y sistemas útiles",
            "part_of_speech": "sustantivo",
            "example": "La tecnología ha cambiado nuestras vidas",
            "synonyms": "técnica, innovación, desarrollo"
        },
        {
            "word": "análisis",
            "definition": "Examen detallado de algo para comprender su naturaleza o estructura",
            "part_of_speech": "sustantivo",
            "example": "El análisis reveló datos importantes",
            "synonyms": "estudio, examen, investigación"
        },
        {
            "word": "procesamiento",
            "definition": "Acción de procesar o transformar datos o información",
            "part_of_speech": "sustantivo",
            "example": "El procesamiento de la información fue rápido",
            "synonyms": "tratamiento, elaboración, transformación"
        },
        {
            "word": "comprensión",
            "definition": "Capacidad de entender el significado o importancia de algo",
            "part_of_speech": "sustantivo",
            "example": "Su comprensión del tema es profunda",
            "synonyms": "entendimiento, percepción, asimilación"
        }
    ]
    
    # Crear directorio si no existe
    Path(db_path).parent.mkdir(parents=True, exist_ok=True)
    
    # Conectar a la base de datos
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Insertar palabras básicas
    inserted_count = 0
    for word_data in basic_words:
        try:
            cursor.execute("""
                INSERT OR IGNORE INTO dictionary_words 
                (word, definition, part_of_speech, example_usage, synonyms, antonyms,
                 confidence_score, source, learned_date)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                word_data['word'],
                word_data['definition'],
                word_data['part_of_speech'],
                word_data.get('example', ''),
                word_data.get('synonyms', ''),
                word_data.get('antonyms', ''),
                1.0,  # Alta confianza para palabras básicas
                'manual_init',
                datetime.now()
            ))
            
            if cursor.rowcount > 0:
                inserted_count += 1
                
        except Exception as e:
            print(f"Error insertando palabra '{word_data['word']}': {e}")
    
    conn.commit()
    conn.close()
    
    print(f"✅ Diccionario inicializado con {inserted_count} palabras básicas")
    return inserted_count

if __name__ == "__main__":
    init_dictionary_with_basic_words()