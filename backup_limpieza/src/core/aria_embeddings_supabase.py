#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🧠 ARIA EMBEDDINGS SUPABASE
==========================

Sistema de embeddings para ARIA que utiliza Supabase como base de datos vectorial.
Almacena y busca embeddings en la nube para ahorrar espacio local.

Características:
✅ Embeddings locales con sentence-transformers
✅ Almacenamiento en Supabase (nube)
✅ Búsqueda semántica rápida
✅ Categorización automática
✅ Sin dependencia de OpenAI
✅ Soporte para múltiples idiomas

Fecha: 24 de octubre de 2025
"""

import os
import json
import numpy as np
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime
import logging
from sentence_transformers import SentenceTransformer
from supabase import create_client, Client

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ARIAEmbeddingsSupabase:
    """Sistema de embeddings para ARIA con almacenamiento en Supabase"""
    
    def __init__(self, supabase_url: str = None, supabase_key: str = None):
        """
        Inicializar el sistema de embeddings
        
        Args:
            supabase_url: URL de tu proyecto Supabase
            supabase_key: API Key de Supabase
        """
        # Cargar configuración desde variables de entorno o archivos
        self.supabase_url = supabase_url or os.getenv('SUPABASE_URL')
        self.supabase_key = supabase_key or os.getenv('SUPABASE_ANON_KEY')
        
        if not self.supabase_url or not self.supabase_key:
            logger.error("❌ Configuración de Supabase no encontrada")
            raise ValueError("Necesitas SUPABASE_URL y SUPABASE_ANON_KEY")
        
        # Inicializar cliente Supabase
        try:
            self.supabase: Client = create_client(self.supabase_url, self.supabase_key)
            logger.info("✅ Conectado a Supabase")
        except Exception as e:
            logger.error(f"❌ Error conectando a Supabase: {e}")
            raise
        
        # Inicializar modelo de embeddings local
        try:
            self.modelo = SentenceTransformer('all-MiniLM-L6-v2')
            logger.info("✅ Modelo de embeddings cargado (all-MiniLM-L6-v2)")
        except Exception as e:
            logger.error(f"❌ Error cargando modelo: {e}")
            raise
        
        # Dimensiones del modelo (384 para all-MiniLM-L6-v2)
        self.embedding_dim = 384
    
    def generar_embedding(self, texto: str) -> List[float]:
        """Generar embedding para un texto"""
        try:
            embedding = self.modelo.encode([texto])[0]
            return embedding.tolist()
        except Exception as e:
            logger.error(f"Error generando embedding: {e}")
            return []
    
    def agregar_texto(self, 
                      texto: str, 
                      categoria: str = 'general',
                      subcategoria: str = None,
                      fuente: str = 'conversation',
                      idioma: str = 'es',
                      metadatos: Dict = None) -> bool:
        """
        Agregar texto con su embedding a Supabase
        
        Args:
            texto: Texto a almacenar
            categoria: Categoría del texto
            subcategoria: Subcategoría opcional
            fuente: Fuente del texto
            idioma: Idioma del texto
            metadatos: Metadatos adicionales
        
        Returns:
            bool: True si se agregó correctamente
        """
        try:
            # Generar embedding
            embedding = self.generar_embedding(texto)
            if not embedding:
                return False
            
            # Preparar datos
            datos = {
                'texto': texto,
                'embedding': embedding,
                'categoria': categoria,
                'subcategoria': subcategoria,
                'fuente': fuente,
                'idioma': idioma,
                'metadatos': metadatos or {}
            }
            
            # Insertar en Supabase
            resultado = self.supabase.table('aria_embeddings').insert(datos).execute()
            
            if resultado.data:
                logger.info(f"✅ Texto agregado: {texto[:50]}...")
                return True
            else:
                logger.error("❌ Error insertando en Supabase")
                return False
                
        except Exception as e:
            logger.error(f"Error agregando texto: {e}")
            return False
    
    def buscar_similares(self, 
                         consulta: str, 
                         limite: int = 5,
                         categoria: str = None,
                         umbral_similitud: float = 0.7) -> List[Dict]:
        """
        Buscar textos similares a una consulta
        
        Args:
            consulta: Texto de búsqueda
            limite: Número máximo de resultados
            categoria: Filtrar por categoría específica
            umbral_similitud: Similitud mínima (0-1)
        
        Returns:
            Lista de textos similares con sus similitudes
        """
        try:
            # Generar embedding de la consulta
            embedding_consulta = self.generar_embedding(consulta)
            if not embedding_consulta:
                return []
            
            # Construir query base
            query = self.supabase.table('aria_embeddings').select('*')
            
            # Filtrar por categoría si se especifica
            if categoria:
                query = query.eq('categoria', categoria)
            
            # Ejecutar búsqueda
            resultado = query.execute()
            
            if not resultado.data:
                return []
            
            # Calcular similitudes manualmente (ya que pgvector se maneja en SQL)
            similitudes = []
            embedding_np = np.array(embedding_consulta)
            
            for item in resultado.data:
                embedding_item = np.array(item['embedding'])
                
                # Calcular similitud coseno
                similitud = np.dot(embedding_np, embedding_item) / (
                    np.linalg.norm(embedding_np) * np.linalg.norm(embedding_item)
                )
                
                if similitud >= umbral_similitud:
                    item['similitud'] = float(similitud)
                    similitudes.append(item)
            
            # Ordenar por similitud descendente
            similitudes.sort(key=lambda x: x['similitud'], reverse=True)
            
            return similitudes[:limite]
            
        except Exception as e:
            logger.error(f"Error buscando similares: {e}")
            return []
    
    def agregar_conocimiento(self,
                           concepto: str,
                           descripcion: str,
                           categoria: str = 'knowledge',
                           tags: List[str] = None,
                           confianza: float = 0.8,
                           ejemplos: List[str] = None,
                           relaciones: Dict = None) -> bool:
        """
        Agregar conocimiento estructurado con embedding
        
        Args:
            concepto: Nombre del concepto
            descripcion: Descripción del concepto
            categoria: Categoría del conocimiento
            tags: Etiquetas asociadas
            confianza: Nivel de confianza (0-1)
            ejemplos: Ejemplos del concepto
            relaciones: Relaciones con otros conceptos
        
        Returns:
            bool: True si se agregó correctamente
        """
        try:
            # Generar embedding de la descripción
            embedding = self.generar_embedding(descripcion)
            if not embedding:
                return False
            
            # Preparar datos
            datos = {
                'concepto': concepto,
                'descripcion': descripcion,
                'embedding': embedding,
                'categoria': categoria,
                'tags': tags or [],
                'confianza': confianza,
                'ejemplos': ejemplos or [],
                'relaciones': relaciones or {}
            }
            
            # Insertar en Supabase
            resultado = self.supabase.table('aria_knowledge_vectors').insert(datos).execute()
            
            if resultado.data:
                logger.info(f"✅ Conocimiento agregado: {concepto}")
                return True
            else:
                logger.error("❌ Error insertando conocimiento")
                return False
                
        except Exception as e:
            logger.error(f"Error agregando conocimiento: {e}")
            return False
    
    def buscar_conocimiento(self, consulta: str, limite: int = 3) -> List[Dict]:
        """
        Buscar conocimiento relacionado con una consulta
        
        Args:
            consulta: Texto de búsqueda
            limite: Número máximo de resultados
        
        Returns:
            Lista de conocimientos relacionados
        """
        try:
            # Generar embedding de la consulta
            embedding_consulta = self.generar_embedding(consulta)
            if not embedding_consulta:
                return []
            
            # Obtener todos los conocimientos
            resultado = self.supabase.table('aria_knowledge_vectors').select('*').execute()
            
            if not resultado.data:
                return []
            
            # Calcular similitudes
            similitudes = []
            embedding_np = np.array(embedding_consulta)
            
            for item in resultado.data:
                embedding_item = np.array(item['embedding'])
                
                # Calcular similitud coseno
                similitud = np.dot(embedding_np, embedding_item) / (
                    np.linalg.norm(embedding_np) * np.linalg.norm(embedding_item)
                )
                
                item['similitud'] = float(similitud)
                similitudes.append(item)
            
            # Ordenar por similitud descendente
            similitudes.sort(key=lambda x: x['similitud'], reverse=True)
            
            return similitudes[:limite]
            
        except Exception as e:
            logger.error(f"Error buscando conocimiento: {e}")
            return []
    
    def obtener_estadisticas(self) -> Dict:
        """Obtener estadísticas de la base de embeddings"""
        try:
            # Contar embeddings por categoría
            resultado_embeddings = self.supabase.table('aria_embeddings').select('categoria').execute()
            resultado_knowledge = self.supabase.table('aria_knowledge_vectors').select('categoria').execute()
            
            categorias_embeddings = {}
            for item in resultado_embeddings.data:
                cat = item['categoria']
                categorias_embeddings[cat] = categorias_embeddings.get(cat, 0) + 1
            
            categorias_knowledge = {}
            for item in resultado_knowledge.data:
                cat = item['categoria']
                categorias_knowledge[cat] = categorias_knowledge.get(cat, 0) + 1
            
            return {
                'total_embeddings': len(resultado_embeddings.data),
                'total_knowledge': len(resultado_knowledge.data),
                'categorias_embeddings': categorias_embeddings,
                'categorias_knowledge': categorias_knowledge
            }
            
        except Exception as e:
            logger.error(f"Error obteniendo estadísticas: {e}")
            return {}
    
    def limpiar_categoria(self, categoria: str) -> bool:
        """Eliminar todos los embeddings de una categoría"""
        try:
            # Eliminar de embeddings
            self.supabase.table('aria_embeddings').delete().eq('categoria', categoria).execute()
            # Eliminar de knowledge
            self.supabase.table('aria_knowledge_vectors').delete().eq('categoria', categoria).execute()
            
            logger.info(f"✅ Categoría '{categoria}' limpiada")
            return True
            
        except Exception as e:
            logger.error(f"Error limpiando categoría: {e}")
            return False

# Funciones de utilidad
def crear_embedding_system():
    """Crear instancia del sistema de embeddings"""
    try:
        return ARIAEmbeddingsSupabase()
    except Exception as e:
        logger.error(f"Error creando sistema de embeddings: {e}")
        return None

def test_embedding_system():
    """Probar el sistema de embeddings"""
    print("🧪 Probando sistema de embeddings...")
    
    # Crear sistema
    system = crear_embedding_system()
    if not system:
        print("❌ No se pudo crear el sistema")
        return
    
    # Agregar algunos textos de prueba
    textos_prueba = [
        ("Los tequeños son una comida venezolana hecha de queso y masa", "comida", "venezolana"),
        ("Python es un lenguaje de programación versátil", "programacion", "lenguajes"),
        ("La inteligencia artificial ayuda a automatizar tareas", "tecnologia", "ia"),
        ("Los gatos son animales domésticos muy independientes", "animales", "mascotas")
    ]
    
    print("\n📝 Agregando textos de prueba...")
    for texto, categoria, subcategoria in textos_prueba:
        if system.agregar_texto(texto, categoria, subcategoria):
            print(f"✅ {texto[:30]}...")
        else:
            print(f"❌ Error con: {texto[:30]}...")
    
    # Probar búsquedas
    consultas = [
        "¿Qué es un tequeño?",
        "lenguajes de programación",
        "automatización con IA"
    ]
    
    print("\n🔍 Probando búsquedas...")
    for consulta in consultas:
        print(f"\nConsulta: {consulta}")
        resultados = system.buscar_similares(consulta, limite=2)
        for resultado in resultados:
            print(f"  • {resultado['texto'][:50]}... (Similitud: {resultado['similitud']:.2f})")
    
    # Mostrar estadísticas
    print("\n📊 Estadísticas:")
    stats = system.obtener_estadisticas()
    print(json.dumps(stats, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    test_embedding_system()