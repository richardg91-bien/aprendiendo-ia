-- 🔧 CORRECCIÓN ESPECÍFICA PARA aria_conversations
-- ================================================
-- Ejecutar en SQL Editor de Supabase

-- 1. Verificar estructura actual de aria_conversations
SELECT column_name, data_type, is_nullable 
FROM information_schema.columns 
WHERE table_name = 'aria_conversations' 
AND table_schema = 'public'
ORDER BY ordinal_position;

-- 2. Agregar columnas faltantes si no existen
ALTER TABLE public.aria_conversations 
ADD COLUMN IF NOT EXISTS user_emotion VARCHAR(50) DEFAULT 'neutral';

ALTER TABLE public.aria_conversations 
ADD COLUMN IF NOT EXISTS aria_emotion VARCHAR(50) DEFAULT 'helpful';

-- 3. Verificar que se agregaron correctamente
SELECT column_name, data_type, column_default 
FROM information_schema.columns 
WHERE table_name = 'aria_conversations' 
AND table_schema = 'public'
AND column_name IN ('user_emotion', 'aria_emotion');

-- 4. Actualizar registros existentes si tienen valores NULL
UPDATE public.aria_conversations 
SET user_emotion = 'curious' 
WHERE user_emotion IS NULL;

UPDATE public.aria_conversations 
SET aria_emotion = 'helpful' 
WHERE aria_emotion IS NULL;

-- 5. Verificar el resultado final
SELECT 
    id, 
    user_message, 
    user_emotion, 
    aria_emotion, 
    created_at 
FROM public.aria_conversations 
ORDER BY created_at DESC 
LIMIT 5;