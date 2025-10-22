# ARIA Frontend - React

Frontend moderno para ARIA (Asistente IA Avanzado) desarrollado con React y Material-UI.

## 🚀 Características

- **💬 Chat Inteligente**: Interfaz moderna para conversaciones con ARIA
- **🌐 Búsqueda Web**: Panel integrado para búsquedas en tiempo real
- **🧠 Entrenamiento Neural**: Control y monitoreo del entrenamiento de la red neuronal
- **📊 Estado en Tiempo Real**: Indicadores de conectividad y estado del servidor
- **🎨 Diseño Moderno**: Interfaz dark con efectos glassmorphism y animaciones
- **📱 Responsive**: Adaptable a diferentes tamaños de pantalla

## 🛠️ Instalación

### Prerrequisitos
- Node.js (versión 14 o superior)
- npm o yarn
- Servidor ARIA Flask ejecutándose en puerto 5002

### Pasos de instalación

1. **Navegar al directorio del frontend:**
   ```bash
   cd aria-frontend
   ```

2. **Instalar dependencias:**
   ```bash
   npm install
   ```

3. **Iniciar el servidor de desarrollo:**
   ```bash
   npm start
   ```

4. **Abrir en el navegador:**
   - Frontend React: `http://localhost:3000`
   - Backend Flask: `http://localhost:5002`

## 🔧 Configuración

### Backend Flask
Asegúrate de que tu servidor Flask esté ejecutándose en el puerto 5002:

```bash
# En el directorio principal del proyecto
python asistente_web.py
```

### Configuración de Proxy
El archivo `package.json` incluye configuración de proxy para redirigir las peticiones API al backend Flask.

## 📂 Estructura del Proyecto

```
aria-frontend/
├── public/
│   ├── index.html
│   └── manifest.json
├── src/
│   ├── components/
│   │   ├── ChatInterface.js      # Interfaz principal de chat
│   │   ├── WebSearchPanel.js     # Panel de búsqueda web
│   │   ├── NeuralTrainingPanel.js # Panel de entrenamiento
│   │   └── StatusIndicator.js    # Indicador de estado
│   ├── App.js                    # Componente principal
│   └── index.js                  # Punto de entrada
└── package.json
```

## 🎨 Tecnologías Utilizadas

- **React 18**: Framework principal
- **Material-UI (MUI)**: Componentes de interfaz
- **Framer Motion**: Animaciones y transiciones
- **Axios**: Cliente HTTP para API calls
- **React Markdown**: Renderizado de contenido markdown

## 🌟 Funcionalidades

### Chat Inteligente
- Conversaciones en tiempo real con ARIA
- Soporte para markdown en respuestas
- Feedback de usuario (👍/👎)
- Indicadores de confianza y categoría
- Historial de conversaciones

### Búsqueda Web
- Búsqueda en tiempo real
- Historial de búsquedas recientes
- Sistema de favoritos
- Visualización de resultados estructurados

### Entrenamiento Neural
- Monitoreo del estado de la red
- Entrenamiento con barra de progreso
- Métricas de rendimiento
- Información detallada de la red neuronal

## 🔌 API Endpoints

El frontend se conecta a los siguientes endpoints del backend:

- `POST /chat` - Enviar mensajes al chat
- `POST /buscar_web` - Realizar búsquedas web
- `POST /entrenar_red_neuronal` - Iniciar entrenamiento
- `POST /feedback` - Enviar feedback de usuario
- `GET /test` - Verificar conectividad
- `GET /red_neuronal_info` - Información de la red neuronal

## 🚀 Comandos Disponibles

```bash
# Iniciar servidor de desarrollo
npm start

# Crear build de producción
npm run build

# Ejecutar tests
npm test

# Eject (no recomendado)
npm run eject
```

## 🎨 Personalización

### Tema
Puedes modificar el tema en `src/index.js`:

```javascript
const theme = createTheme({
  palette: {
    mode: 'dark', // 'light' o 'dark'
    primary: {
      main: '#1976d2', // Color primario
    },
    // ... más configuraciones
  },
});
```

### Componentes
Cada componente está diseñado para ser modular y fácilmente personalizable.

## 🐛 Solución de Problemas

### Problemas de Conectividad
1. Verifica que el servidor Flask esté ejecutándose en puerto 5002
2. Comprueba que no haya conflictos de CORS
3. Revisa la consola del navegador para errores

### Problemas de Instalación
1. Elimina `node_modules` y ejecuta `npm install` nuevamente
2. Verifica la versión de Node.js
3. Usa `npm cache clean --force` si es necesario

## 📝 Desarrollo

Para contribuir al desarrollo:

1. Fork el repositorio
2. Crea una rama para tu feature
3. Desarrolla y prueba
4. Envía un pull request

## 📄 Licencia

Este proyecto es parte del sistema ARIA y sigue la misma licencia del proyecto principal.

---

Desarrollado con ❤️ para el proyecto ARIA