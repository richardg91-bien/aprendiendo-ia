#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🌐 ARIA Cloud Connector - Conexión Integrada
============================================

Conecta ARIA con Supabase y Google Cloud de forma unificada
para máxima funcionalidad y almacenamiento en la nube.

Características:
✅ Conexión a Supabase para base de datos
✅ Integración con Google Cloud APIs
✅ Sistema de cache inteligente
✅ Manejo de errores robusto
✅ Monitoreo de conexiones

Fecha: 23 de octubre de 2025
"""

import os
import json
import asyncio
import logging
from datetime import datetime, timezone
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
import hashlib
import time

# Cargar variables de entorno
from dotenv import load_dotenv
load_dotenv()

# Imports para Supabase
try:
    from supabase import create_client, Client
    SUPABASE_AVAILABLE = True
except ImportError:
    SUPABASE_AVAILABLE = False
    print("⚠️ supabase-py no está instalado")

# Imports para Google Cloud
try:
    import google.generativeai as genai
    from google.oauth2.credentials import Credentials
    from google.auth.transport.requests import Request
    GOOGLE_CLOUD_AVAILABLE = True
except ImportError:
    GOOGLE_CLOUD_AVAILABLE = False
    print("⚠️ google-cloud-aiplatform no está instalado")

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class ConnectionStatus:
    """Estado de las conexiones"""
    supabase: bool = False
    google_cloud: bool = False
    last_check: datetime = None
    error_count: int = 0
    
class ARIACloudConnector:
    """Conector unificado para servicios en la nube de ARIA"""
    
    def __init__(self):
        self.status = ConnectionStatus()
        self.cache = {}
        self.connection_cache_ttl = 300  # 5 minutos
        
        # Configuración de Supabase
        self.supabase_url = os.getenv('SUPABASE_URL')
        self.supabase_key = os.getenv('SUPABASE_ANON_KEY')
        self.supabase_client: Optional[Client] = None
        
        # Configuración de Google Cloud
        self.google_api_key = os.getenv('GOOGLE_CLOUD_API_KEY')
        self.google_oauth_client_id = os.getenv('GOOGLE_OAUTH_CLIENT_ID')
        
        # Inicializar conexiones
        self._initialize_connections()
    
    def _initialize_connections(self):
        """Inicializar todas las conexiones"""
        print("🌐 Inicializando conexiones en la nube...")
        
        # Conectar a Supabase
        self._connect_supabase()
        
        # Conectar a Google Cloud
        self._connect_google_cloud()
        
        # Actualizar estado
        self.status.last_check = datetime.now(timezone.utc)
        
        self._log_status()
    
    def _connect_supabase(self):
        """Conectar a Supabase"""
        try:
            if not SUPABASE_AVAILABLE:
                print("❌ Supabase no disponible - instalando...")
                self._install_supabase()
                return
            
            if not self.supabase_url or not self.supabase_key:
                print("❌ Credenciales de Supabase no configuradas")
                return
            
            # Crear cliente de Supabase
            self.supabase_client = create_client(self.supabase_url, self.supabase_key)
            
            # Probar conexión
            result = self.supabase_client.table('aria_knowledge').select("*").limit(1).execute()
            
            self.status.supabase = True
            print("✅ Conectado a Supabase exitosamente")
            
        except Exception as e:
            self.status.supabase = False
            self.status.error_count += 1
            print(f"❌ Error conectando a Supabase: {e}")
            logger.error(f"Supabase connection error: {e}")
    
    def _connect_google_cloud(self):
        """Conectar a Google Cloud"""
        try:
            if not GOOGLE_CLOUD_AVAILABLE:
                print("❌ Google Cloud no disponible - instalando...")
                self._install_google_cloud()
                return
            
            if not self.google_api_key:
                print("❌ API Key de Google Cloud no configurada")
                return
            
            # Configurar Google AI
            genai.configure(api_key=self.google_api_key)
            
            # Probar conexión
            model = genai.GenerativeModel('gemini-pro')
            response = model.generate_content("Test connection")
            
            self.status.google_cloud = True
            print("✅ Conectado a Google Cloud exitosamente")
            
        except Exception as e:
            self.status.google_cloud = False
            self.status.error_count += 1
            print(f"❌ Error conectando a Google Cloud: {e}")
            logger.error(f"Google Cloud connection error: {e}")
    
    def _install_supabase(self):
        """Instalar Supabase si no está disponible"""
        try:
            import subprocess
            subprocess.check_call(["pip", "install", "supabase"])
            print("✅ Supabase instalado exitosamente")
            global SUPABASE_AVAILABLE
            SUPABASE_AVAILABLE = True
        except Exception as e:
            print(f"❌ Error instalando Supabase: {e}")
    
    def _install_google_cloud(self):
        """Instalar Google Cloud si no está disponible"""
        try:
            import subprocess
            subprocess.check_call(["pip", "install", "google-generativeai", "google-cloud-aiplatform"])
            print("✅ Google Cloud instalado exitosamente")
            global GOOGLE_CLOUD_AVAILABLE
            GOOGLE_CLOUD_AVAILABLE = True
        except Exception as e:
            print(f"❌ Error instalando Google Cloud: {e}")
    
    def _log_status(self):
        """Mostrar estado de las conexiones"""
        print("\n🔗 Estado de Conexiones:")
        print(f"   📊 Supabase: {'✅ Conectado' if self.status.supabase else '❌ Desconectado'}")
        print(f"   🌐 Google Cloud: {'✅ Conectado' if self.status.google_cloud else '❌ Desconectado'}")
        print(f"   🕒 Última verificación: {self.status.last_check}")
        print(f"   ⚠️ Errores: {self.status.error_count}")
    
    # ==========================================
    # MÉTODOS DE SUPABASE
    # ==========================================
    
    def store_knowledge(self, concept: str, description: str, 
                       category: str = "general", confidence: float = 0.8) -> bool:
        """Almacenar conocimiento en Supabase"""
        if not self.status.supabase:
            return False
        
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
                print(f"💾 Conocimiento almacenado: {concept}")
                return True
            
        except Exception as e:
            logger.error(f"Error storing knowledge: {e}")
        
        return False
    
    def get_knowledge(self, concept: str = None) -> List[Dict]:
        """Obtener conocimiento de Supabase"""
        if not self.status.supabase:
            return []
        
        try:
            query = self.supabase_client.table('aria_knowledge')
            
            if concept:
                query = query.eq('concept', concept)
            
            result = query.select("*").execute()
            return result.data if result.data else []
            
        except Exception as e:
            logger.error(f"Error getting knowledge: {e}")
            return []
    
    def store_conversation(self, user_input: str, aria_response: str, 
                          session_id: str) -> bool:
        """Almacenar conversación en Supabase"""
        if not self.status.supabase:
            return False
        
        try:
            data = {
                'session_id': session_id,
                'user_input': user_input,
                'aria_response': aria_response,
                'timestamp': datetime.now(timezone.utc).isoformat(),
                'response_time': 0.5,  # Placeholder
                'user_satisfaction': None
            }
            
            result = self.supabase_client.table('aria_conversations').insert(data).execute()
            
            if result.data:
                print(f"💬 Conversación almacenada")
                return True
                
        except Exception as e:
            logger.error(f"Error storing conversation: {e}")
        
        return False
    
    # ==========================================
    # MÉTODOS DE GOOGLE CLOUD
    # ==========================================
    
    def generate_with_gemini(self, prompt: str, model_name: str = 'gemini-pro') -> str:
        """Generar respuesta con Google Gemini"""
        if not self.status.google_cloud:
            return "Google Cloud no disponible"
        
        try:
            # Verificar cache
            cache_key = hashlib.md5(f"{model_name}:{prompt}".encode()).hexdigest()
            if cache_key in self.cache:
                cache_entry = self.cache[cache_key]
                if time.time() - cache_entry['timestamp'] < self.connection_cache_ttl:
                    return cache_entry['response']
            
            # Generar respuesta
            model = genai.GenerativeModel(model_name)
            response = model.generate_content(prompt)
            
            result = response.text if response.text else "Sin respuesta generada"
            
            # Guardar en cache
            self.cache[cache_key] = {
                'response': result,
                'timestamp': time.time()
            }
            
            return result
            
        except Exception as e:
            logger.error(f"Error with Gemini: {e}")
            return f"Error generando respuesta: {e}"
    
    def analyze_with_google_ai(self, text: str, analysis_type: str = "sentiment") -> Dict:
        """Analizar texto con Google AI"""
        if not self.status.google_cloud:
            return {"error": "Google Cloud no disponible"}
        
        try:
            if analysis_type == "sentiment":
                prompt = f"Analiza el sentimiento del siguiente texto y responde en JSON con 'sentiment' (positive/negative/neutral) y 'confidence' (0-1): {text}"
            elif analysis_type == "summary":
                prompt = f"Resume el siguiente texto en 2-3 oraciones: {text}"
            else:
                prompt = f"Analiza el siguiente texto según el tipo '{analysis_type}': {text}"
            
            result = self.generate_with_gemini(prompt)
            
            return {
                "analysis_type": analysis_type,
                "result": result,
                "success": True
            }
            
        except Exception as e:
            logger.error(f"Error with Google AI analysis: {e}")
            return {"error": str(e), "success": False}
    
    # ==========================================
    # MÉTODOS DE GESTIÓN
    # ==========================================
    
    def check_connections(self) -> Dict[str, bool]:
        """Verificar estado de todas las conexiones"""
        current_time = datetime.now(timezone.utc)
        
        # Verificar si necesita reconexión
        if (self.status.last_check and 
            (current_time - self.status.last_check).seconds > self.connection_cache_ttl):
            self._initialize_connections()
        
        return {
            "supabase": self.status.supabase,
            "google_cloud": self.status.google_cloud,
            "timestamp": current_time.isoformat()
        }
    
    def reconnect_all(self):
        """Reconectar todos los servicios"""
        print("🔄 Reconectando servicios...")
        self.status.error_count = 0
        self._initialize_connections()
    
    def get_status_report(self) -> Dict:
        """Obtener reporte completo de estado"""
        return {
            "connections": {
                "supabase": {
                    "connected": self.status.supabase,
                    "url": self.supabase_url,
                    "available": SUPABASE_AVAILABLE
                },
                "google_cloud": {
                    "connected": self.status.google_cloud,
                    "api_configured": bool(self.google_api_key),
                    "available": GOOGLE_CLOUD_AVAILABLE
                }
            },
            "cache": {
                "entries": len(self.cache),
                "ttl": self.connection_cache_ttl
            },
            "statistics": {
                "last_check": self.status.last_check.isoformat() if self.status.last_check else None,
                "error_count": self.status.error_count,
                "uptime": str(datetime.now(timezone.utc) - (self.status.last_check or datetime.now(timezone.utc)))
            }
        }

# ==========================================
# INSTANCIA GLOBAL
# ==========================================

# Crear instancia global del conector
aria_cloud = ARIACloudConnector()

def get_cloud_connector() -> ARIACloudConnector:
    """Obtener la instancia del conector en la nube"""
    return aria_cloud

# ==========================================
# FUNCIONES DE CONVENIENCIA
# ==========================================

def store_aria_knowledge(concept: str, description: str, category: str = "general") -> bool:
    """Función de conveniencia para almacenar conocimiento"""
    return aria_cloud.store_knowledge(concept, description, category)

def get_aria_knowledge(concept: str = None) -> List[Dict]:
    """Función de conveniencia para obtener conocimiento"""
    return aria_cloud.get_knowledge(concept)

def generate_ai_response(prompt: str) -> str:
    """Función de conveniencia para generar respuestas con IA"""
    return aria_cloud.generate_with_gemini(prompt)

def analyze_text(text: str, analysis_type: str = "sentiment") -> Dict:
    """Función de conveniencia para análisis de texto"""
    return aria_cloud.analyze_with_google_ai(text, analysis_type)

if __name__ == "__main__":
    print("🌐 ARIA Cloud Connector - Prueba de Conexiones")
    print("=" * 50)
    
    # Mostrar estado
    aria_cloud._log_status()
    
    # Probar funcionalidades
    if aria_cloud.status.supabase:
        print("\n📊 Probando Supabase...")
        test_stored = store_aria_knowledge(
            "test_connection", 
            "Prueba de conexión a Supabase desde ARIA",
            "testing"
        )
        print(f"Almacenamiento: {'✅ OK' if test_stored else '❌ Error'}")
    
    if aria_cloud.status.google_cloud:
        print("\n🤖 Probando Google Cloud...")
        test_response = generate_ai_response("Hola, soy ARIA. Responde brevemente que la conexión funciona.")
        print(f"Respuesta AI: {test_response[:100]}...")
    
    # Reporte final
    print("\n📋 Reporte Final:")
    report = aria_cloud.get_status_report()
    print(json.dumps(report, indent=2, default=str))