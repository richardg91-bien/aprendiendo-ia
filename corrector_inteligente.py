#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
🔧 CORRECTOR INTELIGENTE DE TABLAS SUPABASE
==========================================

Script que diagnostica y corrige automáticamente las tablas
"""

import os
import sys
from dotenv import load_dotenv
from supabase import create_client

def main():
    print("🔧 CORRECTOR INTELIGENTE DE TABLAS SUPABASE")
    print("=" * 50)
    
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
        
        print("\n🔍 DIAGNÓSTICO DE OBJETOS EXISTENTES:")
        print("-" * 40)
        
        # Verificar si aria_knowledge_summary existe y qué tipo es
        try:
            # Intentar como tabla
            response = supabase.table('aria_knowledge_summary').select('id').limit(1).execute()
            print("📊 aria_knowledge_summary: TABLA existente")
            summary_type = "table"
        except Exception as e:
            error_str = str(e)
            if "Could not find the table" in error_str:
                print("❌ aria_knowledge_summary: No existe")
                summary_type = "missing"
            elif "column" in error_str:
                print("⚠️ aria_knowledge_summary: Existe pero estructura incorrecta")
                summary_type = "incorrect_structure"
            else:
                print(f"❓ aria_knowledge_summary: Error - {error_str[:50]}...")
                summary_type = "unknown"
        
        # Verificar otras tablas faltantes
        missing_tables = []
        tables_to_check = ['aria_embeddings', 'aria_knowledge_vectors', 'aria_concept_relations']
        
        for table in tables_to_check:
            try:
                response = supabase.table(table).select('id').limit(1).execute()
                print(f"✅ {table}: Existe")
            except Exception as e:
                if "Could not find the table" in str(e):
                    print(f"❌ {table}: No existe")
                    missing_tables.append(table)
                else:
                    print(f"⚠️ {table}: Error - {str(e)[:30]}...")
                    missing_tables.append(table)
        
        print(f"\n📋 PLAN DE CORRECCIÓN:")
        print("-" * 30)
        
        # Generar SQL específico según el diagnóstico
        sql_commands = []
        
        # 1. Habilitar extensión vector
        sql_commands.append("CREATE EXTENSION IF NOT EXISTS vector;")
        
        # 2. Corregir aria_knowledge_summary según su tipo
        if summary_type in ["missing", "incorrect_structure", "unknown"]:
            sql_commands.extend([
                "DROP VIEW IF EXISTS public.aria_knowledge_summary CASCADE;",
                "DROP TABLE IF EXISTS public.aria_knowledge_summary CASCADE;",
                """CREATE TABLE public.aria_knowledge_summary (
                    id BIGSERIAL PRIMARY KEY,
                    category VARCHAR(100) NOT NULL,
                    summary_text TEXT,
                    concept_count INTEGER DEFAULT 0,
                    last_updated TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                    metadata JSONB DEFAULT '{}'
                );"""
            ])
            print("🔧 aria_knowledge_summary: Será recreada")
        
        # 3. Crear tablas faltantes
        if 'aria_embeddings' in missing_tables:
            sql_commands.append("""CREATE TABLE IF NOT EXISTS public.aria_embeddings (
                id BIGSERIAL PRIMARY KEY,
                texto TEXT NOT NULL,
                embedding VECTOR(384),
                categoria VARCHAR(100) DEFAULT 'general',
                origen VARCHAR(255) DEFAULT 'conversation',
                metadata JSONB DEFAULT '{}',
                created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
            );""")
            print("🔧 aria_embeddings: Será creada")
        
        if 'aria_knowledge_vectors' in missing_tables:
            sql_commands.append("""CREATE TABLE IF NOT EXISTS public.aria_knowledge_vectors (
                id BIGSERIAL PRIMARY KEY,
                concept VARCHAR(255) NOT NULL,
                description_vector VECTOR(384),
                categoria VARCHAR(100) DEFAULT 'general',
                confidence REAL DEFAULT 0.5,
                metadata JSONB DEFAULT '{}',
                created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
            );""")
            print("🔧 aria_knowledge_vectors: Será creada")
        
        if 'aria_concept_relations' in missing_tables:
            sql_commands.append("""CREATE TABLE IF NOT EXISTS public.aria_concept_relations (
                id BIGSERIAL PRIMARY KEY,
                concept_a VARCHAR(255) NOT NULL,
                concept_b VARCHAR(255) NOT NULL,
                relation_type VARCHAR(100) DEFAULT 'related',
                strength REAL DEFAULT 0.5 CHECK (strength >= 0 AND strength <= 1),
                created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                UNIQUE(concept_a, concept_b)
            );""")
            print("🔧 aria_concept_relations: Será creada")
        
        # Escribir SQL final
        final_sql = "\n\n".join(sql_commands)
        
        with open('CORRECCION_FINAL.sql', 'w', encoding='utf-8') as f:
            f.write("-- 🔧 SCRIPT DE CORRECCIÓN FINAL PERSONALIZADO\n")
            f.write("-- ============================================\n")
            f.write("-- Generado automáticamente después del diagnóstico\n\n")
            f.write(final_sql)
            f.write("\n\n-- Verificación final\n")
            f.write("""SELECT 'aria_embeddings' as tabla, count(*) as registros FROM public.aria_embeddings
UNION ALL
SELECT 'aria_knowledge_vectors' as tabla, count(*) as registros FROM public.aria_knowledge_vectors
UNION ALL
SELECT 'aria_concept_relations' as tabla, count(*) as registros FROM public.aria_concept_relations
UNION ALL
SELECT 'aria_knowledge_summary' as tabla, count(*) as registros FROM public.aria_knowledge_summary;""")
        
        print(f"\n✅ Script personalizado generado: CORRECCION_FINAL.sql")
        print("\n📋 INSTRUCCIONES:")
        print("1. Ve a tu Dashboard de Supabase")
        print("2. Abre SQL Editor")
        print("3. Ejecuta el contenido de: CORRECCION_FINAL.sql")
        
        return True
        
    except Exception as e:
        print(f"❌ Error general: {e}")
        return False

if __name__ == "__main__":
    success = main()
    if success:
        print("\n🎉 Diagnóstico completado. Usa CORRECCION_FINAL.sql")
    else:
        print("\n⚠️ Error en diagnóstico. Usa método manual.")
    
    input("\nPresiona Enter para continuar...")