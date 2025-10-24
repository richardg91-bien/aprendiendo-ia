#!/usr/bin/env python3
"""
🔧 Script para crear las tablas faltantes de ARIA usando el cliente Python de Supabase
"""

import os
import sys
from dotenv import load_dotenv
from supabase import create_client, Client

def create_missing_tables():
    """Crear las tablas que faltan usando comandos SQL directos"""
    
    print("🔧 CREANDO TABLAS FALTANTES DE ARIA")
    print("=" * 40)
    
    # Cargar variables de entorno
    load_dotenv()
    
    # Obtener credenciales de Supabase
    url = os.getenv('SUPABASE_URL')
    key = os.getenv('SUPABASE_SERVICE_KEY') or os.getenv('SUPABASE_ANON_KEY')
    
    if not url or not key:
        print("❌ Error: No se encontraron las credenciales de Supabase")
        return False
    
    try:
        # Conectar a Supabase
        supabase: Client = create_client(url, key)
        print(f"✅ Conectado a Supabase")
        
        # SQL para crear tablas faltantes
        missing_tables_sql = [
            # Tabla de embeddings
            """
            CREATE TABLE IF NOT EXISTS public.aria_embeddings (
                id SERIAL PRIMARY KEY,
                texto TEXT NOT NULL,
                embedding TEXT, -- Almacenar como JSON string por ahora
                categoria VARCHAR(100) DEFAULT 'general',
                origen VARCHAR(255) DEFAULT 'conversation',
                metadata JSONB,
                created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
            );
            """,
            
            # Tabla de vectores de conocimiento
            """
            CREATE TABLE IF NOT EXISTS public.aria_knowledge_vectors (
                id SERIAL PRIMARY KEY,
                concept VARCHAR(255) NOT NULL,
                description_vector TEXT, -- Almacenar como JSON string por ahora
                categoria VARCHAR(100) DEFAULT 'general',
                confidence REAL DEFAULT 0.5,
                metadata JSONB,
                created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
            );
            """,
            
            # Tabla de relaciones entre conceptos
            """
            CREATE TABLE IF NOT EXISTS public.aria_concept_relations (
                id SERIAL PRIMARY KEY,
                concept_a VARCHAR(255) NOT NULL,
                concept_b VARCHAR(255) NOT NULL,
                relation_type VARCHAR(100) DEFAULT 'related',
                strength REAL DEFAULT 0.5 CHECK (strength >= 0 AND strength <= 1),
                created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                UNIQUE(concept_a, concept_b)
            );
            """,
            
            # Tabla de métricas
            """
            CREATE TABLE IF NOT EXISTS public.aria_metrics (
                id SERIAL PRIMARY KEY,
                session_id VARCHAR(255),
                metric_type VARCHAR(100) NOT NULL,
                metric_value REAL,
                metric_data JSONB,
                timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW()
            );
            """,
            
            # Tabla resumen de conocimiento
            """
            CREATE TABLE IF NOT EXISTS public.aria_knowledge_summary (
                id SERIAL PRIMARY KEY,
                category VARCHAR(100) NOT NULL,
                concept_count INTEGER DEFAULT 0,
                average_confidence REAL DEFAULT 0.5,
                last_updated TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                summary_data JSONB
            );
            """
        ]
        
        # Índices adicionales
        indexes_sql = [
            "CREATE INDEX IF NOT EXISTS idx_aria_embeddings_categoria ON public.aria_embeddings(categoria);",
            "CREATE INDEX IF NOT EXISTS idx_aria_knowledge_vectors_concept ON public.aria_knowledge_vectors(concept);",
            "CREATE INDEX IF NOT EXISTS idx_aria_concept_relations_concept_a ON public.aria_concept_relations(concept_a);",
            "CREATE INDEX IF NOT EXISTS idx_aria_metrics_session ON public.aria_metrics(session_id);",
            "CREATE INDEX IF NOT EXISTS idx_aria_knowledge_summary_category ON public.aria_knowledge_summary(category);"
        ]
        
        print("📊 Creando tablas faltantes...")
        
        # Crear tablas usando un método alternativo
        for i, sql in enumerate(missing_tables_sql, 1):
            try:
                # Intentar usar el raw SQL si está disponible
                result = supabase.postgrest.session.post(
                    f"{url}/rest/v1/rpc/exec",
                    json={"sql": sql.strip()},
                    headers={"apikey": key, "Authorization": f"Bearer {key}"}
                )
                
                if result.status_code == 200:
                    print(f"✅ Tabla {i}/5 creada exitosamente")
                else:
                    print(f"⚠️ Tabla {i}/5: {result.text}")
                    
            except Exception as e:
                print(f"⚠️ Error creando tabla {i}: {str(e)[:50]}...")
                continue
        
        print("\n📊 Creando índices...")
        
        for i, sql in enumerate(indexes_sql, 1):
            try:
                result = supabase.postgrest.session.post(
                    f"{url}/rest/v1/rpc/exec",
                    json={"sql": sql.strip()},
                    headers={"apikey": key, "Authorization": f"Bearer {key}"}
                )
                
                if result.status_code == 200:
                    print(f"✅ Índice {i}/5 creado")
                else:
                    print(f"⚠️ Índice {i}/5: problema menor")
                    
            except Exception as e:
                print(f"⚠️ Error creando índice {i}: {str(e)[:30]}...")
                continue
        
        # Insertar datos iniciales en concept_relations
        print("\n📝 Insertando relaciones entre conceptos...")
        
        relations_data = [
            {
                'concept_a': 'caracas',
                'concept_b': 'venezuela', 
                'relation_type': 'capital_of',
                'strength': 0.9
            },
            {
                'concept_a': 'venezuela',
                'concept_b': 'sudamerica',
                'relation_type': 'located_in', 
                'strength': 0.9
            },
            {
                'concept_a': 'python',
                'concept_b': 'programacion',
                'relation_type': 'subcategory',
                'strength': 0.9
            }
        ]
        
        try:
            result = supabase.table('aria_concept_relations').upsert(relations_data).execute()
            print(f"✅ {len(relations_data)} relaciones insertadas")
        except Exception as e:
            print(f"⚠️ Error insertando relaciones: {str(e)[:50]}...")
        
        # Verificar tablas creadas
        print("\n🔍 Verificando estado final...")
        verify_all_tables(supabase)
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def verify_all_tables(supabase: Client):
    """Verificar todas las tablas de ARIA"""
    
    all_tables = [
        'aria_knowledge',
        'aria_embeddings', 
        'aria_knowledge_vectors',
        'aria_conversations',
        'aria_api_relations',
        'aria_concept_relations',
        'aria_emotions',
        'aria_metrics',
        'aria_knowledge_summary'
    ]
    
    working_tables = 0
    
    for table in all_tables:
        try:
            result = supabase.table(table).select('id').limit(1).execute()
            print(f"✅ {table}")
            working_tables += 1
        except Exception as e:
            print(f"❌ {table}: {str(e)[:30]}...")
    
    print(f"\n📊 Estado: {working_tables}/{len(all_tables)} tablas funcionando")
    
    if working_tables >= 6:  # Las tablas esenciales
        print("🎉 ¡Configuración suficiente para ejecutar ARIA!")
    else:
        print("⚠️ Faltan tablas importantes. Usar configuración manual.")

if __name__ == "__main__":
    success = create_missing_tables()
    
    if success:
        print("\n✅ Proceso completado. ARIA puede ejecutarse con más funciones.")
    else:
        print("\n❌ Proceso falló. Usar configuración manual en Supabase SQL Editor.")
        print("   Archivo: schema_supabase_completo.sql")