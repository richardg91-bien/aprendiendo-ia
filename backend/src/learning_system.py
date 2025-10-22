"""
Sistema de Aprendizaje Avanzado para ARIA
Implementa aprendizaje automático similar a modelos grandes de IA
"""

import sqlite3
import json
import random
import math
from datetime import datetime
import re
from collections import defaultdict
from typing import List, Dict, Any, Tuple
import pickle
import hashlib
from pathlib import Path

class AdvancedLearningSystem:
    def __init__(self, db_path="backend/data/aria_knowledge.db"):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Configuración del sistema de aprendizaje
        self.embedding_dim = 100
        self.context_window = 10
        self.learning_rate = 0.01
        
        # Inicializar base de datos
        self.init_database()
        
        # Cargar o inicializar embeddings
        self.load_embeddings()
        
        # Sistema de memoria
        self.short_term_memory = []
        self.long_term_memory = {}
        
        # Patrones aprendidos
        self.conversation_patterns = defaultdict(list)
        self.response_templates = {}
        
        print("🧠 Sistema de Aprendizaje Avanzado inicializado")
    
    def init_database(self):
        """Inicializar base de datos SQLite para conocimiento persistente"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Tabla de conversaciones
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS conversations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_input TEXT NOT NULL,
                aria_response TEXT NOT NULL,
                context TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                feedback_score REAL DEFAULT 0.0,
                topic_category TEXT,
                sentiment REAL DEFAULT 0.0,
                confidence REAL DEFAULT 0.0
            )
        """)
        
        # Tabla de conocimiento extraído
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS knowledge_base (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                concept TEXT NOT NULL,
                definition TEXT,
                examples TEXT,
                source_conversation_id INTEGER,
                confidence_score REAL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (source_conversation_id) REFERENCES conversations (id)
            )
        """)
        
        # Tabla de patrones de respuesta
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS response_patterns (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                input_pattern TEXT NOT NULL,
                response_template TEXT NOT NULL,
                usage_count INTEGER DEFAULT 1,
                success_rate REAL DEFAULT 0.0,
                last_used DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Tabla de embeddings de palabras
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS word_embeddings (
                word TEXT PRIMARY KEY,
                embedding BLOB,
                frequency INTEGER DEFAULT 1,
                last_updated DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        conn.commit()
        conn.close()
        print("📊 Base de datos de conocimiento inicializada")
    
    def load_embeddings(self):
        """Cargar o inicializar sistema de embeddings simples"""
        self.word_vectors = {}
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT word, embedding FROM word_embeddings")
        for word, embedding_blob in cursor.fetchall():
            self.word_vectors[word] = pickle.loads(embedding_blob)
        
        conn.close()
        
        if not self.word_vectors:
            print("🔤 Inicializando sistema de embeddings...")
            self._create_basic_embeddings()
    
    def _create_basic_embeddings(self):
        """Crear embeddings básicos para palabras comunes"""
        # Palabras base del español con embeddings aleatorios normalizados
        base_words = [
            "hola", "como", "estas", "que", "tal", "bien", "mal", "si", "no",
            "gracias", "por", "favor", "ayuda", "necesito", "quiero", "puedo",
            "tiempo", "dia", "noche", "mañana", "ayer", "hoy", "cuando", "donde",
            "quien", "porque", "como", "cual", "cuanto", "hacer", "decir", "ir",
            "ver", "saber", "conocer", "tener", "ser", "estar", "dar", "venir"
        ]
        
        for word in base_words:
            # Embedding aleatorio normalizado (sin numpy)
            vector = [random.gauss(0, 1) for _ in range(self.embedding_dim)]
            norm = math.sqrt(sum(x*x for x in vector))
            vector = [x/norm if norm > 0 else 0 for x in vector]
            self.word_vectors[word] = vector
            self._save_embedding(word, vector)
    
    def _save_embedding(self, word: str, vector: list):
        """Guardar embedding en la base de datos"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        embedding_blob = pickle.dumps(vector)
        cursor.execute("""
            INSERT OR REPLACE INTO word_embeddings (word, embedding, last_updated)
            VALUES (?, ?, CURRENT_TIMESTAMP)
        """, (word, embedding_blob))
        
        conn.commit()
        conn.close()
    
    def get_sentence_embedding(self, text: str) -> list:
        """Calcular embedding de una oración completa"""
        words = re.findall(r'\b\w+\b', text.lower())
        
        if not words:
            return [0.0] * self.embedding_dim
        
        vectors = []
        for word in words:
            if word in self.word_vectors:
                vectors.append(self.word_vectors[word])
            else:
                # Crear nuevo embedding para palabra desconocida
                new_vector = [random.gauss(0, 1) for _ in range(self.embedding_dim)]
                norm = math.sqrt(sum(x*x for x in new_vector))
                new_vector = [x/norm if norm > 0 else 0 for x in new_vector]
                self.word_vectors[word] = new_vector
                self._save_embedding(word, new_vector)
                vectors.append(new_vector)
        
        # Promedio de vectores de palabras
        if vectors:
            avg_vector = []
            for i in range(self.embedding_dim):
                avg = sum(vector[i] for vector in vectors) / len(vectors)
                avg_vector.append(avg)
            return avg_vector
        else:
            return [0.0] * self.embedding_dim
    
    def learn_from_conversation(self, user_input: str, aria_response: str, 
                              context: Dict = None, feedback_score: float = 0.0):
        """Aprender de una conversación nueva"""
        
        # 1. Guardar conversación en base de datos
        conversation_id = self._save_conversation(
            user_input, aria_response, context, feedback_score
        )
        
        # 2. Extraer conocimiento de la conversación
        self._extract_knowledge(user_input, aria_response, conversation_id)
        
        # 3. Actualizar patrones de respuesta
        self._update_response_patterns(user_input, aria_response, feedback_score)
        
        # 4. Actualizar memoria a corto plazo
        self.short_term_memory.append({
            'input': user_input,
            'response': aria_response,
            'timestamp': datetime.now(),
            'embedding': self.get_sentence_embedding(user_input)
        })
        
        # Mantener solo las últimas conversaciones en memoria
        if len(self.short_term_memory) > self.context_window:
            self.short_term_memory.pop(0)
        
        # 5. Consolidar a memoria a largo plazo si es necesario
        self._consolidate_memory()
        
        print(f"🎓 Aprendizaje completado para conversación {conversation_id}")
    
    def _save_conversation(self, user_input: str, aria_response: str, 
                          context: Dict, feedback_score: float) -> int:
        """Guardar conversación en la base de datos"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        context_json = json.dumps(context) if context else None
        
        # Análisis simple de sentimiento (básico)
        sentiment = self._analyze_sentiment(user_input)
        
        # Categorización de tópico (básica)
        topic = self._categorize_topic(user_input)
        
        cursor.execute("""
            INSERT INTO conversations 
            (user_input, aria_response, context, feedback_score, topic_category, sentiment)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (user_input, aria_response, context_json, feedback_score, topic, sentiment))
        
        conversation_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return conversation_id
    
    def _analyze_sentiment(self, text: str) -> float:
        """Análisis simple de sentimiento (-1 a 1)"""
        positive_words = ['bien', 'bueno', 'excelente', 'perfecto', 'gracias', 'genial', 'increible']
        negative_words = ['mal', 'malo', 'terrible', 'problema', 'error', 'fallo', 'ayuda']
        
        text_lower = text.lower()
        positive_count = sum(1 for word in positive_words if word in text_lower)
        negative_count = sum(1 for word in negative_words if word in text_lower)
        
        if positive_count + negative_count == 0:
            return 0.0
        
        return (positive_count - negative_count) / (positive_count + negative_count)
    
    def _categorize_topic(self, text: str) -> str:
        """Categorización simple de tópicos"""
        topics = {
            'saludo': ['hola', 'buenos', 'dias', 'tardes', 'noches'],
            'pregunta': ['que', 'como', 'cuando', 'donde', 'quien', 'por', 'cual'],
            'ayuda': ['ayuda', 'ayudar', 'problema', 'necesito', 'puedes'],
            'informacion': ['informacion', 'datos', 'saber', 'conocer', 'explicar'],
            'despedida': ['adios', 'hasta', 'luego', 'chao', 'nos', 'vemos']
        }
        
        text_lower = text.lower()
        for topic, keywords in topics.items():
            if any(keyword in text_lower for keyword in keywords):
                return topic
        
        return 'general'
    
    def _extract_knowledge(self, user_input: str, aria_response: str, conversation_id: int):
        """Extraer conocimiento conceptual de la conversación"""
        
        # Buscar patrones de definición
        definition_patterns = [
            r'(.+?) es (.+)',
            r'(.+?) significa (.+)',
            r'(.+?) se define como (.+)'
        ]
        
        combined_text = f"{user_input} {aria_response}"
        
        for pattern in definition_patterns:
            matches = re.findall(pattern, combined_text, re.IGNORECASE)
            for concept, definition in matches:
                self._save_knowledge(concept.strip(), definition.strip(), conversation_id)
    
    def _save_knowledge(self, concept: str, definition: str, conversation_id: int):
        """Guardar conocimiento extraído"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Calcular confianza basada en longitud y coherencia
        confidence = min(1.0, len(definition) / 100.0)
        
        cursor.execute("""
            INSERT INTO knowledge_base 
            (concept, definition, source_conversation_id, confidence_score)
            VALUES (?, ?, ?, ?)
        """, (concept, definition, conversation_id, confidence))
        
        conn.commit()
        conn.close()
    
    def _update_response_patterns(self, user_input: str, aria_response: str, feedback_score: float):
        """Actualizar patrones de respuesta basado en éxito"""
        
        # Crear patrón abstracto del input
        input_pattern = self._create_pattern(user_input)
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Buscar patrón existente
        cursor.execute("""
            SELECT id, usage_count, success_rate FROM response_patterns 
            WHERE input_pattern = ?
        """, (input_pattern,))
        
        result = cursor.fetchone()
        
        if result:
            # Actualizar patrón existente
            pattern_id, usage_count, current_success_rate = result
            new_usage_count = usage_count + 1
            new_success_rate = (current_success_rate * usage_count + feedback_score) / new_usage_count
            
            cursor.execute("""
                UPDATE response_patterns 
                SET response_template = ?, usage_count = ?, success_rate = ?, last_used = CURRENT_TIMESTAMP
                WHERE id = ?
            """, (aria_response, new_usage_count, new_success_rate, pattern_id))
        else:
            # Crear nuevo patrón
            cursor.execute("""
                INSERT INTO response_patterns (input_pattern, response_template, success_rate)
                VALUES (?, ?, ?)
            """, (input_pattern, aria_response, feedback_score))
        
        conn.commit()
        conn.close()
    
    def _create_pattern(self, text: str) -> str:
        """Crear patrón abstracto de un texto"""
        # Simplificar a estructura básica
        text_lower = text.lower()
        
        # Reemplazar entidades específicas con placeholders
        pattern = re.sub(r'\b\d+\b', '[NUMERO]', text_lower)
        pattern = re.sub(r'\b[a-zA-Z]+@[a-zA-Z]+\.[a-zA-Z]+\b', '[EMAIL]', pattern)
        pattern = re.sub(r'\b(enero|febrero|marzo|abril|mayo|junio|julio|agosto|septiembre|octubre|noviembre|diciembre)\b', '[MES]', pattern)
        
        return pattern
    
    def _consolidate_memory(self):
        """Consolidar memoria a corto plazo en memoria a largo plazo"""
        if len(self.short_term_memory) >= self.context_window:
            # Buscar patrones recurrentes
            patterns = defaultdict(int)
            
            for memory in self.short_term_memory:
                pattern = self._create_pattern(memory['input'])
                patterns[pattern] += 1
            
            # Mover patrones frecuentes a memoria a largo plazo
            for pattern, frequency in patterns.items():
                if frequency >= 2 and pattern not in self.long_term_memory:
                    self.long_term_memory[pattern] = {
                        'frequency': frequency,
                        'last_seen': datetime.now(),
                        'examples': [m for m in self.short_term_memory if self._create_pattern(m['input']) == pattern]
                    }
    
    def generate_response(self, user_input: str, context: Dict = None) -> Tuple[str, float]:
        """Generar respuesta basada en aprendizaje previo"""
        
        # 1. Buscar en patrones aprendidos
        learned_response = self._search_learned_patterns(user_input)
        if learned_response:
            return learned_response
        
        # 2. Buscar en conocimiento base
        knowledge_response = self._search_knowledge_base(user_input)
        if knowledge_response:
            return knowledge_response
        
        # 3. Usar memoria contextual
        contextual_response = self._generate_contextual_response(user_input)
        if contextual_response:
            return contextual_response
        
        # 4. Respuesta por defecto con aprendizaje
        return self._generate_learning_response(user_input)
    
    def _search_learned_patterns(self, user_input: str) -> Tuple[str, float]:
        """Buscar respuesta en patrones aprendidos priorizando respuestas naturales"""
        
        # Primero buscar respuestas directas de conversaciones recientes (más naturales)
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Buscar conversaciones exactas o muy similares
        words = user_input.lower().split()
        for word in words:
            cursor.execute("""
                SELECT aria_response, confidence FROM conversations 
                WHERE LOWER(user_input) LIKE ? 
                AND (context LIKE '%natural_response%' OR context LIKE '%personality_enhancement%' OR context LIKE '%spontaneous%')
                ORDER BY confidence DESC, timestamp DESC
                LIMIT 1
            """, (f'%{word}%',))
            
            result = cursor.fetchone()
            if result:
                response, confidence = result
                conn.close()
                return response, confidence
        
        # Si no encuentra respuestas naturales, buscar en patrones tradicionales
        input_pattern = self._create_pattern(user_input)
        
        cursor.execute("""
            SELECT response_template, success_rate FROM response_patterns 
            WHERE input_pattern = ? AND success_rate > 0.5
            ORDER BY success_rate DESC, usage_count DESC
            LIMIT 1
        """, (input_pattern,))
        
        result = cursor.fetchone()
        conn.close()
        
        if result:
            response_template, confidence = result
            return response_template, confidence
        
        return None
    
    def _search_knowledge_base(self, user_input: str) -> Tuple[str, float]:
        """Buscar en la base de conocimiento con respuestas más naturales"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Buscar conceptos relacionados
        words = re.findall(r'\b\w+\b', user_input.lower())
        
        for word in words:
            cursor.execute("""
                SELECT concept, definition, confidence_score FROM knowledge_base 
                WHERE LOWER(concept) LIKE ? OR LOWER(definition) LIKE ?
                ORDER BY confidence_score DESC
                LIMIT 1
            """, (f'%{word}%', f'%{word}%'))
            
            result = cursor.fetchone()
            if result:
                concept, definition, confidence = result
                
                # Respuestas más naturales y variadas
                import random
                natural_intros = [
                    f"¡Oh! Sobre {concept}, ",
                    f"He aprendido que ",
                    f"Richard me enseñó que ",
                    f"Según mi conocimiento, ",
                    f"¡Ah sí! {concept} ",
                    f"Por lo que sé, "
                ]
                
                intro = random.choice(natural_intros)
                response = f"{intro}{definition}"
                
                conn.close()
                return response, confidence
        
        conn.close()
        return None
    
    def _generate_contextual_response(self, user_input: str) -> Tuple[str, float]:
        """Generar respuesta basada en contexto de conversaciones recientes"""
        if not self.short_term_memory:
            return None
        
        # Calcular similitud con conversaciones recientes (sin numpy)
        current_embedding = self.get_sentence_embedding(user_input)
        
        best_similarity = 0
        best_response = None
        
        for memory in self.short_term_memory[-3:]:  # Últimas 3 conversaciones
            # Calcular producto punto manualmente
            similarity = sum(a * b for a, b in zip(current_embedding, memory['embedding']))
            if similarity > best_similarity and similarity > 0.7:
                best_similarity = similarity
                best_response = memory['response']
        
        if best_response:
            return f"Basándome en nuestra conversación anterior, {best_response.lower()}", best_similarity
        
        return None
    
    def _generate_learning_response(self, user_input: str) -> Tuple[str, float]:
        """Generar respuesta natural con capacidad de aprendizaje"""
        import random
        
        # Respuestas más naturales y espontáneas
        curious_responses = [
            "¡Qué interesante! Me encanta cuando me enseñan cosas nuevas. ¿Puedes contarme más?",
            "Hmm, no tengo mucha info sobre eso todavía, pero suena fascinante. ¿Qué sabes tú?",
            "¡Oh! Esa pregunta me tiene curiosa. ¿Me ayudas a entenderlo mejor?",
            "No estoy segura de eso aún, pero me has picado la curiosidad. Cuéntame más",
            "¡Uy! Eso es nuevo para mí. Richard no me ha enseñado sobre eso todavía. ¿Tú qué piensas?"
        ]
        
        friendly_responses = [
            "¡Buena pregunta! Cada día aprendo algo nuevo gracias a conversaciones como esta",
            "Mmm, eso suena interesante pero no tengo experiencia con eso. ¿Podrías explicarme?",
            "¡Me gusta esa pregunta! Aunque no sepa la respuesta exacta, me emociona aprender",
            "No tengo esa información todavía, pero me encanta cuando me enseñan cosas nuevas",
            "¡Qué cool! Eso es algo que me gustaría aprender. ¿Tienes experiencia con eso?"
        ]
        
        # Mezclar tipos de respuesta para más variedad
        all_responses = curious_responses + friendly_responses
        
        return random.choice(all_responses), 0.3
    
    def get_learning_stats(self) -> Dict[str, Any]:
        """Obtener estadísticas del aprendizaje"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        stats = {}
        
        # Estadísticas de conversaciones
        cursor.execute("SELECT COUNT(*) FROM conversations")
        stats['total_conversations'] = cursor.fetchone()[0]
        
        cursor.execute("SELECT AVG(feedback_score) FROM conversations WHERE feedback_score > 0")
        result = cursor.fetchone()[0]
        stats['average_feedback'] = result if result else 0.0
        
        # Estadísticas de conocimiento
        cursor.execute("SELECT COUNT(*) FROM knowledge_base")
        stats['knowledge_entries'] = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM response_patterns")
        stats['learned_patterns'] = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM word_embeddings")
        stats['vocabulary_size'] = cursor.fetchone()[0]
        
        # Memoria actual
        stats['short_term_memory'] = len(self.short_term_memory)
        stats['long_term_patterns'] = len(self.long_term_memory)
        
        conn.close()
        return stats
    
    def export_knowledge(self) -> Dict[str, Any]:
        """Exportar todo el conocimiento aprendido"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        knowledge_export = {}
        
        # Exportar conceptos aprendidos
        cursor.execute("SELECT concept, definition, confidence_score FROM knowledge_base ORDER BY confidence_score DESC")
        knowledge_export['concepts'] = [
            {'concept': row[0], 'definition': row[1], 'confidence': row[2]}
            for row in cursor.fetchall()
        ]
        
        # Exportar patrones de respuesta exitosos
        cursor.execute("SELECT input_pattern, response_template, success_rate FROM response_patterns WHERE success_rate > 0.6 ORDER BY success_rate DESC")
        knowledge_export['successful_patterns'] = [
            {'pattern': row[0], 'response': row[1], 'success_rate': row[2]}
            for row in cursor.fetchall()
        ]
        
        conn.close()
        return knowledge_export

# Instancia global del sistema de aprendizaje
learning_system = AdvancedLearningSystem()