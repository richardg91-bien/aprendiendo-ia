# aprendiendo-ia

Repositorio transformado de playground a app IA modular y escalable.

## Estructura recomendada (FastAPI)

```
aprendiendo-ia/
├── backend/
│   ├── main.py                 # entrypoint FastAPI
│   ├── routes/
│   │   ├── chat.py             # endpoint de texto
│   │   └── voz.py              # endpoint de voz
│   ├── services/
│   │   ├── texto.py            # lógica IA texto
│   │   └── voz.py              # lógica IA voz
│   ├── config.py               # variables de entorno
│   └── __init__.py
├── frontend/
│   ├── index.html
│   ├── script.js
│   └── style.css
├── requirements.txt
├── .env.example
├── modelo_neuronal/
│   ├── train.py
│   ├── inference.py
│   └── README.md
├── tests/
│   └── test_services_texto.py
└── README.md
```

## Cómo correrlo

1. Crear entorno virtual

```bash
python -m venv venv
# En Windows:
venv\Scripts\activate
# En Linux/Mac:
source venv/bin/activate
```

2. Instalar dependencias

```bash
pip install -r requirements.txt
```

3. Configurar tu `.env`

```
OPENAI_API_KEY=tu_clave_aqui
```

4. Ejecutar el backend

```bash
uvicorn backend.main:app --reload
```

5. Abrir `frontend/index.html` en tu navegador.

---

## Ventajas de la estructura
- Modularidad: fácil de mantener y escalar.
- Reutilización: servicios IA pueden usarse en otros proyectos.
- Escalabilidad: listo para desplegar en la nube.
- Mantenibilidad: código limpio, con logging y configuración centralizada.

---

## Extensiones recomendadas
- Añadir endpoints para visión, embeddings, etc.
- Mejorar frontend con frameworks modernos si lo deseas.
- Ampliar cobertura de tests en `tests/`.

---

> Estructura y recomendaciones generadas para evolucionar de sandbox a app IA profesional.
# 🤖 ARIA - Sistema de IA Personal

![ARIA Status](https://img.shields.io/badge/Status-Funcional-green)
![Python](https://img.shields.io/badge/Python-3.8+-blue)
![Supabase](https://img.shields.io/badge/Database-Supabase-green)

## 📋 Descripción

ARIA es un sistema de inteligencia artificial personal que combina conversación natural, detección de emociones y sistema de memoria persistente. Utiliza Supabase como backend y está optimizado para respuestas empáticas y naturales.

## 🚀 Inicio Rápido

### Instalación Automática
```bash
python setup.py
```

### Uso Básico
```bash
python main.py
```
Accede a: http://localhost:5000
- 🎤 **Reconocimiento de Voz** - Habla directamente con ARIA
- 🔊 **Síntesis de Voz** - ARIA responde por audio
- 📱 **Responsive Design** - Funciona en móviles y tablets
- 🛡️ **Protección Infantil** - Sistema completo de seguridad para niños
- 🧠 **Red Neuronal** - Aprendizaje automático avanzado

## 📁 Estructura del Proyecto Organizada

```
aria-project/
├── 📂 backend/              # Backend Flask
│   ├── src/                 # Código fuente principal
│   ├── modelo_neuronal/     # Modelos de IA
│   └── tests/              # Pruebas del backend
├── 📂 frontend/             # Frontend React
│   ├── src/                # Código React
│   ├── build/              # Build de producción  
│   └── public/             # Archivos públicos
├── 📂 config/              # Configuración centralizada
│   ├── settings.py         # Configuración principal
│   ├── parental_settings.json
│   └── database_schema.sql
├── 📂 scripts/             # Scripts organizados
│   ├── start_aria.bat      # Script principal de inicio
│   ├── deploy/             # Scripts de deployment
│   ├── maintenance/        # Scripts de mantenimiento
│   └── development/        # Herramientas de desarrollo
├── 📂 docs/                # Documentación completa
│   ├── installation/       # Guías de instalación
│   ├── deployment/         # Guías de deployment
│   └── features/           # Documentación de características
├── 📂 data/                # Datos y logs
│   └── logs/               # Archivos de log
└── 📂 legacy/              # Código heredado (backup)
```

## 🚀 Inicio Rápido

### **1. Instalación Automática (Recomendado)**
```bash
# Ejecutar script de inicio principal
.\scripts\start_aria.bat
```

### **2. Instalación Manual**
```bash
# 1. Crear y activar entorno virtual
python -m venv venv
.\venv\Scripts\Activate.ps1

# 2. Instalar dependencias
pip install -r backend\requirements.txt

# 3. Construir frontend (solo primera vez)
cd frontend
npm install
npm run build
cd ..

# 4. Iniciar servidor
python backend\src\main.py
```

## 🌐 Acceso al Sistema

- **Aplicación Principal:** http://localhost:8000
- **API Backend:** http://localhost:8000/api/
- **Red Local:** http://192.168.x.x:8000

## 📋 Prerrequisitos

- **Python 3.13+**
- **Node.js 14+** (para frontend)
- **Cuenta OpenAI** con API key (opcional para funciones avanzadas)

## ⚙️ Configuración

### Variables de Entorno
Crea un archivo `.env` en la raíz del proyecto:
```bash
OPENAI_API_KEY=tu_api_key_aqui
FLASK_ENV=development
DEBUG=True
```

### Configuración Parental
El sistema incluye protección infantil avanzada:
```bash
# Activar protección máxima
.\scripts\maintenance\activar_proteccion_infantil.bat
```

## 🔧 Scripts Disponibles

### Scripts Principales
- `.\scripts\start_aria.bat` - Inicia ARIA completo
- `.\scripts\maintenance\restart_aria.bat` - Reinicia el sistema

### Scripts de Desarrollo
- `.\scripts\development\run_dev.py` - Servidor de desarrollo
- `.\scripts\development\servidor_test_simple.py` - Servidor de pruebas

### Scripts de Deployment
- `.\scripts\deploy\prepare_deployment.bat` - Prepara para deployment
- `.\scripts\deploy\test_deployment.py` - Prueba deployment

## 📚 Documentación Completa

- **[Guía de Instalación](docs/installation/)** - Instalación detallada
- **[Guía de Deployment](docs/deployment/)** - Deploy en la nube
- **[Protección Infantil](docs/features/)** - Sistema de seguridad
- **[API Reference](docs/api/)** - Documentación de la API

## 🐛 Solución de Problemas

### Error: "Frontend no disponible"
```bash
cd frontend
npm install
npm run build
```

### Error: "No se encontró Flask"
```bash
.\venv\Scripts\Activate.ps1
pip install -r backend\requirements.txt
```

### Error: Entorno virtual
```bash
python -m venv venv
.\venv\Scripts\Activate.ps1
```

## 🎯 Características Avanzadas

### 🧠 Red Neuronal
- Sistema de aprendizaje automático
- Entrenamiento en tiempo real
- Mejora continua de respuestas

### 🛡️ Protección Infantil
- Filtrado de contenido inteligente
- Logs de conversaciones
- Control parental avanzado
- Bloqueo de información personal

### 📊 Sistema de Feedback
- Aprendizaje basado en retroalimentación
- Análisis de conversaciones
- Mejora automática de respuestas

## 🌩️ Deployment en la Nube

El proyecto está preparado para desplegarse en:
- **Railway** (recomendado)
- **Heroku**
- **Vercel**
- **DigitalOcean**

Ver [Guía de Deployment](docs/deployment/DEPLOYMENT_GUIDE.md) para instrucciones detalladas.

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver archivo `LICENSE` para más detalles.

## 🆘 Soporte

- **Issues:** Crear un issue en GitHub
- **Documentación:** Revisar carpeta `/docs/`
- **Logs:** Verificar archivos en `/data/logs/`

---

### 🎉 **¡ARIA ahora está completamente organizado y listo para usar!**

**Ejecuta `.\scripts\start_aria.bat` para comenzar** 🚀