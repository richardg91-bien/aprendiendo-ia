#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🗄️ ARIA - Super Base (Supabase Integration)
Sistema de almacenamiento avanzado para relaciones de APIs y conocimiento
"""

import os
import json
import logging
from datetime import datetime, timezone
from typing import Dict, List, Optional, Any
import asyncio

# Cargar variables de entorno
try:
    from dotenv import load_dotenv
    # Buscar archivo .env en directorios padre
    current_dir = os.path.dirname(__file__)
    for i in range(3):  # Buscar hasta 3 niveles arriba
        env_path = os.path.join(current_dir, '.env')
        if os.path.exists(env_path):
            load_dotenv(env_path)
            print(f"✅ Variables de entorno cargadas desde: {env_path}")
            break
        current_dir = os.path.dirname(current_dir)
    else:
        # Buscar en raíz del proyecto
        project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        env_path = os.path.join(project_root, '.env')
        if os.path.exists(env_path):
            load_dotenv(env_path)
            print(f"✅ Variables de entorno cargadas desde: {env_path}")
except ImportError:
    print("⚠️ python-dotenv no disponible")

try:
    from supabase import create_client, Client
    SUPABASE_AVAILABLE = True
    print("✅ Supabase disponible")
except ImportError:
    SUPABASE_AVAILABLE = False
    print("⚠️ Supabase no disponible. Instalar con: pip install supabase")

class ARIASuperBase:
    """
    Sistema de base de datos avanzado para ARIA
    """
    Este archivo ahora solo importa el módulo aria_superbase desde backend/services.
    La lógica principal se encuentra en backend/services/aria_superbase.py
    """

    from backend.services.aria_superbase import *
                result = query.execute()
                return result.data or []
                
            except Exception as e:
                print(f"❌ Error recuperando conocimiento: {e}")
        
        # Fallback local
        knowledge = []
        for key, data in self.fallback_storage.items():
            if isinstance(data, dict) and 'concept' in data:
                if not concept or concept.lower() in data['concept'].lower():
                    if not category or data.get('category') == category:
                        knowledge.append(data)
        return knowledge
    
    def get_api_relations(self, api_type: Optional[str] = None) -> List[Dict]:
        """Recuperar relaciones de APIs"""
        if self.connected:
            try:
                query = self.supabase.table('aria_api_relations').select("*")
                if api_type:
                    query = query.eq('api_type', api_type)
                    
                result = query.execute()
                return result.data or []
                
            except Exception as e:
                print(f"❌ Error recuperando APIs: {e}")
        
        # Fallback local
        apis = self.fallback_storage.get('apis', [])
        if api_type:
            apis = [api for api in apis if api.get('api_type') == api_type]
        return apis
    
    def update_api_usage(self, api_name: str, success: bool = True, 
                        response_time: float = None) -> bool:
        """Actualizar estadísticas de uso de API"""
        if self.connected:
            try:
                # Obtener datos actuales
                current = self.supabase.table('aria_api_relations')\
                    .select("*").eq('api_name', api_name).execute()
                
                if current.data:
                    api_data = current.data[0]
                    
                    # Calcular nueva tasa de éxito
                    current_rate = api_data.get('success_rate', 1.0)
                    # Simplificado: promedio con peso
                    new_rate = (current_rate * 0.9) + (1.0 if success else 0.0) * 0.1
                    
                    updates = {
                        'last_used': datetime.now(timezone.utc).isoformat(),
                        'success_rate': new_rate
                    }
                    
                    if response_time:
                        current_avg = api_data.get('response_time_avg', response_time)
                        updates['response_time_avg'] = (current_avg * 0.8) + (response_time * 0.2)
                    
                    self.supabase.table('aria_api_relations')\
                        .update(updates).eq('api_name', api_name).execute()
                    
                    print(f"✅ Estadísticas de {api_name} actualizadas")
                    return True
                    
            except Exception as e:
                print(f"❌ Error actualizando API stats: {e}")
        
        return False
    
    def get_conversation_history(self, session_id: Optional[str] = None, 
                               limit: int = 10) -> List[Dict]:
        """Recuperar historial de conversaciones"""
        if self.connected:
            try:
                query = self.supabase.table('aria_conversations')\
                    .select("*").order('created_at', desc=True)
                
                if session_id:
                    query = query.eq('session_id', session_id)
                    
                query = query.limit(limit)
                result = query.execute()
                return result.data or []
                
            except Exception as e:
                print(f"❌ Error recuperando historial: {e}")
        
        # Fallback local
        conversations = self.fallback_storage.get('conversations', [])
        if session_id:
            conversations = [c for c in conversations if c.get('session_id') == session_id]
        return conversations[-limit:]
    
    def get_database_stats(self) -> Dict[str, Any]:
        """Obtener estadísticas de la base de datos"""
        stats = {
            'connected': self.connected,
            'knowledge_count': 0,
            'api_relations_count': 0,
            'conversations_count': 0,
            'fallback_used': not self.connected
        }
        
        if self.connected:
            try:
                # Contar registros en cada tabla
                tables = ['aria_knowledge', 'aria_api_relations', 'aria_conversations']
                for table in tables:
                    result = self.supabase.table(table).select("id", count="exact").execute()
                    stats[f'{table.replace("aria_", "")}_count'] = result.count or 0
                    
            except Exception as e:
                print(f"❌ Error obteniendo estadísticas: {e}")
        else:
            # Estadísticas locales
            stats['knowledge_count'] = len([k for k in self.fallback_storage.keys() 
                                          if isinstance(self.fallback_storage[k], dict) 
                                          and 'concept' in self.fallback_storage[k]])
            stats['api_relations_count'] = len(self.fallback_storage.get('apis', []))
            stats['conversations_count'] = len(self.fallback_storage.get('conversations', []))
        
        return stats
    
    def search_knowledge(self, query: str) -> List[Dict]:
        """Búsqueda avanzada en la base de conocimiento"""
        if self.connected:
            try:
                # Búsqueda en concepto y descripción
                result = self.supabase.table('aria_knowledge')\
                    .select("*")\
                    .or_(f'concept.ilike.%{query}%,description.ilike.%{query}%')\
                    .order('confidence', desc=True)\
                    .execute()
                
                return result.data or []
                
            except Exception as e:
                print(f"❌ Error en búsqueda: {e}")
        
        # Búsqueda local
        results = []
        for key, data in self.fallback_storage.items():
            if isinstance(data, dict) and 'concept' in data:
                if (query.lower() in data['concept'].lower() or 
                    query.lower() in data.get('description', '').lower()):
                    results.append(data)
        
        return sorted(results, key=lambda x: x.get('confidence', 0), reverse=True)


# Instancia global
aria_superbase = ARIASuperBase()


def initialize_superbase():
    """Función de inicialización pública"""
    print("🗄️ Inicializando ARIA Super Base...")
    
    # Datos de ejemplo para prueba
    sample_data = [
        {
            'concept': 'inteligencia artificial',
            'description': 'Campo de la informática que se enfoca en crear sistemas que pueden realizar tareas que típicamente requieren inteligencia humana',
            'category': 'tecnologia',
            'confidence': 0.9
        },
        {
            'concept': 'machine learning',
            'description': 'Subcampo de la IA que permite a las máquinas aprender y mejorar automáticamente a partir de datos',
            'category': 'tecnologia',
            'confidence': 0.85
        },
        {
            'concept': 'supabase',
            'description': 'Plataforma de desarrollo de aplicaciones que proporciona base de datos PostgreSQL, autenticación y APIs en tiempo real',
            'category': 'database',
            'confidence': 0.8
        }
    ]
    
    # Insertar datos de ejemplo
    for data in sample_data:
        aria_superbase.store_knowledge(**data)
    
    # Ejemplo de relaciones de API
    api_examples = [
        {
            'api_name': 'OpenAI GPT',
            'api_type': 'ai_language',
            'endpoint': 'https://api.openai.com/v1/chat/completions',
            'method': 'POST',
            'description': 'API de OpenAI para generar texto con modelos de lenguaje'
        },
        {
            'api_name': 'Google Translate',
            'api_type': 'translation',
            'endpoint': 'https://translation.googleapis.com/language/translate/v2',
            'method': 'POST',
            'description': 'API de Google para traducción de texto'
        },
        {
            'api_name': 'Wikipedia Search',
            'api_type': 'knowledge_search',
            'endpoint': 'https://en.wikipedia.org/api/rest_v1/page/summary/',
            'method': 'GET',
            'description': 'API de Wikipedia para búsqueda de conocimiento'
        }
    ]
    
    for api in api_examples:
        aria_superbase.store_api_relation(**api)
    
    # Mostrar estadísticas
    stats = aria_superbase.get_database_stats()
    print(f"\n📊 Estadísticas de Super Base:")
    print(f"   🔗 Conectado: {'✅' if stats['connected'] else '❌'}")
    print(f"   🧠 Conocimiento: {stats['knowledge_count']} conceptos")
    print(f"   🔌 APIs: {stats['api_relations_count']} relaciones")
    print(f"   💬 Conversaciones: {stats['conversations_count']} registros")
    
    return aria_superbase


if __name__ == "__main__":
    # Configurar logging
    logging.basicConfig(level=logging.INFO)
    
    # Inicializar sistema
    superbase = initialize_superbase()
    
    # Ejemplo de uso
    print("\n🧪 Ejemplo de búsqueda:")
    results = superbase.search_knowledge("inteligencia")
    for result in results:
        print(f"   📝 {result['concept']}: {result['description'][:50]}...")