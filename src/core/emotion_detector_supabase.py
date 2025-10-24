#!/usr/bin/env python3
"""
🎭 SISTEMA DE EMOCIONES BASADO EN SUPABASE
=========================================

Detector de emociones que usa Supabase como fuente principal de datos
"""

import json
import requests
import logging
from typing import Dict, Optional, List
from datetime import datetime

try:
    from supabase import create_client, Client
    import os
    from dotenv import load_dotenv
    
    # Cargar variables de entorno
    load_dotenv("backend/.env")
    
    # Configuración de Supabase
    SUPABASE_URL = os.getenv('SUPABASE_URL')
    SUPABASE_KEY = os.getenv('SUPABASE_ANON_KEY')
    
    if SUPABASE_URL and SUPABASE_KEY:
        supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
        SUPABASE_AVAILABLE = True
    else:
        SUPABASE_AVAILABLE = False
        
except ImportError:
    SUPABASE_AVAILABLE = False

class EmotionDetectorSupabase:
    """Detector de emociones mejorado con Supabase"""
    
    def __init__(self, api_key: str = ""):
        self.api_key = api_key
        self.headers = {"Authorization": f"Bearer {api_key}"} if api_key else {}
        self.url = "https://api.edenai.run/v2/text/emotion_detection"
        
        # Cache local de emociones (se carga desde Supabase)
        self.emotion_cache = {}
        self.config_cache = {}
        
        # Cargar emociones desde Supabase
        self._load_emotions_from_supabase()
        self._load_config_from_supabase()
        
        # Proveedores EdenAI
        self.providers = self.config_cache.get('edenai_providers', ["vernai"])
        
    def _load_emotions_from_supabase(self):
        """Cargar mapeos de emociones desde Supabase"""
        
        if not SUPABASE_AVAILABLE:
            print("⚠️ Supabase no disponible, usando emociones fallback")
            self._load_fallback_emotions()
            return
            
        try:
            # Obtener todas las emociones de Supabase
            result = supabase.table("aria_knowledge").select("*").eq("category", "emotion_mapping").execute()
            
            if result.data:
                print(f"📊 Cargando {len(result.data)} emociones desde Supabase")
                
                for emotion_record in result.data:
                    try:
                        # Parsear datos de la emoción
                        emotion_data = json.loads(emotion_record['description'])
                        emotion_key = emotion_data['emotion_key']
                        
                        # Estructurar como el formato original
                        self.emotion_cache[emotion_key] = {
                            'color': emotion_data['color_hex'],
                            'rgb': emotion_data['color_rgb'],
                            'name': emotion_data['emotion_name'],
                            'aria_emotion': emotion_data['aria_emotion']
                        }
                        
                    except (json.JSONDecodeError, KeyError) as e:
                        print(f"⚠️ Error procesando emoción {emotion_record.get('concept', 'unknown')}: {e}")
                        
                print(f"✅ {len(self.emotion_cache)} emociones cargadas desde Supabase")
                
            else:
                print("⚠️ No se encontraron emociones en Supabase")
                self._load_fallback_emotions()
                
        except Exception as e:
            print(f"❌ Error cargando emociones desde Supabase: {e}")
            self._load_fallback_emotions()
    
    def _load_config_from_supabase(self):
        """Cargar configuración emocional desde Supabase"""
        
        if not SUPABASE_AVAILABLE:
            self._load_fallback_config()
            return
            
        try:
            result = supabase.table("aria_knowledge").select("*").eq("concept", "emotion_system_config").execute()
            
            if result.data and len(result.data) > 0:
                config_data = json.loads(result.data[0]['description'])
                self.config_cache = config_data
                print("✅ Configuración emocional cargada desde Supabase")
            else:
                print("⚠️ Configuración emocional no encontrada en Supabase")
                self._load_fallback_config()
                
        except Exception as e:
            print(f"❌ Error cargando configuración desde Supabase: {e}")
            self._load_fallback_config()
    
    def _load_fallback_emotions(self):
        """Cargar emociones básicas como fallback"""
        
        self.emotion_cache = {
            'joy': {'color': '#FFD700', 'rgb': '255,215,0', 'name': 'Alegre', 'aria_emotion': 'happy'},
            'happiness': {'color': '#FFD700', 'rgb': '255,215,0', 'name': 'Feliz', 'aria_emotion': 'happy'},
            'sadness': {'color': '#4169E1', 'rgb': '65,105,225', 'name': 'Triste', 'aria_emotion': 'sad'},
            'anger': {'color': '#FF6B6B', 'rgb': '255,107,107', 'name': 'Enfadada', 'aria_emotion': 'frustrated'},
            'neutral': {'color': '#667eea', 'rgb': '102,126,234', 'name': 'Neutral', 'aria_emotion': 'neutral'},
            'curiosity': {'color': '#00CED1', 'rgb': '0,206,209', 'name': 'Curiosa', 'aria_emotion': 'thinking'},
            'learning': {'color': '#00FF7F', 'rgb': '0,255,127', 'name': 'Aprendiendo', 'aria_emotion': 'learning'},
        }
        print(f"📦 Emociones fallback cargadas: {len(self.emotion_cache)} emociones")
    
    def _load_fallback_config(self):
        """Cargar configuración básica como fallback"""
        
        self.config_cache = {
            'edenai_providers': ['vernai'],
            'fallback_enabled': True,
            'confidence_threshold': 0.5,
            'default_emotion': 'neutral',
            'emotion_persistence': True,
            'color_system_enabled': True
        }
        print("📦 Configuración emocional fallback cargada")
    
    def detect_emotion(self, text: str, user_context: str = "user") -> Dict:
        """Detectar emoción usando EdenAI con datos desde Supabase"""
        
        if not self.api_key:
            return self._fallback_emotion(text, user_context)
        
        try:
            payload = {
                "providers": self.providers,
                "text": text,
                "response_as_dict": True,
                "attributes_as_list": False,
                "show_original_response": False
            }
            
            response = requests.post(self.url, json=payload, headers=self.headers, timeout=10)
            
            if response.status_code == 200:
                result = response.json()
                emotion_data = self._extract_best_emotion(result)
                
                # Mapear usando datos de Supabase
                aria_emotion = self._map_to_aria_emotion_supabase(emotion_data)
                
                # Registrar en historial si está disponible
                self._save_emotion_history(text, emotion_data, aria_emotion, user_context)
                
                return {
                    'success': True,
                    'emotion': aria_emotion['aria_emotion'],
                    'emotion_name': aria_emotion['name'],
                    'color': aria_emotion['color'],
                    'rgb': aria_emotion['rgb'],
                    'confidence': emotion_data.get('confidence', 0.8),
                    'raw_emotion': emotion_data.get('emotion', 'neutral'),
                    'provider': emotion_data.get('provider', 'unknown'),
                    'context': user_context,
                    'timestamp': datetime.now().isoformat(),
                    'text_analyzed': text[:100] + "..." if len(text) > 100 else text,
                    'source': 'supabase'
                }
            else:
                return self._fallback_emotion(text, user_context)
                
        except Exception as e:
            print(f"❌ Error en detección de emociones: {e}")
            return self._fallback_emotion(text, user_context)
    
    def _extract_best_emotion(self, result: Dict) -> Dict:
        """Extrae la mejor emoción del resultado de EdenAI"""
        
        for provider in self.providers:
            if provider in result and 'items' in result[provider]:
                items = result[provider]['items']
                if items and len(items) > 0:
                    best_item = max(items, key=lambda x: x.get('confidence', 0))
                    return {
                        'emotion': best_item.get('emotion', 'neutral'),
                        'confidence': best_item.get('confidence', 0.8),
                        'provider': provider
                    }
        
        return {'emotion': 'neutral', 'confidence': 0.5, 'provider': 'fallback'}
    
    def _map_to_aria_emotion_supabase(self, emotion_data: Dict) -> Dict:
        """Mapea la emoción detectada usando datos de Supabase"""
        
        emotion = emotion_data.get('emotion', 'neutral').lower()
        
        # Buscar mapeo directo en cache de Supabase
        if emotion in self.emotion_cache:
            return self.emotion_cache[emotion]
        
        # Buscar mapeos similares
        for key, value in self.emotion_cache.items():
            if emotion in key or key in emotion:
                return value
        
        # Fallback a neutral
        return self.emotion_cache.get('neutral', {
            'color': '#667eea',
            'rgb': '102,126,234',
            'name': 'Neutral',
            'aria_emotion': 'neutral'
        })
    
    def _save_emotion_history(self, text: str, emotion_data: Dict, aria_emotion: Dict, context: str):
        """Guardar historial de emociones en Supabase"""
        
        if not SUPABASE_AVAILABLE:
            return
            
        try:
            # Preparar datos para historial
            history_data = {
                'emotion_detected': emotion_data.get('emotion', 'neutral'),
                'emotion_confidence': emotion_data.get('confidence', 0.5),
                'emotion_provider': emotion_data.get('provider', 'fallback'),
                'user_text': text[:500],  # Limitar longitud
                'aria_response_emotion': aria_emotion['aria_emotion'],
                'color_used': aria_emotion['color'],
                'context_type': context,
                'raw_data': json.dumps({
                    'full_emotion_data': emotion_data,
                    'aria_emotion_data': aria_emotion,
                    'supabase_source': True
                })
            }
            
            # Guardar en tabla de historial (si existe)
            # Nota: Por ahora lo guardamos en la tabla de conocimiento
            supabase.table("aria_knowledge").insert({
                'concept': f"emotion_history_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                'description': json.dumps(history_data),
                'category': 'emotion_history',
                'confidence': emotion_data.get('confidence', 0.5)
            }).execute()
            
        except Exception as e:
            print(f"⚠️ Error guardando historial emocional: {e}")
    
    def _fallback_emotion(self, text: str, context: str) -> Dict:
        """Sistema de emociones fallback usando datos de Supabase"""
        
        text_lower = text.lower()
        
        # Análisis simple basado en palabras clave
        if any(word in text_lower for word in ['error', 'problema', 'fallo', 'mal']):
            emotion_key = 'anger'
        elif any(word in text_lower for word in ['gracias', 'perfecto', 'excelente', 'bien']):
            emotion_key = 'joy'
        elif any(word in text_lower for word in ['aprender', 'enseñar', 'estudiar', 'conocer']):
            emotion_key = 'learning'
        elif '?' in text:
            emotion_key = 'curiosity'
        else:
            emotion_key = 'neutral'
        
        # Obtener emoción del cache de Supabase
        emotion = self.emotion_cache.get(emotion_key, self.emotion_cache.get('neutral'))
        
        return {
            'success': True,
            'emotion': emotion['aria_emotion'],
            'emotion_name': emotion['name'],
            'color': emotion['color'],
            'rgb': emotion['rgb'],
            'confidence': 0.6,
            'raw_emotion': emotion['aria_emotion'],
            'provider': 'supabase_fallback',
            'context': context,
            'timestamp': datetime.now().isoformat(),
            'text_analyzed': text[:100] + "..." if len(text) > 100 else text,
            'source': 'supabase'
        }
    
    def get_available_emotions(self) -> List[Dict]:
        """Obtener lista de emociones disponibles desde Supabase"""
        
        emotions_list = []
        for key, emotion in self.emotion_cache.items():
            emotions_list.append({
                'key': key,
                'name': emotion['name'],
                'aria_emotion': emotion['aria_emotion'],
                'color': emotion['color'],
                'rgb': emotion['rgb']
            })
        
        return emotions_list
    
    def update_emotion_in_supabase(self, emotion_key: str, emotion_data: Dict) -> bool:
        """Actualizar una emoción específica en Supabase"""
        
        if not SUPABASE_AVAILABLE:
            return False
            
        try:
            concept = f"emotion_{emotion_key}"
            description = json.dumps({
                'emotion_key': emotion_key,
                'emotion_name': emotion_data['name'],
                'aria_emotion': emotion_data['aria_emotion'],
                'color_hex': emotion_data['color'],
                'color_rgb': emotion_data['rgb'],
                'category': 'emotion_mapping',
                'type': 'emotion_system'
            })
            
            # Actualizar en Supabase
            result = supabase.table("aria_knowledge").update({
                'description': description,
                'updated_at': datetime.now().isoformat()
            }).eq('concept', concept).execute()
            
            # Actualizar cache local
            if result.data:
                self.emotion_cache[emotion_key] = emotion_data
                print(f"✅ Emoción {emotion_key} actualizada en Supabase")
                return True
            
        except Exception as e:
            print(f"❌ Error actualizando emoción {emotion_key}: {e}")
            
        return False

# Instancia global del detector de emociones con Supabase
emotion_detector_supabase = None

def init_emotion_detector_supabase(api_key: str = ""):
    """Inicializa el detector de emociones con Supabase"""
    global emotion_detector_supabase
    emotion_detector_supabase = EmotionDetectorSupabase(api_key)
    print("✅ Detector de emociones Supabase inicializado")
    return emotion_detector_supabase

def detect_user_emotion_supabase(text: str) -> Dict:
    """Función wrapper para detectar emoción del usuario usando Supabase"""
    if emotion_detector_supabase:
        return emotion_detector_supabase.detect_emotion(text, "user")
    else:
        # Crear instancia temporal
        temp_detector = EmotionDetectorSupabase("")
        return temp_detector.detect_emotion(text, "user")

def detect_aria_emotion_supabase(text: str) -> Dict:
    """Función wrapper para detectar emoción de ARIA usando Supabase"""
    if emotion_detector_supabase:
        return emotion_detector_supabase.detect_emotion(text, "aria")
    else:
        # Crear instancia temporal
        temp_detector = EmotionDetectorSupabase("")
        return temp_detector.detect_emotion(text, "aria")

def get_emotion_stats_supabase() -> Dict:
    """Obtener estadísticas del sistema emocional desde Supabase"""
    
    if not SUPABASE_AVAILABLE:
        return {"error": "Supabase no disponible"}
    
    try:
        # Contar emociones
        emotions = supabase.table("aria_knowledge").select("id").eq("category", "emotion_mapping").execute()
        
        # Contar historial emocional
        history = supabase.table("aria_knowledge").select("id").eq("category", "emotion_history").execute()
        
        # Contar configuraciones
        config = supabase.table("aria_knowledge").select("id").eq("category", "system_config").execute()
        
        return {
            "emotions_available": len(emotions.data) if emotions.data else 0,
            "emotion_history_entries": len(history.data) if history.data else 0,
            "config_entries": len(config.data) if config.data else 0,
            "supabase_status": "connected",
            "cache_loaded": len(emotion_detector_supabase.emotion_cache) if emotion_detector_supabase else 0
        }
        
    except Exception as e:
        return {"error": f"Error obteniendo estadísticas: {e}"}