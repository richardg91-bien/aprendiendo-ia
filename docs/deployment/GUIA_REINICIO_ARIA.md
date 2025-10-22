# 🔄 Guía de Reinicio Rápido de ARIA

## ✨ Scripts Disponibles para Reinicio

Ahora tienes **4 opciones diferentes** para reiniciar ARIA de forma fácil y confiable:

### 1. 🚀 **REINICIAR_ARIA.bat** (MÁS FÁCIL)
```
Doble clic en REINICIAR_ARIA.bat
```
- **Uso**: Doble clic y listo
- **Características**: Interfaz simple, solo presiona una tecla
- **Recomendado para**: Uso diario rápido

### 2. 🔧 **restart_aria_complete.bat** (MÁS COMPLETO)
```
Doble clic en restart_aria_complete.bat
```
- **Uso**: Doble clic desde el explorador
- **Características**: 
  - Detiene TODOS los procesos anteriores
  - Libera puertos ocupados (8000, 5000, 3000)
  - Construye frontend automáticamente
  - Manejo completo de errores
- **Recomendado para**: Cuando hay problemas o necesitas un reinicio limpio

### 3. 🐍 **restart_aria.py** (PARA DESARROLLADORES)
```powershell
python restart_aria.py
```
- **Uso**: Desde terminal/PowerShell
- **Características**:
  - Control avanzado de procesos con psutil
  - Verificación de dependencias
  - Construcción inteligente del frontend
  - Manejo robusto de errores
- **Recomendado para**: Desarrolladores que necesitan más control

### 4. 💻 **restart_aria.ps1** (POWERSHELL AVANZADO)
```powershell
.\restart_aria.ps1
```
**Con opciones:**
```powershell
.\restart_aria.ps1 -SkipFrontend    # Omite construcción del frontend
.\restart_aria.ps1 -Verbose         # Más detalles en los mensajes
```
- **Uso**: Desde PowerShell
- **Características**:
  - Parámetros configurables
  - Logging detallado con timestamps
  - Manejo avanzado de procesos
- **Recomendado para**: Usuarios avanzados de Windows

## 📍 URLs del Sistema
- **Servidor Principal**: http://localhost:8000
- **Interfaz Web**: http://localhost:8000
- **API Base**: http://localhost:8000/api/
- **Estado del Sistema**: http://localhost:8000/api/status

## 🛠️ Solución de Problemas

### ❌ "Puerto ocupado"
Los scripts automáticamente:
1. Detectan procesos en puertos 8000, 5000, 3000
2. Los terminan de forma segura
3. Esperan 2 segundos antes de reiniciar

### ❌ "Entorno virtual no encontrado" 
Los scripts buscan automáticamente en:
- `venv\Scripts\activate.bat`
- `Scripts\activate.bat`
- Si no encuentra, usa Python del sistema

### ❌ "Frontend no construye"
- El script continúa aunque el frontend falle
- Puedes usar `-SkipFrontend` para omitir la construcción

## 🔥 Reinicio de Emergencia

Si ARIA se "cuelga" completamente:

```powershell
# Mata TODOS los procesos Python y Node
taskkill /F /IM python.exe
taskkill /F /IM node.exe

# Luego ejecuta cualquier script de reinicio
.\REINICIAR_ARIA.bat
```

## 📊 Verificación Post-Reinicio

Después del reinicio, verifica:
1. ✅ **Servidor**: http://localhost:8000/api/status
2. ✅ **Chat**: http://localhost:8000 
3. ✅ **Terminal**: Debe mostrar "Servidor disponible en: http://localhost:8000"

## 💡 Consejos

1. **Para uso diario**: Usa `REINICIAR_ARIA.bat`
2. **Para desarrollo**: Usa `restart_aria.py` 
3. **Para depuración**: Usa `restart_aria.ps1 -Verbose`
4. **Si hay problemas**: Usa `restart_aria_complete.bat`

## 📱 Acceso Rápido
Puedes crear un acceso directo en tu escritorio:
1. Clic derecho en `REINICIAR_ARIA.bat`
2. "Crear acceso directo"
3. Arrastra el acceso directo al escritorio

¡Ahora reiniciar ARIA es súper fácil! 🎉