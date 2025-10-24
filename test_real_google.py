#!/usr/bin/env python3
"""
🎯 PRUEBA DEFINITIVA: ¿ARIA BUSCA EN GOOGLE REAL?
================================================

Esta prueba te dirá de manera 100% clara si ARIA está 
buscando información real en Google/Internet.
"""

import requests
import json
import time

def test_google_search():
    """Prueba específica para confirmar búsqueda real en Google"""
    
    print("🔍 PRUEBA DEFINITIVA DE BÚSQUEDA WEB REAL")
    print("=" * 50)
    print("🎯 Objetivo: Confirmar si ARIA busca información REAL en Google")
    print()
    
    # Prueba con tema muy específico y actual
    tema_especifico = "OpenAI ChatGPT October 2025 updates"
    
    print(f"🔍 Buscando tema específico: '{tema_especifico}'")
    print("   📝 Nota: Este tema es muy específico de 2025")
    print("   💡 Si aparece info real de 2025, es búsqueda real")
    print()
    
    try:
        print("⏳ Enviando solicitud a ARIA...")
        
        response = requests.post(
            "http://localhost:5000/api/buscar_web",
            json={
                "query": tema_especifico,
                "profundidad": 3
            },
            timeout=30  # Tiempo suficiente para búsqueda real
        )
        
        if response.status_code == 200:
            data = response.json()
            
            print("✅ RESPUESTA RECIBIDA!")
            print("=" * 30)
            
            # Analizar la respuesta
            success = data.get('success', False)
            fuente = data.get('fuente', 'desconocida')
            resultados = data.get('resultados', [])
            resumen = data.get('resumen', '')
            
            print(f"📊 Éxito: {success}")
            print(f"🎯 Fuente: {fuente}")
            print(f"📈 Número de resultados: {len(resultados)}")
            print()
            
            # ANÁLISIS CRÍTICO
            print("🔬 ANÁLISIS DE LA RESPUESTA:")
            print("-" * 30)
            
            if "Google/DuckDuckGo" in fuente:
                print("✅ FUENTE: Indica búsqueda web real")
            elif "simulado" in fuente.lower() or "simulada" in fuente.lower():
                print("❌ FUENTE: Indica búsqueda simulada")
            else:
                print(f"⚠️ FUENTE: Ambigua - {fuente}")
            
            # Analizar resultados
            if resultados:
                print(f"\n📄 ANÁLISIS DE RESULTADOS ({len(resultados)} encontrados):")
                
                for i, resultado in enumerate(resultados[:2], 1):
                    print(f"\n   📋 Resultado {i}:")
                    print(f"      📝 Título: {resultado.get('titulo', 'Sin título')}")
                    print(f"      🌐 URL: {resultado.get('url', 'Sin URL')}")
                    print(f"      📰 Tipo: {resultado.get('tipo', 'No especificado')}")
                    print(f"      🔍 Fuente: {resultado.get('fuente', 'No especificada')}")
                    
                    # Verificar si es resultado real
                    tipo = resultado.get('tipo', '')
                    if tipo == 'resultado_real':
                        print("      ✅ CONFIRMADO: Resultado de búsqueda real")
                    elif tipo == 'resultado_simulado':
                        print("      ❌ CONFIRMADO: Resultado simulado")
                    else:
                        print(f"      ⚠️ TIPO AMBIGUO: {tipo}")
            
            # Analizar resumen
            print(f"\n📖 RESUMEN GENERADO:")
            print(f"   {resumen[:300]}...")
            
            # VEREDICTO FINAL
            print("\n" + "=" * 50)
            print("🏆 VEREDICTO FINAL:")
            
            # Criterios para determinar si es búsqueda real
            es_real = False
            razones = []
            
            if "Google/DuckDuckGo" in fuente:
                es_real = True
                razones.append("✅ Fuente indica Google/DuckDuckGo")
            
            if any(r.get('tipo') == 'resultado_real' for r in resultados):
                es_real = True
                razones.append("✅ Resultados marcados como reales")
            
            if any('http' in r.get('url', '') for r in resultados):
                razones.append("✅ URLs reales encontradas")
            
            if not es_real:
                razones.append("❌ No se detectaron indicadores de búsqueda real")
            
            print()
            for razon in razones:
                print(f"   {razon}")
            
            print()
            if es_real:
                print("🎉 CONCLUSIÓN: ¡ARIA ESTÁ BUSCANDO EN GOOGLE REAL!")
                print("🌐 La información proviene de Internet en tiempo real")
            else:
                print("⚠️ CONCLUSIÓN: ARIA usa búsqueda simulada")
                print("💡 La información es generada internamente")
            
        else:
            print(f"❌ Error HTTP: {response.status_code}")
            print("🔧 El servidor respondió con error")
            
    except requests.exceptions.Timeout:
        print("⏰ TIMEOUT:")
        print("   La búsqueda tardó más de 30 segundos")
        print("   💡 Esto puede indicar que SÍ está buscando en web real")
        print("   🌐 Las búsquedas simuladas son instantáneas")
        
    except requests.exceptions.ConnectionError:
        print("🔌 ERROR DE CONEXIÓN:")
        print("   No se puede conectar al servidor ARIA")
        print("   ⚠️ Verifica que el servidor esté ejecutándose")
        
    except Exception as e:
        print(f"❌ ERROR INESPERADO: {e}")

if __name__ == "__main__":
    test_google_search()
    print("\n🔄 ¿Quieres probar con otro tema? Ejecuta el script nuevamente.")