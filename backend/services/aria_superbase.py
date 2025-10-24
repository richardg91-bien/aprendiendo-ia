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

try:
    from dotenv import load_dotenv
    current_dir = os.path.dirname(__file__)
    for i in range(3):
        env_path = os.path.join(current_dir, '.env')
        if os.path.exists(env_path):
            load_dotenv(env_path)
            print(f"✅ Variables de entorno cargadas desde: {env_path}")
            break
        current_dir = os.path.dirname(current_dir)
    else:
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
    Clase principal para la gestión avanzada de la base de datos ARIA usando Supabase.

    Permite almacenar y recuperar conocimiento, relaciones con APIs externas y conversaciones,
    utilizando Supabase como backend principal y almacenamiento local como fallback.
    """
    
    def __init__(self):
        """
        Inicializa la conexión con Supabase y prepara el almacenamiento local de respaldo.
        """
        self.supabase: Optional['Client'] = None
        self.connected = False
        self.fallback_storage = {}
        self._initialize_connection()
        
    def _initialize_connection(self):
        """
        Inicializa la conexión con Supabase usando las variables de entorno.
        Si no está disponible, utiliza almacenamiento local como fallback.
        """
        if not SUPABASE_AVAILABLE:
            print("📝 Usando almacenamiento local como fallback")
            return
        try:
            url = os.getenv('SUPABASE_URL')
            key = os.getenv('SUPABASE_ANON_KEY')
            if not url or not key:
                print("⚠️ Configuración de Supabase no encontrada")
                return
            self.supabase = create_client(url, key)
            self.connected = True
            print("✅ Conectado a Supabase")
            self._ensure_tables_exist()
        except Exception as e:
            print(f"❌ Error conectando a Supabase: {e}")
            print("📝 Usando almacenamiento local")
    def _ensure_tables_exist(self):
        """
        Asegura que las tablas necesarias para ARIA existen en la base de datos Supabase.
        """
        if not self.connected:
            return
        tables_sql = [
            """
            CREATE TABLE IF NOT EXISTS aria_knowledge (
                id SERIAL PRIMARY KEY,
                concept VARCHAR(255) UNIQUE NOT NULL,
                description TEXT,
                category VARCHAR(100),
                confidence FLOAT DEFAULT 0.5,
                source VARCHAR(255),
                created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS aria_api_relations (
                id SERIAL PRIMARY KEY,
                api_name VARCHAR(255) NOT NULL,
                api_type VARCHAR(100),
                endpoint VARCHAR(500),
                method VARCHAR(10),
                description TEXT,
                status VARCHAR(50) DEFAULT 'active',
                last_used TIMESTAMP WITH TIME ZONE,
                success_rate FLOAT DEFAULT 1.0,
                response_time_avg FLOAT,
                created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                metadata JSONB
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS aria_conversations (
                id SERIAL PRIMARY KEY,
                user_message TEXT,
                aria_response TEXT,
                emotion_state VARCHAR(50),
                confidence FLOAT,
                apis_used TEXT,
                session_id VARCHAR(100),
                created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
            );
            """
        ]
        for sql in tables_sql:
            try:
                self.supabase.postgrest.rpc('execute_sql', {'sql': sql}).execute()
            except Exception as e:
                print(f"❌ Error creando/verificando tablas: {e}")
    def store_knowledge(self, concept: str, description: str = "", category: str = "general",
                       confidence: float = 0.5, source: str = "manual", extra_data: Dict = None) -> bool:
        """
        Almacena un concepto de conocimiento en la base de datos o en el almacenamiento local.

        Args:
            concept (str): Nombre del concepto.
            description (str): Descripción del concepto.
            category (str): Categoría del conocimiento.
            confidence (float): Nivel de confianza.
            source (str): Fuente del conocimiento.
            extra_data (Dict, opcional): Datos adicionales.
        Returns:
            bool: True si se almacena correctamente.
        """
        knowledge_data = {
            'concept': concept,
            'description': description,
            'category': category,
            'confidence': confidence,
            'source': source,
            'updated_at': datetime.now(timezone.utc).isoformat()
        }
        if extra_data and isinstance(extra_data, dict):
            knowledge_data.update(extra_data)
        if self.connected:
            try:
                result = self.supabase.table('aria_knowledge').upsert(
                    knowledge_data,
                    on_conflict='concept'
                ).execute()
                print(f"✅ Conocimiento almacenado en Supabase: {concept}")
                return True
            except Exception as e:
                print(f"❌ Error almacenando en Supabase: {e}")
        self.fallback_storage[concept] = knowledge_data
        print(f"📝 Conocimiento almacenado localmente: {concept}")
        return True
    def store_api_relation(self, api_name: str, api_type: str,
                          endpoint: str, method: str = "GET",
                          description: str = "", metadata: Dict = None) -> bool:
        """
        Almacena la relación con una API externa en la base de datos o localmente.

        Args:
            api_name (str): Nombre de la API.
            api_type (str): Tipo de API.
            endpoint (str): Endpoint de la API.
            method (str): Método HTTP.
            description (str): Descripción de la API.
            metadata (Dict, opcional): Metadatos adicionales.
        Returns:
            bool: True si se almacena correctamente.
        """
        api_data = {
            'api_name': api_name,
            'api_type': api_type,
            'endpoint': endpoint,
            'method': method.upper(),
            'description': description,
            'status': 'active',
            'last_used': datetime.now(timezone.utc).isoformat(),
            'metadata': json.dumps(metadata or {})
        }
        if self.connected:
            try:
                result = self.supabase.table('aria_api_relations').insert(api_data).execute()
                print(f"✅ Relación API almacenada: {api_name}")
                return True
            except Exception as e:
                print(f"❌ Error almacenando API: {e}")
        if 'apis' not in self.fallback_storage:
            self.fallback_storage['apis'] = []
        self.fallback_storage['apis'].append(api_data)
        print(f"📝 API almacenada localmente: {api_name}")
        return True
    def store_conversation(self, user_message: str, aria_response: str,
                          emotion_state: str = "neutral", confidence: float = 0.8,
                          apis_used: List[str] = None, session_id: str = None) -> bool:
        """
        Almacena una conversación entre el usuario y ARIA en la base de datos o localmente.

        Args:
            user_message (str): Mensaje del usuario.
            aria_response (str): Respuesta de ARIA.
            emotion_state (str): Estado emocional detectado.
            confidence (float): Nivel de confianza.
            apis_used (List[str], opcional): APIs utilizadas en la conversación.
            session_id (str, opcional): ID de sesión.
        Returns:
            bool: True si se almacena correctamente.
        """
        conv_data = {
            'user_message': user_message,
            'aria_response': aria_response,
            'emotion_state': emotion_state,
            'confidence': confidence,
            'apis_used': json.dumps(apis_used or []),
            'session_id': session_id or "default",
            'created_at': datetime.now(timezone.utc).isoformat()
        }
        if self.connected:
            try:
                result = self.supabase.table('aria_conversations').insert(conv_data).execute()
                print(f"✅ Conversación almacenada en Supabase")
                return True
            except Exception as e:
                print(f"❌ Error almacenando conversación: {e}")
        if 'conversations' not in self.fallback_storage:
            self.fallback_storage['conversations'] = []
        self.fallback_storage['conversations'].append(conv_data)
        print(f"📝 Conversación almacenada localmente")
        return True
