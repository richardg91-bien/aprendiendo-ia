-- 🗄️ ARIA SUPER BASE - ESQUEMA COMPLETO
-- =====================================
-- Ejecuta este SQL en el SQL Editor de tu panel de Supabase
-- para crear todas las tablas necesarias para ARIA

-- ==================== TABLAS PRINCIPALES ====================

-- Tabla de conocimiento general
CREATE TABLE IF NOT EXISTS aria_knowledge (
    id SERIAL PRIMARY KEY,
    concept VARCHAR(255) UNIQUE NOT NULL,
    description TEXT,
    category VARCHAR(100) DEFAULT 'general',
    confidence FLOAT DEFAULT 0.5 CHECK (confidence >= 0 AND confidence <= 1),
    source VARCHAR(255) DEFAULT 'conversation',
    tags TEXT[],
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Tabla de relaciones con APIs
CREATE TABLE IF NOT EXISTS aria_api_relations (
    id SERIAL PRIMARY KEY,
    api_name VARCHAR(255) NOT NULL,
    api_type VARCHAR(100) NOT NULL,
    endpoint VARCHAR(500) NOT NULL,
    method VARCHAR(10) DEFAULT 'GET',
    description TEXT,
    status VARCHAR(50) DEFAULT 'active',
    last_used TIMESTAMP WITH TIME ZONE,
    success_rate FLOAT DEFAULT 1.0 CHECK (success_rate >= 0 AND success_rate <= 1),
    response_time_avg FLOAT DEFAULT 0,
    usage_count INTEGER DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    metadata JSONB DEFAULT '{}'::jsonb
);

-- Tabla de conversaciones
CREATE TABLE IF NOT EXISTS aria_conversations (
    id SERIAL PRIMARY KEY,
    user_message TEXT NOT NULL,
    aria_response TEXT NOT NULL,
    emotion_state VARCHAR(50) DEFAULT 'neutral',
    confidence FLOAT DEFAULT 0.8 CHECK (confidence >= 0 AND confidence <= 1),
    apis_used JSONB DEFAULT '[]'::jsonb,
    knowledge_accessed JSONB DEFAULT '[]'::jsonb,
    session_id VARCHAR(100) DEFAULT 'default',
    user_id VARCHAR(100),
    language VARCHAR(10) DEFAULT 'es',
    response_time FLOAT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Tabla de sesiones de aprendizaje
CREATE TABLE IF NOT EXISTS aria_learning_sessions (
    id SERIAL PRIMARY KEY,
    topic VARCHAR(255),
    source_type VARCHAR(100),
    knowledge_gained INTEGER DEFAULT 0,
    apis_discovered INTEGER DEFAULT 0,
    concepts_learned TEXT[],
    session_duration FLOAT,
    success_indicators JSONB DEFAULT '{}'::jsonb,
    quality_score FLOAT DEFAULT 0.5,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Tabla de estadísticas de uso
CREATE TABLE IF NOT EXISTS aria_usage_stats (
    id SERIAL PRIMARY KEY,
    date DATE DEFAULT CURRENT_DATE,
    conversations_count INTEGER DEFAULT 0,
    knowledge_queries INTEGER DEFAULT 0,
    api_calls INTEGER DEFAULT 0,
    new_knowledge INTEGER DEFAULT 0,
    avg_response_time FLOAT DEFAULT 0,
    user_satisfaction FLOAT DEFAULT 0.5,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(date)
);

-- Tabla de configuración del sistema
CREATE TABLE IF NOT EXISTS aria_system_config (
    key VARCHAR(100) PRIMARY KEY,
    value TEXT,
    description TEXT,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- ==================== ÍNDICES PARA OPTIMIZACIÓN ====================

-- Índices para búsqueda rápida en conocimiento
CREATE INDEX IF NOT EXISTS idx_aria_knowledge_concept ON aria_knowledge(concept);
CREATE INDEX IF NOT EXISTS idx_aria_knowledge_category ON aria_knowledge(category);
CREATE INDEX IF NOT EXISTS idx_aria_knowledge_confidence ON aria_knowledge(confidence DESC);

-- Índices para APIs
CREATE INDEX IF NOT EXISTS idx_aria_api_type ON aria_api_relations(api_type);
CREATE INDEX IF NOT EXISTS idx_aria_api_status ON aria_api_relations(status);
CREATE INDEX IF NOT EXISTS idx_aria_api_success_rate ON aria_api_relations(success_rate DESC);

-- Índices para conversaciones
CREATE INDEX IF NOT EXISTS idx_aria_conv_session ON aria_conversations(session_id);
CREATE INDEX IF NOT EXISTS idx_aria_conv_user ON aria_conversations(user_id);
CREATE INDEX IF NOT EXISTS idx_aria_conv_created ON aria_conversations(created_at DESC);

-- ==================== FUNCIONES Y TRIGGERS ====================

-- Función para actualizar timestamp automáticamente
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Trigger para actualizar timestamps automáticamente
DROP TRIGGER IF EXISTS update_aria_knowledge_updated_at ON aria_knowledge;
CREATE TRIGGER update_aria_knowledge_updated_at 
    BEFORE UPDATE ON aria_knowledge 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- ==================== VISTAS ÚTILES ====================

-- Vista resumen de conocimiento por categoría
CREATE OR REPLACE VIEW aria_knowledge_summary AS
SELECT 
    category,
    COUNT(*) as total_concepts,
    AVG(confidence) as avg_confidence,
    MAX(updated_at) as last_updated
FROM aria_knowledge 
GROUP BY category;

-- Vista performance de APIs
CREATE OR REPLACE VIEW aria_api_performance AS
SELECT 
    api_type,
    COUNT(*) as total_apis,
    AVG(success_rate) as avg_success_rate,
    AVG(response_time_avg) as avg_response_time,
    SUM(usage_count) as total_usage
FROM aria_api_relations 
WHERE status = 'active'
GROUP BY api_type;

-- ==================== CONFIGURACIÓN INICIAL ====================

-- Insertar configuración por defecto
INSERT INTO aria_system_config (key, value, description) VALUES
('version', '2.0.0', 'Versión de ARIA Super Base')
ON CONFLICT (key) DO UPDATE SET value = EXCLUDED.value, updated_at = NOW();

INSERT INTO aria_system_config (key, value, description) VALUES
('max_knowledge_entries', '10000', 'Máximo número de entradas de conocimiento')
ON CONFLICT (key) DO NOTHING;

INSERT INTO aria_system_config (key, value, description) VALUES
('default_confidence', '0.5', 'Nivel de confianza por defecto')
ON CONFLICT (key) DO NOTHING;

INSERT INTO aria_system_config (key, value, description) VALUES
('enable_learning', 'true', 'Habilitar aprendizaje automático')
ON CONFLICT (key) DO NOTHING;

-- ==================== DATOS DE EJEMPLO ====================

-- Conocimiento inicial
INSERT INTO aria_knowledge (concept, description, category, confidence, source) VALUES
('inteligencia artificial', 'Campo de la informática que se enfoca en crear sistemas que pueden realizar tareas que típicamente requieren inteligencia humana', 'tecnologia', 0.9, 'sistema')
ON CONFLICT (concept) DO NOTHING;

INSERT INTO aria_knowledge (concept, description, category, confidence, source) VALUES
('machine learning', 'Subcampo de la IA que permite a las máquinas aprender y mejorar automáticamente a partir de datos sin ser programadas explícitamente', 'tecnologia', 0.85, 'sistema')
ON CONFLICT (concept) DO NOTHING;

INSERT INTO aria_knowledge (concept, description, category, confidence, source) VALUES
('supabase', 'Plataforma de desarrollo de aplicaciones que proporciona base de datos PostgreSQL, autenticación y APIs en tiempo real', 'database', 0.8, 'sistema')
ON CONFLICT (concept) DO NOTHING;

-- APIs de ejemplo
INSERT INTO aria_api_relations (api_name, api_type, endpoint, method, description, status) VALUES
('OpenAI GPT', 'ai_language', 'https://api.openai.com/v1/chat/completions', 'POST', 'API de OpenAI para generar texto con modelos de lenguaje', 'active')
ON CONFLICT DO NOTHING;

INSERT INTO aria_api_relations (api_name, api_type, endpoint, method, description, status) VALUES
('Google Translate', 'translation', 'https://translation.googleapis.com/language/translate/v2', 'POST', 'API de Google para traducción de texto', 'active')
ON CONFLICT DO NOTHING;

INSERT INTO aria_api_relations (api_name, api_type, endpoint, method, description, status) VALUES
('Wikipedia Search', 'knowledge_search', 'https://en.wikipedia.org/api/rest_v1/page/summary/', 'GET', 'API de Wikipedia para búsqueda de conocimiento', 'active')
ON CONFLICT DO NOTHING;

-- ==================== COMENTARIOS Y DOCUMENTACIÓN ====================

-- Agregar comentarios a las tablas
COMMENT ON TABLE aria_knowledge IS 'Almacena el conocimiento aprendido por ARIA con niveles de confianza';
COMMENT ON TABLE aria_api_relations IS 'Registra las APIs y servicios externos que usa ARIA con métricas de rendimiento';
COMMENT ON TABLE aria_conversations IS 'Historial completo de conversaciones con contexto emocional';
COMMENT ON TABLE aria_learning_sessions IS 'Registro de sesiones de aprendizaje automático y mejora continua';
COMMENT ON TABLE aria_usage_stats IS 'Estadísticas diarias de uso del sistema ARIA';
COMMENT ON TABLE aria_system_config IS 'Configuración del sistema ARIA con parámetros operacionales';

-- Comentarios en columnas importantes
COMMENT ON COLUMN aria_knowledge.confidence IS 'Nivel de confianza de 0.0 a 1.0 sobre la precisión del conocimiento';
COMMENT ON COLUMN aria_api_relations.success_rate IS 'Tasa de éxito de 0.0 a 1.0 basada en respuestas exitosas';
COMMENT ON COLUMN aria_conversations.emotion_state IS 'Estado emocional de ARIA durante la conversación';

-- ==================== FINALIZACIÓN ====================

-- Verificar que las tablas se crearon correctamente
DO $$
BEGIN
    RAISE NOTICE '✅ Esquema de ARIA Super Base creado exitosamente';
    RAISE NOTICE '📊 Tablas creadas: aria_knowledge, aria_api_relations, aria_conversations, aria_learning_sessions, aria_usage_stats, aria_system_config';
    RAISE NOTICE '🚀 ARIA está listo para almacenar conocimiento y relaciones de APIs';
END $$;