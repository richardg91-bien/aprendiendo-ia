-- 🔧 SCRIPT DE CORRECCIÓN FINAL PERSONALIZADO
-- ============================================
-- Generado automáticamente después del diagnóstico

CREATE EXTENSION IF NOT EXISTS vector;

-- Verificación final
SELECT 'aria_embeddings' as tabla, count(*) as registros FROM public.aria_embeddings
UNION ALL
SELECT 'aria_knowledge_vectors' as tabla, count(*) as registros FROM public.aria_knowledge_vectors
UNION ALL
SELECT 'aria_concept_relations' as tabla, count(*) as registros FROM public.aria_concept_relations
UNION ALL
SELECT 'aria_knowledge_summary' as tabla, count(*) as registros FROM public.aria_knowledge_summary;