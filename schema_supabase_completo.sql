-- 🗄️ ARIA SUPABASE SCHEMA COMPLETO
-- Esquema de base de datos completo para ARIA
-- Incluye todas las tablas necesarias para el funcionamiento completo
-- Ejecutar en el SQL Editor de Supabase

-- 📚 TABLA DE CONOCIMIENTO PRINCIPAL
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

-- 🧠 TABLA DE EMBEDDINGS PARA BÚSQUEDA SEMÁNTICA
CREATE TABLE IF NOT EXISTS public.aria_embeddings (
    id SERIAL PRIMARY KEY,
    texto TEXT NOT NULL,
    embedding VECTOR(384), -- Para all-MiniLM-L6-v2
    categoria VARCHAR(100) DEFAULT 'general',
    origen VARCHAR(255) DEFAULT 'conversation',
    metadata JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 🔗 TABLA DE VECTORES DE CONOCIMIENTO
CREATE TABLE IF NOT EXISTS public.aria_knowledge_vectors (
    id SERIAL PRIMARY KEY,
    concept VARCHAR(255) NOT NULL,
    description_vector VECTOR(384),
    categoria VARCHAR(100) DEFAULT 'general',
    confidence REAL DEFAULT 0.5,
    metadata JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    FOREIGN KEY (concept) REFERENCES aria_knowledge(concept) ON DELETE CASCADE
);

-- 💬 TABLA DE CONVERSACIONES
CREATE TABLE IF NOT EXISTS public.aria_conversations (
    id SERIAL PRIMARY KEY,
    session_id VARCHAR(255) NOT NULL,
    user_input TEXT NOT NULL,
    aria_response TEXT NOT NULL,
    response_time REAL DEFAULT 0,
    confidence REAL DEFAULT 0.5,
    emotion_user VARCHAR(100),
    emotion_aria VARCHAR(100),
    knowledge_accessed TEXT[],
    apis_used TEXT[],
    learning_active BOOLEAN DEFAULT false,
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 🔌 TABLA DE RELACIONES DE APIs
CREATE TABLE IF NOT EXISTS public.aria_api_relations (
    id SERIAL PRIMARY KEY,
    api_name VARCHAR(255) NOT NULL,
    base_url VARCHAR(500),
    description TEXT,
    endpoints JSONB,
    authentication_type VARCHAR(100),
    confidence REAL DEFAULT 0.5,
    discovery_method VARCHAR(100),
    last_verified TIMESTAMP WITH TIME ZONE,
    status VARCHAR(50) DEFAULT 'active',
    metadata JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 🎓 TABLA DE SESIONES DE APRENDIZAJE
CREATE TABLE IF NOT EXISTS public.aria_learning_sessions (
    id SERIAL PRIMARY KEY,
    session_id VARCHAR(255) NOT NULL,
    topic VARCHAR(255),
    source_type VARCHAR(100),
    knowledge_gained INTEGER DEFAULT 0,
    concepts_learned TEXT[],
    apis_discovered INTEGER DEFAULT 0,
    session_duration REAL DEFAULT 0,
    success_indicators JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 🔍 TABLA DE APIs DESCUBIERTAS
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
    metadata JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 🔗 TABLA DE RELACIONES ENTRE CONCEPTOS
CREATE TABLE IF NOT EXISTS public.aria_concept_relations (
    id SERIAL PRIMARY KEY,
    concept_a VARCHAR(255) NOT NULL,
    concept_b VARCHAR(255) NOT NULL,
    relation_type VARCHAR(100) DEFAULT 'related',
    strength REAL DEFAULT 0.5 CHECK (strength >= 0 AND strength <= 1),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(concept_a, concept_b)
);

-- 🎭 TABLA DE EMOCIONES (Si no existe ya)
CREATE TABLE IF NOT EXISTS public.aria_emotions (
    id SERIAL PRIMARY KEY,
    concept VARCHAR(255) NOT NULL,
    description TEXT,
    category VARCHAR(100) DEFAULT 'emotion_mapping',
    confidence REAL DEFAULT 0.8,
    source VARCHAR(255) DEFAULT 'system',
    tags TEXT[],
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 📊 TABLA DE MÉTRICAS Y ESTADÍSTICAS
CREATE TABLE IF NOT EXISTS public.aria_metrics (
    id SERIAL PRIMARY KEY,
    session_id VARCHAR(255),
    metric_type VARCHAR(100) NOT NULL,
    metric_value REAL,
    metric_data JSONB,
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 🗂️ TABLA RESUMEN DE CONOCIMIENTO
CREATE TABLE IF NOT EXISTS public.aria_knowledge_summary (
    id SERIAL PRIMARY KEY,
    category VARCHAR(100) NOT NULL,
    concept_count INTEGER DEFAULT 0,
    average_confidence REAL DEFAULT 0.5,
    last_updated TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    summary_data JSONB
);

-- 📝 CREAR ÍNDICES PARA MEJORAR PERFORMANCE

-- Índices para aria_knowledge
CREATE INDEX IF NOT EXISTS idx_aria_knowledge_concept ON public.aria_knowledge(concept);
CREATE INDEX IF NOT EXISTS idx_aria_knowledge_category ON public.aria_knowledge(category);
CREATE INDEX IF NOT EXISTS idx_aria_knowledge_confidence ON public.aria_knowledge(confidence);

-- Índices para aria_embeddings
CREATE INDEX IF NOT EXISTS idx_aria_embeddings_categoria ON public.aria_embeddings(categoria);
CREATE INDEX IF NOT EXISTS idx_aria_embeddings_origen ON public.aria_embeddings(origen);

-- Índices para aria_knowledge_vectors
CREATE INDEX IF NOT EXISTS idx_aria_knowledge_vectors_concept ON public.aria_knowledge_vectors(concept);
CREATE INDEX IF NOT EXISTS idx_aria_knowledge_vectors_categoria ON public.aria_knowledge_vectors(categoria);

-- Índices para aria_conversations
CREATE INDEX IF NOT EXISTS idx_aria_conversations_session ON public.aria_conversations(session_id);
CREATE INDEX IF NOT EXISTS idx_aria_conversations_timestamp ON public.aria_conversations(timestamp);
CREATE INDEX IF NOT EXISTS idx_aria_conversations_learning ON public.aria_conversations(learning_active);

-- Índices para aria_api_relations
CREATE INDEX IF NOT EXISTS idx_aria_api_relations_name ON public.aria_api_relations(api_name);
CREATE INDEX IF NOT EXISTS idx_aria_api_relations_status ON public.aria_api_relations(status);

-- Índices para aria_learning_sessions
CREATE INDEX IF NOT EXISTS idx_aria_learning_session_id ON public.aria_learning_sessions(session_id);
CREATE INDEX IF NOT EXISTS idx_aria_learning_topic ON public.aria_learning_sessions(topic);

-- Índices para aria_discovered_apis
CREATE INDEX IF NOT EXISTS idx_aria_discovered_apis_name ON public.aria_discovered_apis(api_name);

-- Índices para aria_emotions
CREATE INDEX IF NOT EXISTS idx_aria_emotions_concept ON public.aria_emotions(concept);
CREATE INDEX IF NOT EXISTS idx_aria_emotions_category ON public.aria_emotions(category);

-- Índices para aria_metrics
CREATE INDEX IF NOT EXISTS idx_aria_metrics_session ON public.aria_metrics(session_id);
CREATE INDEX IF NOT EXISTS idx_aria_metrics_type ON public.aria_metrics(metric_type);
CREATE INDEX IF NOT EXISTS idx_aria_metrics_timestamp ON public.aria_metrics(timestamp);

-- 📊 INSERTAR DATOS INICIALES

-- Conocimiento básico
INSERT INTO public.aria_knowledge (concept, description, category, confidence, source) VALUES
('saludo', 'Forma de iniciar una conversación de manera amigable', 'social', 0.9, 'system'),
('inteligencia_artificial', 'Campo de la informática que busca crear sistemas que puedan realizar tareas que requieren inteligencia humana', 'tecnologia', 0.9, 'system'),
('python', 'Lenguaje de programación de alto nivel, interpretado y de propósito general', 'programacion', 0.9, 'system'),
('supabase', 'Plataforma de base de datos como servicio basada en PostgreSQL', 'tecnologia', 0.8, 'system'),
('google_cloud', 'Plataforma de servicios en la nube de Google', 'tecnologia', 0.8, 'system'),
('caracas', 'Capital y ciudad más poblada de Venezuela, centro político y económico del país', 'geografia', 0.9, 'system'),
('venezuela', 'País sudamericano conocido por sus recursos naturales y diversidad geográfica', 'geografia', 0.9, 'system'),
('emotion_system_config', 'Configuración del sistema de detección emocional de ARIA', 'system_config', 1.0, 'system')
ON CONFLICT (concept) DO UPDATE SET
    description = EXCLUDED.description,
    confidence = EXCLUDED.confidence,
    updated_at = NOW();

-- Emociones básicas
INSERT INTO public.aria_emotions (concept, description, category, confidence) VALUES
('alegria', 'Estado emocional positivo caracterizado por sentimientos de felicidad', 'emotion_mapping', 0.9),
('tristeza', 'Estado emocional caracterizado por sentimientos de melancolía', 'emotion_mapping', 0.9),
('enojo', 'Estado emocional de irritación o molestia', 'emotion_mapping', 0.8),
('miedo', 'Estado emocional de ansiedad ante una amenaza', 'emotion_mapping', 0.8),
('sorpresa', 'Estado emocional ante algo inesperado', 'emotion_mapping', 0.8),
('neutral', 'Estado emocional equilibrado sin tendencias marcadas', 'emotion_mapping', 0.9),
('curiosidad', 'Estado emocional de interés por aprender', 'emotion_mapping', 0.8),
('confianza', 'Estado emocional de seguridad y certeza', 'emotion_mapping', 0.8),
('thinking', 'Estado cognitivo de procesamiento y análisis', 'emotion_mapping', 0.8),
('excited', 'Estado emocional de alta energía y entusiasmo', 'emotion_mapping', 0.8)
ON CONFLICT (concept) DO UPDATE SET
    description = EXCLUDED.description,
    confidence = EXCLUDED.confidence,
    updated_at = NOW();

-- APIs predeterminadas
INSERT INTO public.aria_api_relations (api_name, base_url, description, endpoints, confidence, status) VALUES
('google_translate', 'https://translate.googleapis.com/translate_a/single', 'API de Google Translate para traducción de texto', '{"translate": "/translate_a/single"}', 0.9, 'active'),
('openweather', 'https://api.openweathermap.org/data/2.5', 'API del clima de OpenWeatherMap', '{"weather": "/weather", "forecast": "/forecast"}', 0.8, 'active'),
('spanish_apis', 'http://localhost:8001', 'APIs españolas locales para información específica', '{"search": "/search", "translate": "/translate"}', 0.7, 'active')
ON CONFLICT (api_name) DO UPDATE SET
    description = EXCLUDED.description,
    endpoints = EXCLUDED.endpoints,
    confidence = EXCLUDED.confidence;

-- Relaciones entre conceptos
INSERT INTO public.aria_concept_relations (concept_a, concept_b, relation_type, strength) VALUES
('python', 'programacion', 'subcategory', 0.9),
('supabase', 'base_de_datos', 'type_of', 0.8),
('google_cloud', 'inteligencia_artificial', 'provides', 0.7),
('inteligencia_artificial', 'python', 'implemented_in', 0.8),
('caracas', 'venezuela', 'capital_of', 0.9),
('venezuela', 'sudamerica', 'located_in', 0.9)
ON CONFLICT (concept_a, concept_b) DO NOTHING;

-- Resúmenes de conocimiento
INSERT INTO public.aria_knowledge_summary (category, concept_count, average_confidence) VALUES
('tecnologia', 3, 0.85),
('programacion', 1, 0.9),
('social', 1, 0.9),
('geografia', 2, 0.9),
('emotion_mapping', 10, 0.85)
ON CONFLICT (category) DO UPDATE SET
    concept_count = EXCLUDED.concept_count,
    average_confidence = EXCLUDED.average_confidence,
    last_updated = NOW();

-- 🔍 VERIFICAR QUE TODAS LAS TABLAS SE CREARON CORRECTAMENTE
SELECT 
    'aria_knowledge' as tabla, 
    COUNT(*) as registros,
    'Conocimiento principal' as descripcion
FROM public.aria_knowledge
UNION ALL
SELECT 'aria_embeddings', COUNT(*), 'Embeddings para búsqueda semántica' FROM public.aria_embeddings
UNION ALL
SELECT 'aria_knowledge_vectors', COUNT(*), 'Vectores de conocimiento' FROM public.aria_knowledge_vectors
UNION ALL
SELECT 'aria_conversations', COUNT(*), 'Historial de conversaciones' FROM public.aria_conversations
UNION ALL
SELECT 'aria_api_relations', COUNT(*), 'Relaciones de APIs' FROM public.aria_api_relations
UNION ALL
SELECT 'aria_learning_sessions', COUNT(*), 'Sesiones de aprendizaje' FROM public.aria_learning_sessions
UNION ALL
SELECT 'aria_discovered_apis', COUNT(*), 'APIs descubiertas' FROM public.aria_discovered_apis
UNION ALL
SELECT 'aria_concept_relations', COUNT(*), 'Relaciones entre conceptos' FROM public.aria_concept_relations
UNION ALL
SELECT 'aria_emotions', COUNT(*), 'Sistema de emociones' FROM public.aria_emotions
UNION ALL
SELECT 'aria_metrics', COUNT(*), 'Métricas y estadísticas' FROM public.aria_metrics
UNION ALL
SELECT 'aria_knowledge_summary', COUNT(*), 'Resúmenes de conocimiento' FROM public.aria_knowledge_summary
ORDER BY tabla;