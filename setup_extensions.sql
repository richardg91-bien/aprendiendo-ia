-- 🔧 CONFIGURACIÓN INICIAL DE SUPABASE PARA ARIA
-- Ejecutar PRIMERO en el SQL Editor de Supabase
-- Este script habilita las extensiones necesarias

-- Habilitar extensión para vectores (embeddings)
CREATE EXTENSION IF NOT EXISTS vector;

-- Habilitar extensión para texto completo
CREATE EXTENSION IF NOT EXISTS pg_trgm;

-- Habilitar extensión para UUID
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Verificar extensiones instaladas
SELECT 
    extname as "Extension", 
    extversion as "Version",
    'Habilitada' as "Status"
FROM pg_extension 
WHERE extname IN ('vector', 'pg_trgm', 'uuid-ossp')
ORDER BY extname;