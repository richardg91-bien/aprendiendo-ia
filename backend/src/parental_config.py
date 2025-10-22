"""
Configuración de Protección Parental para ARIA
Sistema de protección como el amor de un padre
"""

import json
import os
from datetime import datetime

class ParentalConfig:
    def __init__(self):
        self.config_file = "parental_settings.json"
        self.safety_log_file = "safety_events.log"
        self.load_config()
    
    def load_config(self):
        """Carga la configuración parental"""
        default_config = {
            "child_mode_enabled": True,
            "content_filtering_level": "strict",  # strict, moderate, permissive
            "log_all_conversations": True,
            "block_personal_info_requests": True,
            "educational_content_priority": True,
            "safe_topics_only": True,
            "parental_notification_enabled": True,
            "max_conversation_time": 30,  # minutos
            "allowed_time_ranges": [
                {"start": "09:00", "end": "18:00"}  # 9 AM a 6 PM
            ],
            "blocked_keywords": [
                "violencia", "drogas", "alcohol", "armas", "sangre",
                "muerte", "suicidio", "autolesión", "bullying"
            ],
            "emergency_contacts": [
                {"name": "Papá", "action": "notify_parent"},
                {"name": "Mamá", "action": "notify_parent"}
            ]
        }
        
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    self.config = json.load(f)
                    # Agregar nuevas configuraciones por defecto si no existen
                    for key, value in default_config.items():
                        if key not in self.config:
                            self.config[key] = value
            else:
                self.config = default_config
                self.save_config()
        except Exception as e:
            print(f"Error cargando configuración parental: {e}")
            self.config = default_config
    
    def save_config(self):
        """Guarda la configuración parental"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error guardando configuración parental: {e}")
    
    def is_child_mode_enabled(self):
        """Verifica si el modo infantil está activado"""
        return self.config.get("child_mode_enabled", True)
    
    def get_filtering_level(self):
        """Obtiene el nivel de filtrado de contenido"""
        return self.config.get("content_filtering_level", "strict")
    
    def should_block_keyword(self, keyword):
        """Verifica si una palabra clave debe ser bloqueada"""
        blocked_keywords = self.config.get("blocked_keywords", [])
        return any(blocked in keyword.lower() for blocked in blocked_keywords)
    
    def log_safety_event(self, event_type, message, user_info=None):
        """Registra eventos de seguridad"""
        if not self.config.get("log_all_conversations", True):
            return
        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = {
            "timestamp": timestamp,
            "event_type": event_type,
            "message": message[:100],  # Primeros 100 caracteres
            "user_info": user_info or "unknown",
            "action_taken": "content_filtered" if event_type == "unsafe_content" else "logged"
        }
        
        try:
            with open(self.safety_log_file, 'a', encoding='utf-8') as f:
                f.write(json.dumps(log_entry, ensure_ascii=False) + "\n")
        except Exception as e:
            print(f"Error registrando evento de seguridad: {e}")
    
    def is_time_allowed(self):
        """Verifica si es hora permitida para usar ARIA"""
        current_time = datetime.now().strftime("%H:%M")
        allowed_ranges = self.config.get("allowed_time_ranges", [])
        
        if not allowed_ranges:
            return True  # Si no hay restricciones, siempre permitido
        
        for time_range in allowed_ranges:
            if time_range["start"] <= current_time <= time_range["end"]:
                return True
        
        return False
    
    def get_time_restriction_message(self):
        """Mensaje cuando no es hora permitida"""
        return ("Lo siento, no puedo chatear en este momento. "
                "Pregunta a tus papás cuándo puedes usar ARIA otra vez. "
                "¡Nos vemos pronto! 😊")
    
    def enable_strict_mode(self):
        """Activa el modo más estricto de protección"""
        self.config.update({
            "child_mode_enabled": True,
            "content_filtering_level": "strict",
            "block_personal_info_requests": True,
            "safe_topics_only": True,
            "log_all_conversations": True,
            "parental_notification_enabled": True
        })
        self.save_config()
        print("🛡️ Modo de protección ESTRICTA activado")
    
    def add_blocked_keyword(self, keyword):
        """Agrega una palabra clave a la lista de bloqueadas"""
        if keyword.lower() not in self.config["blocked_keywords"]:
            self.config["blocked_keywords"].append(keyword.lower())
            self.save_config()
            print(f"🚫 Palabra '{keyword}' agregada a la lista de bloqueadas")
    
    def remove_blocked_keyword(self, keyword):
        """Remueve una palabra clave de la lista de bloqueadas"""
        if keyword.lower() in self.config["blocked_keywords"]:
            self.config["blocked_keywords"].remove(keyword.lower())
            self.save_config()
            print(f"✅ Palabra '{keyword}' removida de la lista de bloqueadas")
    
    def get_safety_report(self):
        """Genera un reporte de seguridad para los padres"""
        try:
            with open(self.safety_log_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                recent_events = lines[-10:]  # Últimos 10 eventos
                
                report = "📊 REPORTE DE SEGURIDAD ARIA\n"
                report += "=" * 40 + "\n"
                report += f"Total de eventos registrados: {len(lines)}\n\n"
                
                if recent_events:
                    report += "🕒 Eventos recientes:\n"
                    for event_line in recent_events:
                        try:
                            event = json.loads(event_line.strip())
                            report += f"• {event['timestamp']}: {event['event_type']}\n"
                            report += f"  Mensaje: {event['message']}\n\n"
                        except:
                            continue
                else:
                    report += "✅ No hay eventos de seguridad recientes\n"
                
                return report
        except FileNotFoundError:
            return "✅ No hay eventos de seguridad registrados"
        except Exception as e:
            return f"❌ Error generando reporte: {e}"
    
    def export_settings_for_parents(self):
        """Exporta configuración en formato legible para padres"""
        readable_config = {
            "Modo infantil activado": "Sí" if self.config["child_mode_enabled"] else "No",
            "Nivel de filtrado": self.config["content_filtering_level"].upper(),
            "Bloquer información personal": "Sí" if self.config["block_personal_info_requests"] else "No",
            "Solo temas seguros": "Sí" if self.config["safe_topics_only"] else "No",
            "Registrar conversaciones": "Sí" if self.config["log_all_conversations"] else "No",
            "Horarios permitidos": self.config["allowed_time_ranges"],
            "Palabras bloqueadas": len(self.config["blocked_keywords"])
        }
        
        return readable_config

# Instancia global de configuración parental
parental_config = ParentalConfig()

def activate_maximum_protection():
    """Activa la máxima protección posible"""
    print("🛡️ ACTIVANDO PROTECCIÓN MÁXIMA PARA NIÑOS")
    print("👨‍👧‍👦 Como padre protector, implementando todas las medidas de seguridad")
    
    parental_config.enable_strict_mode()
    
    # Agregar palabras adicionales de protección
    additional_blocked_words = [
        "contraseña", "password", "dirección", "teléfono", "tarjeta",
        "dinero", "comprar", "pagar", "cita", "encuentro", "foto"
    ]
    
    for word in additional_blocked_words:
        parental_config.add_blocked_keyword(word)
    
    print("✅ PROTECCIÓN MÁXIMA ACTIVADA")
    print("📋 Configuración exportada para revisión parental")
    
    return parental_config.export_settings_for_parents()

if __name__ == "__main__":
    print("👨‍👧‍👦 CONFIGURACIÓN DE PROTECCIÓN PARENTAL")
    print("🛡️ Protegiendo a los niños con amor y tecnología")
    print("=" * 50)
    
    settings = activate_maximum_protection()
    
    print("\n📊 CONFIGURACIÓN ACTUAL:")
    for key, value in settings.items():
        print(f"• {key}: {value}")
    
    print(f"\n📝 Logs guardados en: {parental_config.safety_log_file}")
    print("🎯 ARIA está ahora completamente protegida para niños")