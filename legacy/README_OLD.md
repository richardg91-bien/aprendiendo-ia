# 🤖 ARIA - Asistente Virtual de IA

Sistema completo de inteligencia artificial que combina transcripción de audio, reconocimiento de voz, síntesis de habla y asistente virtual conversacional.

## 🌟 Características Principales

- 🎙️ **Transcripción de Audio** - Convierte audio a texto usando Whisper
- 🤖 **Asistente Virtual** - Conversación natural por voz y texto  
- 🌐 **Interfaz Web Moderna** - Drag & drop, chat en tiempo real
- 🎤 **Reconocimiento de Voz** - Habla directamente con ARIA
- 🔊 **Síntesis de Voz** - ARIA responde por audio
- 📱 **Responsive Design** - Funciona en móviles y tablets

## 📋 Prerrequisitos

- Python 3.13+
- Cuenta de OpenAI con API key
- Archivo de audio en formato MP3, WAV, M4A o WEBM

## 🚀 Configuración Inicial

### 1. Clonar o descargar el proyecto
```bash
# Si usas git
git clone <tu-repositorio>
cd aprediendo-ia
```

### 2. Crear y activar entorno virtual
```bash
# Crear entorno virtual
py -m venv venv

# Activar entorno virtual (Windows)
.\venv\Scripts\Activate.ps1

# Activar entorno virtual (macOS/Linux)
source venv/bin/activate
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4. Configurar API Key de OpenAI

1. Ve a [OpenAI API Keys](https://platform.openai.com/api-keys)
2. Crea una nueva API key
3. Copia el archivo `.env.example` a `.env`:
   ```bash
   cp .env.example .env
   ```
4. Edita el archivo `.env` y reemplaza `tu_api_key_aqui` con tu API key real:
   ```
   OPENAI_API_KEY=sk-tu_api_key_real_aqui
   ```

## 📁 Estructura del Proyecto

```
aprediendo-ia/
├── app.py              # Archivo principal de la aplicación
├── requirements.txt    # Dependencias del proyecto
├── .env               # Variables de entorno (API keys)
├── .gitignore         # Archivos ignorados por git
├── README.md          # Este archivo
├── prueba.mp3         # Archivo de audio de ejemplo
└── venv/             # Entorno virtual (no subir a git)
```

## 💻 Uso

1. **Coloca tu archivo de audio**: Asegúrate de que tienes un archivo llamado `prueba.mp3` en el directorio raíz, o modifica el nombre en `app.py`

2. **Ejecuta el script**:
   ```bash
   python app.py
   ```

3. **Resultados**: La transcripción aparecerá en la consola

## 🔧 Personalización

### Cambiar el archivo de audio
Edita la línea 12 en `app.py`:
```python
audio_file_path = "tu_archivo.mp3"  # Cambia por el nombre de tu archivo
```

### Formatos de audio soportados
- MP3
- WAV 
- M4A
- WEBM

## ⚠️ Notas Importantes

### Mensaje de Advertencia
Es normal ver este mensaje al ejecutar:
```
Could not find platform independent libraries <prefix>
```
**Este es solo una advertencia y NO afecta el funcionamiento del programa.**

### Límites de la API
- OpenAI tiene límites de uso en su API
- Los archivos de audio muy largos pueden tardar más en procesarse
- Revisa los costos en [OpenAI Pricing](https://openai.com/pricing)

## 🐛 Solución de Problemas

### Error: "Incorrect API key provided"
- Verifica que tu API key esté correctamente configurada en `.env`
- Asegúrate de que la API key sea válida y activa

### Error: "No se encontró el archivo"
- Verifica que el archivo de audio exista en el directorio
- Comprueba que el nombre del archivo coincida con el especificado en `app.py`

### Error: "Unable to create process"
- Desactiva y reactiva el entorno virtual:
  ```bash
  deactivate
  .\venv\Scripts\Activate.ps1
  ```

## 📝 Dependencias Principales

- `openai==2.3.0` - Cliente oficial de OpenAI
- `python-dotenv==1.1.1` - Manejo de variables de entorno

## 🤝 Contribuir

1. Fork el proyecto
2. Crea una branch para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la branch (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## 🆘 Soporte

Si tienes problemas o preguntas:
1. Revisa la sección de "Solución de Problemas"
2. Verifica que seguiste todos los pasos de configuración
3. Consulta la documentación de [OpenAI](https://platform.openai.com/docs)