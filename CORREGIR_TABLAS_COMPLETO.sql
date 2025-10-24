-- 🔧 SCRIPT PARA CORREGIR TABLAS FALTANTES EN SUPABASE
-- 2. CORREGIR aria_knowledge_summary (eliminar vista y crear tabla)
DROP TABLE IF EXISTS public.aria_knowledge_summary CASCADE;
CREATE TABLE public.aria_knowledge_summary (
    id BIGSERIAL PRIMARY KEY,
    category VARCHAR(100) NOT NULL,
    summary_text TEXT,
    concept_count INTEGER DEFAULT 0,
    last_updated TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    metadata JSONB DEFAULT '{}'
);

-- 2.1. CORREGIR aria_conversations (agregar columnas faltantes)
ALTER TABLE public.aria_conversations 
ADD COLUMN IF NOT EXISTS user_emotion VARCHAR(50) DEFAULT 'neutral';

ALTER TABLE public.aria_conversations 
ADD COLUMN IF NOT EXISTS aria_emotion VARCHAR(50) DEFAULT 'helpful';

-- Actualizar registros existentes
UPDATE public.aria_conversations 
SET user_emotion = 'curious' 
WHERE user_emotion IS NULL;

UPDATE public.aria_conversations 
SET aria_emotion = 'helpful' 
WHERE aria_emotion IS NULL;

-- 3. CREAR aria_embeddings (para búsqueda semántica)
CREATE TABLE IF NOT EXISTS public.aria_embeddings (
    id BIGSERIAL PRIMARY KEY,
    texto TEXT NOT NULL,
    embedding VECTOR(384),
    categoria VARCHAR(100) DEFAULT 'general',
    origen VARCHAR(255) DEFAULT 'conversation',
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 4. CREAR aria_knowledge_vectors (vectores de conocimiento)
CREATE TABLE IF NOT EXISTS public.aria_knowledge_vectors (
    id BIGSERIAL PRIMARY KEY,
    concept VARCHAR(255) NOT NULL,
    description_vector VECTOR(384),
    categoria VARCHAR(100) DEFAULT 'general',
    confidence REAL DEFAULT 0.5,
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 5. CREAR aria_concept_relations (relaciones entre conceptos)
CREATE TABLE IF NOT EXISTS public.aria_concept_relations (
    id BIGSERIAL PRIMARY KEY,
    concept_a VARCHAR(255) NOT NULL,
    concept_b VARCHAR(255) NOT NULL,
    relation_type VARCHAR(100) DEFAULT 'related',
    strength REAL DEFAULT 0.5 CHECK (strength >= 0 AND strength <= 1),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(concept_a, concept_b)
);

-- 6. CREAR ÍNDICES para mejorar rendimiento

-- Índices para aria_embeddings
CREATE INDEX IF NOT EXISTS idx_aria_embeddings_categoria ON public.aria_embeddings(categoria);
CREATE INDEX IF NOT EXISTS idx_aria_embeddings_origen ON public.aria_embeddings(origen);
CREATE INDEX IF NOT EXISTS idx_aria_embeddings_created_at ON public.aria_embeddings(created_at);

-- Índices para aria_knowledge_vectors
CREATE INDEX IF NOT EXISTS idx_aria_knowledge_vectors_concept ON public.aria_knowledge_vectors(concept);
CREATE INDEX IF NOT EXISTS idx_aria_knowledge_vectors_categoria ON public.aria_knowledge_vectors(categoria);
CREATE INDEX IF NOT EXISTS idx_aria_knowledge_vectors_confidence ON public.aria_knowledge_vectors(confidence);

-- Índices para aria_concept_relations
CREATE INDEX IF NOT EXISTS idx_aria_concept_relations_concepts ON public.aria_concept_relations(concept_a, concept_b);
CREATE INDEX IF NOT EXISTS idx_aria_concept_relations_type ON public.aria_concept_relations(relation_type);
CREATE INDEX IF NOT EXISTS idx_aria_concept_relations_strength ON public.aria_concept_relations(strength);

-- Índices para aria_knowledge_summary
CREATE INDEX IF NOT EXISTS idx_aria_knowledge_summary_category ON public.aria_knowledge_summary(category);
CREATE INDEX IF NOT EXISTS idx_aria_knowledge_summary_updated ON public.aria_knowledge_summary(last_updated);

-- 7. INSERTAR datos iniciales en aria_knowledge_summary
INSERT INTO public.aria_knowledge_summary (category, summary_text, concept_count) VALUES
('general', 'Conocimiento general del sistema ARIA', 0),
('emotions', 'Sistema emocional y detección de sentimientos', 0),
('geography', 'Información geográfica y ciudades', 0),
('conversations', 'Historial y patrones de conversaciones', 0)
ON CONFLICT DO NOTHING;

-- 8. VERIFICAR que todas las tablas se crearon correctamente
SELECT 
    table_name,
    CASE 
        WHEN table_name IN (
            'aria_conversations', 
            'aria_knowledge', 
            'aria_api_relations', 
            'aria_emotions',
            'aria_knowledge_summary',
            'aria_embeddings',
            'aria_knowledge_vectors',
            'aria_concept_relations'
        ) THEN '✅ ARIA Table'
        ELSE '❓ Other Table'
    END as status
FROM information_schema.tables 
WHERE table_schema = 'public' 
AND table_name LIKE 'aria_%'
ORDER BY table_name;

-- 9. MOSTRAR conteo de registros en cada tabla
SELECT 'aria_conversations' as tabla, count(*) as registros FROM public.aria_conversations
UNION ALL
SELECT 'aria_knowledge' as tabla, count(*) as registros FROM public.aria_knowledge
UNION ALL
SELECT 'aria_api_relations' as tabla, count(*) as registros FROM public.aria_api_relations
UNION ALL
SELECT 'aria_emotions' as tabla, count(*) as registros FROM public.aria_emotions
UNION ALL
SELECT 'aria_knowledge_summary' as tabla, count(*) as registros FROM public.aria_knowledge_summary
UNION ALL
SELECT 'aria_embeddings' as tabla, count(*) as registros FROM public.aria_embeddings
UNION ALL
SELECT 'aria_knowledge_vectors' as tabla, count(*) as registros FROM public.aria_knowledge_vectors
UNION ALL
SELECT 'aria_concept_relations' as tabla, count(*) as registros FROM public.aria_concept_relations
ORDER BY tabla;