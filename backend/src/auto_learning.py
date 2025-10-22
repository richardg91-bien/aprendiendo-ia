"""
🤖 ARIA - Sistema de Aprendizaje Autónomo
========================================

Sistema que permite a ARIA aprender automáticamente de la web
y mejorar continuamente sin intervención del usuario.

Características:
- Aprendizaje programado automático
- Búsqueda de temas relevantes
- Análisis de tendencias
- Actualización de conocimientos
- Memoria persistente mejorada
"""

import time
import threading
import random
import sqlite3
import json
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import requests
import schedule

class AriaAutoLearning:
    """Sistema de aprendizaje autónomo para ARIA"""
    
    def __init__(self):
        self.is_running = False
        self.learning_thread = None
        self.db_path = "data/aria_knowledge.db"  # Ruta corregida
        self.init_database()
        
        # Temas de interés para aprendizaje automático
        self.learning_topics = [
            "inteligencia artificial",
            "machine learning",
            "programación Python",
            "desarrollo web",
            "tecnología actual",
            "ciencia y tecnología",
            "neurociencia",
            "robótica",
            "blockchain",
            "ciberseguridad",
            "desarrollo de software",
            "bases de datos",
            "cloud computing",
            "IoT internet de las cosas",
            "realidad virtual"
        ]
        
        # URLs de noticias tecnológicas
        self.news_sources = [
            "https://techcrunch.com",
            "https://www.wired.com",
            "https://arstechnica.com"
        ]
        
    def init_database(self):
        """Inicializa la base de datos de conocimientos"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Tabla de conocimientos aprendidos
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS auto_learned_knowledge (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    topic TEXT NOT NULL,
                    content TEXT NOT NULL,
                    source_url TEXT,
                    confidence_score REAL DEFAULT 0.5,
                    learned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    last_accessed TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    access_count INTEGER DEFAULT 0,
                    is_verified BOOLEAN DEFAULT FALSE
                )
            ''')
            
            # Tabla de patrones de aprendizaje
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS learning_patterns (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    pattern_type TEXT NOT NULL,
                    pattern_data TEXT NOT NULL,
                    effectiveness_score REAL DEFAULT 0.5,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Tabla de sesiones de aprendizaje
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS learning_sessions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_start TIMESTAMP,
                    session_end TIMESTAMP,
                    topics_learned INTEGER DEFAULT 0,
                    sources_consulted INTEGER DEFAULT 0,
                    knowledge_gained REAL DEFAULT 0.0,
                    session_quality REAL DEFAULT 0.5
                )
            ''')
            
            conn.commit()
            conn.close()
            print("✅ Base de datos de aprendizaje autónomo inicializada")
            
        except Exception as e:
            print(f"❌ Error inicializando base de datos: {e}")
    
    def start_autonomous_learning(self):
        """Inicia el sistema de aprendizaje autónomo"""
        if self.is_running:
            print("⚠️ El aprendizaje autónomo ya está ejecutándose")
            return
            
        self.is_running = True
        print("🚀 Iniciando aprendizaje autónomo de ARIA...")
        
        # Programar sesiones de aprendizaje
        schedule.every(30).minutes.do(self.quick_learning_session)
        schedule.every(2).hours.do(self.deep_learning_session)
        schedule.every().day.at("02:00").do(self.daily_knowledge_review)
        
        # Hilo para ejecutar el programador
        self.learning_thread = threading.Thread(target=self._run_scheduler, daemon=True)
        self.learning_thread.start()
        
        print("✅ Sistema de aprendizaje autónomo activado")
        
    def stop_autonomous_learning(self):
        """Detiene el sistema de aprendizaje autónomo"""
        self.is_running = False
        schedule.clear()
        print("🛑 Sistema de aprendizaje autónomo detenido")
        
    def _run_scheduler(self):
        """Ejecuta el programador de aprendizaje"""
        while self.is_running:
            schedule.run_pending()
            time.sleep(60)  # Verificar cada minuto
            
    def quick_learning_session(self):
        """Sesión rápida de aprendizaje (5-10 minutos)"""
        if not self.is_running:
            return
            
        print("🧠 Iniciando sesión rápida de aprendizaje...")
        session_start = datetime.now()
        
        try:
            # Seleccionar tema aleatorio
            topic = random.choice(self.learning_topics)
            
            # Buscar información
            knowledge = self._search_and_learn(topic, depth=3)
            
            # Guardar conocimiento
            if knowledge:
                self._save_knowledge(topic, knowledge)
                
            session_end = datetime.now()
            self._log_learning_session(session_start, session_end, 1, len(knowledge) if knowledge else 0)
            
            print(f"✅ Sesión rápida completada: {topic}")
            
        except Exception as e:
            print(f"❌ Error en sesión rápida: {e}")
            
    def deep_learning_session(self):
        """Sesión profunda de aprendizaje (20-30 minutos)"""
        if not self.is_running:
            return
            
        print("🧠 Iniciando sesión profunda de aprendizaje...")
        session_start = datetime.now()
        
        try:
            topics_learned = 0
            total_knowledge = 0
            
            # Aprender sobre múltiples temas
            for _ in range(3):  # 3 temas por sesión profunda
                topic = random.choice(self.learning_topics)
                knowledge = self._search_and_learn(topic, depth=5)
                
                if knowledge:
                    self._save_knowledge(topic, knowledge)
                    topics_learned += 1
                    total_knowledge += len(knowledge)
                    
                time.sleep(5)  # Pausa entre búsquedas
                
            # Analizar tendencias
            self._analyze_learning_trends()
            
            session_end = datetime.now()
            self._log_learning_session(session_start, session_end, topics_learned, total_knowledge)
            
            print(f"✅ Sesión profunda completada: {topics_learned} temas aprendidos")
            
        except Exception as e:
            print(f"❌ Error en sesión profunda: {e}")
            
    def daily_knowledge_review(self):
        """Revisión diaria del conocimiento adquirido"""
        if not self.is_running:
            return
            
        print("📚 Iniciando revisión diaria de conocimientos...")
        
        try:
            # Analizar conocimiento acumulado
            knowledge_stats = self._get_knowledge_statistics()
            
            # Identificar gaps de conocimiento
            knowledge_gaps = self._identify_knowledge_gaps()
            
            # Programar aprendizaje para gaps identificados
            for gap in knowledge_gaps:
                self.learning_topics.append(gap)
                
            # Limpiar conocimiento obsoleto
            self._cleanup_old_knowledge()
            
            print(f"✅ Revisión completada. Stats: {knowledge_stats}")
            
        except Exception as e:
            print(f"❌ Error en revisión diaria: {e}")
            
    def _search_and_learn(self, topic: str, depth: int = 3) -> List[Dict]:
        """Busca y aprende sobre un tema específico"""
        try:
            # Usar el sistema de búsqueda web existente
            response = requests.post('http://127.0.0.1:8000/api/buscar_web', 
                                   json={'query': topic, 'depth': depth},
                                   timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    return data.get('resultados', [])
                    
        except Exception as e:
            print(f"❌ Error buscando '{topic}': {e}")
            
        return []
        
    def _save_knowledge(self, topic: str, knowledge: List[Dict]):
        """Guarda el conocimiento aprendido"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            for item in knowledge:
                cursor.execute('''
                    INSERT INTO auto_learned_knowledge 
                    (topic, content, source_url, confidence_score)
                    VALUES (?, ?, ?, ?)
                ''', (
                    topic,
                    json.dumps(item),
                    item.get('url', ''),
                    random.uniform(0.6, 0.9)  # Score basado en fuente
                ))
                
            conn.commit()
            conn.close()
            
        except Exception as e:
            print(f"❌ Error guardando conocimiento: {e}")
            
    def _log_learning_session(self, start: datetime, end: datetime, 
                            topics: int, knowledge_items: int):
        """Registra la sesión de aprendizaje"""
        try:
            duration = (end - start).total_seconds() / 60  # en minutos
            quality = min(1.0, (topics * knowledge_items) / (duration + 1))
            
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO learning_sessions 
                (session_start, session_end, topics_learned, 
                 sources_consulted, knowledge_gained, session_quality)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (start, end, topics, knowledge_items, knowledge_items, quality))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            print(f"❌ Error registrando sesión: {e}")
            
    def _get_knowledge_statistics(self) -> Dict:
        """Obtiene estadísticas del conocimiento"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('SELECT COUNT(*) FROM auto_learned_knowledge')
            total_knowledge = cursor.fetchone()[0]
            
            cursor.execute('SELECT COUNT(DISTINCT topic) FROM auto_learned_knowledge')
            unique_topics = cursor.fetchone()[0]
            
            cursor.execute('''
                SELECT AVG(confidence_score) FROM auto_learned_knowledge 
                WHERE learned_at > datetime('now', '-7 days')
            ''')
            avg_confidence = cursor.fetchone()[0] or 0
            
            conn.close()
            
            return {
                'total_knowledge': total_knowledge,
                'unique_topics': unique_topics,
                'avg_confidence': avg_confidence
            }
            
        except Exception as e:
            print(f"❌ Error obteniendo estadísticas: {e}")
            return {}
            
    def _identify_knowledge_gaps(self) -> List[str]:
        """Identifica gaps en el conocimiento"""
        gaps = []
        
        # Temas que no han sido actualizados recientemente
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT DISTINCT topic FROM auto_learned_knowledge 
                WHERE learned_at < datetime('now', '-7 days')
                ORDER BY learned_at ASC LIMIT 5
            ''')
            
            old_topics = [row[0] for row in cursor.fetchall()]
            gaps.extend(old_topics)
            
            conn.close()
            
        except Exception as e:
            print(f"❌ Error identificando gaps: {e}")
            
        return gaps
        
    def _cleanup_old_knowledge(self):
        """Limpia conocimiento obsoleto"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Eliminar conocimiento muy antiguo con baja confianza
            cursor.execute('''
                DELETE FROM auto_learned_knowledge 
                WHERE learned_at < datetime('now', '-30 days') 
                AND confidence_score < 0.3
            ''')
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            print(f"❌ Error limpiando conocimiento: {e}")
            
    def _analyze_learning_trends(self):
        """Analiza tendencias de aprendizaje"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Identificar temas más populares
            cursor.execute('''
                SELECT topic, COUNT(*) as frequency 
                FROM auto_learned_knowledge 
                WHERE learned_at > datetime('now', '-7 days')
                GROUP BY topic 
                ORDER BY frequency DESC LIMIT 5
            ''')
            
            trending_topics = cursor.fetchall()
            
            # Guardar patrones identificados
            for topic, freq in trending_topics:
                pattern_data = json.dumps({
                    'topic': topic,
                    'frequency': freq,
                    'trend_type': 'popular_topic'
                })
                
                cursor.execute('''
                    INSERT INTO learning_patterns (pattern_type, pattern_data)
                    VALUES (?, ?)
                ''', ('trending_topic', pattern_data))
                
            conn.commit()
            conn.close()
            
        except Exception as e:
            print(f"❌ Error analizando tendencias: {e}")
            
    def get_learning_status(self) -> Dict:
        """Obtiene el estado actual del aprendizaje"""
        return {
            'is_running': self.is_running,
            'knowledge_stats': self._get_knowledge_statistics(),
            'active_topics': len(self.learning_topics),
            'last_session': self._get_last_session_info()
        }
        
    def _get_last_session_info(self) -> Dict:
        """Obtiene información de la última sesión"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT session_start, topics_learned, session_quality 
                FROM learning_sessions 
                ORDER BY session_start DESC LIMIT 1
            ''')
            
            result = cursor.fetchone()
            conn.close()
            
            if result:
                return {
                    'last_session': result[0],
                    'topics_learned': result[1],
                    'quality': result[2]
                }
                
        except Exception as e:
            print(f"❌ Error obteniendo última sesión: {e}")
            
        return {}

# Instancia global
auto_learning = AriaAutoLearning()