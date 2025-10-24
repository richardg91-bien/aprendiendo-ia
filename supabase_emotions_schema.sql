-- 🎨 ARIA FUTURISTIC INTERFACE - TABLAS ADICIONALES PARA EMOCIONES
-- ================================================================
-- Ejecuta este SQL ADICIONAL en Supabase para soportar la interfaz moderna

-- Tabla de emociones de ARIA
CREATE TABLE IF NOT EXISTS aria_emotions (
    id SERIAL PRIMARY KEY,
    session_id VARCHAR(100) NOT NULL,
    emotion_type VARCHAR(50) NOT NULL,
    color_code VARCHAR(7) NOT NULL,  -- Código hexadecimal del color
    intensity FLOAT DEFAULT 0.5 CHECK (intensity >= 0 AND intensity <= 1),
    context TEXT,
    triggered_by VARCHAR(255),
    duration_seconds INTEGER DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Tabla de sesiones de usuario
CREATE TABLE IF NOT EXISTS aria_sessions (
    id SERIAL PRIMARY KEY,
    session_id VARCHAR(100) UNIQUE NOT NULL,
    user_id VARCHAR(100),
    start_time TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    end_time TIMESTAMP WITH TIME ZONE,
    total_messages INTEGER DEFAULT 0,
    avg_emotion_intensity FLOAT DEFAULT 0.5,
    dominant_emotion VARCHAR(50) DEFAULT 'neutral',
    knowledge_learned INTEGER DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Índices para emociones
CREATE INDEX IF NOT EXISTS idx_aria_emotions_session ON aria_emotions(session_id);
CREATE INDEX IF NOT EXISTS idx_aria_emotions_type ON aria_emotions(emotion_type);
CREATE INDEX IF NOT EXISTS idx_aria_emotions_created ON aria_emotions(created_at DESC);

-- Índices para sesiones
CREATE INDEX IF NOT EXISTS idx_aria_sessions_user ON aria_sessions(user_id);
CREATE INDEX IF NOT EXISTS idx_aria_sessions_start ON aria_sessions(start_time DESC);

-- Vista para obtener emociones recientes
CREATE OR REPLACE VIEW aria_recent_emotions AS
SELECT 
    e.*,
    s.user_id
FROM aria_emotions e
LEFT JOIN aria_sessions s ON e.session_id = s.session_id
ORDER BY e.created_at DESC
LIMIT 50;

-- Insertar emociones de ejemplo
INSERT INTO aria_emotions (session_id, emotion_type, color_code, intensity, context, triggered_by) VALUES
('demo-session', 'neutral', '#0080FF', 0.5, 'Estado inicial', 'system_start'),
('demo-session', 'learning', '#00FF00', 0.8, 'Aprendiendo algo nuevo', 'knowledge_acquisition'),
('demo-session', 'happy', '#FFD700', 0.9, 'Respuesta exitosa', 'successful_interaction'),
('demo-session', 'thinking', '#8A2BE2', 0.7, 'Procesando información compleja', 'complex_query'),
('demo-session', 'excited', '#FF69B4', 0.8, 'Descubrimiento interesante', 'interesting_topic')
ON CONFLICT DO NOTHING;

-- Función para registrar emociones automáticamente
CREATE OR REPLACE FUNCTION log_aria_emotion(
    p_session_id VARCHAR(100),
    p_emotion_type VARCHAR(50),
    p_color_code VARCHAR(7),
    p_intensity FLOAT DEFAULT 0.5,
    p_context TEXT DEFAULT NULL,
    p_triggered_by VARCHAR(255) DEFAULT NULL
)
RETURNS INTEGER AS $$
DECLARE
    emotion_id INTEGER;
BEGIN
    INSERT INTO aria_emotions (session_id, emotion_type, color_code, intensity, context, triggered_by)
    VALUES (p_session_id, p_emotion_type, p_color_code, p_intensity, p_context, p_triggered_by)
    RETURNING id INTO emotion_id;
    
    RETURN emotion_id;
END;
$$ LANGUAGE plpgsql;

-- Función para obtener emociones recientes de una sesión
CREATE OR REPLACE FUNCTION get_recent_emotions(p_session_id VARCHAR(100), p_limit INTEGER DEFAULT 10)
RETURNS TABLE (
    id INTEGER,
    emotion_type VARCHAR(50),
    color_code VARCHAR(7),
    intensity FLOAT,
    context TEXT,
    created_at TIMESTAMP WITH TIME ZONE
) AS $$
BEGIN
    RETURN QUERY
    SELECT e.id, e.emotion_type, e.color_code, e.intensity, e.context, e.created_at
    FROM aria_emotions e
    WHERE e.session_id = p_session_id
    ORDER BY e.created_at DESC
    LIMIT p_limit;
END;
$$ LANGUAGE plpgsql;

-- Verificación
DO $$
BEGIN
    RAISE NOTICE '🎨 Tablas para interfaz futurística creadas exitosamente';
    RAISE NOTICE '📊 Nuevas tablas: aria_emotions, aria_sessions';
    RAISE NOTICE '🌈 Soporte para emociones con cambios de color activado';
    RAISE NOTICE '🚀 Interfaz moderna lista para usar';
END $$;