#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
🔧 CORRECTOR DE TABLAS SUPABASE
==============================

Script para corregir y crear las tablas faltantes de ARIA
"""

import os
import sys
from dotenv import load_dotenv
from supabase import create_client

def main():
    print("🔧 CORRECTOR DE TABLAS SUPABASE")
    print("=" * 40)
    
    # Cargar variables de entorno
    load_dotenv()
    
    supabase_url = os.getenv('SUPABASE_URL')
    supabase_key = os.getenv('SUPABASE_ANON_KEY')
    
    if not supabase_url or not supabase_key:
        print("❌ Variables de entorno no encontradas")
        return False
    
    try:
        # Conectar a Supabase
        supabase = create_client(supabase_url, supabase_key)
        print("✅ Conectado a Supabase")
        
        # SQLs para corregir/crear tablas
        sqls = [
            {
                'name': 'Habilitar extensión vector',
                'sql': 'CREATE EXTENSION IF NOT EXISTS vector;'
            },
            {
                'name': 'Corregir aria_knowledge_summary',
                'sql': '''
                DROP TABLE IF EXISTS public.aria_knowledge_summary CASCADE;
                CREATE TABLE IF NOT EXISTS public.aria_knowledge_summary (
                    id BIGSERIAL PRIMARY KEY,
                    category VARCHAR(100) NOT NULL,
                    summary_text TEXT,
                    concept_count INTEGER DEFAULT 0,
                    last_updated TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                    metadata JSONB DEFAULT '{}'
                );
                '''
            },
            {
                'name': 'Crear aria_embeddings',
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
                'name': 'Crear aria_knowledge_vectors',
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
                'name': 'Crear aria_concept_relations',
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
            },
            {
                'name': 'Crear índices para embeddings',
                'sql': '''
                CREATE INDEX IF NOT EXISTS idx_aria_embeddings_categoria ON public.aria_embeddings(categoria);
                CREATE INDEX IF NOT EXISTS idx_aria_embeddings_origen ON public.aria_embeddings(origen);
                '''
            },
            {
                'name': 'Crear índices para knowledge_vectors',
                'sql': '''
                CREATE INDEX IF NOT EXISTS idx_aria_knowledge_vectors_concept ON public.aria_knowledge_vectors(concept);
                CREATE INDEX IF NOT EXISTS idx_aria_knowledge_vectors_categoria ON public.aria_knowledge_vectors(categoria);
                '''
            },
            {
                'name': 'Crear índices para concept_relations',
                'sql': '''
                CREATE INDEX IF NOT EXISTS idx_aria_concept_relations_concepts ON public.aria_concept_relations(concept_a, concept_b);
                CREATE INDEX IF NOT EXISTS idx_aria_concept_relations_type ON public.aria_concept_relations(relation_type);
                '''
            }
        ]
        
        success_count = 0
        
        for sql_item in sqls:
            name = sql_item['name']
            sql = sql_item['sql']
            
            print(f"\n🔄 Ejecutando: {name}")
            
            try:
                # Intentar ejecutar usando rpc (si existe)
                try:
                    result = supabase.rpc('exec_sql', {'sql_command': sql}).execute()
                    print(f"✅ {name}: Exitoso (RPC)")
                    success_count += 1
                except:
                    # Si RPC no funciona, usar método directo
                    # Nota: Esto puede no funcionar dependiendo de permisos
                    print(f"⚠️ {name}: RPC no disponible, usando método alternativo")
                    # Aquí normalmente tendrías que ejecutar en el dashboard
                    print(f"📝 SQL a ejecutar manualmente:\n{sql}")
                    
            except Exception as e:
                print(f"❌ {name}: Error - {e}")
        
        print(f"\n📊 RESULTADO:")
        print(f"✅ Operaciones completadas: {success_count}/{len(sqls)}")
        
        if success_count < len(sqls):
            print("\n📋 INSTRUCCIONES MANUALES:")
            print("1. Ve a tu Dashboard de Supabase")
            print("2. Abre 'SQL Editor'")
            print("3. Ejecuta estos comandos uno por uno:")
            print("\n" + "="*50)
            
            for sql_item in sqls:
                print(f"\n-- {sql_item['name']}")
                print(sql_item['sql'])
            
            print("="*50)
        
        return success_count > 0
        
    except Exception as e:
        print(f"❌ Error general: {e}")
        return False

if __name__ == "__main__":
    success = main()
    if success:
        print("\n🎉 Proceso completado. Verifica las tablas.")
    else:
        print("\n⚠️ Proceso con errores. Usa el método manual.")
    
    input("\nPresiona Enter para continuar...")