#!/usr/bin/env python3
"""
🧪 PRUEBA DEL SISTEMA EMOCIONAL CON SUPABASE
==========================================

Script para probar el nuevo detector de emociones que usa Supabase
"""

import json
from datetime import datetime

try:
    from emotion_detector_supabase import (
        init_emotion_detector_supabase, 
        detect_user_emotion_supabase,
        detect_aria_emotion_supabase,
        get_emotion_stats_supabase
    )
    EMOTION_SUPABASE_AVAILABLE = True
except ImportError as e:
    print(f"❌ Error importando sistema emocional Supabase: {e}")
    EMOTION_SUPABASE_AVAILABLE = False

def test_emotion_initialization():
    """Probar la inicialización del sistema emocional"""
    
    print("🔧 PROBANDO INICIALIZACIÓN DEL SISTEMA EMOCIONAL")
    print("=" * 55)
    
    if not EMOTION_SUPABASE_AVAILABLE:
        print("❌ Sistema emocional Supabase no disponible")
        return False
    
    try:
        # Inicializar sin API key (modo fallback)
        detector = init_emotion_detector_supabase("")
        
        if detector:
            print("✅ Detector inicializado correctamente")
            
            # Mostrar emociones disponibles
            emotions = detector.get_available_emotions()
            print(f"📊 Emociones disponibles: {len(emotions)}")
            
            # Mostrar algunas emociones
            for i, emotion in enumerate(emotions[:5]):
                print(f"   {i+1}. {emotion['name']} ({emotion['key']}) - {emotion['color']}")
            
            if len(emotions) > 5:
                print(f"   ... y {len(emotions) - 5} más")
            
            return True
        else:
            print("❌ Error inicializando detector")
            return False
            
    except Exception as e:
        print(f"❌ Error en inicialización: {e}")
        return False

def test_emotion_detection():
    """Probar detección de emociones"""
    
    print("\n🎭 PROBANDO DETECCIÓN DE EMOCIONES")
    print("=" * 40)
    
    if not EMOTION_SUPABASE_AVAILABLE:
        print("❌ Sistema no disponible")
        return False
    
    # Textos de prueba con diferentes emociones
    test_texts = [
        ("¡Estoy muy feliz!", "joy"),
        ("Me siento triste hoy", "sadness"),
        ("¡Esto es increíble!", "excitement"),
        ("¿Cómo funciona esto?", "curiosity"),
        ("Quiero aprender más", "learning"),
        ("No entiendo nada", "confusion"),
        ("Gracias por tu ayuda", "satisfaction"),
        ("¿Qué es la inteligencia artificial?", "curiosity"),
        ("Hola ARIA", "neutral"),
        ("Esto está mal", "anger")
    ]
    
    print("🔍 Analizando textos de prueba:")
    
    for i, (text, expected) in enumerate(test_texts, 1):
        try:
            print(f"\n{i:2d}. Texto: '{text}'")
            
            # Detectar emoción
            result = detect_user_emotion_supabase(text)
            
            if result.get('success'):
                emotion = result.get('emotion', 'unknown')
                name = result.get('emotion_name', 'Desconocida')
                color = result.get('color', '#000000')
                confidence = result.get('confidence', 0)
                provider = result.get('provider', 'unknown')
                source = result.get('source', 'unknown')
                
                print(f"    🎨 Emoción: {name} ({emotion})")
                print(f"    📊 Confianza: {confidence:.2f}")
                print(f"    🎯 Color: {color}")
                print(f"    🔧 Proveedor: {provider}")
                print(f"    🗄️ Fuente: {source}")
                
                # Verificar si coincide con lo esperado
                if emotion in expected or expected in emotion:
                    print("    ✅ Detección esperada")
                else:
                    print(f"    ⚠️ Esperada: {expected}, Obtenida: {emotion}")
            else:
                print("    ❌ Error en detección")
                
        except Exception as e:
            print(f"    ❌ Error: {e}")

def test_aria_emotions():
    """Probar emociones específicas de ARIA"""
    
    print("\n🤖 PROBANDO EMOCIONES DE ARIA")
    print("=" * 35)
    
    aria_responses = [
        "Estoy aprendiendo mucho contigo",
        "Me alegra poder ayudarte",
        "No estoy segura de entender eso",
        "¡Qué interesante pregunta!",
        "Lo siento, no pude encontrar esa información"
    ]
    
    for i, response in enumerate(aria_responses, 1):
        try:
            print(f"\n{i}. Respuesta ARIA: '{response}'")
            
            result = detect_aria_emotion_supabase(response)
            
            if result.get('success'):
                emotion_name = result.get('emotion_name', 'Desconocida')
                color = result.get('color', '#000000')
                rgb = result.get('rgb', '0,0,0')
                
                print(f"   🎭 Emoción ARIA: {emotion_name}")
                print(f"   🎨 Color HEX: {color}")
                print(f"   🌈 Color RGB: {rgb}")
            else:
                print("   ❌ Error detectando emoción de ARIA")
                
        except Exception as e:
            print(f"   ❌ Error: {e}")

def test_emotion_stats():
    """Probar estadísticas del sistema emocional"""
    
    print("\n📊 ESTADÍSTICAS DEL SISTEMA EMOCIONAL")
    print("=" * 42)
    
    try:
        stats = get_emotion_stats_supabase()
        
        if 'error' not in stats:
            print("✅ Estadísticas obtenidas correctamente:")
            print(f"   📚 Emociones disponibles: {stats.get('emotions_available', 0)}")
            print(f"   📝 Entradas de historial: {stats.get('emotion_history_entries', 0)}")
            print(f"   ⚙️ Configuraciones: {stats.get('config_entries', 0)}")
            print(f"   🗄️ Estado Supabase: {stats.get('supabase_status', 'unknown')}")
            print(f"   💾 Cache cargado: {stats.get('cache_loaded', 0)} emociones")
        else:
            print(f"❌ Error obteniendo estadísticas: {stats['error']}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

def test_specific_emotions():
    """Probar emociones específicas que sabemos que están en Supabase"""
    
    print("\n🎯 PROBANDO EMOCIONES ESPECÍFICAS DE SUPABASE")
    print("=" * 50)
    
    # Emociones que sabemos que migramos
    specific_tests = [
        ("Roma me encanta", "joy"),  # Debería activar alegría
        ("No encuentro información", "sadness"),  # Debería activar tristeza
        ("¿Qué puedes hacer?", "curiosity"),  # Debería activar curiosidad
        ("Enséñame sobre inteligencia artificial", "learning"),  # Debería activar aprendizaje
        ("hola", "neutral")  # Debería ser neutral
    ]
    
    print("🔍 Probando emociones migradas desde local:")
    
    for i, (text, expected_category) in enumerate(specific_tests, 1):
        try:
            print(f"\n{i}. Test específico: '{text}'")
            
            result = detect_user_emotion_supabase(text)
            
            if result.get('success'):
                # Mostrar información completa
                print(f"   🎭 Emoción detectada: {result.get('emotion_name', 'N/A')}")
                print(f"   🔧 Emoción interna: {result.get('emotion', 'N/A')}")
                print(f"   🎨 Color: {result.get('color', 'N/A')}")
                print(f"   📊 Confianza: {result.get('confidence', 0):.2f}")
                print(f"   🌐 Proveedor: {result.get('provider', 'N/A')}")
                print(f"   📍 Fuente: {result.get('source', 'N/A')}")
                
                # Verificar que viene de Supabase
                if result.get('source') == 'supabase':
                    print("   ✅ Datos cargados desde Supabase")
                else:
                    print("   ⚠️ No viene de Supabase")
                    
            else:
                print("   ❌ Error en detección")
                
        except Exception as e:
            print(f"   ❌ Error: {e}")

def main():
    """Función principal de pruebas"""
    
    print("🚀 PRUEBA COMPLETA DEL SISTEMA EMOCIONAL SUPABASE")
    print("=" * 60)
    print(f"🕒 Inicio de pruebas: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Ejecutar todas las pruebas
    tests = [
        ("Inicialización", test_emotion_initialization),
        ("Detección General", test_emotion_detection),
        ("Emociones ARIA", test_aria_emotions),
        ("Estadísticas", test_emotion_stats),
        ("Emociones Específicas", test_specific_emotions)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            print(f"\n{'='*20} {test_name.upper()} {'='*20}")
            success = test_func()
            results.append((test_name, success))
        except Exception as e:
            print(f"❌ Error en prueba {test_name}: {e}")
            results.append((test_name, False))
    
    # Resumen final
    print("\n" + "="*60)
    print("📊 RESUMEN DE PRUEBAS")
    print("="*60)
    
    passed = 0
    for test_name, success in results:
        status = "✅ PASSED" if success else "❌ FAILED"
        print(f"   {status}: {test_name}")
        if success:
            passed += 1
    
    print(f"\n🎯 Resultado: {passed}/{len(results)} pruebas exitosas")
    
    if passed == len(results):
        print("🎉 ¡TODAS LAS PRUEBAS EXITOSAS!")
        print("✅ El sistema emocional con Supabase está funcionando correctamente")
    else:
        print("⚠️ Algunas pruebas fallaron")
        print("🔧 Revisa la configuración del sistema emocional")
    
    print(f"\n🕒 Fin de pruebas: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    main()