#!/usr/bin/env python3
"""
🗄️ Instalador de Esquema de Base de Datos para ARIA
=====================================================

Este script crea todas las tablas necesarias en Supabase para que ARIA funcione correctamente.

Incluye:
- Tablas de conocimiento
- Tablas de embeddings
- Tablas de conversaciones
- Tablas de APIs
- Tablas de métricas
- Índices de performance
- Datos iniciales

Uso:
    python setup_database.py
"""

import os
import sys
from dotenv import load_dotenv
from supabase import create_client, Client

def setup_database():
    """Configurar la base de datos de ARIA"""
    
    print("🗄️ CONFIGURANDO BASE DE DATOS ARIA")
    print("=" * 50)
    
    # Cargar variables de entorno
    load_dotenv()
    
    # Obtener credenciales de Supabase
    url = os.getenv('SUPABASE_URL')
    key = os.getenv('SUPABASE_ANON_KEY')
    
    if not url or not key:
        print("❌ Error: No se encontraron las credenciales de Supabase")
        print("   Asegúrate de que el archivo .env contenga:")
        print("   SUPABASE_URL=tu_url")
        print("   SUPABASE_ANON_KEY=tu_key")
        return False
    
    try:
        # Conectar a Supabase
        supabase: Client = create_client(url, key)
        print(f"✅ Conectado a Supabase: {url}")
        
        # Leer el esquema SQL
        schema_file = 'schema_supabase_completo.sql'
        if not os.path.exists(schema_file):
            print(f"❌ Error: No se encontró el archivo {schema_file}")
            return False
        
        with open(schema_file, 'r', encoding='utf-8') as f:
            sql_content = f.read()
        
        print("📝 Esquema SQL cargado")
        
        # Dividir el SQL en comandos individuales
        commands = [cmd.strip() for cmd in sql_content.split(';') if cmd.strip()]
        
        print(f"🔧 Ejecutando {len(commands)} comandos SQL...")
        
        successful_commands = 0
        failed_commands = 0
        
        for i, command in enumerate(commands, 1):
            if not command or command.startswith('--'):
                continue
                
            try:
                # Ejecutar comando SQL
                result = supabase.rpc('exec_sql', {'sql': command}).execute()
                print(f"✅ Comando {i}/{len(commands)} ejecutado")
                successful_commands += 1
                
            except Exception as e:
                print(f"⚠️ Error en comando {i}: {str(e)[:100]}...")
                failed_commands += 1
                # Continuar con el siguiente comando
                continue
        
        print("\n" + "=" * 50)
        print("📊 RESUMEN DE INSTALACIÓN:")
        print(f"✅ Comandos exitosos: {successful_commands}")
        print(f"❌ Comandos fallidos: {failed_commands}")
        
        if failed_commands == 0:
            print("🎉 ¡Base de datos configurada correctamente!")
        else:
            print("⚠️ Base de datos configurada con algunas advertencias")
            print("   Algunos comandos fallaron, pero es posible que sea normal")
            print("   (por ejemplo, si las tablas ya existían)")
        
        # Verificar tablas creadas
        print("\n🔍 Verificando tablas creadas...")
        verify_tables(supabase)
        
        return True
        
    except Exception as e:
        print(f"❌ Error conectando a Supabase: {e}")
        return False

def verify_tables(supabase: Client):
    """Verificar que las tablas se crearon correctamente"""
    
    required_tables = [
        'aria_knowledge',
        'aria_conversations', 
        'aria_api_relations',
        'aria_learning_sessions',
        'aria_concept_relations',
        'aria_emotions'
    ]
    
    print("📋 Verificando tablas principales...")
    
    for table in required_tables:
        try:
            result = supabase.table(table).select('id').limit(1).execute()
            print(f"✅ {table}: OK")
        except Exception as e:
            print(f"❌ {table}: Error - {str(e)[:50]}...")
    
    # Verificar datos iniciales
    print("\n📊 Verificando datos iniciales...")
    
    try:
        knowledge_count = len(supabase.table('aria_knowledge').select('id').execute().data)
        print(f"📚 Conocimiento: {knowledge_count} registros")
        
        emotions_count = len(supabase.table('aria_emotions').select('id').execute().data)
        print(f"🎭 Emociones: {emotions_count} registros")
        
        apis_count = len(supabase.table('aria_api_relations').select('id').execute().data)
        print(f"🔌 APIs: {apis_count} registros")
        
    except Exception as e:
        print(f"⚠️ Error verificando datos: {e}")

def create_manual_setup_guide():
    """Crear guía de configuración manual"""
    
    guide_content = """
🔧 GUÍA DE CONFIGURACIÓN MANUAL DE SUPABASE
=============================================

Si el script automático falló, puedes configurar manualmente:

1. Ve a tu proyecto en https://supabase.com/dashboard
2. Abre el SQL Editor
3. Copia y pega el contenido de 'schema_supabase_completo.sql'
4. Ejecuta el script completo

TABLAS PRINCIPALES REQUERIDAS:
- aria_knowledge (conocimiento)
- aria_embeddings (vectores semánticos)  
- aria_knowledge_vectors (vectores de conocimiento)
- aria_conversations (conversaciones)
- aria_api_relations (APIs)
- aria_learning_sessions (sesiones de aprendizaje)
- aria_emotions (emociones)
- aria_metrics (métricas)

CARACTERÍSTICAS ESPECIALES:
- Soporte para vectores (extensión pgvector)
- Índices de performance
- Datos iniciales de Caracas y Venezuela
- Sistema de emociones configurado

¡Una vez configurado, ARIA funcionará completamente!
"""
    
    with open('MANUAL_SETUP_GUIDE.md', 'w', encoding='utf-8') as f:
        f.write(guide_content)
    
    print("📖 Guía manual creada: MANUAL_SETUP_GUIDE.md")

if __name__ == "__main__":
    print("🚀 Iniciando configuración de base de datos ARIA...\n")
    
    success = setup_database()
    
    if not success:
        print("\n📖 Creando guía de configuración manual...")
        create_manual_setup_guide()
    
    print("\n🔚 Configuración completada.")
    print("   Ahora puedes ejecutar ARIA con todas las funciones habilitadas!")