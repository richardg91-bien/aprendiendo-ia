"""
Sistema de Memoria y Retroalimentación para ARIA
Permite que la IA aprenda y mejore con cada conversación
"""

import json
import os
import datetime
from collections import defaultdict, Counter

class MemoriaARIA:
    def __init__(self):
        self.archivo_memoria = "memoria_conversaciones.json"
        self.archivo_feedback = "feedback_usuario.json" 
        self.archivo_patrones = "patrones_aprendidos.json"
        self.conversacion_actual = []
        self.memoria = self.cargar_memoria()
        self.feedback = self.cargar_feedback()
        self.patrones = self.cargar_patrones()
        
    def cargar_memoria(self):
        """Carga el historial de conversaciones"""
        try:
            if os.path.exists(self.archivo_memoria):
                with open(self.archivo_memoria, 'r', encoding='utf-8') as f:
                    return json.load(f)
            return {"conversaciones": [], "estadisticas": {}}
        except:
            return {"conversaciones": [], "estadisticas": {}}
    
    def cargar_feedback(self):
        """Carga el feedback del usuario"""
        try:
            if os.path.exists(self.archivo_feedback):
                with open(self.archivo_feedback, 'r', encoding='utf-8') as f:
                    return json.load(f)
            return {"respuestas_positivas": [], "respuestas_negativas": [], "sugerencias": []}
        except:
            return {"respuestas_positivas": [], "respuestas_negativas": [], "sugerencias": []}
    
    def cargar_patrones(self):
        """Carga patrones aprendidos"""
        try:
            if os.path.exists(self.archivo_patrones):
                with open(self.archivo_patrones, 'r', encoding='utf-8') as f:
                    return json.load(f)
            return {
                "preguntas_frecuentes": {},
                "respuestas_exitosas": {},
                "contextos_populares": {},
                "preferencias_usuario": {}
            }
        except:
            return {
                "preguntas_frecuentes": {},
                "respuestas_exitosas": {},
                "contextos_populares": {},
                "preferencias_usuario": {}
            }
    
    def guardar_memoria(self):
        """Guarda toda la memoria en archivos"""
        try:
            with open(self.archivo_memoria, 'w', encoding='utf-8') as f:
                json.dump(self.memoria, f, ensure_ascii=False, indent=2)
            
            with open(self.archivo_feedback, 'w', encoding='utf-8') as f:
                json.dump(self.feedback, f, ensure_ascii=False, indent=2)
                
            with open(self.archivo_patrones, 'w', encoding='utf-8') as f:
                json.dump(self.patrones, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Error guardando memoria: {e}")
    
    def agregar_interaccion(self, pregunta, respuesta, calificacion=None):
        """Agrega una nueva interacción a la memoria"""
        interaccion = {
            "timestamp": datetime.datetime.now().isoformat(),
            "pregunta": pregunta.lower().strip(),
            "respuesta": respuesta,
            "calificacion": calificacion,
            "contexto": self.obtener_contexto_actual()
        }
        
        self.conversacion_actual.append(interaccion)
        self.memoria["conversaciones"].append(interaccion)
        
        # Analizar y actualizar patrones
        self.analizar_patron(pregunta, respuesta, calificacion)
        self.actualizar_estadisticas(pregunta)
        
    def obtener_contexto_actual(self):
        """Obtiene el contexto de la conversación actual"""
        if len(self.conversacion_actual) > 0:
            return {
                "tema_anterior": self.conversacion_actual[-1]["pregunta"][:50],
                "num_intercambios": len(self.conversacion_actual)
            }
        return {"tema_anterior": None, "num_intercambios": 0}
    
    def guardar_conversacion(self, pregunta, respuesta, categoria=None):
        """Método compatible para guardar conversación con categoría"""
        self.agregar_interaccion(pregunta, respuesta)
        self.guardar_memoria()
    
    
    def analizar_patron(self, pregunta, respuesta, calificacion):
        """Analiza patrones en las interacciones"""
        pregunta_key = pregunta.lower().strip()
        
        # Contar preguntas frecuentes
        if pregunta_key in self.patrones["preguntas_frecuentes"]:
            self.patrones["preguntas_frecuentes"][pregunta_key] += 1
        else:
            self.patrones["preguntas_frecuentes"][pregunta_key] = 1
        
        # Guardar respuestas exitosas
        if calificacion and calificacion >= 4:  # Calificación alta
            if pregunta_key not in self.patrones["respuestas_exitosas"]:
                self.patrones["respuestas_exitosas"][pregunta_key] = []
            self.patrones["respuestas_exitosas"][pregunta_key].append({
                "respuesta": respuesta,
                "calificacion": calificacion,
                "timestamp": datetime.datetime.now().isoformat()
            })
    
    def actualizar_estadisticas(self, pregunta):
        """Actualiza estadísticas generales"""
        if "total_interacciones" not in self.memoria["estadisticas"]:
            self.memoria["estadisticas"]["total_interacciones"] = 0
        
        self.memoria["estadisticas"]["total_interacciones"] += 1
        self.memoria["estadisticas"]["ultima_actualizacion"] = datetime.datetime.now().isoformat()
        
        # Análisis de palabras clave
        palabras = pregunta.lower().split()
        if "palabras_clave" not in self.memoria["estadisticas"]:
            self.memoria["estadisticas"]["palabras_clave"] = {}
        
        for palabra in palabras:
            if len(palabra) > 2:  # Solo palabras significativas
                if palabra in self.memoria["estadisticas"]["palabras_clave"]:
                    self.memoria["estadisticas"]["palabras_clave"][palabra] += 1
                else:
                    self.memoria["estadisticas"]["palabras_clave"][palabra] = 1
    
    def obtener_respuesta_mejorada(self, pregunta):
        """Obtiene una respuesta mejorada basada en el aprendizaje"""
        pregunta_key = pregunta.lower().strip()
        
        # Buscar si hay respuestas exitosas previas para preguntas similares
        for pregunta_anterior, respuestas in self.patrones["respuestas_exitosas"].items():
            if self.calcular_similitud(pregunta_key, pregunta_anterior) > 0.7:
                # Devolver la respuesta más exitosa
                mejor_respuesta = max(respuestas, key=lambda x: x["calificacion"])
                return {
                    "respuesta": mejor_respuesta["respuesta"],
                    "confianza": mejor_respuesta["calificacion"],
                    "aprendida": True,
                    "contexto": f"He aprendido esto de {len(respuestas)} interacciones anteriores"
                }
        
        return None
    
    def calcular_similitud(self, texto1, texto2):
        """Calcula similitud básica entre dos textos"""
        palabras1 = set(texto1.split())
        palabras2 = set(texto2.split())
        
        if not palabras1 or not palabras2:
            return 0
            
        interseccion = len(palabras1.intersection(palabras2))
        union = len(palabras1.union(palabras2))
        
        return interseccion / union if union > 0 else 0
    
    def agregar_feedback(self, pregunta, respuesta, es_positivo, comentario=""):
        """Agrega feedback del usuario"""
        feedback_item = {
            "timestamp": datetime.datetime.now().isoformat(),
            "pregunta": pregunta,
            "respuesta": respuesta,
            "comentario": comentario
        }
        
        if es_positivo:
            self.feedback["respuestas_positivas"].append(feedback_item)
        else:
            self.feedback["respuestas_negativas"].append(feedback_item)
            
        self.guardar_memoria()
    
    def obtener_estadisticas(self):
        """Devuelve estadísticas de aprendizaje"""
        total_conversaciones = len(self.memoria["conversaciones"])
        total_feedback_positivo = len(self.feedback["respuestas_positivas"])
        total_feedback_negativo = len(self.feedback["respuestas_negativas"])
        
        # Top 5 preguntas más frecuentes
        top_preguntas = sorted(
            self.patrones["preguntas_frecuentes"].items(),
            key=lambda x: x[1],
            reverse=True
        )[:5]
        
        return {
            "total_conversaciones": total_conversaciones,
            "feedback_positivo": total_feedback_positivo,
            "feedback_negativo": total_feedback_negativo,
            "ratio_satisfaccion": total_feedback_positivo / max(1, total_feedback_positivo + total_feedback_negativo),
            "top_preguntas": top_preguntas,
            "respuestas_aprendidas": len(self.patrones["respuestas_exitosas"])
        }
    
    def nueva_sesion(self):
        """Inicia una nueva sesión de conversación"""
        if self.conversacion_actual:
            # Guardar la conversación actual
            sesion = {
                "timestamp": datetime.datetime.now().isoformat(),
                "interacciones": self.conversacion_actual.copy(),
                "duracion_minutos": len(self.conversacion_actual) * 2  # Estimación
            }
            
            if "sesiones" not in self.memoria:
                self.memoria["sesiones"] = []
            self.memoria["sesiones"].append(sesion)
            
        self.conversacion_actual = []
        self.guardar_memoria()
    
    def obtener_contexto_conversacion(self):
        """Obtiene el contexto actual de la conversación"""
        if not self.conversacion_actual:
            return "Iniciando nueva conversación"
        
        temas_recientes = []
        for interaccion in self.conversacion_actual[-3:]:  # Últimas 3 interacciones
            palabras_clave = [p for p in interaccion["pregunta"].split() if len(p) > 3]
            temas_recientes.extend(palabras_clave[:2])
        
        if temas_recientes:
            return f"Contexto: hemos hablado de {', '.join(set(temas_recientes))}"
        return "Continuando conversación"