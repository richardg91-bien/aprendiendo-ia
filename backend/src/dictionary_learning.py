"""
Sistema de Aprendizaje Automático desde Diccionario
Permite a ARIA aprender palabras y significados automáticamente
"""

import sqlite3
import json
import requests
import time
import random
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import threading
import logging

class DictionaryLearningSystem:
    def __init__(self, db_path="backend/data/aria_knowledge.db"):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Configuración del sistema
        self.learning_enabled = True
        self.max_words_per_session = 10
        self.learning_interval = 300  # 5 minutos entre sesiones
        self.confidence_threshold = 0.7
        
        # APIs de diccionario (gratuitas)
        self.dictionary_apis = [
            "https://api.dictionaryapi.dev/api/v2/entries/en/",
            "https://api.wordnik.com/v4/word.json/"
        ]
        
        # Estado del sistema
        self.last_learning_session = None
        self.words_learned_today = 0
        self.learning_thread = None
        self.stop_learning = False
        
        # Inicializar base de datos
        self.init_dictionary_database()
        
        # Configurar logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        
        print("📚 Sistema de Aprendizaje de Diccionario inicializado")
    
    def init_dictionary_database(self):
        """Inicializar tablas específicas para el diccionario"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Tabla de palabras del diccionario
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS dictionary_words (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                word TEXT UNIQUE NOT NULL,
                definition TEXT NOT NULL,
                part_of_speech TEXT,
                pronunciation TEXT,
                example_usage TEXT,
                etymology TEXT,
                synonyms TEXT,
                antonyms TEXT,
                difficulty_level INTEGER DEFAULT 1,
                frequency_score REAL DEFAULT 0.0,
                confidence_score REAL DEFAULT 1.0,
                source TEXT DEFAULT 'auto_learning',
                learned_date DATETIME DEFAULT CURRENT_TIMESTAMP,
                last_used DATETIME DEFAULT CURRENT_TIMESTAMP,
                usage_count INTEGER DEFAULT 0
            )
        """)
        
        # Tabla de categorías semánticas
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS semantic_categories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                category_name TEXT UNIQUE NOT NULL,
                description TEXT,
                word_count INTEGER DEFAULT 0,
                created_date DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Tabla de relaciones entre palabras
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS word_relations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                word1_id INTEGER,
                word2_id INTEGER,
                relation_type TEXT, -- synonym, antonym, related, etc.
                strength REAL DEFAULT 1.0,
                FOREIGN KEY (word1_id) REFERENCES dictionary_words (id),
                FOREIGN KEY (word2_id) REFERENCES dictionary_words (id)
            )
        """)
        
        # Tabla de aprendizaje automático
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS learning_sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_date DATETIME DEFAULT CURRENT_TIMESTAMP,
                words_learned INTEGER,
                success_rate REAL,
                time_spent INTEGER, -- en segundos
                source TEXT
            )
        """)
        
        conn.commit()
        conn.close()
    
    def start_automatic_learning(self):
        """Iniciar el aprendizaje automático en segundo plano"""
        if self.learning_thread and self.learning_thread.is_alive():
            self.logger.info("El aprendizaje automático ya está en ejecución")
            return
        
        self.stop_learning = False
        self.learning_thread = threading.Thread(target=self._learning_loop, daemon=True)
        self.learning_thread.start()
        self.logger.info("🚀 Aprendizaje automático iniciado")
    
    def stop_automatic_learning(self):
        """Detener el aprendizaje automático"""
        self.stop_learning = True
        if self.learning_thread:
            self.learning_thread.join(timeout=5)
        self.logger.info("⏹️ Aprendizaje automático detenido")
    
    def _learning_loop(self):
        """Bucle principal de aprendizaje automático"""
        while not self.stop_learning:
            try:
                if self._should_learn():
                    self._perform_learning_session()
                
                # Esperar antes de la siguiente sesión
                time.sleep(self.learning_interval)
                
            except Exception as e:
                self.logger.error(f"Error en sesión de aprendizaje: {e}")
                time.sleep(60)  # Esperar 1 minuto antes de reintentar
    
    def _should_learn(self) -> bool:
        """Determinar si debería realizar una sesión de aprendizaje"""
        now = datetime.now()
        
        # Verificar si es un buen momento para aprender
        if self.last_learning_session:
            time_since_last = now - self.last_learning_session
            if time_since_last.total_seconds() < self.learning_interval:
                return False
        
        # Verificar límite diario
        if self.words_learned_today >= 50:  # Límite diario
            return False
        
        # Verificar si hay palabras nuevas que aprender
        unknown_words = self._get_unknown_words_from_conversations()
        return len(unknown_words) > 0
    
    def _perform_learning_session(self):
        """Realizar una sesión de aprendizaje"""
        session_start = time.time()
        words_learned = 0
        
        try:
            # Obtener palabras desconocidas de conversaciones recientes
            unknown_words = self._get_unknown_words_from_conversations()
            
            # Seleccionar palabras para aprender
            words_to_learn = unknown_words[:self.max_words_per_session]
            
            for word in words_to_learn:
                if self.stop_learning:
                    break
                
                success = self._learn_word(word)
                if success:
                    words_learned += 1
                    self.words_learned_today += 1
                
                # Pequeña pausa entre palabras
                time.sleep(1)
            
            # Registrar sesión
            session_time = int(time.time() - session_start)
            success_rate = words_learned / len(words_to_learn) if words_to_learn else 0
            
            self._record_learning_session(words_learned, success_rate, session_time)
            self.last_learning_session = datetime.now()
            
            self.logger.info(f"📖 Sesión completada: {words_learned} palabras aprendidas")
            
        except Exception as e:
            self.logger.error(f"Error en sesión de aprendizaje: {e}")
    
    def _get_unknown_words_from_conversations(self) -> List[str]:
        """Obtener palabras desconocidas de conversaciones recientes"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Obtener conversaciones recientes
        cursor.execute("""
            SELECT user_input, aria_response FROM conversations 
            WHERE timestamp > datetime('now', '-1 day')
            ORDER BY timestamp DESC LIMIT 100
        """)
        
        conversations = cursor.fetchall()
        conn.close()
        
        # Extraer palabras únicas
        all_words = set()
        for user_input, aria_response in conversations:
            words = self._extract_words(user_input + " " + aria_response)
            all_words.update(words)
        
        # Filtrar palabras ya conocidas
        unknown_words = []
        for word in all_words:
            if not self._is_word_known(word) and self._is_valid_word(word):
                unknown_words.append(word)
        
        return list(unknown_words)[:50]  # Limitar a 50 palabras
    
    def _extract_words(self, text: str) -> List[str]:
        """Extraer palabras válidas del texto"""
        import re
        
        # Limpiar y tokenizar
        text = re.sub(r'[^\w\s]', ' ', text.lower())
        words = text.split()
        
        # Filtrar palabras válidas (3+ caracteres, no números)
        valid_words = []
        for word in words:
            if len(word) >= 3 and word.isalpha() and not word.isdigit():
                valid_words.append(word)
        
        return valid_words
    
    def _is_word_known(self, word: str) -> bool:
        """Verificar si una palabra ya está en la base de datos"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT 1 FROM dictionary_words WHERE word = ?", (word.lower(),))
        result = cursor.fetchone()
        
        conn.close()
        return result is not None
    
    def _is_valid_word(self, word: str) -> bool:
        """Verificar si una palabra es válida para aprender"""
        # Filtrar palabras muy comunes o no útiles
        common_words = {
            'the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of',
            'with', 'by', 'from', 'this', 'that', 'these', 'those', 'a', 'an',
            'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has',
            'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should',
            'may', 'might', 'can', 'must', 'shall', 'i', 'you', 'he', 'she',
            'it', 'we', 'they', 'me', 'him', 'her', 'us', 'them', 'my', 'your',
            'his', 'her', 'its', 'our', 'their'
        }
        
        return word.lower() not in common_words and len(word) >= 3
    
    def _learn_word(self, word: str) -> bool:
        """Aprender una palabra específica usando APIs de diccionario"""
        try:
            word_data = self._fetch_word_definition(word)
            if word_data:
                self._store_word_data(word_data)
                return True
            return False
        except Exception as e:
            self.logger.error(f"Error aprendiendo palabra '{word}': {e}")
            return False
    
    def _fetch_word_definition(self, word: str) -> Optional[Dict]:
        """Obtener definición de palabra desde API"""
        try:
            # Intentar con API gratuita de diccionario
            url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
            response = requests.get(url, timeout=5)  # Reducir timeout
            
            if response.status_code == 200:
                data = response.json()
                if data and len(data) > 0:
                    entry = data[0]
                    
                    # Extraer información relevante
                    word_info = {
                        'word': entry.get('word', word).lower(),
                        'pronunciation': self._extract_pronunciation(entry),
                        'meanings': []
                    }
                    
                    # Procesar significados
                    for meaning in entry.get('meanings', []):
                        part_of_speech = meaning.get('partOfSpeech', '')
                        definitions = meaning.get('definitions', [])
                        
                        for definition in definitions[:2]:  # Máximo 2 definiciones
                            word_info['meanings'].append({
                                'part_of_speech': part_of_speech,
                                'definition': definition.get('definition', ''),
                                'example': definition.get('example', ''),
                                'synonyms': definition.get('synonyms', []),
                                'antonyms': definition.get('antonyms', [])
                            })
                    
                    return word_info
            
        except requests.exceptions.Timeout:
            self.logger.warning(f"Timeout obteniendo definición para '{word}' - saltando")
        except requests.exceptions.RequestException as e:
            self.logger.warning(f"Error de conexión para '{word}': {e}")
        except Exception as e:
            self.logger.warning(f"Error general obteniendo definición para '{word}': {e}")
        
        return None
    
    def _extract_pronunciation(self, entry: Dict) -> str:
        """Extraer pronunciación de la entrada del diccionario"""
        phonetics = entry.get('phonetics', [])
        for phonetic in phonetics:
            if 'text' in phonetic:
                return phonetic['text']
        return ""
    
    def _store_word_data(self, word_data: Dict):
        """Almacenar datos de palabra en la base de datos"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        word = word_data['word']
        pronunciation = word_data.get('pronunciation', '')
        
        # Combinar todas las definiciones
        definitions = []
        examples = []
        synonyms = set()
        antonyms = set()
        parts_of_speech = set()
        
        for meaning in word_data.get('meanings', []):
            if meaning['definition']:
                definitions.append(f"({meaning['part_of_speech']}) {meaning['definition']}")
            if meaning['example']:
                examples.append(meaning['example'])
            synonyms.update(meaning.get('synonyms', []))
            antonyms.update(meaning.get('antonyms', []))
            parts_of_speech.add(meaning['part_of_speech'])
        
        # Preparar datos para insertar
        definition_text = "; ".join(definitions)
        example_text = "; ".join(examples)
        synonyms_text = ", ".join(list(synonyms)[:10])  # Limitar sinónimos
        antonyms_text = ", ".join(list(antonyms)[:10])  # Limitar antónimos
        part_of_speech = ", ".join(parts_of_speech)
        
        # Insertar palabra
        cursor.execute("""
            INSERT OR REPLACE INTO dictionary_words 
            (word, definition, part_of_speech, pronunciation, example_usage, 
             synonyms, antonyms, confidence_score, source, learned_date)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            word, definition_text, part_of_speech, pronunciation,
            example_text, synonyms_text, antonyms_text,
            0.9, 'api_dictionary', datetime.now()
        ))
        
        conn.commit()
        conn.close()
    
    def _record_learning_session(self, words_learned: int, success_rate: float, time_spent: int):
        """Registrar sesión de aprendizaje"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO learning_sessions 
            (words_learned, success_rate, time_spent, source)
            VALUES (?, ?, ?, ?)
        """, (words_learned, success_rate, time_spent, 'automatic'))
        
        conn.commit()
        conn.close()
    
    def get_word_definition(self, word: str) -> Optional[Dict]:
        """Obtener definición de una palabra de la base de datos"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT word, definition, part_of_speech, pronunciation, 
                   example_usage, synonyms, antonyms, confidence_score
            FROM dictionary_words 
            WHERE word = ?
        """, (word.lower(),))
        
        result = cursor.fetchone()
        conn.close()
        
        if result:
            return {
                'word': result[0],
                'definition': result[1],
                'part_of_speech': result[2],
                'pronunciation': result[3],
                'example': result[4],
                'synonyms': result[5],
                'antonyms': result[6],
                'confidence': result[7]
            }
        
        return None
    
    def get_learning_stats(self) -> Dict:
        """Obtener estadísticas del aprendizaje"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Contar palabras totales
        cursor.execute("SELECT COUNT(*) FROM dictionary_words")
        total_words = cursor.fetchone()[0]
        
        # Palabras aprendidas hoy
        cursor.execute("""
            SELECT COUNT(*) FROM dictionary_words 
            WHERE DATE(learned_date) = DATE('now')
        """)
        words_today = cursor.fetchone()[0]
        
        # Última sesión
        cursor.execute("""
            SELECT session_date, words_learned, success_rate 
            FROM learning_sessions 
            ORDER BY session_date DESC LIMIT 1
        """)
        last_session = cursor.fetchone()
        
        conn.close()
        
        return {
            'total_words': total_words,
            'words_learned_today': words_today,
            'learning_enabled': self.learning_enabled,
            'last_session': {
                'date': last_session[0] if last_session else None,
                'words_learned': last_session[1] if last_session else 0,
                'success_rate': last_session[2] if last_session else 0
            }
        }
    
    def search_related_words(self, query: str, limit: int = 5) -> List[Dict]:
        """Buscar palabras relacionadas"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT word, definition, part_of_speech, confidence_score
            FROM dictionary_words 
            WHERE word LIKE ? OR definition LIKE ? 
            ORDER BY confidence_score DESC, usage_count DESC
            LIMIT ?
        """, (f"%{query}%", f"%{query}%", limit))
        
        results = cursor.fetchall()
        conn.close()
        
        return [
            {
                'word': result[0],
                'definition': result[1],
                'part_of_speech': result[2],
                'confidence': result[3]
            }
            for result in results
        ]
    
    def update_word_usage(self, word: str):
        """Actualizar contador de uso de una palabra"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            UPDATE dictionary_words 
            SET usage_count = usage_count + 1, last_used = CURRENT_TIMESTAMP
            WHERE word = ?
        """, (word.lower(),))
        
        conn.commit()
        conn.close()

# Instancia global del sistema
dictionary_learning = DictionaryLearningSystem()