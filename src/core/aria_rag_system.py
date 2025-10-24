#!/usr/bin/env python3
"""
🧠 SISTEMA RAG AVANZADO PARA ARIA
=================================

Retrieval-Augmented Generation que combina:
- Búsqueda semántica en múltiples fuentes
- Generación contextual con IA
- Memoria conversacional
- Aprendizaje continuo
"""

import os
import json
import requests
import logging
from datetime import datetime, timezone
from typing import Dict, List, Any, Optional
import re
from dataclasses import dataclass
from collections import defaultdict

@dataclass
class DocumentChunk:
    """Fragmento de documento con metadatos"""
    content: str
    source: str
    category: str
    confidence: float
    timestamp: str
    embedding_vector: Optional[List[float]] = None
    
@dataclass
class RAGResponse:
    """Respuesta RAG completa"""
    answer: str
    sources: List[Dict]
    confidence: float
    context_used: List[str]
    generation_method: str
    search_time: float
    total_time: float

class ARIARAGSystem:
    """Sistema RAG completo para ARIA"""
    
    def __init__(self, cloud_connector=None, emotion_detector=None):
        self.cloud_connector = cloud_connector
        self.emotion_detector = emotion_detector
        
        # Configuración RAG
        self.max_context_length = 4000
        self.min_confidence_threshold = 0.3
        self.max_sources = 5
        
        # Cache de contexto conversacional
        self.conversation_context = []
        self.user_profile = {
            'interests': defaultdict(int),
            'expertise_level': 'intermediate',
            'preferred_response_style': 'educational',
            'language': 'es'
        }
        
        # Fuentes de datos disponibles
        self.data_sources = {
            'supabase_knowledge': self._search_supabase_knowledge,
            'web_search': self._search_web_content,
            'conversation_memory': self._search_conversation_memory,
            'local_knowledge': self._search_local_knowledge,
            'real_time_data': self._search_real_time_data
        }
        
        print("🧠 Sistema RAG inicializado")
    
    def generate_rag_response(self, query: str, context: Dict = None) -> RAGResponse:
        """Generar respuesta RAG completa"""
        start_time = datetime.now()
        
        # 1. ANÁLISIS DE CONSULTA
        query_analysis = self._analyze_query(query)
        
        # 2. BÚSQUEDA MULTI-FUENTE
        search_start = datetime.now()
        relevant_chunks = self._multi_source_retrieval(query, query_analysis)
        search_time = (datetime.now() - search_start).total_seconds()
        
        # 3. RANKING Y FILTRADO
        ranked_chunks = self._rank_and_filter_chunks(relevant_chunks, query)
        
        # 4. GENERACIÓN CONTEXTUAL
        generated_response = self._generate_contextual_response(
            query, ranked_chunks, query_analysis
        )
        
        # 5. POST-PROCESAMIENTO
        final_response = self._post_process_response(
            generated_response, ranked_chunks, query
        )
        
        # 6. APRENDIZAJE CONTINUO
        self._update_user_profile(query, final_response)
        self._store_interaction(query, final_response, ranked_chunks)
        
        total_time = (datetime.now() - start_time).total_seconds()
        
        return RAGResponse(
            answer=final_response['answer'],
            sources=final_response['sources'],
            confidence=final_response['confidence'],
            context_used=final_response['context_used'],
            generation_method=final_response['method'],
            search_time=search_time,
            total_time=total_time
        )
    
    def _analyze_query(self, query: str) -> Dict:
        """Análisis profundo de la consulta"""
        analysis = {
            'intent': self._detect_intent(query),
            'entities': self._extract_entities(query),
            'complexity': self._assess_complexity(query),
            'domain': self._identify_domain(query),
            'question_type': self._classify_question_type(query),
            'requires_real_time': self._needs_real_time_data(query),
            'emotional_context': None
        }
        
        # Análisis emocional si está disponible
        if self.emotion_detector:
            try:
                emotion_result = self.emotion_detector.detect_user_emotion(query)
                analysis['emotional_context'] = emotion_result
            except:
                pass
        
        return analysis
    
    def _multi_source_retrieval(self, query: str, analysis: Dict) -> List[DocumentChunk]:
        """Búsqueda en múltiples fuentes de datos"""
        all_chunks = []
        
        # Priorizar fuentes según el tipo de consulta
        source_priority = self._determine_source_priority(analysis)
        
        for source_name in source_priority:
            if source_name in self.data_sources:
                try:
                    chunks = self.data_sources[source_name](query, analysis)
                    all_chunks.extend(chunks)
                    print(f"🔍 {source_name}: {len(chunks)} resultados")
                except Exception as e:
                    print(f"⚠️ Error en {source_name}: {e}")
        
        return all_chunks
    
    def _search_supabase_knowledge(self, query: str, analysis: Dict) -> List[DocumentChunk]:
        """Búsqueda en conocimiento de Supabase"""
        chunks = []
        
        if not self.cloud_connector:
            return chunks
        
        try:
            # Buscar conocimiento relevante
            knowledge_items = self.cloud_connector.get_knowledge()
            
            for item in knowledge_items:
                # Calcular relevancia
                relevance = self._calculate_relevance(
                    query, item.get('concept', ''), item.get('description', '')
                )
                
                if relevance > self.min_confidence_threshold:
                    chunk = DocumentChunk(
                        content=item.get('description', ''),
                        source='supabase_knowledge',
                        category=item.get('category', 'general'),
                        confidence=relevance,
                        timestamp=item.get('created_at', datetime.now().isoformat())
                    )
                    chunks.append(chunk)
        
        except Exception as e:
            print(f"❌ Error búsqueda Supabase: {e}")
        
        return sorted(chunks, key=lambda x: x.confidence, reverse=True)[:10]
    
    def _search_web_content(self, query: str, analysis: Dict) -> List[DocumentChunk]:
        """Búsqueda en contenido web"""
        chunks = []
        
        # Solo para consultas que requieren datos actuales
        if not analysis.get('requires_real_time', False):
            return chunks
        
        try:
            # Usar el buscador web real si está disponible
            from buscador_web_aria import BuscadorWebARIA
            buscador = BuscadorWebARIA()
            
            resultados = buscador.buscar_google(query)
            
            if resultados and 'resultados' in resultados:
                for i, resultado in enumerate(resultados['resultados'][:3]):
                    if 'descripcion' in resultado and resultado['descripcion']:
                        chunk = DocumentChunk(
                            content=resultado['descripcion'],
                            source='web_search',
                            category='real_time',
                            confidence=0.8 - (i * 0.1),  # Degradar confianza
                            timestamp=datetime.now().isoformat()
                        )
                        chunks.append(chunk)
        
        except ImportError:
            print("⚠️ Buscador web no disponible")
        except Exception as e:
            print(f"❌ Error búsqueda web: {e}")
        
        return chunks
    
    def _search_conversation_memory(self, query: str, analysis: Dict) -> List[DocumentChunk]:
        """Búsqueda en memoria conversacional"""
        chunks = []
        
        # Buscar en contexto de conversación reciente
        for i, conv in enumerate(self.conversation_context[-10:]):  # Últimas 10
            relevance = self._calculate_relevance(
                query, conv.get('user_query', ''), conv.get('response', '')
            )
            
            if relevance > 0.4:  # Umbral más alto para memoria
                chunk = DocumentChunk(
                    content=f"Contexto previo: {conv.get('response', '')}",
                    source='conversation_memory',
                    category='contextual',
                    confidence=relevance * 0.8,  # Reducir peso de memoria
                    timestamp=conv.get('timestamp', datetime.now().isoformat())
                )
                chunks.append(chunk)
        
        return chunks
    
    def _search_local_knowledge(self, query: str, analysis: Dict) -> List[DocumentChunk]:
        """Búsqueda en conocimiento local (BD SQLite + fallback)"""
        chunks = []
        
        # 1. BÚSQUEDA EN BASE DE DATOS LOCAL
        try:
            import sqlite3
            from pathlib import Path
            
            db_path = Path("config/knowledge_base.db")
            if db_path.exists():
                conn = sqlite3.connect(db_path)
                cursor = conn.cursor()
                
                # Búsqueda con LIKE para encontrar coincidencias parciales
                cursor.execute("""
                    SELECT concept, description, category, tags 
                    FROM knowledge 
                    WHERE concept LIKE ? OR description LIKE ? OR tags LIKE ?
                    ORDER BY 
                        CASE 
                            WHEN concept LIKE ? THEN 1 
                            WHEN tags LIKE ? THEN 2 
                            ELSE 3 
                        END
                    LIMIT 5
                """, (
                    f"%{query}%", f"%{query}%", f"%{query}%",
                    f"%{query}%", f"%{query}%"
                ))
                
                results = cursor.fetchall()
                conn.close()
                
                for concept, description, category, tags in results:
                    # Calcular relevancia más sofisticada
                    relevance = self._calculate_relevance(query, concept, description)
                    
                    # Bonus por coincidencia exacta en concepto
                    if query.lower() in concept.lower():
                        relevance += 0.3
                    
                    # Bonus por coincidencia en tags
                    if tags and query.lower() in tags.lower():
                        relevance += 0.2
                    
                    if relevance > 0.1:  # Umbral bajo para incluir más resultados
                        chunk = DocumentChunk(
                            content=description,
                            source='local_knowledge_db',
                            category=category or 'general',
                            confidence=min(relevance, 1.0),
                            timestamp=datetime.now().isoformat()
                        )
                        chunks.append(chunk)
                        print(f"  📚 DB Local: {concept} (confianza: {relevance:.2f})")
        
        except Exception as e:
            print(f"⚠️ Error búsqueda BD local: {e}")
        
        # 2. BÚSQUEDA EN CONOCIMIENTO HARDCODEADO (FALLBACK)
        local_knowledge = {
            'inteligencia artificial': "La IA es la simulación de procesos de inteligencia humana por máquinas, especialmente sistemas informáticos.",
            'machine learning': "ML es un método de análisis de datos que automatiza la construcción de modelos analíticos.",
            'rag': "RAG (Retrieval-Augmented Generation) combina búsqueda de información con generación de texto por IA para respuestas más precisas y actualizadas.",
            'programación': "La programación es el proceso de crear un conjunto de instrucciones que le dicen a una computadora cómo realizar una tarea.",
            'roma': "Roma es la capital de Italia, conocida como la Ciudad Eterna, centro del antiguo Imperio Romano.",
            'ciudad': "Una ciudad es un asentamiento urbano con alta densidad de población y infraestructura desarrollada."
        }
        
        query_lower = query.lower()
        for concept, description in local_knowledge.items():
            if concept in query_lower or query_lower in concept:
                chunk = DocumentChunk(
                    content=description,
                    source='local_knowledge_fallback',
                    category='fallback',
                    confidence=0.6,
                    timestamp=datetime.now().isoformat()
                )
                chunks.append(chunk)
                print(f"  💾 Fallback: {concept}")
        
        return sorted(chunks, key=lambda x: x.confidence, reverse=True)
    
    def _search_real_time_data(self, query: str, analysis: Dict) -> List[DocumentChunk]:
        """Búsqueda de datos en tiempo real"""
        chunks = []
        
        # Detectar consultas que requieren datos actuales
        real_time_indicators = ['hoy', 'actual', 'últimas noticias', 'precio actual', 'tiempo']
        
        if any(indicator in query.lower() for indicator in real_time_indicators):
            chunk = DocumentChunk(
                content=f"Información en tiempo real sobre '{query}' no disponible en este momento. Sugiero consultar fuentes oficiales.",
                source='real_time_placeholder',
                category='real_time',
                confidence=0.5,
                timestamp=datetime.now().isoformat()
            )
            chunks.append(chunk)
        
        return chunks
    
    def _calculate_relevance(self, query: str, title: str, content: str) -> float:
        """Calcular relevancia entre consulta y contenido"""
        query_words = set(query.lower().split())
        title_words = set(title.lower().split()) if title else set()
        content_words = set(content.lower().split()) if content else set()
        
        # Intersección con título (peso mayor)
        title_match = len(query_words & title_words) / max(len(query_words), 1)
        
        # Intersección con contenido
        content_match = len(query_words & content_words) / max(len(query_words), 1)
        
        # Puntuación combinada
        relevance = (title_match * 0.7) + (content_match * 0.3)
        
        return min(relevance, 1.0)
    
    def _rank_and_filter_chunks(self, chunks: List[DocumentChunk], query: str) -> List[DocumentChunk]:
        """Ranking y filtrado de chunks relevantes"""
        
        # Filtrar por confianza mínima
        filtered_chunks = [c for c in chunks if c.confidence > self.min_confidence_threshold]
        
        # Ordenar por confianza y diversidad de fuentes
        ranked_chunks = sorted(filtered_chunks, key=lambda x: (
            x.confidence,
            1 if x.source == 'supabase_knowledge' else 0.8,  # Priorizar Supabase
            -len(x.content)  # Preferir contenido más conciso
        ), reverse=True)
        
        return ranked_chunks[:self.max_sources]
    
    def _generate_contextual_response(self, query: str, chunks: List[DocumentChunk], analysis: Dict) -> Dict:
        """Generar respuesta contextual usando chunks relevantes"""
        
        if not chunks:
            # MEJORAR: Respuesta más inteligente cuando no hay resultados
            fallback_suggestions = self._generate_fallback_suggestions(query, analysis)
            
            return {
                'answer': fallback_suggestions,
                'method': 'intelligent_fallback',
                'confidence': 0.3
            }
        
        # Construir contexto
        context_parts = []
        sources_used = []
        
        for chunk in chunks:
            context_parts.append(chunk.content)
            sources_used.append({
                'source': chunk.source,
                'category': chunk.category,
                'confidence': chunk.confidence
            })
        
        # Generar respuesta basada en contexto
        if len(chunks) == 1:
            # Respuesta directa para un solo resultado relevante
            answer = f"{chunks[0].content}\n\n¿Te gustaría que profundice en algún aspecto específico?"
            method = 'direct_retrieval'
            confidence = chunks[0].confidence
        else:
            # Síntesis de múltiples fuentes
            answer = self._synthesize_multiple_sources(query, chunks, analysis)
            method = 'multi_source_synthesis'
            confidence = sum(c.confidence for c in chunks) / len(chunks)
        
        return {
            'answer': answer,
            'sources': sources_used,
            'confidence': confidence,
            'method': method,
            'context_used': context_parts
        }
    
    def _generate_fallback_suggestions(self, query: str, analysis: Dict) -> str:
        """Generar sugerencias inteligentes cuando no hay resultados directos"""
        
        query_lower = query.lower()
        
        # Detectar el tipo de consulta y ofrecer ayuda específica
        if any(word in query_lower for word in ['ciudad', 'roma', 'parís', 'madrid', 'londres']):
            return """🌍 No encontré información específica sobre esa ciudad en mi base de conocimiento actual.

¿Te interesa que:
• 📍 Busque información actualizada en la web
• 🏛️ Te cuente sobre ciudades históricas importantes
• 🗺️ Te explique sobre geografía en general

También puedes preguntar sobre ciudades específicas como Roma, París, Madrid o Londres."""
        
        elif any(word in query_lower for word in ['país', 'nación', 'geografia']):
            return """🗺️ No tengo información específica sobre ese país en este momento.

Puedo ayudarte con:
• 🌍 Información sobre países europeos
• 📍 Geografía general
• 🏛️ Historia de civilizaciones
• 🌐 Buscar información actualizada en internet

¿Sobre qué país específico te gustaría aprender?"""
        
        elif any(word in query_lower for word in ['historia', 'antiguo', 'antigua']):
            return """📚 No encontré información histórica específica sobre tu consulta.

Puedo contarte sobre:
• 🏛️ Imperio Romano y Roma antigua
• 🎨 Renacimiento europeo
• 🌍 Civilizaciones antiguas
• 📖 Períodos históricos importantes

¿Hay algún período histórico específico que te interese?"""
        
        elif any(word in query_lower for word in ['tecnología', 'ciencia', 'ia', 'programación']):
            return """💻 No encontré información específica sobre ese tema tecnológico.

Puedo ayudarte con:
• 🤖 Inteligencia Artificial y Machine Learning
• 💾 Programación en Python
• 🌐 Desarrollo web con Flask y React
• 🧠 Sistemas RAG como yo mismo

¿Te interesa algún tema tecnológico específico?"""
        
        else:
            # Fallback general
            return f"""🤔 No encontré información específica sobre "{query}" en mi base de conocimiento actual.

Esto podría ayudarte:
• 🔍 Reformula tu pregunta con más detalles
• 🌐 Puedo buscar información actualizada en internet
• 📚 Tengo conocimiento sobre geografía, historia, tecnología y cultura
• 💬 También puedes preguntarme sobre mis propias capacidades

¿Hay algo específico sobre lo que te gustaría que busque?"""
    
    def _synthesize_multiple_sources(self, query: str, chunks: List[DocumentChunk], analysis: Dict) -> str:
        """Sintetizar información de múltiples fuentes"""
        
        # Agrupar por categoría
        by_category = defaultdict(list)
        for chunk in chunks:
            by_category[chunk.category].append(chunk)
        
        # Construir respuesta sintética
        response_parts = []
        
        # Introducción contextual
        topic = self._extract_main_topic(query)
        response_parts.append(f"Basándome en múltiples fuentes, puedo explicarte sobre **{topic}**:")
        
        # Información principal
        main_chunks = sorted(chunks, key=lambda x: x.confidence, reverse=True)[:3]
        for i, chunk in enumerate(main_chunks, 1):
            source_name = {
                'supabase_knowledge': 'mi base de conocimiento',
                'web_search': 'información web reciente',
                'conversation_memory': 'nuestras conversaciones previas',
                'local_knowledge_db': 'mi base de datos local',
                'local_knowledge_fallback': 'conocimiento fundamental'
            }.get(chunk.source, 'fuentes adicionales')
            
            response_parts.append(f"\n**{i}. Desde {source_name}:**\n{chunk.content}")
        
        # Conclusión
        if len(chunks) > 3:
            response_parts.append(f"\n*Información adicional disponible desde {len(chunks) - 3} fuentes más.*")
        
        response_parts.append("\n¿Hay algún aspecto específico que te gustaría explorar más a fondo?")
        
        return "\n".join(response_parts)
    
    def _extract_main_topic(self, query: str) -> str:
        """Extraer el tema principal de la consulta"""
        
        # Limpiar la consulta
        query_clean = query.lower().strip()
        
        # Patrones comunes
        city_patterns = ['ciudad de', 'la ciudad', 'en ']
        for pattern in city_patterns:
            if pattern in query_clean:
                # Extraer lo que viene después del patrón
                parts = query_clean.split(pattern)
                if len(parts) > 1:
                    return parts[1].strip().title()
        
        # Capitalizar primera letra de cada palabra importante
        words = query_clean.split()
        important_words = []
        skip_words = ['de', 'la', 'el', 'en', 'del', 'que', 'es', 'como', 'por', 'para']
        
        for word in words:
            if word not in skip_words and len(word) > 2:
                important_words.append(word.title())
        
        if important_words:
            return ' '.join(important_words)
        else:
            return query.title()
            response_parts.append(f"\n*Información adicional disponible desde {len(chunks) - 3} fuentes más.*")
        
        response_parts.append("\n¿Hay algún aspecto específico que te gustaría explorar más a fondo?")
        
        return "\n".join(response_parts)
    
    def _post_process_response(self, generated_response: Dict, chunks: List[DocumentChunk], query: str) -> Dict:
        """Post-procesamiento de la respuesta"""
        
        # Agregar metadatos
        generated_response.update({
            'context_used': [chunk.content[:100] + "..." for chunk in chunks],
            'sources': generated_response.get('sources', []),
            'query_analyzed': query,
            'timestamp': datetime.now().isoformat()
        })
        
        return generated_response
    
    def _update_user_profile(self, query: str, response: Dict):
        """Actualizar perfil del usuario basado en la interacción"""
        
        # Extraer intereses
        entities = self._extract_entities(query)
        for entity in entities:
            self.user_profile['interests'][entity] += 1
        
        # Ajustar nivel de experticia
        if any(word in query.lower() for word in ['explica', 'qué es', 'define']):
            # Usuario pidiendo explicaciones básicas
            if self.user_profile['expertise_level'] == 'advanced':
                self.user_profile['expertise_level'] = 'intermediate'
        elif any(word in query.lower() for word in ['implementar', 'configurar', 'optimizar']):
            # Usuario con consultas avanzadas
            if self.user_profile['expertise_level'] == 'beginner':
                self.user_profile['expertise_level'] = 'intermediate'
    
    def _store_interaction(self, query: str, response: Dict, chunks: List[DocumentChunk]):
        """Almacenar interacción para memoria conversacional"""
        
        interaction = {
            'user_query': query,
            'response': response.get('answer', ''),
            'confidence': response.get('confidence', 0),
            'sources_used': [chunk.source for chunk in chunks],
            'timestamp': datetime.now().isoformat()
        }
        
        self.conversation_context.append(interaction)
        
        # Mantener solo las últimas 20 interacciones
        if len(self.conversation_context) > 20:
            self.conversation_context = self.conversation_context[-20:]
    
    # Métodos auxiliares de análisis
    def _detect_intent(self, query: str) -> str:
        """Detectar intención de la consulta"""
        intents = {
            'definition': ['qué es', 'define', 'significa', 'definición'],
            'explanation': ['explica', 'cómo', 'por qué', 'para qué'],
            'comparison': ['diferencia', 'comparar', 'versus', 'mejor'],
            'procedure': ['pasos', 'proceso', 'implementar', 'hacer'],
            'recommendation': ['recomienda', 'sugiere', 'mejor opción'],
            'troubleshooting': ['problema', 'error', 'no funciona', 'ayuda']
        }
        
        query_lower = query.lower()
        for intent, keywords in intents.items():
            if any(keyword in query_lower for keyword in keywords):
                return intent
        
        return 'general'
    
    def _extract_entities(self, query: str) -> List[str]:
        """Extraer entidades nombradas simples"""
        # Implementación básica - podría mejorarse con NLP
        entities = []
        
        # Palabras técnicas comunes
        tech_terms = [
            'python', 'javascript', 'html', 'css', 'react', 'node',
            'machine learning', 'deep learning', 'ai', 'blockchain',
            'docker', 'kubernetes', 'aws', 'azure', 'google cloud'
        ]
        
        query_lower = query.lower()
        for term in tech_terms:
            if term in query_lower:
                entities.append(term)
        
        return entities
    
    def _assess_complexity(self, query: str) -> str:
        """Evaluar complejidad de la consulta"""
        word_count = len(query.split())
        
        if word_count < 5:
            return 'simple'
        elif word_count < 15:
            return 'medium'
        else:
            return 'complex'
    
    def _identify_domain(self, query: str) -> str:
        """Identificar dominio de la consulta"""
        domains = {
            'programming': ['código', 'programar', 'python', 'javascript', 'html'],
            'ai_ml': ['inteligencia artificial', 'machine learning', 'IA', 'modelo'],
            'philosophy': ['amor', 'vida', 'existencia', 'libertad', 'verdad'],
            'science': ['universo', 'física', 'química', 'biología', 'evolución'],
            'technology': ['internet', 'blockchain', 'cloud', 'ciberseguridad'],
            'health': ['salud', 'ejercicio', 'nutrición', 'meditación'],
            'general': []
        }
        
        query_lower = query.lower()
        for domain, keywords in domains.items():
            if any(keyword in query_lower for keyword in keywords):
                return domain
        
        return 'general'
    
    def _classify_question_type(self, query: str) -> str:
        """Clasificar tipo de pregunta"""
        if '?' not in query:
            return 'statement'
        
        question_words = ['qué', 'cómo', 'cuándo', 'dónde', 'por qué', 'para qué', 'quién']
        query_lower = query.lower()
        
        for word in question_words:
            if word in query_lower:
                return f'question_{word}'
        
        return 'question_general'
    
    def _needs_real_time_data(self, query: str) -> bool:
        """Determinar si la consulta requiere datos en tiempo real"""
        real_time_indicators = [
            'hoy', 'actual', 'últimas', 'reciente', 'precio actual',
            'tiempo', 'clima', 'noticias', 'tendencias'
        ]
        
        query_lower = query.lower()
        return any(indicator in query_lower for indicator in real_time_indicators)
    
    def _determine_source_priority(self, analysis: Dict) -> List[str]:
        """Determinar prioridad de fuentes según análisis"""
        
        priority = ['supabase_knowledge']  # Siempre primera prioridad
        
        if analysis.get('requires_real_time', False):
            priority.append('web_search')
            priority.append('real_time_data')
        
        if analysis.get('intent') in ['comparison', 'explanation']:
            priority.append('conversation_memory')
        
        priority.extend(['local_knowledge'])
        
        return priority

# Función de fábrica para crear el sistema RAG
def create_rag_system(cloud_connector=None, emotion_detector=None) -> ARIARAGSystem:
    """Crear una instancia del sistema RAG"""
    return ARIARAGSystem(cloud_connector, emotion_detector)