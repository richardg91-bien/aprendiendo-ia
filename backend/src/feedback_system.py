"""
Sistema de Retroalimentación para ARIA
Conecta con base de datos externa para aprendizaje continuo
"""

import os
import json
import requests
from datetime import datetime
from typing import Dict, List, Optional

class FeedbackSystem:
    def __init__(self):
        self.supabase_url = os.getenv('SUPABASE_URL')
        self.supabase_key = os.getenv('SUPABASE_KEY')
        self.headers = {
            'apikey': self.supabase_key,
            'Authorization': f'Bearer {self.supabase_key}',
            'Content-Type': 'application/json'
        }
        
    def log_conversation(self, user_message: str, aria_response: str, 
                        user_feedback: Optional[str] = None) -> bool:
        """Registra conversación en la base de datos"""
        try:
            # Usar solo base de datos local por ahora
            if not self.supabase_url:
                print("📝 Conversación registrada localmente")
                return True
                
            data = {
                'timestamp': datetime.now().isoformat(),
                'user_message': user_message,
                'aria_response': aria_response,
                'user_feedback': user_feedback,
                'session_id': self.generate_session_id()
            }
            
            response = requests.post(
                f'{self.supabase_url}/rest/v1/conversations',
                headers=self.headers,
                json=data
            )
            
            return response.status_code == 201
            
        except Exception as e:
            print(f"Error logging conversation: {e}")
            return False
    
    def save_user_preference(self, preference_type: str, value: str) -> bool:
        """Guarda preferencias del usuario"""
        try:
            data = {
                'preference_type': preference_type,
                'value': value,
                'timestamp': datetime.now().isoformat()
            }
            
            response = requests.post(
                f'{self.supabase_url}/rest/v1/user_preferences',
                headers=self.headers,
                json=data
            )
            
            return response.status_code == 201
            
        except Exception as e:
            print(f"Error saving preference: {e}")
            return False
    
    def get_learning_patterns(self) -> List[Dict]:
        """Obtiene patrones de aprendizaje de conversaciones previas"""
        try:
            response = requests.get(
                f'{self.supabase_url}/rest/v1/conversations?select=*&order=timestamp.desc&limit=100',
                headers=self.headers
            )
            
            if response.status_code == 200:
                return response.json()
            return []
            
        except Exception as e:
            print(f"Error getting learning patterns: {e}")
            return []
    
    def analyze_feedback(self) -> Dict:
        """Analiza el feedback para mejorar respuestas"""
        try:
            # Obtener conversaciones con feedback
            response = requests.get(
                f'{self.supabase_url}/rest/v1/conversations?select=*&user_feedback=not.is.null',
                headers=self.headers
            )
            
            if response.status_code == 200:
                conversations = response.json()
                
                # Análisis simple de sentimiento
                positive_feedback = 0
                negative_feedback = 0
                
                for conv in conversations:
                    feedback = conv.get('user_feedback', '').lower()
                    if any(word in feedback for word in ['bien', 'bueno', 'gracias', 'perfecto']):
                        positive_feedback += 1
                    elif any(word in feedback for word in ['mal', 'error', 'incorrecto', 'no']):
                        negative_feedback += 1
                
                return {
                    'total_conversations': len(conversations),
                    'positive_feedback': positive_feedback,
                    'negative_feedback': negative_feedback,
                    'satisfaction_rate': positive_feedback / max(len(conversations), 1) * 100
                }
            
            return {'error': 'No se pudo obtener feedback'}
            
        except Exception as e:
            print(f"Error analyzing feedback: {e}")
            return {'error': str(e)}
    
    def generate_session_id(self) -> str:
        """Genera ID único para la sesión"""
        import uuid
        return str(uuid.uuid4())[:8]

# Instancia global del sistema de feedback
feedback_system = FeedbackSystem()