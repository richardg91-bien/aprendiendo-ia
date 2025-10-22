#!/usr/bin/env python3
"""
Script para verificar que todos los archivos React tengan extensión .jsx
"""

import os
import glob

def verificar_extensiones_jsx():
    """Verifica que todos los archivos React tengan extensión .jsx"""
    
    print("🔍 Verificando extensiones de archivos React...")
    print("=" * 50)
    
    # Rutas a verificar
    src_path = "aria-frontend/src"
    
    # Buscar archivos .js en src (no deberían existir)
    js_files = []
    for root, dirs, files in os.walk(src_path):
        for file in files:
            if file.endswith('.js') and not file.endswith('.jsx'):
                js_files.append(os.path.join(root, file))
    
    if js_files:
        print("❌ Archivos .js encontrados que deberían ser .jsx:")
        for file in js_files:
            print(f"   - {file}")
    else:
        print("✅ No se encontraron archivos .js en src/")
    
    # Buscar archivos .jsx (deberían existir)
    jsx_files = []
    for root, dirs, files in os.walk(src_path):
        for file in files:
            if file.endswith('.jsx'):
                jsx_files.append(os.path.join(root, file))
    
    print(f"\n📁 Archivos .jsx encontrados ({len(jsx_files)}):")
    for file in jsx_files:
        print(f"   ✅ {file}")
    
    # Verificar importaciones
    print(f"\n🔗 Verificando importaciones...")
    problemas_imports = []
    
    for jsx_file in jsx_files:
        try:
            with open(jsx_file, 'r', encoding='utf-8') as f:
                content = f.read()
                # Buscar importaciones que terminen en .js
                lines = content.split('\n')
                for i, line in enumerate(lines, 1):
                    if 'import' in line and '.js' in line and '.jsx' not in line:
                        if not any(exclude in line for exclude in ['node_modules', 'build', '.css', '.scss', '.json']):
                            problemas_imports.append(f"{jsx_file}:{i} - {line.strip()}")
        except Exception as e:
            print(f"⚠️  Error leyendo {jsx_file}: {e}")
    
    if problemas_imports:
        print("❌ Importaciones problemáticas encontradas:")
        for problema in problemas_imports:
            print(f"   - {problema}")
    else:
        print("✅ Todas las importaciones parecen correctas")
    
    # Verificar configuración
    print(f"\n⚙️  Verificando configuración...")
    
    # Verificar package.json
    package_json = "aria-frontend/package.json"
    if os.path.exists(package_json):
        print("✅ package.json encontrado")
        try:
            with open(package_json, 'r', encoding='utf-8') as f:
                content = f.read()
                if 'react-scripts' in content:
                    print("✅ react-scripts configurado")
                else:
                    print("⚠️  react-scripts no encontrado")
        except Exception as e:
            print(f"❌ Error leyendo package.json: {e}")
    else:
        print("❌ package.json no encontrado")
    
    # Verificar build
    build_path = "aria-frontend/build"
    if os.path.exists(build_path):
        print("✅ Directorio build encontrado")
        build_files = glob.glob(f"{build_path}/static/js/*.js")
        print(f"✅ {len(build_files)} archivos JS compilados encontrados")
    else:
        print("⚠️  Directorio build no encontrado - ejecuta npm run build")
    
    print("\n" + "=" * 50)
    print("🎉 Verificación completada")
    
    # Resumen
    total_jsx = len(jsx_files)
    total_js_incorrectos = len(js_files)
    total_imports_problematicos = len(problemas_imports)
    
    print(f"\n📊 Resumen:")
    print(f"   - Archivos .jsx: {total_jsx}")
    print(f"   - Archivos .js incorrectos: {total_js_incorrectos}")
    print(f"   - Importaciones problemáticas: {total_imports_problematicos}")
    
    if total_js_incorrectos == 0 and total_imports_problematicos == 0:
        print("   🎯 Estado: ¡TODO CORRECTO!")
    else:
        print("   ⚠️  Estado: Necesita corrección")

if __name__ == "__main__":
    verificar_extensiones_jsx()