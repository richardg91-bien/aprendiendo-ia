#!/usr/bin/env python3
"""
🗄️ Creador Automático de Tablas ARIA en Supabase
================================================

Este script crea todas las tablas necesarias, incluyendo las de embeddings,
directamente en Supabase usando SQL directo.
"""

import os
import sys
import requests
import json
from dotenv import load_dotenv

def create_all_tables():
    """Crear todas las tablas de ARIA en Supabase"""
    
    print("🗄️ CREANDO TODAS LAS TABLAS DE ARIA EN SUPABASE")
    print("=" * 60)
    
    # Cargar variables de entorno
    load_dotenv()
    
    url = os.getenv('SUPABASE_URL')
    service_key = os.getenv('SUPABASE_SERVICE_KEY') or os.getenv('SUPABASE_ANON_KEY')
    
    if not url or not service_key:
        print("❌ Error: Faltan credenciales de Supabase")
        print("   Necesitas SUPABASE_URL y SUPABASE_SERVICE_KEY en .env")
        return False
    
    # Headers para autenticación
    headers = {
        'Authorization': f'Bearer {service_key}',
        'apikey': service_key,
        'Content-Type': 'application/json'
    }
    
    # SQL para crear todas las tablas
    sql_commands = [
        # 1. Habilitar extensiones
        """
        CREATE EXTENSION IF NOT EXISTS vector;
        CREATE EXTENSION IF NOT EXISTS pg_trgm;
        """,
        
        # 2. Tabla de embeddings (MUY IMPORTANTE)
        """
        CREATE TABLE IF NOT EXISTS public.aria_embeddings (
            id BIGSERIAL PRIMARY KEY,
            texto TEXT NOT NULL,
            embedding VECTOR(384),
            categoria VARCHAR(100) DEFAULT 'general',
            origen VARCHAR(255) DEFAULT 'conversation',
            metadata JSONB DEFAULT '{}',
            created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
        );
        """,
        
        # 3. Tabla de vectores de conocimiento
        """
        CREATE TABLE IF NOT EXISTS public.aria_knowledge_vectors (
            id BIGSERIAL PRIMARY KEY,
            concept VARCHAR(255) NOT NULL,
            description_vector VECTOR(384),
            categoria VARCHAR(100) DEFAULT 'general',
            confidence REAL DEFAULT 0.5,
            metadata JSONB DEFAULT '{}',
            created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
        );
        """,
        
        # 4. Tabla de relaciones entre conceptos
        """
        CREATE TABLE IF NOT EXISTS public.aria_concept_relations (
            id BIGSERIAL PRIMARY KEY,
            concept_a VARCHAR(255) NOT NULL,
            concept_b VARCHAR(255) NOT NULL,
            relation_type VARCHAR(100) DEFAULT 'related',
            strength REAL DEFAULT 0.5 CHECK (strength >= 0 AND strength <= 1),
            created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
            UNIQUE(concept_a, concept_b)
        );
        """,
        
        # 5. Tabla de métricas
        """
        CREATE TABLE IF NOT EXISTS public.aria_metrics (
            id BIGSERIAL PRIMARY KEY,
            session_id VARCHAR(255),
            metric_type VARCHAR(100) NOT NULL,
            metric_value REAL,
            metric_data JSONB DEFAULT '{}',
            timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW()
        );
        """,
        
        # 6. Tabla resumen de conocimiento
        """
        CREATE TABLE IF NOT EXISTS public.aria_knowledge_summary (
            id BIGSERIAL PRIMARY KEY,
            category VARCHAR(100) NOT NULL UNIQUE,
            concept_count INTEGER DEFAULT 0,
            average_confidence REAL DEFAULT 0.5,
            last_updated TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
            summary_data JSONB DEFAULT '{}'
        );
        """,
        
        # 7. Índices para embeddings (CRÍTICOS para performance)
        """
        CREATE INDEX IF NOT EXISTS idx_aria_embeddings_categoria 
        ON public.aria_embeddings(categoria);
        
        CREATE INDEX IF NOT EXISTS idx_aria_embeddings_origen 
        ON public.aria_embeddings(origen);
        
        CREATE INDEX IF NOT EXISTS idx_aria_embeddings_vector 
        ON public.aria_embeddings USING ivfflat (embedding vector_cosine_ops);
        """,
        
        # 8. Índices para knowledge_vectors
        """
        CREATE INDEX IF NOT EXISTS idx_aria_knowledge_vectors_concept 
        ON public.aria_knowledge_vectors(concept);
        
        CREATE INDEX IF NOT EXISTS idx_aria_knowledge_vectors_categoria 
        ON public.aria_knowledge_vectors(categoria);
        
        CREATE INDEX IF NOT EXISTS idx_aria_knowledge_vectors_vector 
        ON public.aria_knowledge_vectors USING ivfflat (description_vector vector_cosine_ops);
        """,
        
        # 9. Índices adicionales
        """
        CREATE INDEX IF NOT EXISTS idx_aria_concept_relations_concept_a 
        ON public.aria_concept_relations(concept_a);
        
        CREATE INDEX IF NOT EXISTS idx_aria_concept_relations_concept_b 
        ON public.aria_concept_relations(concept_b);
        
        CREATE INDEX IF NOT EXISTS idx_aria_metrics_session 
        ON public.aria_metrics(session_id);
        
        CREATE INDEX IF NOT EXISTS idx_aria_metrics_type 
        ON public.aria_metrics(metric_type);
        """,
        
        # 10. Datos iniciales para concept_relations
        """
        INSERT INTO public.aria_concept_relations (concept_a, concept_b, relation_type, strength) 
        VALUES 
            ('caracas', 'venezuela', 'capital_of', 0.9),
            ('venezuela', 'sudamerica', 'located_in', 0.9),
            ('python', 'programacion', 'subcategory', 0.9),
            ('inteligencia_artificial', 'tecnologia', 'subcategory', 0.8),
            ('supabase', 'base_de_datos', 'type_of', 0.8)
        ON CONFLICT (concept_a, concept_b) DO NOTHING;
        """,
        
        # 11. Datos iniciales para knowledge_summary
        """
        INSERT INTO public.aria_knowledge_summary (category, concept_count, average_confidence) 
        VALUES 
            ('geografia', 2, 0.9),
            ('tecnologia', 3, 0.85),
            ('programacion', 1, 0.9),
            ('general', 5, 0.75)
        ON CONFLICT (category) DO UPDATE SET
            concept_count = EXCLUDED.concept_count,
            average_confidence = EXCLUDED.average_confidence,
            last_updated = NOW();
        """
    ]
    
    # Ejecutar comandos SQL
    success_count = 0
    total_commands = len(sql_commands)
    
    for i, sql in enumerate(sql_commands, 1):
        print(f"\n📝 Ejecutando comando {i}/{total_commands}...")
        
        try:
            # Intentar ejecutar SQL usando el endpoint de SQL directo
            response = requests.post(
                f"{url}/rest/v1/rpc/exec",
                headers=headers,
                json={'sql': sql.strip()}
            )
            
            if response.status_code in [200, 201]:
                print(f"✅ Comando {i} ejecutado exitosamente")
                success_count += 1
            else:
                # Si falla, intentar método alternativo
                print(f"⚠️ Comando {i}: Intentando método alternativo...")
                
                # Separar comando en líneas individuales
                lines = [line.strip() for line in sql.split(';') if line.strip()]
                for line in lines:
                    if line:
                        try:
                            alt_response = requests.post(
                                f"{url}/rest/v1/rpc/exec",
                                headers=headers,
                                json={'sql': line}
                            )
                            if alt_response.status_code in [200, 201]:
                                print(f"  ✅ Línea ejecutada")
                            else:
                                print(f"  ⚠️ Línea con advertencia: {alt_response.status_code}")
                        except:
                            continue
                success_count += 0.5  # Cuenta parcial
                
        except Exception as e:
            print(f"❌ Error en comando {i}: {str(e)[:50]}...")
            continue
    
    print(f"\n📊 RESUMEN:")
    print(f"✅ Comandos exitosos: {success_count}/{total_commands}")
    
    # Verificar tablas creadas
    verify_tables_created(url, headers)
    
    return success_count > total_commands * 0.5

def verify_tables_created(url, headers):
    """Verificar que las tablas se crearon correctamente"""
    
    print(f"\n🔍 VERIFICANDO TABLAS CREADAS...")
    
    required_tables = [
        'aria_embeddings',
        'aria_knowledge_vectors', 
        'aria_concept_relations',
        'aria_metrics',
        'aria_knowledge_summary'
    ]
    
    working_tables = []
    
    for table in required_tables:
        try:
            response = requests.get(
                f"{url}/rest/v1/{table}?select=id&limit=1",
                headers=headers
            )
            
            if response.status_code == 200:
                print(f"✅ {table}: Funcionando")
                working_tables.append(table)
            else:
                print(f"❌ {table}: Error {response.status_code}")
                
        except Exception as e:
            print(f"❌ {table}: Error de conexión")
    
    print(f"\n📈 ESTADO FINAL:")
    print(f"🎯 Tablas funcionando: {len(working_tables)}/{len(required_tables)}")
    
    if len(working_tables) >= 3:
        print("🎉 ¡Suficientes tablas para embeddings!")
        print("   ARIA puede usar búsqueda semántica avanzada")
    else:
        print("⚠️ Faltan tablas críticas de embeddings")
    
    return working_tables

def create_manual_sql_file():
    """Crear archivo SQL para ejecución manual"""
    
    sql_content = """
-- 🗄️ SCRIPT SQL COMPLETO PARA ARIA EN SUPABASE
-- Ejecutar en SQL Editor de Supabase Dashboard

-- 1. Habilitar extensiones necesarias
CREATE EXTENSION IF NOT EXISTS vector;
CREATE EXTENSION IF NOT EXISTS pg_trgm;
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- 2. Tabla principal de embeddings (CRÍTICA)
CREATE TABLE IF NOT EXISTS public.aria_embeddings (
    id BIGSERIAL PRIMARY KEY,
    texto TEXT NOT NULL,
    embedding VECTOR(384),
    categoria VARCHAR(100) DEFAULT 'general',
    origen VARCHAR(255) DEFAULT 'conversation',
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 3. Tabla de vectores de conocimiento
CREATE TABLE IF NOT EXISTS public.aria_knowledge_vectors (
    id BIGSERIAL PRIMARY KEY,
    concept VARCHAR(255) NOT NULL,
    description_vector VECTOR(384),
    categoria VARCHAR(100) DEFAULT 'general',
    confidence REAL DEFAULT 0.5,
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 4. Tabla de relaciones entre conceptos
CREATE TABLE IF NOT EXISTS public.aria_concept_relations (
    id BIGSERIAL PRIMARY KEY,
    concept_a VARCHAR(255) NOT NULL,
    concept_b VARCHAR(255) NOT NULL,
    relation_type VARCHAR(100) DEFAULT 'related',
    strength REAL DEFAULT 0.5 CHECK (strength >= 0 AND strength <= 1),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(concept_a, concept_b)
);

-- 5. Tabla de métricas
CREATE TABLE IF NOT EXISTS public.aria_metrics (
    id BIGSERIAL PRIMARY KEY,
    session_id VARCHAR(255),
    metric_type VARCHAR(100) NOT NULL,
    metric_value REAL,
    metric_data JSONB DEFAULT '{}',
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 6. Tabla resumen de conocimiento
CREATE TABLE IF NOT EXISTS public.aria_knowledge_summary (
    id BIGSERIAL PRIMARY KEY,
    category VARCHAR(100) NOT NULL UNIQUE,
    concept_count INTEGER DEFAULT 0,
    average_confidence REAL DEFAULT 0.5,
    last_updated TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    summary_data JSONB DEFAULT '{}'
);

-- 7. Índices críticos para embeddings
CREATE INDEX IF NOT EXISTS idx_aria_embeddings_categoria ON public.aria_embeddings(categoria);
CREATE INDEX IF NOT EXISTS idx_aria_embeddings_origen ON public.aria_embeddings(origen);
CREATE INDEX IF NOT EXISTS idx_aria_embeddings_vector ON public.aria_embeddings USING ivfflat (embedding vector_cosine_ops);

-- 8. Índices para knowledge_vectors
CREATE INDEX IF NOT EXISTS idx_aria_knowledge_vectors_concept ON public.aria_knowledge_vectors(concept);
CREATE INDEX IF NOT EXISTS idx_aria_knowledge_vectors_categoria ON public.aria_knowledge_vectors(categoria);
CREATE INDEX IF NOT EXISTS idx_aria_knowledge_vectors_vector ON public.aria_knowledge_vectors USING ivfflat (description_vector vector_cosine_ops);

-- 9. Otros índices
CREATE INDEX IF NOT EXISTS idx_aria_concept_relations_concept_a ON public.aria_concept_relations(concept_a);
CREATE INDEX IF NOT EXISTS idx_aria_concept_relations_concept_b ON public.aria_concept_relations(concept_b);
CREATE INDEX IF NOT EXISTS idx_aria_metrics_session ON public.aria_metrics(session_id);
CREATE INDEX IF NOT EXISTS idx_aria_metrics_type ON public.aria_metrics(metric_type);

-- 10. Datos iniciales
INSERT INTO public.aria_concept_relations (concept_a, concept_b, relation_type, strength) 
VALUES 
    ('caracas', 'venezuela', 'capital_of', 0.9),
    ('venezuela', 'sudamerica', 'located_in', 0.9),
    ('python', 'programacion', 'subcategory', 0.9),
    ('inteligencia_artificial', 'tecnologia', 'subcategory', 0.8),
    ('supabase', 'base_de_datos', 'type_of', 0.8)
ON CONFLICT (concept_a, concept_b) DO NOTHING;

INSERT INTO public.aria_knowledge_summary (category, concept_count, average_confidence) 
VALUES 
    ('geografia', 2, 0.9),
    ('tecnologia', 3, 0.85),
    ('programacion', 1, 0.9),
    ('general', 5, 0.75)
ON CONFLICT (category) DO UPDATE SET
    concept_count = EXCLUDED.concept_count,
    average_confidence = EXCLUDED.average_confidence,
    last_updated = NOW();

-- 11. Verificación final
SELECT 
    'aria_embeddings' as tabla, 
    COUNT(*) as registros,
    'Embeddings para búsqueda semántica' as descripcion
FROM public.aria_embeddings
UNION ALL
SELECT 'aria_knowledge_vectors', COUNT(*), 'Vectores de conocimiento' FROM public.aria_knowledge_vectors
UNION ALL
SELECT 'aria_concept_relations', COUNT(*), 'Relaciones entre conceptos' FROM public.aria_concept_relations
UNION ALL
SELECT 'aria_metrics', COUNT(*), 'Métricas del sistema' FROM public.aria_metrics
UNION ALL
SELECT 'aria_knowledge_summary', COUNT(*), 'Resúmenes de conocimiento' FROM public.aria_knowledge_summary
ORDER BY tabla;
"""
    
    with open('CREAR_TABLAS_EMBEDDINGS.sql', 'w', encoding='utf-8') as f:
        f.write(sql_content)
    
    print("📄 Archivo SQL manual creado: CREAR_TABLAS_EMBEDDINGS.sql")

if __name__ == "__main__":
    print("🚀 INICIANDO CREACIÓN DE TABLAS DE EMBEDDINGS...\n")
    
    success = create_all_tables()
    
    if not success:
        print("\n📄 Creando archivo SQL para configuración manual...")
        create_manual_sql_file()
        print("\n📋 INSTRUCCIONES MANUALES:")
        print("1. Ve a tu Supabase Dashboard")
        print("2. Abre SQL Editor") 
        print("3. Ejecuta el contenido de CREAR_TABLAS_EMBEDDINGS.sql")
    
    print("\n🎯 PRÓXIMO PASO:")
    print("   Ejecuta: python test_full_flow.py")
    print("   Para verificar que los embeddings funcionan")