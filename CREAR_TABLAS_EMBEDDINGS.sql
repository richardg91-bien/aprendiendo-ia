
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
