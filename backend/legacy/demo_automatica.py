"""
🎯 DEMOSTRACIÓN AUTOMÁTICA - ARIA Sistema de Aprendizaje
Muestra automáticamente las capacidades sin menú interactivo
"""

import json
import os
from memoria_aria import MemoriaARIA

def mostrar_banner():
    print("""
╔══════════════════════════════════════════════════════════════╗
║                  🧠 ARIA IA DEMO AUTOMÁTICA 🧠              ║
║                                                              ║
║              ¡Mira cómo ARIA aprende automáticamente!       ║
╚══════════════════════════════════════════════════════════════╝
    """)

def mostrar_archivos_memoria():
    """Muestra el contenido de los archivos de memoria"""
    
    print("📁 ARCHIVOS DE MEMORIA GENERADOS:")
    print("=" * 60)
    
    archivos = [
        ("memoria_conversaciones.json", "💭 Memoria de Conversaciones"),
        ("feedback_usuario.json", "👍 Feedback del Usuario"), 
        ("patrones_aprendidos.json", "🎯 Patrones Aprendidos")
    ]
    
    for archivo, titulo in archivos:
        if os.path.exists(archivo):
            size = os.path.getsize(archivo)
            print(f"\n{titulo}")
            print(f"📄 Archivo: {archivo} ({size:,} bytes)")
            
            try:
                with open(archivo, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    
                if archivo == "memoria_conversaciones.json":
                    conversaciones = data.get('conversaciones', [])
                    print(f"   📊 {len(conversaciones)} conversaciones guardadas")
                    
                    if conversaciones:
                        print("   🔸 Últimas 3 conversaciones:")
                        for conv in conversaciones[-3:]:
                            timestamp = conv.get('timestamp', 'N/A')[:19].replace('T', ' ')
                            pregunta = conv.get('pregunta', 'N/A')[:30]
                            calificacion = conv.get('calificacion', 'N/A')
                            print(f"      • {timestamp} | '{pregunta}...' | ⭐{calificacion}")
                    
                elif archivo == "feedback_usuario.json":
                    positivos = len(data.get('respuestas_positivas', []))
                    negativos = len(data.get('respuestas_negativas', []))
                    total = positivos + negativos
                    ratio = (positivos / total * 100) if total > 0 else 0
                    
                    print(f"   👍 Feedback positivo: {positivos}")
                    print(f"   👎 Feedback negativo: {negativos}")
                    print(f"   📈 Ratio de satisfacción: {ratio:.1f}%")
                    
                elif archivo == "patrones_aprendidos.json":
                    frecuentes = data.get('preguntas_frecuentes', {})
                    exitosas = data.get('respuestas_exitosas', {})
                    
                    print(f"   🔥 {len(frecuentes)} preguntas frecuentes identificadas")
                    print(f"   🎯 {len(exitosas)} respuestas exitosas aprendidas")
                    
                    if frecuentes:
                        print("   📈 Top 3 preguntas más frecuentes:")
                        top_3 = sorted(frecuentes.items(), key=lambda x: x[1], reverse=True)[:3]
                        for i, (pregunta, count) in enumerate(top_3, 1):
                            print(f"      {i}. '{pregunta}' → {count} veces")
                        
            except Exception as e:
                print(f"   ❌ Error leyendo archivo: {e}")
        else:
            print(f"❌ {archivo} no encontrado")

def demostrar_aprendizaje_automatico():
    """Demuestra el aprendizaje automático de ARIA"""
    
    print("\n🧠 DEMOSTRACIÓN DE APRENDIZAJE AUTOMÁTICO:")
    print("=" * 60)
    
    try:
        memoria = MemoriaARIA()
        
        # Preguntas de prueba
        preguntas_test = [
            "hola",
            "cómo programar", 
            "cuéntame un chiste",
            "qué hora es",
            "cómo estás"
        ]
        
        print("🔍 Probando respuestas aprendidas para preguntas comunes...\n")
        
        respuestas_encontradas = 0
        
        for i, pregunta in enumerate(preguntas_test, 1):
            print(f"{i}. Pregunta: '{pregunta}'")
            
            respuesta_aprendida = memoria.obtener_respuesta_mejorada(pregunta)
            
            if respuesta_aprendida:
                respuestas_encontradas += 1
                print(f"   ✅ RESPUESTA APRENDIDA (Confianza: ⭐{respuesta_aprendida['confianza']})")
                respuesta_cortada = respuesta_aprendida['respuesta'][:80]
                print(f"   💬 '{respuesta_cortada}...'")
                print(f"   🧠 {respuesta_aprendida['contexto']}")
            else:
                print(f"   ❌ Sin respuesta aprendida - usaría respuesta genérica")
            
            print()
        
        print(f"📊 RESULTADO: {respuestas_encontradas}/{len(preguntas_test)} preguntas tienen respuestas aprendidas")
        porcentaje = (respuestas_encontradas / len(preguntas_test)) * 100
        print(f"🎯 Eficiencia del aprendizaje: {porcentaje:.1f}%")
        
    except Exception as e:
        print(f"❌ Error en demostración: {e}")

def mostrar_estadisticas_completas():
    """Muestra estadísticas completas del sistema"""
    
    print("\n📊 ESTADÍSTICAS COMPLETAS DEL SISTEMA:")
    print("=" * 60)
    
    try:
        memoria = MemoriaARIA()
        stats = memoria.obtener_estadisticas()
        
        print(f"🔢 Total de conversaciones: {stats['total_conversaciones']}")
        print(f"👍 Feedback positivo: {stats['feedback_positivo']}")
        print(f"👎 Feedback negativo: {stats['feedback_negativo']}")
        print(f"📈 Ratio de satisfacción: {stats['ratio_satisfaccion']:.1%}")
        print(f"🧠 Respuestas aprendidas: {stats['respuestas_aprendidas']}")
        
        if stats['top_preguntas']:
            print(f"\n🔥 TOP PREGUNTAS MÁS FRECUENTES:")
            for i, (pregunta, count) in enumerate(stats['top_preguntas'][:5], 1):
                barra = "█" * min(count, 20)  # Gráfico de barras simple
                print(f"   {i}. '{pregunta}' → {count} veces {barra}")
        
        # Análisis de tendencias
        if stats['total_conversaciones'] > 10:
            print(f"\n📈 ANÁLISIS DE TENDENCIAS:")
            if stats['ratio_satisfaccion'] > 0.8:
                print("   🎉 ¡Excelente! Alta satisfacción del usuario")
            elif stats['ratio_satisfaccion'] > 0.6:
                print("   👍 Buena satisfacción, hay espacio para mejorar")
            else:
                print("   ⚠️  Satisfacción baja, necesita más entrenamiento")
                
            if stats['respuestas_aprendidas'] > 5:
                print("   🧠 Sistema maduro: Muchas respuestas aprendidas")
            else:
                print("   🌱 Sistema en crecimiento: Aprendiendo patrones")
        
    except Exception as e:
        print(f"❌ Error obteniendo estadísticas: {e}")

def mostrar_estado_servidor():
    """Verifica si el servidor web está ejecutándose"""
    
    print(f"\n🌐 ESTADO DEL SERVIDOR WEB:")
    print("=" * 60)
    
    try:
        import requests
        
        try:
            response = requests.get("http://localhost:5001", timeout=2)
            if response.status_code == 200:
                print("✅ Servidor ARIA activo en http://localhost:5001")
                print("🎮 Puedes interactuar con ARIA a través del navegador")
            else:
                print(f"⚠️  Servidor responde pero con código: {response.status_code}")
        except requests.exceptions.ConnectionError:
            print("❌ Servidor no está ejecutándose")
            print("💡 Para iniciar: .\\venv\\Scripts\\python.exe asistente_web.py")
        except Exception as e:
            print(f"⚠️  Error verificando servidor: {e}")
            
    except ImportError:
        print("⚠️  Librería requests no disponible para verificación")

def main():
    """Función principal de la demo automática"""
    
    mostrar_banner()
    
    print("🎯 Esta demostración muestra automáticamente cómo funciona")
    print("   el sistema de aprendizaje de ARIA basado en retroalimentación.\n")
    
    # Ejecutar todas las demostraciones automáticamente
    mostrar_archivos_memoria()
    mostrar_estadisticas_completas()
    demostrar_aprendizaje_automatico()
    mostrar_estado_servidor()
    
    print("\n" + "=" * 60)
    print("🎉 DEMOSTRACIÓN COMPLETADA")
    print("=" * 60)
    print("💡 Para usar ARIA interactivamente:")
    print("   🌐 Web: http://localhost:5001")
    print("   🎤 Voz: python asistente_virtual.py") 
    print("   📋 Menú: python menu_asistente.py")
    print("\n👋 ¡ARIA está lista para aprender contigo!")

if __name__ == "__main__":
    main()