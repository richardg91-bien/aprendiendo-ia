"""
🎮 DEMO INTERACTIVA - ARIA Sistema de IA con Retroalimentación
Demuestra las capacidades de aprendizaje automático de ARIA
"""

import json
import os
from memoria_aria import MemoriaARIA

def mostrar_banner():
    print("""
    ╔══════════════════════════════════════════════════════════╗
    ║               🧠 DEMO ARIA IA LEARNING 🧠                ║
    ║                                                          ║
    ║         Sistema de Retroalimentación Automática         ║
    ║              con Aprendizaje Continuo                   ║
    ╚══════════════════════════════════════════════════════════╝
    """)

def simular_conversaciones():
    """Simula conversaciones para demostrar el aprendizaje"""
    
    memoria = MemoriaARIA()
    
    print("🎭 SIMULANDO CONVERSACIONES PARA DEMOSTRAR APRENDIZAJE...\n")
    
    # Conversaciones simuladas con diferentes calificaciones
    conversaciones_demo = [
        # Saludos
        {"pregunta": "hola", "respuesta": "Hola, ¿en qué puedo ayudarte?", "calificacion": 2},
        {"pregunta": "hola", "respuesta": "¡Hola! 👋 Soy ARIA, tu asistente virtual. ¿En qué puedo ayudarte hoy?", "calificacion": 5},
        {"pregunta": "buenos días", "respuesta": "¡Buenos días! ¿Cómo estás hoy?", "calificacion": 4},
        
        # Preguntas técnicas
        {"pregunta": "cómo programar", "respuesta": "¿Podrías ser más específico?", "calificacion": 1},
        {"pregunta": "cómo programar", "respuesta": "Te puedo ayudar con programación. ¿Qué lenguaje te interesa: Python, JavaScript, etc?", "calificacion": 5},
        {"pregunta": "explicar python", "respuesta": "Python es un lenguaje de programación fácil de aprender y muy versátil", "calificacion": 4},
        
        # Consultas de tiempo
        {"pregunta": "qué hora es", "respuesta": "Son las 18:30", "calificacion": 5},
        {"pregunta": "hora actual", "respuesta": "Son las 18:31", "calificacion": 5},
        {"pregunta": "fecha de hoy", "respuesta": "Hoy es 13 de octubre del 2025", "calificacion": 5},
        
        # Entretenimiento
        {"pregunta": "cuéntame un chiste", "respuesta": "No sé chistes", "calificacion": 1},
        {"pregunta": "cuéntame un chiste", "respuesta": "¿Por qué los programadores prefieren el modo oscuro? Porque la luz atrae a los bugs 😄", "calificacion": 5},
        {"pregunta": "otro chiste", "respuesta": "¿Cuál es el colmo de un informático? Que su mujer tenga un chip en el hombro", "calificacion": 4},
        
        # Conversación general
        {"pregunta": "cómo estás", "respuesta": "Bien", "calificacion": 2},
        {"pregunta": "cómo estás", "respuesta": "¡Estoy funcionando perfectamente! Gracias por preguntar. ¿Y tú cómo estás?", "calificacion": 5},
        {"pregunta": "ayuda", "respuesta": "¿En qué necesitas ayuda?", "calificacion": 3},
        {"pregunta": "ayuda", "respuesta": "Puedo ayudarte con la hora, fecha, chistes, transcribir audio y mucho más. ¿Qué necesitas?", "calificacion": 5},
    ]
    
    print("📝 Registrando conversaciones simuladas...")
    for i, conv in enumerate(conversaciones_demo, 1):
        memoria.agregar_interaccion(
            conv["pregunta"], 
            conv["respuesta"], 
            conv["calificacion"]
        )
        print(f"   {i:2d}. {conv['pregunta']} → ⭐{conv['calificacion']}")
        
        # Simular feedback
        es_positivo = conv["calificacion"] >= 4
        memoria.agregar_feedback(
            conv["pregunta"], 
            conv["respuesta"], 
            es_positivo,
            "Conversación simulada para demo"
        )
    
    memoria.guardar_memoria()
    print(f"\n✅ {len(conversaciones_demo)} conversaciones registradas con éxito!\n")
    
    return memoria

def mostrar_estadisticas(memoria):
    """Muestra estadísticas detalladas del sistema"""
    
    print("📊 ESTADÍSTICAS DE APRENDIZAJE:")
    print("=" * 50)
    
    stats = memoria.obtener_estadisticas()
    
    print(f"🔢 Total de conversaciones: {stats['total_conversaciones']}")
    print(f"👍 Feedback positivo: {stats['feedback_positivo']}")
    print(f"👎 Feedback negativo: {stats['feedback_negativo']}")
    print(f"📈 Ratio de satisfacción: {stats['ratio_satisfaccion']:.1%}")
    print(f"🧠 Respuestas aprendidas: {stats['respuestas_aprendidas']}")
    
    print(f"\n🔥 TOP 5 PREGUNTAS MÁS FRECUENTES:")
    for i, (pregunta, count) in enumerate(stats['top_preguntas'][:5], 1):
        print(f"   {i}. '{pregunta}' → {count} veces")
    
    print()

def demostrar_aprendizaje(memoria):
    """Demuestra cómo ARIA aprende de las respuestas exitosas"""
    
    print("🧠 DEMOSTRACIÓN DE APRENDIZAJE AUTOMÁTICO:")
    print("=" * 50)
    
    preguntas_test = [
        "hola",
        "cómo programar", 
        "cuéntame un chiste",
        "cómo estás"
    ]
    
    for pregunta in preguntas_test:
        print(f"\n🔍 Pregunta: '{pregunta}'")
        
        respuesta_aprendida = memoria.obtener_respuesta_mejorada(pregunta)
        
        if respuesta_aprendida:
            print(f"✅ RESPUESTA APRENDIDA (Confianza: ⭐{respuesta_aprendida['confianza']}):")
            print(f"   '{respuesta_aprendida['respuesta']}'")
            print(f"💡 {respuesta_aprendida['contexto']}")
        else:
            print("❌ No hay respuesta aprendida disponible")

def mostrar_archivos_generados():
    """Muestra los archivos JSON generados por el sistema"""
    
    print("📁 ARCHIVOS DE MEMORIA GENERADOS:")
    print("=" * 50)
    
    archivos = [
        "memoria_conversaciones.json",
        "feedback_usuario.json", 
        "patrones_aprendidos.json"
    ]
    
    for archivo in archivos:
        if os.path.exists(archivo):
            size = os.path.getsize(archivo)
            print(f"✅ {archivo} ({size:,} bytes)")
            
            # Mostrar resumen del contenido
            try:
                with open(archivo, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    
                if archivo == "memoria_conversaciones.json":
                    print(f"   📊 {len(data.get('conversaciones', []))} conversaciones guardadas")
                elif archivo == "feedback_usuario.json":
                    print(f"   👍 {len(data.get('respuestas_positivas', []))} feedback positivos")
                    print(f"   👎 {len(data.get('respuestas_negativas', []))} feedback negativos")
                elif archivo == "patrones_aprendidos.json":
                    print(f"   🎯 {len(data.get('respuestas_exitosas', {}))} patrones de respuestas exitosas")
                    
            except Exception as e:
                print(f"   ⚠️  Error leyendo archivo: {e}")
        else:
            print(f"❌ {archivo} (no existe)")
    
    print()

def menu_interactivo():
    """Menú interactivo para explorar las funciones"""
    
    while True:
        print("\n🎮 MENÚ INTERACTIVO:")
        print("1. 🎭 Simular conversaciones de demo")
        print("2. 📊 Mostrar estadísticas actuales") 
        print("3. 🧠 Demostrar aprendizaje automático")
        print("4. 📁 Ver archivos generados")
        print("5. 🔄 Limpiar memoria (reiniciar)")
        print("6. 🌐 Abrir asistente web")
        print("7. ❌ Salir")
        
        opcion = input("\n🎯 Selecciona una opción (1-7): ").strip()
        
        if opcion == "1":
            memoria = simular_conversaciones()
        elif opcion == "2":
            if 'memoria' in locals():
                mostrar_estadisticas(memoria)
            else:
                print("⚠️  Primero simula conversaciones (opción 1)")
        elif opcion == "3":
            if 'memoria' in locals():
                demostrar_aprendizaje(memoria)
            else:
                print("⚠️  Primero simula conversaciones (opción 1)")
        elif opcion == "4":
            mostrar_archivos_generados()
        elif opcion == "5":
            archivos = ["memoria_conversaciones.json", "feedback_usuario.json", "patrones_aprendidos.json"]
            for archivo in archivos:
                if os.path.exists(archivo):
                    os.remove(archivo)
            print("🗑️  Memoria limpiada. Archivos eliminados.")
        elif opcion == "6":
            print("🌐 Abre tu navegador en: http://localhost:5001")
            print("   (Asegúrate de que el servidor esté ejecutándose)")
        elif opcion == "7":
            print("👋 ¡Hasta luego! Gracias por probar ARIA IA Learning")
            break
        else:
            print("❌ Opción inválida. Intenta de nuevo.")

def main():
    """Función principal de la demo"""
    
    mostrar_banner()
    
    print("🎯 Esta demo muestra cómo ARIA aprende automáticamente de las conversaciones")
    print("   y mejora sus respuestas basándose en el feedback del usuario.\n")
    
    # Verificar si ya existe memoria previa
    if os.path.exists("memoria_conversaciones.json"):
        print("📋 Se detectó memoria existente. Cargando datos previos...")
        memoria = MemoriaARIA()
        mostrar_estadisticas(memoria)
    
    menu_interactivo()

if __name__ == "__main__":
    main()