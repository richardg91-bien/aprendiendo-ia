# 🚀 GUÍA DE DEPLOYMENT - ARIA EN SERVIDOR GRATUITO

## 📋 Resumen de Opciones

Tu proyecto ARIA ya está preparado para desplegarse en múltiples plataformas gratuitas con retroalimentación automática.

## 🎯 **OPCIÓN RECOMENDADA: Railway + Supabase**

### **Paso 1: Configurar Supabase (Base de Datos)**

1. Ve a [supabase.com](https://supabase.com) y crea cuenta gratuita
2. Crea un nuevo proyecto
3. En el SQL Editor, ejecuta el contenido de `database_schema.sql`
4. Ve a Settings → API y copia:
   - `URL` del proyecto
   - `anon public` key

### **Paso 2: Configurar Railway (Servidor)**

1. Ve a [railway.app](https://railway.app) y conecta tu GitHub
2. Sube tu proyecto a un repositorio GitHub
3. En Railway: "New Project" → "Deploy from GitHub repo"
4. Configura las variables de entorno:
   ```
   SUPABASE_URL=tu_url_de_supabase
   SUPABASE_KEY=tu_key_de_supabase
   OPENAI_API_KEY=tu_openai_api_key
   FLASK_ENV=production
   PORT=8000
   ```

### **Paso 3: Deploy Automático**

Railway detectará automáticamente:
- `railway.json` - Configuración del build
- `Procfile` - Comando de inicio
- `requirements.txt` - Dependencias Python

¡Tu app estará disponible en una URL como `aria-production.up.railway.app`!

## 🔄 **Sistema de Retroalimentación Incluido**

### **Endpoints Disponibles:**
- `POST /api/feedback/conversation` - Registra conversaciones
- `POST /api/feedback/preference` - Guarda preferencias
- `GET /api/feedback/analytics` - Análisis de feedback
- `GET /api/feedback/patterns` - Patrones de aprendizaje

### **Características:**
- ✅ Registro automático de todas las conversaciones
- ✅ Análisis de satisfacción del usuario
- ✅ Patrones de aprendizaje
- ✅ Preferencias personalizadas
- ✅ Métricas en tiempo real

## 🌟 **ALTERNATIVAS**

### **Render.com**
- Fácil de usar
- PostgreSQL gratuita incluida
- Se duerme tras 15 min de inactividad

### **Vercel + PlanetScale**
- Deploy ultrarrápido
- MySQL gratuita
- Solo para frontend + serverless functions

### **Fly.io**
- Containers Docker
- PostgreSQL + Redis gratuitos
- Excelente performance

## 📊 **Monitoreo y Analytics**

Una vez desplegado, podrás:

1. **Ver conversaciones** en tiempo real en Supabase
2. **Analizar satisfacción** con `/api/feedback/analytics`
3. **Detectar patrones** de uso con `/api/feedback/patterns`
4. **Optimizar respuestas** basado en feedback

## 🔧 **Configuración Local para Testing**

```bash
# Instalar dependencias actualizadas
pip install -r backend/requirements.txt

# Configurar variables de entorno
cp .env.production .env
# Editar .env con tus keys reales

# Probar localmente
python backend/src/main.py
```

## 💡 **Próximos Pasos**

1. **Subir a GitHub** tu código actualizado
2. **Configurar Supabase** con el schema incluido
3. **Desplegar en Railway** con las variables de entorno
4. **Probar los endpoints** de retroalimentación
5. **Monitorear analytics** conforme la gente use ARIA

## 🆘 **Solución de Problemas**

### Error de Build:
- Verificar que `requirements.txt` esté en la raíz
- Confirmar que `railway.json` está configurado

### Error de Base de Datos:
- Verificar variables SUPABASE_URL y SUPABASE_KEY
- Confirmar que las tablas existen en Supabase

### Error de CORS:
- Flask-CORS ya está configurado
- Verificar que el frontend apunte a la URL correcta

¡Tu ARIA estará funcionando 24/7 aprendiendo de cada interacción! 🚀