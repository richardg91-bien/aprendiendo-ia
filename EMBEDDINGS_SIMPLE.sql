-- 🚀 SCRIPT SQL SIMPLE PARA TABLAS DE EMBEDDINGS
-- Copia este contenido y pégalo en el SQL Editor de tu dashboard de Supabase

-- 1. Habilitar extensión de vectores
CREATE EXTENSION IF NOT EXISTS vector;

-- 2. Crear tabla principal de embeddings
CREATE TABLE IF NOT EXISTS public.aria_embeddings (
    id BIGSERIAL PRIMARY KEY,
    texto TEXT NOT NULL,
    embedding VECTOR(384),
    categoria VARCHAR(100) DEFAULT 'general',
    origen VARCHAR(255) DEFAULT 'conversation',
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 3. Crear tabla de vectores de conocimiento
CREATE TABLE IF NOT EXISTS public.aria_knowledge_vectors (
    id BIGSERIAL PRIMARY KEY,
    concept VARCHAR(255) NOT NULL,
    description_vector VECTOR(384),
    categoria VARCHAR(100) DEFAULT 'general',
    confidence REAL DEFAULT 0.5,
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 4. Crear tabla de relaciones entre conceptos
CREATE TABLE IF NOT EXISTS public.aria_concept_relations (
    id BIGSERIAL PRIMARY KEY,
    concept_a VARCHAR(255) NOT NULL,
    concept_b VARCHAR(255) NOT NULL,
    relation_type VARCHAR(100) DEFAULT 'related',
    strength REAL DEFAULT 0.5 CHECK (strength >= 0 AND strength <= 1),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(concept_a, concept_b)
);

-- 5. Crear índices para mejorar rendimiento
CREATE INDEX IF NOT EXISTS idx_aria_embeddings_categoria ON public.aria_embeddings(categoria);
CREATE INDEX IF NOT EXISTS idx_aria_embeddings_origen ON public.aria_embeddings(origen);
CREATE INDEX IF NOT EXISTS idx_aria_knowledge_vectors_concept ON public.aria_knowledge_vectors(concept);
CREATE INDEX IF NOT EXISTS idx_aria_concept_relations_concepts ON public.aria_concept_relations(concept_a, concept_b);

-- 6. Verificar que las tablas se crearon
SELECT 'aria_embeddings' as tabla, count(*) as registros FROM public.aria_embeddings
UNION ALL
SELECT 'aria_knowledge_vectors' as tabla, count(*) as registros FROM public.aria_knowledge_vectors
UNION ALL  
SELECT 'aria_concept_relations' as tabla, count(*) as registros FROM public.aria_concept_relations;