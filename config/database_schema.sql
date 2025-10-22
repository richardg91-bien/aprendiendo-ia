-- Esquema de base de datos para Supabase
-- Crea estas tablas en tu proyecto de Supabase

-- Tabla para conversaciones
CREATE TABLE conversations (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMPTZ DEFAULT NOW(),
    session_id VARCHAR(50),
    user_message TEXT NOT NULL,
    aria_response TEXT NOT NULL,
    user_feedback TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Tabla para preferencias de usuario
CREATE TABLE user_preferences (
    id SERIAL PRIMARY KEY,
    preference_type VARCHAR(100) NOT NULL,
    value TEXT NOT NULL,
    timestamp TIMESTAMPTZ DEFAULT NOW(),
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Tabla para métricas de aprendizaje
CREATE TABLE learning_metrics (
    id SERIAL PRIMARY KEY,
    metric_name VARCHAR(100) NOT NULL,
    metric_value DECIMAL(10,2),
    timestamp TIMESTAMPTZ DEFAULT NOW(),
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Tabla para conceptos aprendidos
CREATE TABLE learned_concepts (
    id SERIAL PRIMARY KEY,
    concept VARCHAR(200) NOT NULL,
    definition TEXT NOT NULL,
    confidence_score DECIMAL(3,2) DEFAULT 0.5,
    usage_count INTEGER DEFAULT 0,
    last_used TIMESTAMPTZ DEFAULT NOW(),
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Índices para mejorar performance
CREATE INDEX idx_conversations_timestamp ON conversations(timestamp);
CREATE INDEX idx_conversations_session ON conversations(session_id);
CREATE INDEX idx_preferences_type ON user_preferences(preference_type);
CREATE INDEX idx_concepts_concept ON learned_concepts(concept);

-- Habilitar Row Level Security (RLS)
ALTER TABLE conversations ENABLE ROW LEVEL SECURITY;
ALTER TABLE user_preferences ENABLE ROW LEVEL SECURITY;
ALTER TABLE learning_metrics ENABLE ROW LEVEL SECURITY;
ALTER TABLE learned_concepts ENABLE ROW LEVEL SECURITY;

-- Políticas básicas (ajustar según necesidades)
CREATE POLICY "Enable insert for all users" ON conversations FOR INSERT WITH CHECK (true);
CREATE POLICY "Enable select for all users" ON conversations FOR SELECT USING (true);

CREATE POLICY "Enable insert for all users" ON user_preferences FOR INSERT WITH CHECK (true);
CREATE POLICY "Enable select for all users" ON user_preferences FOR SELECT USING (true);

CREATE POLICY "Enable insert for all users" ON learning_metrics FOR INSERT WITH CHECK (true);
CREATE POLICY "Enable select for all users" ON learning_metrics FOR SELECT USING (true);

CREATE POLICY "Enable insert for all users" ON learned_concepts FOR INSERT WITH CHECK (true);
CREATE POLICY "Enable select for all users" ON learned_concepts FOR SELECT USING (true);
CREATE POLICY "Enable update for all users" ON learned_concepts FOR UPDATE USING (true);