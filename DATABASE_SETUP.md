# 🗄️ Configuración de Base de Datos para ARIA

Esta carpeta contiene los archivos necesarios para configurar completamente la base de datos de ARIA en Supabase.

## 📋 Archivos Incluidos

- `setup_extensions.sql` - Configuración inicial de extensiones
- `schema_supabase_completo.sql` - Esquema completo de la base de datos  
- `setup_database.py` - Script automático de instalación
- `schema_supabase.sql` - Esquema básico original (para referencia)

## 🚀 Instalación Rápida

### Opción 1: Script Automático (Recomendado)
```bash
python setup_database.py
```

### Opción 2: Configuración Manual

1. **Configurar extensiones** (ejecutar primero):
   - Abre el SQL Editor en tu proyecto Supabase
   - Copia y pega el contenido de `setup_extensions.sql`
   - Ejecuta el script

2. **Crear esquema completo**:
   - En el mismo SQL Editor
   - Copia y pega el contenido de `schema_supabase_completo.sql`
   - Ejecuta el script completo

## 📊 Tablas Creadas

### Tablas Principales
- `aria_knowledge` - Conocimiento base de ARIA
- `aria_conversations` - Historial de conversaciones
- `aria_api_relations` - APIs conectadas
- `aria_learning_sessions` - Sesiones de aprendizaje

### Tablas de Embeddings
- `aria_embeddings` - Vectores semánticos para búsqueda
- `aria_knowledge_vectors` - Vectores de conocimiento específico

### Tablas Auxiliares
- `aria_emotions` - Sistema de emociones
- `aria_concept_relations` - Relaciones entre conceptos
- `aria_metrics` - Métricas y estadísticas
- `aria_knowledge_summary` - Resúmenes de conocimiento

## 🎯 Datos Iniciales

El esquema incluye datos precargados:

### Conocimiento Base
- Conceptos de tecnología (IA, Python, Supabase)
- Información geográfica (Caracas, Venezuela)
- Conceptos sociales básicos

### Sistema de Emociones
- 10+ emociones básicas configuradas
- Mapeos emocionales para respuestas naturales

### APIs Predeterminadas
- Google Translate
- OpenWeatherMap  
- APIs españolas locales

## 🔧 Características Técnicas

### Índices de Performance
- Índices optimizados para búsquedas rápidas
- Soporte para consultas complejas
- Optimización para embeddings

### Soporte para Vectores
- Extensión pgvector habilitada
- Vectores de 384 dimensiones (all-MiniLM-L6-v2)
- Búsqueda semántica optimizada

### Integridad de Datos
- Restricciones de integridad referencial
- Validaciones de tipos de datos
- Valores por defecto configurados

## 🐛 Solución de Problemas

### Error: "Could not find table"
```sql
-- Verificar que las tablas existen
SELECT table_name FROM information_schema.tables 
WHERE table_schema = 'public' 
AND table_name LIKE 'aria_%';
```

### Error: "Extension vector does not exist"
```sql
-- Crear extensión manualmente
CREATE EXTENSION IF NOT EXISTS vector;
```

### Error de Permisos
- Asegúrate de usar la clave de servicio correcta
- Verifica que tu usuario tiene permisos de escritura

## 📈 Verificación de Instalación

Después de la instalación, verifica que todo funciona:

```python
# Ejecutar desde el directorio principal
python test_full_flow.py
```

Deberías ver:
- ✅ Conexión a Supabase exitosa
- ✅ Tablas accesibles
- ✅ Respuestas de Caracas funcionando
- ✅ Sistema de embeddings operativo

## 🔄 Actualización

Para actualizar el esquema:

1. Respalda tus datos importantes
2. Ejecuta el nuevo esquema
3. Los comandos `ON CONFLICT` preservarán datos existentes

## 📞 Soporte

Si tienes problemas:

1. Revisa los logs de error en la consola
2. Verifica las credenciales en `.env`
3. Consulta la documentación de Supabase
4. Usa `MANUAL_SETUP_GUIDE.md` para configuración manual

---

🎉 **¡Una vez configurado, ARIA tendrá acceso completo a todas sus funciones avanzadas!**