"""
🤖 ARIA - Verificación Final del Sistema Completo
================================================

Verifica que todo el sistema esté configurado correctamente
"""

import os
import requests
import json
from datetime import datetime

def check_desktop_shortcut():
    """Verifica el acceso directo en el escritorio"""
    desktop_path = os.path.expanduser("~/OneDrive/Desktop")
    shortcut_path = os.path.join(desktop_path, "ARIA Asistente IA.lnk")
    
    if os.path.exists(shortcut_path):
        print("✅ Acceso directo encontrado en el escritorio")
        print(f"   📁 Ubicación: {shortcut_path}")
        return True
    else:
        print("❌ Acceso directo no encontrado")
        return False

def check_icon_files():
    """Verifica los archivos de iconos"""
    icon_files = [
        "aria_icon.ico",
        "aria_icon_premium.ico",
        "aria_icon_premium.png",
        "aria_icon_premium_multi.ico"
    ]
    
    found_icons = []
    for icon in icon_files:
        if os.path.exists(icon):
            size = os.path.getsize(icon)
            found_icons.append(f"   ✅ {icon} ({size:,} bytes)")
        else:
            found_icons.append(f"   ❌ {icon} (no encontrado)")
    
    print("🎨 Archivos de iconos:")
    for icon_status in found_icons:
        print(icon_status)
    
    return len([i for i in found_icons if "✅" in i])

def check_system_status():
    """Verifica el estado del sistema backend"""
    try:
        response = requests.get("http://localhost:8000/api/status", timeout=5)
        if response.status_code == 200:
            print("✅ Backend Flask funcionando (puerto 8000)")
            return True
        else:
            print(f"⚠️ Backend responde con código: {response.status_code}")
            return False
    except requests.exceptions.RequestException:
        print("❌ Backend no accesible (¿está ejecutándose?)")
        return False

def check_auto_learning_system():
    """Verifica el sistema de aprendizaje autónomo"""
    try:
        response = requests.get("http://localhost:8000/api/auto_learning/status", timeout=5)
        if response.status_code == 200:
            data = response.json()
            status = data.get('status', {})
            
            print("🧠 Sistema de Aprendizaje Autónomo:")
            print(f"   • Estado: {'🟢 ACTIVO' if status.get('is_running') else '🔴 DETENIDO'}")
            print(f"   • Conocimiento total: {status.get('knowledge_stats', {}).get('total_knowledge', 0)}")
            print(f"   • Áreas especializadas: {status.get('knowledge_stats', {}).get('unique_topics', 0)}")
            print(f"   • Confianza promedio: {status.get('knowledge_stats', {}).get('avg_confidence', 0):.2%}")
            print(f"   • Temas activos: {status.get('active_topics', 0)}")
            
            return status.get('is_running', False)
        else:
            print("❌ Sistema de aprendizaje no accesible")
            return False
    except requests.exceptions.RequestException:
        print("❌ Sistema de aprendizaje no responde")
        return False

def check_frontend_access():
    """Verifica acceso al frontend"""
    # Probar ambos puertos
    ports = [3000, 3001]
    
    for port in ports:
        try:
            response = requests.get(f"http://localhost:{port}", timeout=5)
            if response.status_code == 200:
                print(f"✅ Frontend React accesible (puerto {port})")
                return True
        except requests.exceptions.RequestException:
            continue
    
    print("❌ Frontend no accesible en puertos 3000 o 3001")
    return False

def run_full_verification():
    """Ejecuta verificación completa del sistema"""
    
    print("🤖 ARIA - VERIFICACIÓN FINAL DEL SISTEMA")
    print("=" * 50)
    print(f"📅 Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Contadores de éxito
    checks_passed = 0
    total_checks = 5
    
    # 1. Verificar acceso directo
    print("1️⃣ VERIFICANDO ACCESO DIRECTO DEL ESCRITORIO...")
    if check_desktop_shortcut():
        checks_passed += 1
    print()
    
    # 2. Verificar iconos
    print("2️⃣ VERIFICANDO ARCHIVOS DE ICONOS...")
    icons_found = check_icon_files()
    if icons_found >= 3:  # Al menos 3 iconos
        checks_passed += 1
    print()
    
    # 3. Verificar backend
    print("3️⃣ VERIFICANDO BACKEND FLASK...")
    if check_system_status():
        checks_passed += 1
    print()
    
    # 4. Verificar sistema de aprendizaje
    print("4️⃣ VERIFICANDO SISTEMA DE APRENDIZAJE AUTÓNOMO...")
    if check_auto_learning_system():
        checks_passed += 1
    print()
    
    # 5. Verificar frontend
    print("5️⃣ VERIFICANDO FRONTEND REACT...")
    if check_frontend_access():
        checks_passed += 1
    print()
    
    # Resultado final
    print("📊 RESULTADO FINAL")
    print("=" * 30)
    print(f"✅ Verificaciones pasadas: {checks_passed}/{total_checks}")
    
    if checks_passed == total_checks:
        print("🎉 ¡SISTEMA COMPLETAMENTE FUNCIONAL!")
        print("💡 Todo está listo para usar ARIA")
        print()
        print("🚀 CÓMO USAR:")
        print("   1. Hacer doble clic en 'ARIA Asistente IA' del escritorio")
        print("   2. Esperar que carguen los servicios")
        print("   3. Acceder a http://localhost:3000")
        print("   4. ¡Disfrutar del sistema futurista!")
        
    elif checks_passed >= 3:
        print("⚠️ SISTEMA PARCIALMENTE FUNCIONAL")
        print("💡 Algunos componentes pueden necesitar ser iniciados manualmente")
        
    else:
        print("❌ SISTEMA CON PROBLEMAS")
        print("💡 Revisar configuración y dependencias")
    
    print()
    print("🔗 ENLACES ÚTILES:")
    print("   • Frontend: http://localhost:3001 (o http://localhost:3000)")
    print("   • Backend:  http://localhost:8000")
    print("   • API Status: http://localhost:8000/api/auto_learning/status")
    print()

if __name__ == "__main__":
    run_full_verification()