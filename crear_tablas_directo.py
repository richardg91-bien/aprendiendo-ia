#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
🚀 CREADOR DE TABLAS ARIA - MÉTODO DIRECTO
==========================================

Este script crea las tablas necesarias usando el mismo método que ARIA utiliza
para conectarse a Supabase, evitando problemas de configuración.
"""

import os
import sys

def main():
    print("🚀 CREADOR DE TABLAS ARIA - MÉTODO DIRECTO")
    print("=" * 50)
    
    try:
        # Importar ARIA server para usar su configuración
        sys.path.append('src')
        from aria_servidor_superbase import ARIASuperServer
        
        print("📡 Creando servidor ARIA para obtener configuración...")
        
        # Crear una instancia temporal del servidor
        server = ARIASuperServer()
        
        print("✅ Servidor ARIA inicializado")
        print("🗄️ Accediendo a la base de datos...")
        
        # Verificar conexión con una consulta simple
        response = server.superbase.supabase.table('aria_conversations').select('id').limit(1).execute()
        print("✅ Conexión a Supabase verificada")
        
        # Obtener referencia a supabase
        supabase_client = server.superbase.supabase
        
        # Lista de tablas a crear
        tables_to_create = [
            {
                'name': 'aria_embeddings',
                'sql': '''
                CREATE TABLE IF NOT EXISTS public.aria_embeddings (
                    id BIGSERIAL PRIMARY KEY,
                    texto TEXT NOT NULL,
                    embedding VECTOR(384),
                    categoria VARCHAR(100) DEFAULT 'general',
                    origen VARCHAR(255) DEFAULT 'conversation',
                    metadata JSONB DEFAULT '{}',
                    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
                );
                '''
            },
            {
                'name': 'aria_knowledge_vectors',
                'sql': '''
                CREATE TABLE IF NOT EXISTS public.aria_knowledge_vectors (
                    id BIGSERIAL PRIMARY KEY,
                    concept VARCHAR(255) NOT NULL,
                    description_vector VECTOR(384),
                    categoria VARCHAR(100) DEFAULT 'general',
                    confidence REAL DEFAULT 0.5,
                    metadata JSONB DEFAULT '{}',
                    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
                );
                '''
            },
            {
                'name': 'aria_concept_relations',
                'sql': '''
                CREATE TABLE IF NOT EXISTS public.aria_concept_relations (
                    id BIGSERIAL PRIMARY KEY,
                    concept_a VARCHAR(255) NOT NULL,
                    concept_b VARCHAR(255) NOT NULL,
                    relation_type VARCHAR(100) DEFAULT 'related',
                    strength REAL DEFAULT 0.5 CHECK (strength >= 0 AND strength <= 1),
                    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                    UNIQUE(concept_a, concept_b)
                );
                '''
            }
        ]
        
        # Intentar crear cada tabla
        success_count = 0
        
        for table_info in tables_to_create:
            table_name = table_info['name']
            table_sql = table_info['sql']
            
            print(f"\n📝 Creando tabla: {table_name}")
            
            try:
                # Ejecutar SQL usando RPC
                result = supabase_client.rpc('create_table_if_not_exists', {
                    'table_sql': table_sql
                }).execute()
                
                print(f"✅ Tabla {table_name} creada exitosamente")
                success_count += 1
                
            except Exception as e:
                print(f"⚠️ Error creando {table_name}: {e}")
                # Intentar método alternativo
                try:
                    # Usar SQL editor directo
                    result = supabase_client.postgrest.schema().execute(table_sql)
                    print(f"✅ Tabla {table_name} creada con método alternativo")
                    success_count += 1
                except Exception as e2:
                    print(f"❌ Error definitivo en {table_name}: {e2}")
        
        print(f"\n📊 RESUMEN:")
        print(f"✅ Tablas creadas exitosamente: {success_count}/{len(tables_to_create)}")
        
        if success_count == len(tables_to_create):
            print("🎉 ¡Todas las tablas fueron creadas!")
            print("\n🚀 Siguiente paso:")
            print("   python main.py")
            print("   Y prueba: '¿Qué sabes sobre caracas?'")
        else:
            print("⚠️ Algunas tablas no se pudieron crear automáticamente")
            print("📄 Usa el archivo CREAR_TABLAS_EMBEDDINGS.sql en Supabase Dashboard")
            
    except ImportError as e:
        print(f"❌ Error importando ARIA: {e}")
        print("🔧 Verifica que todos los módulos estén instalados:")
        print("   pip install -r requirements.txt")
        
    except Exception as e:
        print(f"❌ Error general: {e}")
        print(f"   Tipo: {type(e).__name__}")
        
        print("\n📋 PLAN B - MANUAL:")
        print("1. Ve a tu Supabase Dashboard")
        print("2. Abre SQL Editor")
        print("3. Ejecuta el contenido de CREAR_TABLAS_EMBEDDINGS.sql")

if __name__ == "__main__":
    main()