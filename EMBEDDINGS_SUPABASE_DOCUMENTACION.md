# 🧠 SISTEMA DE EMBEDDINGS SUPABASE PARA ARIA
===============================================

## 📖 Descripción

Sistema de embeddings local con almacenamiento en Supabase que permite a ARIA:

- 🧠 **Memoria semántica**: Buscar información por significado, no solo palabras exactas
- ☁️ **Almacenamiento en nube**: Los embeddings se guardan en Supabase (sin usar espacio local)
- 🚀 **Sin OpenAI**: Usa modelos locales (sentence-transformers)
- 📚 **Aprendizaje continuo**: ARIA recuerda conversaciones pasadas
- 🔍 **Búsqueda inteligente**: Encuentra información relacionada aunque uses palabras diferentes

## 🛠️ Instalación

### 1. Instalar dependencias
```bash
python instalar_embeddings_deps.py
```

### 2. Configurar Supabase

#### a) Crear proyecto en Supabase
1. Ve a [supabase.com](https://supabase.com)
2. Crea una cuenta y un nuevo proyecto
3. Anota tu `URL` y `API Key`

#### b) Ejecutar esquema SQL
1. Ve al SQL Editor en tu panel de Supabase
2. Copia y pega el contenido de `supabase_embeddings_schema.sql`
3. Ejecuta el script

#### c) Configurar variables de entorno
```bash
# Editar .env o crear .env.embeddings
SUPABASE_URL=https://tu-proyecto.supabase.co
SUPABASE_ANON_KEY=tu_anon_key_aqui
```

### 3. Probar el sistema
```bash
python aria_embeddings_supabase.py
```

### 4. Ejecutar ARIA con embeddings
```bash
python aria_servidor_superbase.py
```

## 🗄️ Estructura de Base de Datos

### Tablas principales:

#### `aria_embeddings`
- Almacena textos con sus embeddings
- Categorización automática
- Metadatos de contexto

#### `aria_knowledge_vectors`
- Conocimiento estructurado con embeddings
- Conceptos, descripciones, tags
- Relaciones entre conceptos

#### `aria_documents`
- Documentos completos
- Embeddings de título y contenido

## 🚀 Uso del Sistema

### API Endpoints

#### Búsqueda semántica
```http
GET /embeddings/search?q=¿qué es python?&limit=5&threshold=0.7
```

#### Búsqueda de conocimiento
```http
GET /embeddings/knowledge?q=programación&limit=3
```

#### Agregar texto
```http
POST /embeddings/add
{
  "texto": "Python es un lenguaje de programación",
  "categoria": "programacion",
  "metadatos": {"fuente": "manual"}
}
```

#### Agregar conocimiento
```http
POST /embeddings/knowledge
{
  "concepto": "Machine Learning",
  "descripcion": "Rama de la IA que permite aprender patrones",
  "tags": ["ia", "algoritmos"],
  "confianza": 0.9
}
```

#### Estadísticas
```http
GET /embeddings/stats
```

### Chat con embeddings

El chat normal de ARIA ahora incluye automáticamente:

```python
# Busca conocimiento relacionado con embeddings
POST /chat
{
  "message": "¿Cómo funciona el machine learning?"
}

# Respuesta incluye:
{
  "response": "Respuesta basada en conocimiento previo...",
  "knowledge_used": [...],  # Conocimiento encontrado con embeddings
  "confidence": 0.8,
  "embeddings_used": true
}
```

## 🧠 Funcionalidades

### 1. Aprendizaje automático
- ARIA guarda cada conversación como embedding
- Extrae conceptos clave automáticamente
- Relaciona información nueva con conocimiento previo

### 2. Búsqueda semántica
```python
# Encuentra información aunque uses palabras diferentes
"¿Qué es un algoritmo?" → encuentra textos sobre "programación", "lógica", "pasos"
"comida venezolana" → encuentra "tequeños", "empanadas", "arepas"
```

### 3. Categorización inteligente
- `conversation`: Mensajes de chat
- `knowledge`: Conocimiento estructurado  
- `programacion`: Código y conceptos técnicos
- `general`: Información general

### 4. Persistencia en la nube
- ✅ No usa espacio en tu computadora
- ✅ Acceso desde cualquier lugar
- ✅ Backup automático en Supabase
- ✅ Escalabilidad infinita

## 🔧 Configuración Avanzada

### Variables de entorno disponibles:

```bash
# Configuración principal
SUPABASE_URL=https://tu-proyecto.supabase.co
SUPABASE_ANON_KEY=tu_anon_key

# Configuración de embeddings
EMBEDDINGS_MODEL=all-MiniLM-L6-v2  # Modelo local
EMBEDDINGS_DIMENSIONS=384           # Dimensiones del vector
EMBEDDINGS_BATCH_SIZE=32           # Tamaño de lote

# Configuración de búsqueda
SIMILARITY_THRESHOLD=0.6           # Umbral mínimo de similitud
MAX_RESULTS=10                     # Máximo resultados por búsqueda
```

### Modelos de embeddings soportados:
- `all-MiniLM-L6-v2` (384 dim) - **Recomendado** 🟢
- `all-MiniLM-L12-v2` (384 dim) - Más preciso, más lento
- `paraphrase-multilingual-MiniLM-L12-v2` - Multiidioma
- `distiluse-base-multilingual-cased` - Para español optimizado

## 🧪 Ejemplos de Uso

### Ejemplo 1: Agregar conocimiento
```python
from aria_embeddings_supabase import crear_embedding_system

system = crear_embedding_system()

# Agregar conocimiento sobre programación
system.agregar_conocimiento(
    concepto="FastAPI",
    descripcion="Framework web moderno para Python con documentación automática",
    categoria="programacion",
    tags=["python", "web", "api", "framework"],
    ejemplos=["@app.get('/users')", "uvicorn main:app --reload"]
)

# Buscar información relacionada
resultados = system.buscar_conocimiento("crear una API web")
# Encuentra información sobre FastAPI aunque no menciones "FastAPI"
```

### Ejemplo 2: Búsqueda conversacional
```python
# Agregar conversación
system.agregar_texto(
    "El usuario preguntó sobre machine learning y le expliqué que es una rama de la IA",
    categoria="conversation",
    metadatos={"usuario": "juan", "tema": "ml"}
)

# Buscar conversaciones similares
similares = system.buscar_similares("inteligencia artificial")
# Encuentra la conversación aunque uses "inteligencia artificial" en lugar de "machine learning"
```

## 📊 Monitoreo

### Ver estadísticas:
```bash
curl http://localhost:5000/embeddings/stats
```

### Logs del sistema:
- ✅ Embeddings agregados
- 🔍 Búsquedas realizadas  
- ❌ Errores de conexión
- 📊 Métricas de rendimiento

## 🔍 Resolución de Problemas

### Error: "Sistema de embeddings no disponible"
```bash
# 1. Verificar instalación
pip install sentence-transformers supabase

# 2. Verificar configuración
python -c "import os; print(os.getenv('SUPABASE_URL'))"

# 3. Probar conexión
python aria_embeddings_supabase.py
```

### Error: "pgvector extension not found"
```sql
-- Ejecutar en Supabase SQL Editor:
CREATE EXTENSION IF NOT EXISTS vector;
```

### Rendimiento lento
```bash
# Usar modelo más pequeño
EMBEDDINGS_MODEL=all-MiniLM-L6-v2

# Reducir umbral de similitud
SIMILARITY_THRESHOLD=0.5

# Limitar resultados
MAX_RESULTS=5
```

## 🚀 Próximas Mejoras

- [ ] 🗂️ Indexado automático de documentos
- [ ] 🔄 Sincronización offline
- [ ] 📈 Métricas de uso avanzadas
- [ ] 🌍 Soporte para más idiomas
- [ ] 🎯 Fine-tuning del modelo
- [ ] 📱 API GraphQL
- [ ] 🔐 Encriptación de embeddings sensibles

## 📞 Soporte

Si tienes problemas:

1. 🧪 Ejecuta las pruebas: `python aria_embeddings_supabase.py`
2. 📋 Revisa los logs en la consola
3. 🔧 Verifica la configuración de Supabase
4. 📖 Consulta la documentación de Supabase

---

**🎉 ¡Disfruta de ARIA con memoria semántica!**