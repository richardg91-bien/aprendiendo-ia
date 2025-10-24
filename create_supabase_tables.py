#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🗄️ Creador de Tablas Supabase via API
=====================================

Crea las tablas de ARIA en Supabase usando la API REST
cuando no podemos usar la conexión directa a PostgreSQL.

Fecha: 23 de octubre de 2025
"""

import os
import requests
import json
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

def create_tables_via_api():
    """Crear tablas usando la API de Supabase"""
    
    supabase_url = os.getenv('SUPABASE_URL')
    supabase_key = os.getenv('SUPABASE_ANON_KEY')
    
    if not supabase_url or not supabase_key:
        print("❌ Variables de Supabase no configuradas")
        return False
    
    print("🗄️ Creando tablas de ARIA en Supabase via API...")
    
    # Headers para las requests
    headers = {
        'apikey': supabase_key,
        'Authorization': f'Bearer {supabase_key}',
        'Content-Type': 'application/json',
        'Prefer': 'return=minimal'
    }
    
    # Crear datos de ejemplo para inicializar las tablas
    # (las tablas se crean automáticamente cuando insertamos datos)
    
    # 1. Tabla aria_knowledge
    knowledge_data = [
        {
            'concept': 'saludo',
            'description': 'Forma de iniciar una conversación de manera amigable',
            'category': 'social',
            'confidence': 0.9,
            'source': 'system_init'
        },
        {
            'concept': 'inteligencia_artificial',
            'description': 'Campo de la informática que busca crear sistemas que puedan realizar tareas que requieren inteligencia humana',
            'category': 'tecnologia',
            'confidence': 0.9,
            'source': 'system_init'
        },
        {
            'concept': 'python',
            'description': 'Lenguaje de programación de alto nivel, interpretado y de propósito general',
            'category': 'programacion',
            'confidence': 0.9,
            'source': 'system_init'
        }
    ]
    
    # Intentar crear tabla de conocimiento
    try:
        url = f"{supabase_url}/rest/v1/aria_knowledge"
        response = requests.post(url, headers=headers, json=knowledge_data)
        
        if response.status_code in [200, 201]:
            print("✅ Tabla aria_knowledge creada/inicializada")
        else:
            print(f"⚠️ Error creando aria_knowledge: {response.status_code}")
            print(f"Detalle: {response.text}")
            
    except Exception as e:
        print(f"❌ Error con aria_knowledge: {e}")
    
    # 2. Tabla aria_conversations
    conversation_data = [
        {
            'session_id': 'init_session',
            'user_input': 'Hola ARIA',
            'aria_response': '¡Hola! Bienvenido a ARIA. Sistema inicializado correctamente.',
            'response_time': 0.1
        }
    ]
    
    try:
        url = f"{supabase_url}/rest/v1/aria_conversations"
        response = requests.post(url, headers=headers, json=conversation_data)
        
        if response.status_code in [200, 201]:
            print("✅ Tabla aria_conversations creada/inicializada")
        else:
            print(f"⚠️ Error creando aria_conversations: {response.status_code}")
            print(f"Detalle: {response.text}")
            
    except Exception as e:
        print(f"❌ Error con aria_conversations: {e}")
    
    # 3. Verificar que las tablas existen
    try:
        # Test: obtener datos de conocimiento
        url = f"{supabase_url}/rest/v1/aria_knowledge?select=*&limit=1"
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Verificación exitosa: {len(data)} registros encontrados")
            return True
        else:
            print(f"❌ Error verificando tablas: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error verificando: {e}")
        return False

def test_supabase_connection():
    """Probar la conexión a Supabase"""
    
    supabase_url = os.getenv('SUPABASE_URL')
    supabase_key = os.getenv('SUPABASE_ANON_KEY')
    
    print("🔍 Probando conexión a Supabase...")
    print(f"URL: {supabase_url}")
    print(f"Key: {supabase_key[:20]}..." if supabase_key else "Key: No configurada")
    
    headers = {
        'apikey': supabase_key,
        'Authorization': f'Bearer {supabase_key}'
    }
    
    try:
        # Probar endpoint de health check
        url = f"{supabase_url}/rest/v1/"
        response = requests.get(url, headers=headers)
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text[:200]}...")
        
        if response.status_code == 200:
            print("✅ Conexión a Supabase exitosa")
            return True
        else:
            print("❌ Error de conexión")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def show_manual_instructions():
    """Mostrar instrucciones manuales"""
    
    print("\n" + "="*60)
    print("📋 INSTRUCCIONES MANUALES PARA SUPABASE")
    print("="*60)
    print("\n1. Ve a tu dashboard de Supabase:")
    print("   https://supabase.com/dashboard")
    
    print("\n2. Selecciona tu proyecto")
    
    print("\n3. Ve a 'SQL Editor' en el menú lateral")
    
    print("\n4. Crea una nueva query y pega el siguiente SQL:")
    print("\n" + "-"*40)
    
    sql_content = """-- Crear tabla de conocimiento
CREATE TABLE IF NOT EXISTS public.aria_knowledge (
    id SERIAL PRIMARY KEY,
    concept VARCHAR(255) UNIQUE NOT NULL,
    description TEXT,
    category VARCHAR(100) DEFAULT 'general',
    confidence REAL DEFAULT 0.5,
    source VARCHAR(255) DEFAULT 'conversation',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Crear tabla de conversaciones  
CREATE TABLE IF NOT EXISTS public.aria_conversations (
    id SERIAL PRIMARY KEY,
    session_id VARCHAR(255) NOT NULL,
    user_input TEXT NOT NULL,
    aria_response TEXT NOT NULL,
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    response_time REAL DEFAULT 0
);

-- Insertar datos de ejemplo
INSERT INTO public.aria_knowledge (concept, description, category, confidence) VALUES
('saludo', 'Forma de iniciar una conversación', 'social', 0.9),
('inteligencia_artificial', 'IA y sistemas inteligentes', 'tecnologia', 0.9)
ON CONFLICT (concept) DO NOTHING;"""
    
    print(sql_content)
    print("-"*40)
    
    print("\n5. Ejecuta la query (botón RUN)")
    
    print("\n6. Verifica que las tablas se crearon en 'Table Editor'")
    
    print("\n7. Una vez creadas, ejecuta de nuevo:")
    print("   python aria_integrated_server.py")
    
    print("\n" + "="*60)

def main():
    """Función principal"""
    
    print("🗄️ ARIA SUPABASE TABLE CREATOR")
    print("="*40)
    
    # Probar conexión
    if test_supabase_connection():
        # Intentar crear tablas via API
        if create_tables_via_api():
            print("\n✅ ¡Tablas creadas exitosamente!")
            print("🚀 Ahora puedes ejecutar aria_integrated_server.py")
        else:
            print("\n⚠️ No se pudieron crear todas las tablas via API")
            show_manual_instructions()
    else:
        print("\n❌ No se pudo conectar a Supabase")
        show_manual_instructions()

if __name__ == "__main__":
    main()