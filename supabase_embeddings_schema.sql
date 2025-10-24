-- 🧠 ARIA EMBEDDINGS - ESQUEMA PARA SUPABASE
-- ==========================================
-- Ejecuta este SQL en tu panel de Supabase para crear las tablas de embeddings

-- Habilitar la extensión vector para embeddings
CREATE EXTENSION IF NOT EXISTS vector;

-- Tabla principal para almacenar embeddings y textos
CREATE TABLE IF NOT EXISTS aria_embeddings (
    id SERIAL PRIMARY KEY,
    texto TEXT NOT NULL,
    embedding vector(384), -- 384 dimensiones para all-MiniLM-L6-v2
    categoria VARCHAR(100) DEFAULT 'general',
    subcategoria VARCHAR(100),
    fuente VARCHAR(255) DEFAULT 'conversation',
    idioma VARCHAR(10) DEFAULT 'es',
    metadatos JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Índice para búsqueda vectorial rápida
CREATE INDEX IF NOT EXISTS aria_embeddings_vector_idx 
ON aria_embeddings USING ivfflat (embedding vector_cosine_ops) 
WITH (lists = 100);

-- Índice para categorías
CREATE INDEX IF NOT EXISTS aria_embeddings_categoria_idx 
ON aria_embeddings (categoria);

-- Índice para búsqueda de texto
CREATE INDEX IF NOT EXISTS aria_embeddings_texto_idx 
ON aria_embeddings USING gin (to_tsvector('spanish', texto));

-- Tabla para guardar conocimiento estructurado con embeddings
CREATE TABLE IF NOT EXISTS aria_knowledge_vectors (
    id SERIAL PRIMARY KEY,
    concepto VARCHAR(255) NOT NULL,
    descripcion TEXT,
    embedding vector(384),
    categoria VARCHAR(100) DEFAULT 'knowledge',
    tags TEXT[],
    confianza FLOAT DEFAULT 0.8 CHECK (confianza >= 0 AND confianza <= 1),
    ejemplos JSONB DEFAULT '[]'::jsonb,
    relaciones JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Índice vectorial para knowledge
CREATE INDEX IF NOT EXISTS aria_knowledge_vector_idx 
ON aria_knowledge_vectors USING ivfflat (embedding vector_cosine_ops) 
WITH (lists = 50);

-- Tabla para embeddings de documentos completos
CREATE TABLE IF NOT EXISTS aria_documents (
    id SERIAL PRIMARY KEY,
    titulo VARCHAR(255) NOT NULL,
    contenido TEXT NOT NULL,
    resumen TEXT,
    embedding_titulo vector(384),
    embedding_contenido vector(384),
    tipo VARCHAR(50) DEFAULT 'document',
    archivo_origen VARCHAR(255),
    tamano_bytes INTEGER,
    procesado BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Función para búsqueda semántica
CREATE OR REPLACE FUNCTION buscar_similares(
    query_embedding vector(384),
    limite INTEGER DEFAULT 5,
    umbral_similitud FLOAT DEFAULT 0.7
)
RETURNS TABLE(
    id INTEGER,
    texto TEXT,
    categoria VARCHAR(100),
    similitud FLOAT
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        e.id,
        e.texto,
        e.categoria,
        (1 - (e.embedding <=> query_embedding)) as similitud
    FROM aria_embeddings e
    WHERE (1 - (e.embedding <=> query_embedding)) > umbral_similitud
    ORDER BY e.embedding <=> query_embedding
    LIMIT limite;
END;
$$ LANGUAGE plpgsql;

-- Función para buscar conocimiento relacionado
CREATE OR REPLACE FUNCTION buscar_conocimiento_relacionado(
    query_embedding vector(384),
    limite INTEGER DEFAULT 3
)
RETURNS TABLE(
    id INTEGER,
    concepto VARCHAR(255),
    descripcion TEXT,
    similitud FLOAT
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        k.id,
        k.concepto,
        k.descripcion,
        (1 - (k.embedding <=> query_embedding)) as similitud
    FROM aria_knowledge_vectors k
    ORDER BY k.embedding <=> query_embedding
    LIMIT limite;
END;
$$ LANGUAGE plpgsql;

-- Trigger para actualizar updated_at automáticamente
CREATE OR REPLACE FUNCTION actualizar_timestamp()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER aria_embeddings_update_timestamp
    BEFORE UPDATE ON aria_embeddings
    FOR EACH ROW
    EXECUTE FUNCTION actualizar_timestamp();

CREATE TRIGGER aria_knowledge_vectors_update_timestamp
    BEFORE UPDATE ON aria_knowledge_vectors
    FOR EACH ROW
    EXECUTE FUNCTION actualizar_timestamp();

-- Vista para estadísticas de embeddings
CREATE OR REPLACE VIEW aria_embeddings_stats AS
SELECT 
    categoria,
    COUNT(*) as total_embeddings,
    AVG(LENGTH(texto)) as longitud_promedio_texto,
    MIN(created_at) as primer_embedding,
    MAX(created_at) as ultimo_embedding
FROM aria_embeddings
GROUP BY categoria;

COMMENT ON TABLE aria_embeddings IS 'Almacena textos y sus embeddings para búsqueda semántica';
COMMENT ON TABLE aria_knowledge_vectors IS 'Conocimiento estructurado con embeddings para ARIA';
COMMENT ON TABLE aria_documents IS 'Documentos completos con embeddings de título y contenido';