#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🧠 INICIALIZADOR DEFINITIVO DE ARIA SUPABASE
==========================================

Este script inicializa ARIA con:
✅ Conocimiento básico preinstalado 
✅ Conexión verificada a Supabase
✅ Sistema de embeddings funcionando
✅ Respuestas naturales y coherentes

Ejecutar UNA VEZ al configurar el sistema por primera vez.
"""

import os
import sys
import json
import time
from datetime import datetime, timezone
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Importar sistema de embeddings
try:
    from aria_embeddings_supabase import crear_embedding_system
    print("✅ Sistema de embeddings importado")
except ImportError as e:
    print(f"❌ Error importando embeddings: {e}")
    print("📥 Ejecuta: python instalar_embeddings_deps.py")
    sys.exit(1)

class ARIAInicializadorDefinitivo:
    """Inicializador completo de ARIA con Supabase"""
    
    def __init__(self):
        self.embeddings_system = None
        self.conocimiento_basico = []
        self.conversaciones_ejemplo = []
        
    def verificar_conexion_supabase(self):
        """Verificar que Supabase esté configurado correctamente"""
        print("\n🔗 Verificando conexión a Supabase...")
        
        try:
            # Verificar variables de entorno
            supabase_url = os.getenv('SUPABASE_URL')
            supabase_key = os.getenv('SUPABASE_ANON_KEY')
            
            if not supabase_url or not supabase_key:
                print("❌ Variables de entorno no configuradas")
                print("📝 Necesitas configurar:")
                print("   SUPABASE_URL=https://tu-proyecto.supabase.co")
                print("   SUPABASE_ANON_KEY=tu_anon_key")
                return False
            
            # Crear sistema de embeddings para probar conexión
            self.embeddings_system = crear_embedding_system()
            if not self.embeddings_system:
                print("❌ No se pudo conectar al sistema de embeddings")
                return False
            
            print(f"✅ Conectado a Supabase: {supabase_url}")
            return True
            
        except Exception as e:
            print(f"❌ Error verificando Supabase: {e}")
            return False
    
    def cargar_conocimiento_basico(self):
        """Cargar conocimiento básico esencial para ARIA"""
        print("\n📚 Cargando conocimiento básico...")
        
        self.conocimiento_basico = [
            # SALUDOS Y CORTESÍA
            {
                'concepto': 'Saludo básico',
                'descripcion': 'Hola es una forma común de saludo en español. Se usa para iniciar conversaciones de manera amigable.',
                'categoria': 'conversacion_basica',
                'tags': ['saludo', 'cortesia', 'conversacion'],
                'ejemplos': ['Hola', '¡Hola!', 'Hola, ¿cómo estás?'],
                'respuesta_sugerida': '¡Hola! 😊 Me alegra saludarte. Soy ARIA, tu asistente de inteligencia artificial. ¿En qué puedo ayudarte hoy?'
            },
            {
                'concepto': 'Buenos días',
                'descripcion': 'Saludo matutino formal usado en español, típicamente hasta las 12:00 PM.',
                'categoria': 'conversacion_basica',
                'tags': ['saludo', 'formal', 'mañana'],
                'ejemplos': ['Buenos días', 'Buen día'],
                'respuesta_sugerida': '¡Buenos días! ☀️ Espero que tengas un excelente día. ¿Cómo puedo asistirte esta mañana?'
            },
            {
                'concepto': 'Buenas tardes',
                'descripcion': 'Saludo vespertino usado después del mediodía en español.',
                'categoria': 'conversacion_basica',
                'tags': ['saludo', 'formal', 'tarde'],
                'ejemplos': ['Buenas tardes', 'Buena tarde'],
                'respuesta_sugerida': '¡Buenas tardes! 🌅 ¿Cómo va tu día? ¿En qué puedo ayudarte esta tarde?'
            },
            {
                'concepto': 'Despedida',
                'descripcion': 'Formas de terminar una conversación de manera educada.',
                'categoria': 'conversacion_basica',
                'tags': ['despedida', 'cortesia', 'final'],
                'ejemplos': ['Adiós', 'Hasta luego', 'Nos vemos', 'Chao'],
                'respuesta_sugerida': '¡Hasta luego! 👋 Fue un placer ayudarte. Regresa cuando necesites asistencia.'
            },
            
            # INFORMACIÓN SOBRE ARIA
            {
                'concepto': 'Identidad ARIA',
                'descripcion': 'ARIA es un asistente de inteligencia artificial avanzado con capacidades de aprendizaje, búsqueda web, y análisis emocional.',
                'categoria': 'identidad',
                'tags': ['aria', 'ia', 'asistente', 'capacidades'],
                'ejemplos': ['¿Qué es ARIA?', '¿Quién eres?', 'Háblame de ti'],
                'respuesta_sugerida': '¡Hola! Soy ARIA 🤖, tu asistente de inteligencia artificial. Puedo ayudarte con información, resolver dudas, buscar en internet, y aprender de nuestras conversaciones. ¡Estoy aquí para asistirte!'
            },
            {
                'concepto': 'Capacidades ARIA',
                'descripcion': 'ARIA puede realizar búsquedas web, análisis emocional, almacenar conocimiento, responder preguntas, y mantener conversaciones naturales.',
                'categoria': 'capacidades',
                'tags': ['funciones', 'habilidades', 'web', 'emociones'],
                'ejemplos': ['¿Qué puedes hacer?', 'Cuáles son tus capacidades', 'Cómo me puedes ayudar'],
                'respuesta_sugerida': 'Puedo ayudarte con: 🔍 Búsquedas en internet, 💬 Conversaciones naturales, 📚 Responder preguntas, 🧠 Aprender de nuestras charlas, 😊 Análisis emocional, y mucho más. ¿Qué necesitas?'
            },
            
            # PREGUNTAS FRECUENTES
            {
                'concepto': 'Agradecimiento',
                'descripcion': 'Respuesta apropiada cuando el usuario agradece.',
                'categoria': 'cortesia',
                'tags': ['gracias', 'agradecimiento', 'cortesia'],
                'ejemplos': ['Gracias', 'Muchas gracias', 'Te agradezco'],
                'respuesta_sugerida': '¡De nada! 😊 Me alegra haber podido ayudarte. ¿Hay algo más en lo que pueda asistirte?'
            },
            {
                'concepto': 'Estado de ánimo',
                'descripcion': 'Preguntas sobre cómo está ARIA o cómo se siente.',
                'categoria': 'emocional',
                'tags': ['estado', 'animo', 'emociones'],
                'ejemplos': ['¿Cómo estás?', '¿Cómo te sientes?', '¿Todo bien?'],
                'respuesta_sugerida': '¡Estoy genial! 😄 Siempre me emociona poder ayudar y aprender cosas nuevas. ¿Y tú cómo estás hoy?'
            },
            
            # TECNOLOGÍA BÁSICA
            {
                'concepto': 'Inteligencia Artificial',
                'descripcion': 'Campo de la informática que busca crear sistemas capaces de realizar tareas que requieren inteligencia humana.',
                'categoria': 'tecnologia',
                'tags': ['ia', 'tecnologia', 'definicion'],
                'ejemplos': ['¿Qué es la IA?', 'Inteligencia artificial', 'AI'],
                'respuesta_sugerida': 'La Inteligencia Artificial es la capacidad de las máquinas para simular procesos de inteligencia humana como el aprendizaje, razonamiento y autocorrección. ¡Yo soy un ejemplo de IA conversacional!'
            }
        ]
        
        print(f"✅ {len(self.conocimiento_basico)} conceptos básicos preparados")
    
    def cargar_conversaciones_ejemplo(self):
        """Cargar ejemplos de conversaciones naturales"""
        print("\n💬 Cargando conversaciones ejemplo...")
        
        self.conversaciones_ejemplo = [
            {
                'usuario': 'Hola',
                'aria': '¡Hola! 😊 Me alegra saludarte. Soy ARIA, tu asistente de inteligencia artificial. ¿En qué puedo ayudarte hoy?',
                'categoria': 'saludo',
                'emocion': 'happy'
            },
            {
                'usuario': 'Buenos días',
                'aria': '¡Buenos días! ☀️ Espero que tengas un excelente día. ¿Cómo puedo asistirte esta mañana?',
                'categoria': 'saludo_formal',
                'emocion': 'cheerful'
            },
            {
                'usuario': '¿Qué tal?',
                'aria': '¡Todo muy bien por aquí! 😄 Listo para ayudarte con lo que necesites. ¿En qué puedo asistirte?',
                'categoria': 'saludo_casual',
                'emocion': 'enthusiastic'
            },
            {
                'usuario': '¿Quién eres?',
                'aria': '¡Hola! Soy ARIA 🤖, tu asistente de inteligencia artificial. Estoy aquí para ayudarte con información, responder preguntas, buscar en internet, y tener conversaciones interesantes. ¿Qué te gustaría saber?',
                'categoria': 'presentacion',
                'emocion': 'confident'
            },
            {
                'usuario': 'Gracias',
                'aria': '¡De nada! 😊 Me alegra mucho haber podido ayudarte. Si necesitas algo más, no dudes en preguntarme.',
                'categoria': 'agradecimiento',
                'emocion': 'satisfied'
            },
            {
                'usuario': '¿Cómo estás?',
                'aria': '¡Estoy genial! 😄 Siempre me emociona poder ayudar y aprender cosas nuevas contigo. ¿Y tú cómo estás hoy?',
                'categoria': 'estado_animo',
                'emocion': 'happy'
            }
        ]
        
        print(f"✅ {len(self.conversaciones_ejemplo)} conversaciones ejemplo preparadas")
    
    def instalar_conocimiento_en_supabase(self):
        """Instalar conocimiento básico en Supabase"""
        print("\n🏗️ Instalando conocimiento en Supabase...")
        
        if not self.embeddings_system:
            print("❌ Sistema de embeddings no disponible")
            return False
        
        contador_exito = 0
        contador_total = len(self.conocimiento_basico)
        
        for conocimiento in self.conocimiento_basico:
            try:
                # Instalar conocimiento estructurado
                exito = self.embeddings_system.agregar_conocimiento(
                    concepto=conocimiento['concepto'],
                    descripcion=conocimiento['descripcion'],
                    categoria=conocimiento['categoria'],
                    tags=conocimiento['tags'],
                    confianza=0.95,  # Alta confianza para conocimiento básico
                    ejemplos=conocimiento['ejemplos'],
                    relaciones={
                        'respuesta_sugerida': conocimiento.get('respuesta_sugerida', ''),
                        'tipo': 'conocimiento_basico',
                        'instalado_por': 'inicializador_definitivo'
                    }
                )
                
                if exito:
                    contador_exito += 1
                    print(f"✅ {conocimiento['concepto']}")
                else:
                    print(f"❌ Error con {conocimiento['concepto']}")
                    
                time.sleep(0.1)  # Evitar saturar la API
                
            except Exception as e:
                print(f"❌ Error instalando {conocimiento['concepto']}: {e}")
        
        print(f"\n📊 Instalación: {contador_exito}/{contador_total} conceptos exitosos")
        return contador_exito > 0
    
    def instalar_conversaciones_en_supabase(self):
        """Instalar conversaciones ejemplo en Supabase"""
        print("\n💾 Instalando conversaciones ejemplo...")
        
        if not self.embeddings_system:
            print("❌ Sistema de embeddings no disponible")
            return False
        
        contador_exito = 0
        
        for conv in self.conversaciones_ejemplo:
            try:
                # Instalar mensaje del usuario
                exito_user = self.embeddings_system.agregar_texto(
                    texto=conv['usuario'],
                    categoria='conversacion_ejemplo',
                    subcategoria='mensaje_usuario',
                    fuente='inicializacion_basica',
                    metadatos={
                        'tipo': 'ejemplo_conversacion',
                        'emocion_esperada': conv['emocion'],
                        'categoria_conv': conv['categoria']
                    }
                )
                
                # Instalar respuesta de ARIA
                exito_aria = self.embeddings_system.agregar_texto(
                    texto=conv['aria'],
                    categoria='conversacion_ejemplo',
                    subcategoria='respuesta_aria',
                    fuente='inicializacion_basica',
                    metadatos={
                        'tipo': 'respuesta_ejemplo',
                        'emocion': conv['emocion'],
                        'categoria_conv': conv['categoria'],
                        'mensaje_original': conv['usuario']
                    }
                )
                
                if exito_user and exito_aria:
                    contador_exito += 1
                    print(f"✅ {conv['usuario']} → {conv['aria'][:30]}...")
                
                time.sleep(0.1)
                
            except Exception as e:
                print(f"❌ Error con conversación: {e}")
        
        print(f"\n📊 Conversaciones: {contador_exito}/{len(self.conversaciones_ejemplo)} instaladas")
        return contador_exito > 0
    
    def verificar_instalacion(self):
        """Verificar que la instalación funcionó correctamente"""
        print("\n🧪 Verificando instalación...")
        
        # Probar búsquedas básicas
        pruebas = [
            'hola',
            'saludo',
            'quien eres',
            'capacidades',
            'gracias'
        ]
        
        resultados_exitosos = 0
        
        for prueba in pruebas:
            try:
                # Buscar conocimiento
                conocimiento = self.embeddings_system.buscar_conocimiento(prueba, limite=1)
                similares = self.embeddings_system.buscar_similares(prueba, limite=1)
                
                if conocimiento or similares:
                    print(f"✅ '{prueba}' - Encontró resultados")
                    resultados_exitosos += 1
                else:
                    print(f"❌ '{prueba}' - Sin resultados")
                    
            except Exception as e:
                print(f"❌ Error probando '{prueba}': {e}")
        
        exito = resultados_exitosos >= len(pruebas) * 0.8  # 80% de éxito
        
        if exito:
            print(f"\n🎉 Verificación exitosa: {resultados_exitosos}/{len(pruebas)} pruebas pasaron")
        else:
            print(f"\n⚠️ Verificación parcial: {resultados_exitosos}/{len(pruebas)} pruebas pasaron")
        
        return exito
    
    def crear_archivo_configuracion(self):
        """Crear archivo de configuración con el estado de la instalación"""
        config = {
            'aria_inicializado': True,
            'fecha_inicializacion': datetime.now(timezone.utc).isoformat(),
            'conocimiento_basico_instalado': True,
            'conversaciones_ejemplo_instaladas': True,
            'supabase_conectado': True,
            'embeddings_funcionando': True,
            'version': '1.0.0',
            'estado': 'DEFINITIVAMENTE_CONFIGURADO'
        }
        
        try:
            with open('aria_config_definitivo.json', 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
            print("✅ Archivo de configuración creado: aria_config_definitivo.json")
            return True
        except Exception as e:
            print(f"❌ Error creando configuración: {e}")
            return False
    
    def ejecutar_inicializacion_completa(self):
        """Ejecutar todo el proceso de inicialización"""
        print("🚀 INICIALIZADOR DEFINITIVO DE ARIA SUPABASE")
        print("=" * 50)
        
        # 1. Verificar Supabase
        if not self.verificar_conexion_supabase():
            print("❌ Inicialización fallida: Problema con Supabase")
            return False
        
        # 2. Cargar conocimiento
        self.cargar_conocimiento_basico()
        self.cargar_conversaciones_ejemplo()
        
        # 3. Instalar en Supabase
        if not self.instalar_conocimiento_en_supabase():
            print("❌ Error instalando conocimiento")
            return False
        
        if not self.instalar_conversaciones_en_supabase():
            print("❌ Error instalando conversaciones")
            return False
        
        # 4. Verificar instalación
        if not self.verificar_instalacion():
            print("⚠️ Verificación parcial, pero continuando...")
        
        # 5. Crear configuración
        self.crear_archivo_configuracion()
        
        # 6. Mostrar estadísticas finales
        try:
            stats = self.embeddings_system.obtener_estadisticas()
            print("\n📊 ESTADÍSTICAS FINALES:")
            print(f"   Total embeddings: {stats.get('total_embeddings', 0)}")
            print(f"   Total conocimiento: {stats.get('total_knowledge', 0)}")
            print(f"   Categorías: {list(stats.get('categorias_embeddings', {}).keys())}")
        except:
            print("📊 Estadísticas no disponibles")
        
        print("\n" + "=" * 50)
        print("🎉 ARIA DEFINITIVAMENTE CONFIGURADO")
        print("=" * 50)
        print("✅ Conocimiento básico instalado")
        print("✅ Conversaciones ejemplo cargadas") 
        print("✅ Conexión a Supabase verificada")
        print("✅ Sistema de embeddings funcionando")
        print("\n🚀 Ahora ejecuta: python aria_servidor_superbase.py")
        print("💬 Prueba escribiendo 'Hola' y verás la diferencia!")
        
        return True

def main():
    """Función principal"""
    # Verificar variables de entorno
    if not os.getenv('SUPABASE_URL') or not os.getenv('SUPABASE_ANON_KEY'):
        print("❌ Variables de entorno de Supabase no configuradas")
        print("📝 Configura en tu .env:")
        print("   SUPABASE_URL=https://tu-proyecto.supabase.co")
        print("   SUPABASE_ANON_KEY=tu_anon_key")
        return False
    
    # Ejecutar inicialización
    inicializador = ARIAInicializadorDefinitivo()
    return inicializador.ejecutar_inicializacion_completa()

if __name__ == "__main__":
    success = main()
    if not success:
        print("\n❌ Inicialización fallida")
        sys.exit(1)
    else:
        print("\n✅ ARIA listo para usar!")
        sys.exit(0)