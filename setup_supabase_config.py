#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Configurador de credenciales de Supabase
"""

import os

def setup_supabase_credentials():
    print("🔧 CONFIGURADOR DE SUPABASE")
    print("=" * 40)
    
    # Buscar credenciales en archivos existentes
    config_files = [
        'src/aria_servidor_superbase.py',
        'src/core/aria_embeddings_supabase.py',
        'main.py'
    ]
    
    print("\n🔍 Buscando credenciales existentes...")
    
    for file_path in config_files:
        if os.path.exists(file_path):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                # Buscar URLs de Supabase
                if 'supabase.co' in content.lower():
                    lines = content.split('\n')
                    for i, line in enumerate(lines):
                        if 'supabase.co' in line.lower():
                            print(f"📄 {file_path}:{i+1}: {line.strip()}")
                            
                # Buscar claves
                if 'eyJ' in content:  # Típico inicio de JWT tokens
                    lines = content.split('\n')
                    for i, line in enumerate(lines):
                        if 'eyJ' in line and len(line) > 50:
                            key_preview = line[:50] + "..."
                            print(f"🔑 {file_path}:{i+1}: {key_preview}")
                            
            except Exception as e:
                print(f"⚠️ Error leyendo {file_path}: {e}")
    
    print("\n" + "=" * 40)
    print("📋 INSTRUCCIONES:")
    print("1. Ve a tu proyecto Supabase")
    print("2. Settings > API")
    print("3. Copia Project URL y anon/public key")
    print("4. Ejecuta este script de nuevo para continuar")

if __name__ == "__main__":
    setup_supabase_credentials()