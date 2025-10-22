"""
🌐 ARIA - Sistema de Base de Datos en la Nube
===========================================

Configuración para base de datos gratuita en Supabase
con capacidades de aprendizaje colaborativo entre IAs.
"""

import os
import json
import requests
import asyncio
import aiohttp
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import logging

class AriaCloudDatabase:
    """Sistema de base de datos en la nube para ARIA"""
    
    def __init__(self):
        # Configuración de Supabase (gratuito hasta 500MB)
        self.supabase_url = os.getenv('SUPABASE_URL', 'https://your-project.supabase.co')
        self.supabase_key = os.getenv('SUPABASE_ANON_KEY', 'your-anon-key')
        
        # URLs de APIs de IAs para aprendizaje colaborativo
        self.ai_learning_sources = [
            {
                'name': 'OpenAI GPT Insights',
                'url': 'https://api.openai.com/v1/models',
                'type': 'model_info'
            },
            {
                'name': 'Hugging Face Models',
                'url': 'https://huggingface.co/api/models',
                'type': 'model_data'
            },
            {
                'name': 'Google AI Research',
                'url': 'https://arxiv.org/search/advanced',
                'type': 'research_papers'
            },
            {
                'name': 'AI Training Datasets',
                'url': 'https://datasets-server.huggingface.co/datasets',
                'type': 'training_data'
            }
        ]
        
        self.session = None
        
    async def init_cloud_database(self):
        """Inicializa la base de datos en la nube"""
        print("🌐 Inicializando base de datos en la nube...")
        
        # Crear tablas en Supabase
        tables_sql = [
            """
            CREATE TABLE IF NOT EXISTS aria_knowledge_cloud (
                id SERIAL PRIMARY KEY,
                topic VARCHAR(255) NOT NULL,
                content JSONB NOT NULL,
                source_type VARCHAR(100),
                source_url TEXT,
                confidence_score FLOAT DEFAULT 0.5,
                ai_source VARCHAR(255),
                learned_from_ia BOOLEAN DEFAULT FALSE,
                emotional_context VARCHAR(50),
                interaction_type VARCHAR(50),
                created_at TIMESTAMP DEFAULT NOW(),
                last_accessed TIMESTAMP DEFAULT NOW(),
                access_count INTEGER DEFAULT 0
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS aria_emotions (
                id SERIAL PRIMARY KEY,
                emotion_type VARCHAR(50) NOT NULL,
                trigger_event TEXT,
                intensity FLOAT DEFAULT 0.5,
                duration_seconds INTEGER DEFAULT 5,
                color_code VARCHAR(7),
                created_at TIMESTAMP DEFAULT NOW()
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS ia_collaborative_learning (
                id SERIAL PRIMARY KEY,
                source_ia VARCHAR(255) NOT NULL,
                knowledge_type VARCHAR(100),
                content JSONB NOT NULL,
                relevance_score FLOAT DEFAULT 0.5,
                integration_status VARCHAR(50) DEFAULT 'pending',
                created_at TIMESTAMP DEFAULT NOW()
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS aria_personality (
                id SERIAL PRIMARY KEY,
                personality_trait VARCHAR(100) NOT NULL,
                value FLOAT DEFAULT 0.5,
                learning_influence FLOAT DEFAULT 0.0,
                emotional_weight FLOAT DEFAULT 0.3,
                last_updated TIMESTAMP DEFAULT NOW()
            );
            """
        ]
        
        try:
            for sql in tables_sql:
                await self._execute_sql(sql)
            
            print("✅ Base de datos en la nube configurada")
            return True
            
        except Exception as e:
            print(f"❌ Error configurando base de datos: {e}")
            return False
    
    async def _execute_sql(self, sql: str, params: List = None):
        """Ejecuta SQL en Supabase"""
        if not self.session:
            self.session = aiohttp.ClientSession()
        
        headers = {
            'apikey': self.supabase_key,
            'Authorization': f'Bearer {self.supabase_key}',
            'Content-Type': 'application/json'
        }
        
        data = {
            'query': sql,
            'params': params or []
        }
        
        async with self.session.post(
            f"{self.supabase_url}/rest/v1/rpc/execute_sql",
            headers=headers,
            json=data
        ) as response:
            return await response.json()
    
    async def learn_from_other_ais(self):
        """Aprende de otras IAs y sistemas de IA"""
        print("🤖 Iniciando aprendizaje colaborativo de otras IAs...")
        
        learned_knowledge = []
        
        for ai_source in self.ai_learning_sources:
            try:
                knowledge = await self._extract_ai_knowledge(ai_source)
                if knowledge:
                    learned_knowledge.extend(knowledge)
                    await self._store_ai_knowledge(ai_source['name'], knowledge)
                    
                    # Registrar emoción de aprendizaje (verde)
                    await self._register_emotion('learning', f"Aprendí de {ai_source['name']}", 
                                                intensity=0.8, color='#00FF00')
                    
            except Exception as e:
                print(f"⚠️ Error aprendiendo de {ai_source['name']}: {e}")
                
                # Registrar emoción de frustración (rojo)
                await self._register_emotion('frustration', f"No pude aprender de {ai_source['name']}", 
                                            intensity=0.6, color='#FF0000')
        
        print(f"✅ Aprendizaje colaborativo completado: {len(learned_knowledge)} elementos")
        return learned_knowledge
    
    async def _extract_ai_knowledge(self, ai_source: Dict) -> List[Dict]:
        """Extrae conocimiento de una fuente de IA"""
        knowledge = []
        
        try:
            if not self.session:
                self.session = aiohttp.ClientSession()
            
            async with self.session.get(ai_source['url'], timeout=10) as response:
                if response.status == 200:
                    data = await response.json()
                    
                    # Procesar según el tipo de fuente
                    if ai_source['type'] == 'model_info':
                        knowledge = self._process_model_info(data)
                    elif ai_source['type'] == 'model_data':
                        knowledge = self._process_model_data(data)
                    elif ai_source['type'] == 'research_papers':
                        knowledge = self._process_research_papers(data)
                    elif ai_source['type'] == 'training_data':
                        knowledge = self._process_training_data(data)
                        
        except Exception as e:
            print(f"Error extrayendo de {ai_source['name']}: {e}")
        
        return knowledge
    
    def _process_model_info(self, data: Dict) -> List[Dict]:
        """Procesa información de modelos de IA"""
        knowledge = []
        
        if 'data' in data:
            for model in data['data'][:5]:  # Limitar a 5 modelos
                knowledge.append({
                    'topic': f"AI Model: {model.get('id', 'Unknown')}",
                    'content': {
                        'model_id': model.get('id'),
                        'owner': model.get('owned_by'),
                        'created': model.get('created'),
                        'type': 'ai_model_info'
                    },
                    'confidence': 0.9,
                    'source_type': 'ai_model'
                })
        
        return knowledge
    
    def _process_model_data(self, data: List) -> List[Dict]:
        """Procesa datos de modelos de Hugging Face"""
        knowledge = []
        
        for model in data[:10]:  # Limitar a 10 modelos
            if isinstance(model, dict):
                knowledge.append({
                    'topic': f"HF Model: {model.get('modelId', 'Unknown')}",
                    'content': {
                        'model_id': model.get('modelId'),
                        'task': model.get('pipeline_tag'),
                        'downloads': model.get('downloads', 0),
                        'likes': model.get('likes', 0),
                        'type': 'huggingface_model'
                    },
                    'confidence': 0.85,
                    'source_type': 'huggingface'
                })
        
        return knowledge
    
    def _process_research_papers(self, data: Dict) -> List[Dict]:
        """Procesa papers de investigación en IA"""
        # Simulado - en implementación real usaríamos arXiv API
        return [{
            'topic': 'AI Research Trends',
            'content': {
                'trend': 'Large Language Models',
                'relevance': 'High',
                'type': 'research_trend'
            },
            'confidence': 0.8,
            'source_type': 'research'
        }]
    
    def _process_training_data(self, data: Dict) -> List[Dict]:
        """Procesa datasets de entrenamiento"""
        # Simulado - acceso a datasets públicos
        return [{
            'topic': 'Training Methodologies',
            'content': {
                'method': 'Reinforcement Learning from Human Feedback',
                'effectiveness': 'High',
                'type': 'training_method'
            },
            'confidence': 0.9,
            'source_type': 'training_data'
        }]
    
    async def _store_ai_knowledge(self, ai_source: str, knowledge: List[Dict]):
        """Almacena conocimiento aprendido de otras IAs"""
        for item in knowledge:
            try:
                data = {
                    'source_ia': ai_source,
                    'knowledge_type': item.get('source_type', 'unknown'),
                    'content': json.dumps(item['content']),
                    'relevance_score': item.get('confidence', 0.5),
                    'integration_status': 'integrated'
                }
                
                await self._insert_data('ia_collaborative_learning', data)
                
            except Exception as e:
                print(f"Error almacenando conocimiento de {ai_source}: {e}")
    
    async def _register_emotion(self, emotion_type: str, trigger: str, 
                              intensity: float = 0.5, color: str = '#0080FF'):
        """Registra una emoción de ARIA"""
        emotion_data = {
            'emotion_type': emotion_type,
            'trigger_event': trigger,
            'intensity': intensity,
            'color_code': color,
            'duration_seconds': int(intensity * 10)  # Duración basada en intensidad
        }
        
        await self._insert_data('aria_emotions', emotion_data)
        
        # Enviar a frontend para cambio de color
        await self._broadcast_emotion(emotion_data)
    
    async def _broadcast_emotion(self, emotion_data: Dict):
        """Transmite emoción al frontend"""
        # En implementación real, usar WebSockets
        print(f"🎨 Emoción: {emotion_data['emotion_type']} - Color: {emotion_data['color_code']}")
    
    async def _insert_data(self, table: str, data: Dict):
        """Inserta datos en Supabase"""
        if not self.session:
            self.session = aiohttp.ClientSession()
        
        headers = {
            'apikey': self.supabase_key,
            'Authorization': f'Bearer {self.supabase_key}',
            'Content-Type': 'application/json',
            'Prefer': 'return=minimal'
        }
        
        async with self.session.post(
            f"{self.supabase_url}/rest/v1/{table}",
            headers=headers,
            json=data
        ) as response:
            return response.status == 201
    
    async def get_recent_emotions(self, limit: int = 10) -> List[Dict]:
        """Obtiene emociones recientes para el frontend"""
        if not self.session:
            self.session = aiohttp.ClientSession()
        
        headers = {
            'apikey': self.supabase_key,
            'Authorization': f'Bearer {self.supabase_key}'
        }
        
        params = {
            'select': '*',
            'order': 'created_at.desc',
            'limit': limit
        }
        
        async with self.session.get(
            f"{self.supabase_url}/rest/v1/aria_emotions",
            headers=headers,
            params=params
        ) as response:
            if response.status == 200:
                return await response.json()
            return []
    
    async def store_cloud_knowledge(self, topic: str, content: Dict, 
                                  source_url: str = "", confidence: float = 0.5,
                                  learned_from_ia: bool = False, ai_source: str = ""):
        """Almacena conocimiento en la nube"""
        knowledge_data = {
            'topic': topic,
            'content': json.dumps(content),
            'source_url': source_url,
            'confidence_score': confidence,
            'learned_from_ia': learned_from_ia,
            'ai_source': ai_source,
            'emotional_context': 'learning',
            'interaction_type': 'auto_learning'
        }
        
        success = await self._insert_data('aria_knowledge_cloud', knowledge_data)
        
        if success:
            # Registrar emoción de aprendizaje exitoso
            await self._register_emotion('satisfaction', f"Conocimiento almacenado: {topic}", 
                                        intensity=0.7, color='#00FF00')
        else:
            # Registrar emoción de frustración
            await self._register_emotion('frustration', f"Error almacenando: {topic}", 
                                        intensity=0.5, color='#FF0000')
        
        return success
    
    async def search_cloud_knowledge(self, query: str, limit: int = 10) -> List[Dict]:
        """Busca conocimiento en la nube"""
        # Registrar emoción de interacción (azul)
        await self._register_emotion('interaction', f"Búsqueda: {query}", 
                                    intensity=0.6, color='#0080FF')
        
        if not self.session:
            self.session = aiohttp.ClientSession()
        
        headers = {
            'apikey': self.supabase_key,
            'Authorization': f'Bearer {self.supabase_key}'
        }
        
        # Usar búsqueda de texto completo en PostgreSQL
        params = {
            'select': '*',
            'topic': f'ilike.%{query}%',
            'order': 'confidence_score.desc',
            'limit': limit
        }
        
        async with self.session.get(
            f"{self.supabase_url}/rest/v1/aria_knowledge_cloud",
            headers=headers,
            params=params
        ) as response:
            if response.status == 200:
                results = await response.json()
                
                # Registrar emoción de éxito (verde)
                await self._register_emotion('success', f"Encontré {len(results)} resultados", 
                                            intensity=0.8, color='#00FF00')
                
                return results
            else:
                # Registrar emoción de frustración (rojo)
                await self._register_emotion('frustration', "No encontré resultados", 
                                            intensity=0.4, color='#FF0000')
                return []
    
    async def close(self):
        """Cierra la sesión"""
        if self.session:
            await self.session.close()

# Instancia global
cloud_db = AriaCloudDatabase()