#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🤖 ARIA Enhanced Connector - Versión Robusta
============================================

Conector mejorado que funciona incluso cuando algunas APIs no están disponibles.
Proporciona fallbacks y funcionalidad offline cuando es necesario.

Fecha: 23 de octubre de 2025
"""

import os
import json
import logging
from datetime import datetime, timezone
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
import hashlib
import time

# Cargar variables de entorno
from dotenv import load_dotenv
load_dotenv()

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class ConnectionStatus:
    """Estado de las conexiones"""
    supabase: bool = False
    google_cloud: bool = False
    offline_mode: bool = False
    last_check: datetime = None
    error_count: int = 0

class ARIAEnhancedConnector:
    """Conector mejorado y resistente para ARIA"""
    
    def __init__(self):
        self.status = ConnectionStatus()
        self.cache = {}
        self.offline_storage = {}
        self.connection_cache_ttl = 300  # 5 minutos
        
        # Configuración
        self.supabase_url = os.getenv('SUPABASE_URL')
        self.supabase_key = os.getenv('SUPABASE_ANON_KEY')
        self.google_api_key = os.getenv('GOOGLE_CLOUD_API_KEY')
        
        # Clientes
        self.supabase_client = None
        
        # Inicializar
        self._initialize_connections()
    
    def _initialize_connections(self):
        """Inicializar conexiones de forma robusta"""
        print("🌐 Inicializando conexiones ARIA...")
        
        # Intentar Supabase
        self._try_supabase_connection()
        
        # Intentar Google Cloud (modo básico)
        self._try_google_connection()
        
        # Configurar modo offline si es necesario
        if not self.status.supabase and not self.status.google_cloud:
            self.status.offline_mode = True
            print("📱 Modo offline activado")
        
        self.status.last_check = datetime.now(timezone.utc)
        self._log_status()
    
    def _try_supabase_connection(self):
        """Intentar conexión a Supabase"""
        try:
            from supabase import create_client
            
            if not self.supabase_url or not self.supabase_key:
                print("⚠️ Credenciales de Supabase faltantes")
                return
            
            self.supabase_client = create_client(self.supabase_url, self.supabase_key)
            
            # Probar conexión simple
            result = self.supabase_client.table('aria_knowledge').select("id").limit(1).execute()
            
            self.status.supabase = True
            print("✅ Supabase conectado")
            
        except Exception as e:
            self.status.supabase = False
            print(f"⚠️ Supabase no disponible: {str(e)[:100]}...")
            logger.debug(f"Supabase error: {e}")
    
    def _try_google_connection(self):
        """Intentar conexión básica a Google"""
        try:
            if not self.google_api_key:
                print("⚠️ Google API key faltante")
                return
            
            # Solo verificar que la key existe, no hacer llamadas
            self.status.google_cloud = bool(self.google_api_key)
            print("✅ Google Cloud configurado (modo limitado)")
            
        except Exception as e:
            self.status.google_cloud = False
            print(f"⚠️ Google Cloud no disponible: {e}")
    
    def _log_status(self):
        """Mostrar estado de conexiones"""
        print("\n🔗 Estado de Conexiones ARIA:")
        print(f"   📊 Supabase: {'✅ Conectado' if self.status.supabase else '❌ Desconectado'}")
        print(f"   🌐 Google Cloud: {'✅ Limitado' if self.status.google_cloud else '❌ Desconectado'}")
        print(f"   📱 Modo Offline: {'✅ Activo' if self.status.offline_mode else '❌ Inactivo'}")
        print(f"   🕒 Última verificación: {self.status.last_check}")
    
    # ==========================================
    # MÉTODOS DE ALMACENAMIENTO
    # ==========================================
    
    def store_knowledge(self, concept: str, description: str, 
                       category: str = "general", confidence: float = 0.8) -> bool:
        """Almacenar conocimiento (Supabase o local)"""
        
        # Intentar Supabase primero
        if self.status.supabase:
            try:
                data = {
                    'concept': concept,
                    'description': description,
                    'category': category,
                    'confidence': confidence,
                    'source': 'aria_interaction',
                    'created_at': datetime.now(timezone.utc).isoformat(),
                    'updated_at': datetime.now(timezone.utc).isoformat()
                }
                
                result = self.supabase_client.table('aria_knowledge').upsert(data).execute()
                
                if result.data:
                    print(f"💾 Conocimiento guardado en Supabase: {concept}")
                    return True
                    
            except Exception as e:
                logger.warning(f"Error guardando en Supabase: {e}")
        
        # Fallback: almacenamiento local
        if concept not in self.offline_storage:
            self.offline_storage[concept] = {
                'description': description,
                'category': category,
                'confidence': confidence,
                'timestamp': datetime.now(timezone.utc).isoformat()
            }
            print(f"💾 Conocimiento guardado localmente: {concept}")
            return True
        
        return False
    
    def get_knowledge(self, concept: str = None) -> List[Dict]:
        """Obtener conocimiento (Supabase o local)"""
        
        # Intentar Supabase primero
        if self.status.supabase:
            try:
                query = self.supabase_client.table('aria_knowledge')
                
                if concept:
                    query = query.eq('concept', concept)
                
                result = query.select("*").execute()
                if result.data:
                    return result.data
                    
            except Exception as e:
                logger.warning(f"Error obteniendo de Supabase: {e}")
        
        # Fallback: almacenamiento local
        if concept:
            if concept in self.offline_storage:
                return [{'concept': concept, **self.offline_storage[concept]}]
            return []
        else:
            return [{'concept': k, **v} for k, v in self.offline_storage.items()]
    
    def store_conversation(self, user_input: str, aria_response: str, 
                          session_id: str) -> bool:
        """Almacenar conversación"""
        
        if self.status.supabase:
            try:
                data = {
                    'session_id': session_id,
                    'user_input': user_input,
                    'aria_response': aria_response,
                    'timestamp': datetime.now(timezone.utc).isoformat(),
                    'response_time': 0.5
                }
                
                result = self.supabase_client.table('aria_conversations').insert(data).execute()
                
                if result.data:
                    print(f"💬 Conversación guardada")
                    return True
                    
            except Exception as e:
                logger.warning(f"Error guardando conversación: {e}")
        
        # Fallback local (simple)
        conv_key = f"conv_{int(time.time())}"
        self.offline_storage[conv_key] = {
            'session_id': session_id,
            'user_input': user_input,
            'aria_response': aria_response,
            'timestamp': datetime.now(timezone.utc).isoformat()
        }
        
        return True
    
    # ==========================================
    # MÉTODOS UTILITARIOS
    # ==========================================
    
    def get_status_report(self) -> Dict:
        """Reporte de estado completo"""
        return {
            "connections": {
                "supabase": self.status.supabase,
                "google_cloud": self.status.google_cloud,
                "offline_mode": self.status.offline_mode
            },
            "storage": {
                "local_entries": len(self.offline_storage),
                "cache_entries": len(self.cache)
            },
            "last_check": self.status.last_check.isoformat() if self.status.last_check else None,
            "error_count": self.status.error_count
        }
    
    def test_all_features(self):
        """Probar todas las funcionalidades"""
        print("\n🧪 Probando funcionalidades ARIA...")
        
        # Test 1: Almacenar conocimiento
        test1 = self.store_knowledge(
            "test_enhanced_connector", 
            "Prueba del conector mejorado de ARIA",
            "testing"
        )
        print(f"Test almacenamiento: {'✅ OK' if test1 else '❌ Fallo'}")
        
        # Test 2: Recuperar conocimiento
        test2 = self.get_knowledge("test_enhanced_connector")
        print(f"Test recuperación: {'✅ OK' if test2 else '❌ Fallo'}")
        
        # Test 3: Almacenar conversación
        test3 = self.store_conversation(
            "Hola ARIA",
            "¡Hola! Soy ARIA, tu asistente inteligente.",
            "test_session_123"
        )
        print(f"Test conversación: {'✅ OK' if test3 else '❌ Fallo'}")
        
        return test1 and test2 and test3
    
    # ==========================================
    # MÉTODOS PARA EMOCIONES (INTERFAZ FUTURÍSTICA)
    # ==========================================
    
    def log_emotion(self, session_id: str, emotion_type: str, color_code: str, 
                   intensity: float = 0.5, context: str = None, 
                   triggered_by: str = None) -> bool:
        """Registrar una emoción de ARIA"""
        try:
            if self.status.supabase and self.supabase:
                # Intentar registrar en Supabase
                data = {
                    'session_id': session_id,
                    'emotion_type': emotion_type,
                    'color_code': color_code,
                    'intensity': intensity,
                    'context': context,
                    'triggered_by': triggered_by,
                    'created_at': datetime.now(timezone.utc).isoformat()
                }
                
                result = self.supabase.table('aria_emotions').insert(data).execute()
                
                if result.data:
                    logger.info(f"Emoción registrada en Supabase: {emotion_type}")
                    return True
                    
        except Exception as e:
            logger.warning(f"Error registrando emoción en Supabase: {e}")
        
        # Fallback: almacenar localmente
        emotion_key = f"emotion_{session_id}_{int(time.time())}"
        self.offline_storage[emotion_key] = {
            'session_id': session_id,
            'emotion_type': emotion_type,
            'color_code': color_code,
            'intensity': intensity,
            'context': context,
            'triggered_by': triggered_by,
            'created_at': datetime.now(timezone.utc).isoformat(),
            'stored_locally': True
        }
        
        logger.info(f"Emoción almacenada localmente: {emotion_type}")
        return True
    
    def get_recent_emotions(self, session_id: str = None, limit: int = 10) -> List[Dict]:
        """Obtener emociones recientes"""
        try:
            if self.status.supabase and self.supabase:
                # Obtener de Supabase
                query = self.supabase.table('aria_emotions').select('*')
                
                if session_id:
                    query = query.eq('session_id', session_id)
                
                result = query.order('created_at', desc=True).limit(limit).execute()
                
                if result.data:
                    logger.info(f"Emociones obtenidas de Supabase: {len(result.data)}")
                    return result.data
                    
        except Exception as e:
            logger.warning(f"Error obteniendo emociones de Supabase: {e}")
        
        # Fallback: obtener emociones locales
        local_emotions = []
        for key, emotion in self.offline_storage.items():
            if key.startswith('emotion_'):
                if not session_id or emotion.get('session_id') == session_id:
                    local_emotions.append(emotion)
        
        # Ordenar por fecha y limitar
        local_emotions.sort(key=lambda x: x.get('created_at', ''), reverse=True)
        return local_emotions[:limit]
    
    def create_session(self, session_id: str, user_id: str = None) -> bool:
        """Crear una nueva sesión de usuario"""
        try:
            if self.status.supabase and self.supabase:
                data = {
                    'session_id': session_id,
                    'user_id': user_id,
                    'start_time': datetime.now(timezone.utc).isoformat(),
                    'total_messages': 0,
                    'avg_emotion_intensity': 0.5,
                    'dominant_emotion': 'neutral',
                    'knowledge_learned': 0
                }
                
                result = self.supabase.table('aria_sessions').insert(data).execute()
                
                if result.data:
                    logger.info(f"Sesión creada en Supabase: {session_id}")
                    return True
                    
        except Exception as e:
            logger.warning(f"Error creando sesión en Supabase: {e}")
        
        # Fallback: almacenar localmente
        self.offline_storage[f"session_{session_id}"] = {
            'session_id': session_id,
            'user_id': user_id,
            'start_time': datetime.now(timezone.utc).isoformat(),
            'total_messages': 0,
            'stored_locally': True
        }
        
        logger.info(f"Sesión almacenada localmente: {session_id}")
        return True

# ==========================================
# INSTANCIA GLOBAL MEJORADA
# ==========================================

aria_enhanced = ARIAEnhancedConnector()

def get_enhanced_connector():
    """Obtener el conector mejorado"""
    return aria_enhanced

if __name__ == "__main__":
    print("🤖 ARIA Enhanced Connector - Pruebas")
    print("=" * 50)
    
    # Mostrar estado
    aria_enhanced._log_status()
    
    # Probar funcionalidades
    aria_enhanced.test_all_features()
    
    # Reporte final
    print("\n📋 Reporte Final:")
    report = aria_enhanced.get_status_report()
    print(json.dumps(report, indent=2, default=str))
