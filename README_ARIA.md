# 🤖 ARIA - Asistente Virtual con IA Avanzada

**ARIA** es un asistente virtual inteligente con capacidades de aprendizaje automático, síntesis de voz y procesamiento de lenguaje natural.

## 🚀 Características Principales

### 🧠 Red Neuronal Avanzada
- Sistema de aprendizaje automático persistente
- Memoria de conversaciones con SQLite
- Entrenamiento adaptativo en tiempo real
- Análisis de patrones de comportamiento

### 🔊 Síntesis de Voz
- Integración con Windows SAPI
- Múltiples voces disponibles (Helena Spanish, Zira English, etc.)
- Sistema híbrido con fallback PowerShell
- Síntesis de texto en tiempo real

### 📚 Aprendizaje de Vocabulario
- Sistema de diccionarios dinámicos
- Integración con APIs externas
- Expansión automática de conocimientos
- Procesamiento de datasets (DailyDialog)

### 🌐 Interfaz Web Moderna
- Frontend React con diseño responsivo
- Chat en tiempo real
- Panel de control de red neuronal
- Monitoreo de sistema en vivo

## 🛠️ Tecnologías Utilizadas

### Backend
- **Python 3.9+** - Lenguaje principal
- **Flask** - Framework web
- **SQLite** - Base de datos persistente
- **Windows SAPI** - Síntesis de voz
- **Requests** - Cliente HTTP

### Frontend
- **React** - Framework de interfaz
- **HTML5/CSS3** - Estructura y estilos
- **JavaScript ES6+** - Lógica de cliente

### Inteligencia Artificial
- **Red Neuronal Personalizada** - Procesamiento de lenguaje
- **Sistema de Memoria** - Persistencia de aprendizaje
- **Análisis de Patrones** - Detección de comportamientos

## 📁 Estructura del Proyecto

```
📦 ARIA/
├── 🔧 backend/
│   ├── 📊 config/         # Configuraciones
│   ├── 🗃️ data/           # Datos y logs
│   ├── 🧠 modelo_neuronal/ # Red neuronal entrenada
│   ├── 📂 src/            # Código fuente principal
│   │   ├── main_stable.py      # Servidor principal
│   │   ├── neural_network.py   # Sistema de IA
│   │   ├── voice_system.py     # Síntesis de voz
│   │   └── dictionary_learning.py # Aprendizaje
│   └── 🧪 tests/         # Pruebas automatizadas
├── 🎨 frontend/          # Interfaz React
│   ├── 📦 public/        # Archivos estáticos
│   └── 📄 src/           # Componentes React
├── 📚 docs/              # Documentación
├── ⚙️ config/            # Configuración global
└── 🗂️ legacy/            # Versiones anteriores
```

## 🚀 Instalación y Uso

### Prerrequisitos
- Python 3.9 o superior
- Node.js 16+ (para frontend)
- Windows 10/11 (para síntesis de voz)

### Instalación Backend
```bash
cd backend
pip install -r requirements.txt
cd src
python main_stable.py
```

### Instalación Frontend
```bash
cd frontend
npm install
npm start
```

### Acceso
- **Backend**: http://127.0.0.1:8000
- **Frontend**: http://localhost:3000

## 🎯 Funcionalidades

### 💬 Chat Inteligente
- Conversaciones naturales
- Memoria de contexto
- Respuestas adaptativas

### 🔊 Voz Interactiva
```bash
# Probar síntesis de voz
python test_aria_voice.py
```

### 🧠 Entrenamiento IA
- Entrenamiento automático con conversaciones
- Análisis de patrones de usuario
- Mejora continua de respuestas

### 🌐 Búsqueda Web
- Integración con motores de búsqueda
- Respuestas basadas en información actualizada

## 📊 Estado del Proyecto

✅ **Completado:**
- ✅ Red neuronal con memoria persistente
- ✅ Sistema de voz Windows SAPI
- ✅ Interfaz web funcional
- ✅ API REST completa
- ✅ Sistema de aprendizaje

🔄 **En desarrollo:**
- 🔄 Expansión de datasets
- 🔄 Mejoras de rendimiento
- 🔄 Optimización de memoria

## 🔧 Scripts de Utilidad

- `start_aria_robust.py` - Inicio robusto del sistema
- `test_aria_voice.py` - Prueba de síntesis de voz
- `test_voice.ps1` - Validación PowerShell

## 📈 Versión

**Versión actual:** 2.0 Estable
**Última actualización:** Octubre 2025

## 👨‍💻 Desarrollador

Desarrollado por Richard García  
Proyecto de Aprendizaje de IA  

---

*ARIA - Donde la Inteligencia Artificial se encuentra con la Creatividad* 🌟