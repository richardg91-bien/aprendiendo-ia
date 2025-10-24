-- 🗄️ ARIA SUPABASE SCHEMA
-- Esquema de base de datos para ARIA
-- Ejecutar en el SQL Editor de Supabase

-- Crear tabla de conocimiento
CREATE TABLE IF NOT EXISTS public.aria_knowledge (
    id SERIAL PRIMARY KEY,
    concept VARCHAR(255) UNIQUE NOT NULL,
    description TEXT,
    category VARCHAR(100) DEFAULT 'general',
    confidence REAL DEFAULT 0.5 CHECK (confidence >= 0 AND confidence <= 1),
    source VARCHAR(255) DEFAULT 'conversation',
    tags TEXT[],
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Crear tabla de conversaciones
CREATE TABLE IF NOT EXISTS public.aria_conversations (
    id SERIAL PRIMARY KEY,
    session_id VARCHAR(255) NOT NULL,
    user_input TEXT NOT NULL,
    aria_response TEXT NOT NULL,
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    response_time REAL DEFAULT 0,
    user_satisfaction INTEGER CHECK (user_satisfaction >= 1 AND user_satisfaction <= 5)
);

-- Crear tabla de sesiones de aprendizaje
CREATE TABLE IF NOT EXISTS public.aria_learning_sessions (
    id SERIAL PRIMARY KEY,
    session_id VARCHAR(255) NOT NULL,
    topic VARCHAR(255),
    source_type VARCHAR(100),
    knowledge_gained INTEGER DEFAULT 0,
    apis_discovered INTEGER DEFAULT 0,
    session_duration REAL DEFAULT 0,
    success_indicators JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Crear tabla de APIs descubiertas
CREATE TABLE IF NOT EXISTS public.aria_discovered_apis (
    id SERIAL PRIMARY KEY,
    api_name VARCHAR(255) NOT NULL,
    base_url VARCHAR(500),
    description TEXT,
    endpoints JSONB,
    authentication_type VARCHAR(100),
    confidence REAL DEFAULT 0.5,
    discovery_method VARCHAR(100),
    last_verified TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Crear tabla de relaciones entre conceptos
CREATE TABLE IF NOT EXISTS public.aria_concept_relations (
    id SERIAL PRIMARY KEY,
    concept_a VARCHAR(255) NOT NULL,
    concept_b VARCHAR(255) NOT NULL,
    relation_type VARCHAR(100) DEFAULT 'related',
    strength REAL DEFAULT 0.5 CHECK (strength >= 0 AND strength <= 1),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(concept_a, concept_b)
);

-- Crear índices para mejorar performance
CREATE INDEX IF NOT EXISTS idx_aria_knowledge_concept ON public.aria_knowledge(concept);
CREATE INDEX IF NOT EXISTS idx_aria_knowledge_category ON public.aria_knowledge(category);
CREATE INDEX IF NOT EXISTS idx_aria_conversations_session ON public.aria_conversations(session_id);
CREATE INDEX IF NOT EXISTS idx_aria_conversations_timestamp ON public.aria_conversations(timestamp);
CREATE INDEX IF NOT EXISTS idx_aria_learning_session_id ON public.aria_learning_sessions(session_id);
CREATE INDEX IF NOT EXISTS idx_aria_apis_name ON public.aria_discovered_apis(api_name);

-- Insertar algunos datos de ejemplo
INSERT INTO public.aria_knowledge (concept, description, category, confidence) VALUES
('saludo', 'Forma de iniciar una conversación de manera amigable', 'social', 0.9),
('inteligencia_artificial', 'Campo de la informática que busca crear sistemas que puedan realizar tareas que requieren inteligencia humana', 'tecnologia', 0.9),
('python', 'Lenguaje de programación de alto nivel, interpretado y de propósito general', 'programacion', 0.9),
('supabase', 'Plataforma de base de datos como servicio basada en PostgreSQL', 'tecnologia', 0.8),
('google_cloud', 'Plataforma de servicios en la nube de Google', 'tecnologia', 0.8)
ON CONFLICT (concept) DO NOTHING;

-- Insertar relaciones entre conceptos
INSERT INTO public.aria_concept_relations (concept_a, concept_b, relation_type, strength) VALUES
('python', 'programacion', 'subcategory', 0.9),
('supabase', 'base_de_datos', 'type_of', 0.8),
('google_cloud', 'inteligencia_artificial', 'provides', 0.7),
('inteligencia_artificial', 'python', 'implemented_in', 0.8)
ON CONFLICT (concept_a, concept_b) DO NOTHING;

-- Verificar que las tablas se crearon correctamente
SELECT 'aria_knowledge' as table_name, COUNT(*) as row_count FROM public.aria_knowledge
UNION ALL
SELECT 'aria_conversations', COUNT(*) FROM public.aria_conversations
UNION ALL
SELECT 'aria_learning_sessions', COUNT(*) FROM public.aria_learning_sessions
UNION ALL
SELECT 'aria_discovered_apis', COUNT(*) FROM public.aria_discovered_apis
UNION ALL
SELECT 'aria_concept_relations', COUNT(*) FROM public.aria_concept_relations;