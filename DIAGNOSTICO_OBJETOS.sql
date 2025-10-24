-- 🔍 DIAGNÓSTICO DE OBJETOS EXISTENTES EN SUPABASE
-- ================================================
-- Ejecutar ANTES de corregir las tablas

-- 1. Ver todos los objetos relacionados con ARIA
SELECT 
    schemaname,
    tablename as object_name,
    'TABLE' as object_type
FROM pg_tables 
WHERE tablename LIKE 'aria_%'

UNION ALL

SELECT 
    schemaname,
    viewname as object_name,
    'VIEW' as object_type
FROM pg_views 
WHERE viewname LIKE 'aria_%'

UNION ALL

SELECT 
    n.nspname as schemaname,
    p.proname as object_name,
    'FUNCTION' as object_type
FROM pg_proc p
JOIN pg_namespace n ON p.pronamespace = n.oid
WHERE p.proname LIKE 'aria_%'

ORDER BY object_type, object_name;

-- 2. Verificar específicamente aria_knowledge_summary
SELECT 
    CASE 
        WHEN EXISTS (SELECT 1 FROM pg_tables WHERE tablename = 'aria_knowledge_summary') THEN 'TABLE'
        WHEN EXISTS (SELECT 1 FROM pg_views WHERE viewname = 'aria_knowledge_summary') THEN 'VIEW'
        ELSE 'NOT_FOUND'
    END as aria_knowledge_summary_type;

-- 3. Si es una vista, mostrar su definición
SELECT definition 
FROM pg_views 
WHERE viewname = 'aria_knowledge_summary';