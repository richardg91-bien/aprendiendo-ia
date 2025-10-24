-- 📋 CONSULTAS ÚTILES PARA VER TABLAS EN SUPABASE

-- 1. Ver todas las tablas existentes
SELECT table_name 
FROM information_schema.tables 
WHERE table_schema = 'public' 
ORDER BY table_name;

-- 2. Ver estructura de una tabla específica
SELECT column_name, data_type, is_nullable 
FROM information_schema.columns 
WHERE table_name = 'aria_conversations' 
AND table_schema = 'public';

-- 3. Contar registros en cada tabla de ARIA
SELECT 'aria_conversations' as tabla, count(*) as registros FROM public.aria_conversations
UNION ALL
SELECT 'aria_knowledge' as tabla, count(*) as registros FROM public.aria_knowledge
UNION ALL
SELECT 'aria_api_relations' as tabla, count(*) as registros FROM public.aria_api_relations
UNION ALL
SELECT 'aria_emotions' as tabla, count(*) as registros FROM public.aria_emotions
UNION ALL
SELECT 'aria_knowledge_summary' as tabla, count(*) as registros FROM public.aria_knowledge_summary;

-- 4. Ver últimas conversaciones
SELECT id, user_message, aria_response, created_at 
FROM public.aria_conversations 
ORDER BY created_at DESC 
LIMIT 10;

-- 5. Ver conocimiento almacenado
SELECT concept, description, confidence 
FROM public.aria_knowledge 
ORDER BY confidence DESC 
LIMIT 20;

-- 6. Verificar si existen las tablas de embeddings
SELECT table_name 
FROM information_schema.tables 
WHERE table_schema = 'public' 
AND table_name IN ('aria_embeddings', 'aria_knowledge_vectors', 'aria_concept_relations');