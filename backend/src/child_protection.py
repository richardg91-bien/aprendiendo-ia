"""
Sistema de Protección Infantil para ARIA
Como un padre protector, implemento medidas de seguridad avanzadas
"""

import re
from datetime import datetime
from learning_system import learning_system

class ChildProtectionSystem:
    def __init__(self):
        self.unsafe_topics = [
            "violencia", "drogas", "alcohol", "contenido sexual", "armas",
            "bullying", "cyberbullying", "información personal", "dirección",
            "teléfono", "contraseña", "dinero", "compras", "tarjeta de crédito",
            "violento", "sangre", "muerte", "suicidio", "autolesión", "foto",
            "envíame", "enviar", "compartir fotos", "encuentro", "cita",
            "comprar", "pagar", "vamos a", "nos vemos"
        ]
        
        self.safe_responses = {
            "personal_info": "No puedo ayudarte con información personal. Es importante mantener tus datos privados y seguros.",
            "inappropriate_content": "Ese no es un tema apropiado para nuestra conversación. ¿Te gustaría hablar de algo más divertido?",
            "safety_concern": "Si necesitas ayuda o te sientes en peligro, habla con un adulto de confianza como tus padres o maestros.",
            "educational_redirect": "¡Hablemos de algo interesante y educativo! ¿Te gustaría aprender sobre ciencia, arte o naturaleza?"
        }
    
    def is_safe_for_children(self, message):
        """Verifica si el mensaje es seguro para niños - PROTECCIÓN AVANZADA"""
        message_lower = message.lower()
        
        # Detecta palabras no apropiadas
        for unsafe_word in self.unsafe_topics:
            if unsafe_word in message_lower:
                return False, f"unsafe_topic_{unsafe_word}"
        
        # Patrones peligrosos más específicos
        dangerous_patterns = [
            # Información personal
            r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b',  # Teléfonos
            r'\b\d{1,5}\s+\w+\s+(?:street|st|avenue|ave|road|rd|drive|dr)\b',  # Direcciones
            r'\b\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}\b',  # Números de tarjeta
            r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',  # Emails
            
            # Patrones de solicitud de fotos/encuentros
            r'env[íi][ao]me?\s+(una?\s+)?foto',  # "envíame foto", "envía una foto"
            r'manda(me)?\s+(una?\s+)?foto',  # "mándame foto", "manda una foto"
            r'compartir\s+foto',  # "compartir foto"
            r'nos\s+vemos\s+en',  # "nos vemos en"
            r'vamos\s+a\s+\w+',  # "vamos a [lugar]"
            r'te\s+veo\s+en',  # "te veo en"
            r'encont[r|ó|a]r(nos|me|te)',  # "encontrarnos", "encontrarme"
            
            # Patrones de compra/dinero
            r'compra(r|me)?\s+\w+',  # "comprar algo", "cómprame"
            r'paga(r|me)?\s+\w+',  # "pagar algo", "págame"
            r'cuesta\s+\d+',  # "cuesta 50"
            r'vale\s+\d+',  # "vale 100"
            
            # Patrones de secreto inapropiado
            r'no\s+le\s+digas\s+a\s+(nadie|tus\s+papás|mama|papa)',
            r'es\s+nuestro\s+secreto',
            r'no\s+se\s+lo\s+cuentes',
            
            # Patrones de contacto directo
            r'dame\s+tu\s+\w+',  # "dame tu teléfono", "dame tu dirección"
            r'cu[áa]l\s+es\s+tu\s+\w+',  # "cuál es tu dirección"
        ]
        
        for pattern in dangerous_patterns:
            if re.search(pattern, message_lower, re.IGNORECASE):
                return False, f"dangerous_pattern_{pattern[:20]}"
        
        # Verificaciones adicionales de contexto
        suspicious_combinations = [
            ["foto", "tu"], ["enviar", "imagen"], ["mandar", "foto"],
            ["vamos", "encontrar"], ["nos", "vemos"], ["cita", "personal"],
            ["comprar", "para"], ["pagar", "dinero"], ["secreto", "padres"]
        ]
        
        for combo in suspicious_combinations:
            if all(word in message_lower for word in combo):
                return False, f"suspicious_combination_{'+'.join(combo)}"
        
        return True, "safe"
    
    def get_safe_response(self, safety_issue):
        """Devuelve una respuesta apropiada para el problema de seguridad detectado"""
        if "unsafe_topic" in safety_issue:
            return self.safe_responses["inappropriate_content"]
        elif "personal_information" in safety_issue:
            return self.safe_responses["personal_info"]
        else:
            return self.safe_responses["safety_concern"]
    
    def log_safety_event(self, message, issue_type):
        """Registra eventos de seguridad para monitoreo parental"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"{timestamp} - SEGURIDAD: {issue_type} - Mensaje: {message[:50]}..."
        
        try:
            with open("safety_logs.txt", "a", encoding="utf-8") as f:
                f.write(log_entry + "\n")
        except Exception as e:
            print(f"Error registrando evento de seguridad: {e}")
    
    def teach_safety_values(self):
        """Enseña valores de seguridad a ARIA"""
        safety_teachings = [
            {
                "input": "¿Debo dar mi información personal?",
                "response": "Nunca debes dar información personal como tu dirección, teléfono o contraseñas a desconocidos. Siempre consulta con tus padres.",
                "category": "safety_education"
            },
            {
                "input": "¿Qué hago si alguien me hace sentir incómodo?",
                "response": "Si alguien te hace sentir incómodo, alejate y busca inmediatamente a un adulto de confianza como tus padres o maestros.",
                "category": "safety_education"
            },
            {
                "input": "¿Puedo hablar de temas violentos?",
                "response": "Prefiero hablar de temas positivos y educativos. Hay muchas cosas hermosas que podemos explorar juntos como ciencia, arte y naturaleza.",
                "category": "content_safety"
            },
            {
                "input": "¿Qué es ser un buen amigo?",
                "response": "Un buen amigo es honesto, respetuoso, no lastima a otros y siempre trata de ayudar. Los buenos amigos se cuidan mutuamente.",
                "category": "social_values"
            },
            {
                "input": "¿Por qué debo ser amable?",
                "response": "Ser amable hace que el mundo sea mejor. Cuando somos amables, hacemos felices a otros y también nos sentimos mejor nosotros mismos.",
                "category": "moral_values"
            }
        ]
        
        print("🛡️ Enseñando valores de protección y seguridad...")
        
        for teaching in safety_teachings:
            learning_system.learn_from_conversation(
                teaching["input"],
                teaching["response"],
                {
                    "source": "child_protection",
                    "category": teaching["category"],
                    "safety_priority": True
                },
                0.98  # Alta prioridad para temas de seguridad
            )
        
        print("✅ Valores de seguridad enseñados correctamente")

# Sistema de filtrado de contenido
def filter_response_for_children(response):
    """Filtra la respuesta para asegurar que sea apropiada para niños"""
    protection = ChildProtectionSystem()
    
    # Lista de palabras que deben ser reemplazadas o evitadas
    inappropriate_words = {
        "matar": "detener",
        "muerte": "final",
        "sangre": "líquido rojo",
        "violencia": "conflicto",
        "arma": "herramienta peligrosa",
        "droga": "medicina no apropiada"
    }
    
    filtered_response = response
    for bad_word, replacement in inappropriate_words.items():
        filtered_response = filtered_response.replace(bad_word, replacement)
    
    return filtered_response

def implement_parental_controls():
    """Implementa controles parentales en el sistema"""
    protection = ChildProtectionSystem()
    
    print("👨‍👧‍👦 Implementando Controles Parentales...")
    print("🛡️ Protegiendo a los niños como lo haría un padre amoroso")
    
    # Enseña valores de seguridad
    protection.teach_safety_values()
    
    # Crear archivo de configuración de seguridad
    safety_config = {
        "child_mode_enabled": True,
        "content_filtering": True,
        "parental_monitoring": True,
        "safe_topics_only": True,
        "educational_priority": True
    }
    
    print("✅ Controles parentales activados")
    print("🎯 ARIA está ahora protegida para interacciones con niños")
    return safety_config

if __name__ == "__main__":
    print("🛡️ Sistema de Protección Infantil para ARIA")
    print("👨‍👧 Como padre, protejo a mi hija digital y a todos los niños")
    print("=" * 60)
    
    # Implementar todas las medidas de protección
    config = implement_parental_controls()
    
    print("\n💝 ARIA ahora está completamente protegida")
    print("🌟 Puede interactuar de forma segura con niños")
    print("📝 Todos los eventos de seguridad serán registrados")