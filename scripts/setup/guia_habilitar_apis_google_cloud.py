#!/usr/bin/env python3
"""
🚀 GUÍA PASO A PASO: HABILITAR GOOGLE CLOUD APIS PARA ARIA
========================================================

Tu clave API está configurada correctamente pero necesitas habilitar
los servicios específicos en Google Cloud Console.

Clave API configurada: AIzaSyAS...CiYo ✅
Variable de entorno: GOOGLE_CLOUD_API_KEY ✅

PRÓXIMO PASO: Habilitar las APIs necesarias

Fecha: 22 de octubre de 2025
"""

import webbrowser
import json
from datetime import datetime
from pathlib import Path

class GoogleCloudSetupGuide:
    """Guía interactiva para habilitar APIs de Google Cloud"""
    
    def __init__(self):
        self.api_key = "AIzaSyAS...CiYo"
        self.project_url = None
        
        # APIs que necesita ARIA con sus URLs directas
        self.required_apis = {
            'Translation API': {
                'name': 'Google Cloud Translation API',
                'service': 'translate.googleapis.com',
                'url': 'https://console.cloud.google.com/apis/library/translate.googleapis.com',
                'description': 'Traducción automática entre más de 100 idiomas',
                'free_quota': '500,000 caracteres/mes'
            },
            'Natural Language API': {
                'name': 'Google Cloud Natural Language API', 
                'service': 'language.googleapis.com',
                'url': 'https://console.cloud.google.com/apis/library/language.googleapis.com',
                'description': 'Análisis de sentimientos, entidades y sintaxis',
                'free_quota': '5,000 unidades/mes'
            },
            'Text-to-Speech API': {
                'name': 'Google Cloud Text-to-Speech API',
                'service': 'texttospeech.googleapis.com', 
                'url': 'https://console.cloud.google.com/apis/library/texttospeech.googleapis.com',
                'description': 'Síntesis de voz con más de 380 voces',
                'free_quota': '1 millón de caracteres/mes'
            }
        }
        
        print("🚀 GUÍA INTERACTIVA: HABILITAR GOOGLE CLOUD APIS")
        print("=" * 50)
        print(f"🔑 Tu clave API: {self.api_key}")
        print("📋 Estado: Variables configuradas ✅")
        print("🎯 Objetivo: Habilitar 3 APIs necesarias")
        print()
    
    def show_prerequisites(self):
        """Muestra prerequisitos"""
        print("📋 PREREQUISITOS")
        print("-" * 15)
        print("✅ Clave API de Google Cloud (ya tienes)")
        print("✅ Proyecto de Google Cloud activo")
        print("✅ Facturación habilitada (para cuotas gratuitas)")
        print("✅ Acceso a Google Cloud Console")
        print()
        
        print("💡 INFORMACIÓN IMPORTANTE:")
        print("   • Las APIs tienen cuotas GRATUITAS generosas")
        print("   • No se cobrará automáticamente")
        print("   • Puedes configurar alertas de facturación")
        print("   • ARIA funciona dentro de los límites gratuitos")
        print()
    
    def interactive_setup(self):
        """Configuración interactiva paso a paso"""
        print("🎯 CONFIGURACIÓN PASO A PASO")
        print("-" * 29)
        
        print("Vamos a habilitar las APIs necesarias una por una.")
        print("Para cada API:")
        print("  1. Se abrirá la página en tu navegador")
        print("  2. Haz clic en 'HABILITAR' (ENABLE)")
        print("  3. Espera a que se complete")
        print("  4. Regresa aquí y confirma")
        print()
        
        enabled_apis = []
        
        for api_name, api_info in self.required_apis.items():
            print(f"📚 {api_name}")
            print(f"   {api_info['description']}")
            print(f"   💰 Cuota gratuita: {api_info['free_quota']}")
            print()
            
            choice = input(f"¿Habilitar {api_name}? (s/n): ").lower()
            
            if choice == 's':
                print(f"🌐 Abriendo Google Cloud Console para {api_name}...")
                try:
                    webbrowser.open(api_info['url'])
                    print(f"✅ Página abierta: {api_info['url']}")
                    
                    input("⏳ Presiona ENTER después de habilitar la API...")
                    
                    enabled_apis.append(api_name)
                    print(f"✅ {api_name} marcada como habilitada")
                    
                except Exception as e:
                    print(f"❌ Error abriendo navegador: {e}")
                    print(f"💡 Abre manualmente: {api_info['url']}")
                    
                    manual = input("¿Habilitaste la API manualmente? (s/n): ").lower()
                    if manual == 's':
                        enabled_apis.append(api_name)
            else:
                print(f"⏭️ {api_name} omitida")
            
            print()
        
        return enabled_apis
    
    def verify_apis_enabled(self, enabled_apis: list) -> dict:
        """Verifica que las APIs estén habilitadas"""
        print("🧪 VERIFICANDO APIS HABILITADAS")
        print("-" * 30)
        
        if not enabled_apis:
            print("⚠️ No se habilitaron APIs")
            return {'success': False, 'enabled_count': 0}
        
        print(f"📊 APIs que dijiste habilitar: {len(enabled_apis)}")
        for api in enabled_apis:
            print(f"   ✅ {api}")
        
        print()
        print("🔄 Para verificar automáticamente, ejecutaremos una prueba...")
        
        # Ejecutar verificación automática
        return self._run_api_tests()
    
    def _run_api_tests(self) -> dict:
        """Ejecuta pruebas de APIs"""
        try:
            print("🧪 Ejecutando: python configurar_clave_google_cloud.py")
            
            # Simular resultado (en una implementación real ejecutaríamos el test)
            import subprocess
            import sys
            
            result = subprocess.run([
                sys.executable, 'configurar_clave_google_cloud.py'
            ], capture_output=True, text=True, timeout=60, input='s\n')
            
            if 'COMPLETAMENTE FUNCIONAL' in result.stdout:
                print("✅ Todas las APIs funcionan correctamente")
                return {'success': True, 'enabled_count': 3}
            elif 'MAYORMENTE FUNCIONAL' in result.stdout:
                print("✅ La mayoría de APIs funcionan")
                return {'success': True, 'enabled_count': 2}
            else:
                print("⚠️ Algunas APIs aún no funcionan")
                return {'success': False, 'enabled_count': 1}
                
        except Exception as e:
            print(f"⚠️ Error en verificación automática: {e}")
            print("💡 Procederemos con verificación manual")
            return {'success': False, 'enabled_count': 0}
    
    def show_manual_verification_steps(self):
        """Muestra pasos de verificación manual"""
        print("🔍 VERIFICACIÓN MANUAL")
        print("-" * 21)
        
        print("Si las pruebas automáticas no funcionan, puedes verificar manualmente:")
        print()
        
        print("1. 🧪 Probar Google Cloud APIs:")
        print("   python backend/src/google_cloud_apis.py")
        print()
        
        print("2. 🔄 Probar integración completa:")
        print("   python aria_google_cloud_integration.py")
        print()
        
        print("3. 🚀 Iniciar servidor ARIA completo:")
        print("   python backend/src/main_stable.py")
        print()
        
        print("✅ Si alguno de estos comandos muestra resultados positivos,")
        print("   las APIs están funcionando correctamente.")
    
    def create_completion_summary(self, enabled_apis: list, verification_result: dict):
        """Crea resumen de configuración completada"""
        
        summary = {
            'timestamp': datetime.now().isoformat(),
            'api_key_configured': True,
            'apis_enabled': enabled_apis,
            'apis_count': len(enabled_apis),
            'verification_success': verification_result.get('success', False),
            'estimated_functionality': self._estimate_functionality(enabled_apis),
            'next_steps': self._get_next_steps(enabled_apis, verification_result)
        }
        
        # Mostrar resumen
        print("📊 RESUMEN DE CONFIGURACIÓN")
        print("-" * 25)
        print(f"🔑 Clave API: Configurada ✅")
        print(f"📚 APIs habilitadas: {len(enabled_apis)}/3")
        
        for api in enabled_apis:
            print(f"   ✅ {api}")
        
        functionality = summary['estimated_functionality']
        print(f"🚀 Funcionalidad estimada: {functionality['percentage']}%")
        print(f"💡 Estado: {functionality['status']}")
        
        # Guardar resumen
        self._save_summary(summary)
        
        return summary
    
    def _estimate_functionality(self, enabled_apis: list) -> dict:
        """Estima funcionalidad basada en APIs habilitadas"""
        total_apis = len(self.required_apis)
        enabled_count = len(enabled_apis)
        
        percentage = (enabled_count / total_apis) * 100
        
        if percentage >= 100:
            status = "🎉 COMPLETAMENTE FUNCIONAL"
        elif percentage >= 66:
            status = "✅ MAYORMENTE FUNCIONAL"  
        elif percentage >= 33:
            status = "⚠️ PARCIALMENTE FUNCIONAL"
        else:
            status = "❌ FUNCIONALIDAD LIMITADA"
        
        return {
            'percentage': percentage,
            'status': status,
            'enabled_count': enabled_count,
            'total_count': total_apis
        }
    
    def _get_next_steps(self, enabled_apis: list, verification_result: dict) -> list:
        """Obtiene próximos pasos recomendados"""
        steps = []
        
        if len(enabled_apis) == 3:
            steps = [
                "¡Configuración completa! Probar sistema ARIA",
                "python aria_google_cloud_integration.py",
                "python backend/src/main_stable.py",
                "Explorar funcionalidades avanzadas"
            ]
        elif len(enabled_apis) >= 1:
            steps = [
                "Habilitar APIs restantes para funcionalidad completa",
                "Probar funcionalidades disponibles",
                "python backend/src/google_cloud_apis.py"
            ]
        else:
            steps = [
                "Habilitar al menos Translation API para funcionalidad básica",
                "Revisar configuración de proyecto en Google Cloud",
                "Verificar facturación habilitada"
            ]
        
        return steps
    
    def _save_summary(self, summary: dict):
        """Guarda resumen en archivo"""
        try:
            summary_file = Path(f"google_cloud_setup_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
            
            with open(summary_file, 'w', encoding='utf-8') as f:
                json.dump(summary, f, indent=2, ensure_ascii=False, default=str)
            
            print(f"💾 Resumen guardado: {summary_file}")
            
        except Exception as e:
            print(f"⚠️ Error guardando resumen: {e}")
    
    def run_complete_setup(self):
        """Ejecuta configuración completa"""
        print("🎯 CONFIGURACIÓN INTERACTIVA DE GOOGLE CLOUD PARA ARIA")
        print("=" * 55)
        
        try:
            # Paso 1: Mostrar prerequisitos
            self.show_prerequisites()
            
            # Paso 2: Configuración interactiva
            enabled_apis = self.interactive_setup()
            
            # Paso 3: Verificar APIs
            verification_result = self.verify_apis_enabled(enabled_apis)
            
            # Paso 4: Mostrar verificación manual si es necesario
            if not verification_result.get('success', False):
                self.show_manual_verification_steps()
            
            # Paso 5: Crear resumen
            summary = self.create_completion_summary(enabled_apis, verification_result)
            
            # Paso 6: Mostrar próximos pasos
            print(f"\n🚀 PRÓXIMOS PASOS:")
            for i, step in enumerate(summary['next_steps'], 1):
                print(f"   {i}. {step}")
            
            print(f"\n" + "="*55)
            print(f"🎉 CONFIGURACIÓN DE GOOGLE CLOUD COMPLETADA")
            print(f"   APIs habilitadas: {len(enabled_apis)}/3")
            print(f"   Estado: {summary['estimated_functionality']['status']}")
            print("="*55)
            
            return len(enabled_apis) >= 1
            
        except KeyboardInterrupt:
            print(f"\n⏹️ Configuración interrumpida por el usuario")
            return False
        except Exception as e:
            print(f"\n❌ Error durante configuración: {e}")
            return False

def main():
    """Función principal"""
    guide = GoogleCloudSetupGuide()
    
    print("🎯 Esta guía te ayudará a:")
    print("   • Habilitar Google Cloud APIs necesarias")
    print("   • Verificar que funcionan correctamente")  
    print("   • Integrar con tu sistema ARIA")
    print("   • Activar funcionalidades premium")
    print()
    
    choice = input("¿Comenzar configuración interactiva? (s/n): ").lower()
    
    if choice == 's':
        success = guide.run_complete_setup()
        
        if success:
            print("\n🎉 ¡Configuración exitosa!")
            print("💡 Tu sistema ARIA ahora puede usar Google Cloud APIs")
        else:
            print("\n💡 Configuración pausada")
            print("   Puedes continuarla en cualquier momento")
            
        return success
    else:
        print("👋 Configuración postponed")
        print("💡 Ejecutar cuando estés listo: python guia_habilitar_apis_google_cloud.py")
        return False

if __name__ == "__main__":
    main()