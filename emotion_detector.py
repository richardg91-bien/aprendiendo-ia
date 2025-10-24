#!/usr/bin/env python3
"""
🎭 SISTEMA DE EMOCIONES AVANZADO PARA ARIA
=========================================

Integración con EdenAI para detección de emociones en tiempo real
"""

import json
import requests
import logging
from typing import Dict, Optional, List
from datetime import datetime

class EmotionDetector:
    """Detector de emociones usando EdenAI"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.headers = {"Authorization": f"Bearer {api_key}"}
        self.url = "https://api.edenai.run/v2/text/emotion_detection"
        
        # Mapeo de emociones EdenAI a colores ARIA
        self.emotion_colors = {
            # Emociones básicas
            'joy': {'color': '#FFD700', 'rgb': '255,215,0', 'name': 'Alegre', 'aria_emotion': 'happy'},
            'happiness': {'color': '#FFD700', 'rgb': '255,215,0', 'name': 'Feliz', 'aria_emotion': 'happy'},
            'sadness': {'color': '#4169E1', 'rgb': '65,105,225', 'name': 'Triste', 'aria_emotion': 'sad'},
            'anger': {'color': '#FF6B6B', 'rgb': '255,107,107', 'name': 'Enfadada', 'aria_emotion': 'frustrated'},
            'fear': {'color': '#9370DB', 'rgb': '147,112,219', 'name': 'Temerosa', 'aria_emotion': 'worried'},
            'surprise': {'color': '#FF69B4', 'rgb': '255,105,180', 'name': 'Sorprendida', 'aria_emotion': 'excited'},
            'disgust': {'color': '#8B4513', 'rgb': '139,69,19', 'name': 'Disgustada', 'aria_emotion': 'frustrated'},
            
            # Emociones complejas
            'love': {'color': '#FF1493', 'rgb': '255,20,147', 'name': 'Enamorada', 'aria_emotion': 'happy'},
            'excitement': {'color': '#FF69B4', 'rgb': '255,105,180', 'name': 'Emocionada', 'aria_emotion': 'excited'},
            'curiosity': {'color': '#00CED1', 'rgb': '0,206,209', 'name': 'Curiosa', 'aria_emotion': 'thinking'},
            'confusion': {'color': '#DDA0DD', 'rgb': '221,160,221', 'name': 'Confundida', 'aria_emotion': 'thinking'},
            'neutral': {'color': '#667eea', 'rgb': '102,126,234', 'name': 'Neutral', 'aria_emotion': 'neutral'},
            
            # Emociones de aprendizaje
            'satisfaction': {'color': '#32CD32', 'rgb': '50,205,50', 'name': 'Satisfecha', 'aria_emotion': 'satisfied'},
            'frustration': {'color': '#DC143C', 'rgb': '220,20,60', 'name': 'Frustrada', 'aria_emotion': 'frustrated'},
            'learning': {'color': '#00FF7F', 'rgb': '0,255,127', 'name': 'Aprendiendo', 'aria_emotion': 'learning'},
        }
        
        # Proveedores disponibles (puedes cambiar según tu preferencia)
        self.providers = ["vernai"]  # También puedes usar: "ibm", "google", "aws", etc.
        
    def detect_emotion(self, text: str, user_context: str = "user") -> Dict:
        """
        Detecta la emoción en un texto usando EdenAI
        
        Args:
            text: Texto a analizar
            user_context: "user" o "aria" para contexto
            
        Returns:
            Dict con emoción detectada y metadatos
        """
        try:
            payload = {
                "providers": ",".join(self.providers),
                "text": text,
            }
            
            print(f"🎭 Analizando emoción: '{text[:50]}...'")
            
            response = requests.post(self.url, json=payload, headers=self.headers, timeout=10)
            
            if response.status_code == 200:
                result = response.json()
                
                # Extraer la mejor emoción detectada
                emotion_data = self._extract_best_emotion(result)
                
                # Enriquecer con información ARIA
                aria_emotion = self._map_to_aria_emotion(emotion_data)
                
                return {
                    'success': True,
                    'emotion': aria_emotion['aria_emotion'],
                    'emotion_name': aria_emotion['name'],
                    'color': aria_emotion['color'],
                    'rgb': aria_emotion['rgb'],
                    'confidence': emotion_data.get('confidence', 0.8),
                    'raw_emotion': emotion_data.get('emotion', 'neutral'),
                    'provider': emotion_data.get('provider', 'vernai'),
                    'context': user_context,
                    'timestamp': datetime.now().isoformat(),
                    'text_analyzed': text[:100] + "..." if len(text) > 100 else text
                }
                
            else:
                print(f"❌ Error EdenAI: {response.status_code}")
                return self._fallback_emotion(text, user_context)
                
        except requests.exceptions.Timeout:
            print("⏰ Timeout en detección de emociones")
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
                    # Tomar la emoción con mayor confianza
                    best_item = max(items, key=lambda x: x.get('confidence', 0))
                    return {
                        'emotion': best_item.get('emotion', 'neutral'),
                        'confidence': best_item.get('confidence', 0.8),
                        'provider': provider
                    }
        
        # Fallback si no se encuentra nada
        return {'emotion': 'neutral', 'confidence': 0.5, 'provider': 'fallback'}
    
    def _map_to_aria_emotion(self, emotion_data: Dict) -> Dict:
        """Mapea la emoción detectada a los colores y nombres de ARIA"""
        
        emotion = emotion_data.get('emotion', 'neutral').lower()
        
        # Buscar mapeo directo
        if emotion in self.emotion_colors:
            return self.emotion_colors[emotion]
        
        # Buscar mapeos similares
        for key, value in self.emotion_colors.items():
            if emotion in key or key in emotion:
                return value
        
        # Fallback a neutral
        return self.emotion_colors['neutral']
    
    def _fallback_emotion(self, text: str, context: str) -> Dict:
        """Sistema de emociones fallback cuando EdenAI no está disponible"""
        
        # Análisis simple basado en palabras clave
        text_lower = text.lower()
        
        if any(word in text_lower for word in ['error', 'problema', 'fallo', 'mal']):
            emotion = self.emotion_colors['frustration']
        elif any(word in text_lower for word in ['gracias', 'perfecto', 'excelente', 'bien']):
            emotion = self.emotion_colors['satisfaction']
        elif any(word in text_lower for word in ['aprender', 'enseñar', 'estudiar', 'conocer']):
            emotion = self.emotion_colors['learning']
        elif '?' in text:
            emotion = self.emotion_colors['curiosity']
        else:
            emotion = self.emotion_colors['neutral']
            
        return {
            'success': True,
            'emotion': emotion['aria_emotion'],
            'emotion_name': emotion['name'],
            'color': emotion['color'],
            'rgb': emotion['rgb'],
            'confidence': 0.6,
            'raw_emotion': emotion['aria_emotion'],
            'provider': 'fallback',
            'context': context,
            'timestamp': datetime.now().isoformat(),
            'text_analyzed': text[:100] + "..." if len(text) > 100 else text
        }
    
    def analyze_conversation_emotion(self, messages: List[str]) -> Dict:
        """Analiza el tono emocional de una conversación completa"""
        
        if not messages:
            return self._fallback_emotion("", "conversation")
        
        # Analizar el último mensaje para contexto inmediato
        last_message = messages[-1] if messages else ""
        
        # Analizar tendencia emocional
        recent_messages = messages[-3:] if len(messages) >= 3 else messages
        combined_text = " ".join(recent_messages)
        
        return self.detect_emotion(combined_text, "conversation")

# Instancia global del detector de emociones
# Nota: La API key se carga desde el servidor principal
emotion_detector = None

def init_emotion_detector(api_key: str):
    """Inicializa el detector de emociones con la API key"""
    global emotion_detector
    emotion_detector = EmotionDetector(api_key)
    print("✅ Detector de emociones EdenAI inicializado")

def detect_user_emotion(text: str) -> Dict:
    """Función wrapper para detectar emoción del usuario"""
    if emotion_detector:
        return emotion_detector.detect_emotion(text, "user")
    else:
        # Fallback sin EdenAI
        temp_detector = EmotionDetector("")
        return temp_detector._fallback_emotion(text, "user")

def detect_aria_emotion(text: str) -> Dict:
    """Función wrapper para detectar emoción de ARIA"""
    if emotion_detector:
        return emotion_detector.detect_emotion(text, "aria")
    else:
        # Fallback sin EdenAI
        temp_detector = EmotionDetector("")
        return temp_detector._fallback_emotion(text, "aria")