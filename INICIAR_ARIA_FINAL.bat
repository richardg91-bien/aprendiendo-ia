@echo off
:: 🚀 ARIA - Launcher Final Mejorado
:: Este launcher inicia ARIA de forma robusta y confiable

title ARIA - Asistente IA Futurista
color 0A

echo.
echo ================================================================================
echo 🤖 ARIA - ASISTENTE IA FUTURISTA 
echo ================================================================================
echo 🌟 Iniciando sistema completo...
echo.

:: Verificar que estamos en el directorio correcto
if not exist "backend\src\aria_server_final.py" (
    echo ❌ Error: No se encuentra el servidor ARIA
    echo 💡 Ejecuta este script desde la carpeta raíz del proyecto
    echo.
    pause
    exit /b 1
)

:: Cambiar al directorio del proyecto
cd /d "%~dp0"

echo 📂 Directorio actual: %CD%
echo.

:: Activar entorno virtual si existe
if exist "venv\Scripts\activate.bat" (
    echo 🔧 Activando entorno virtual...
    call venv\Scripts\activate.bat
    echo ✅ Entorno virtual activado
) else if exist ".venv\Scripts\activate.bat" (
    echo 🔧 Activando entorno virtual...
    call .venv\Scripts\activate.bat
    echo ✅ Entorno virtual activado
) else (
    echo ⚠️ No se encontró entorno virtual, usando Python global
)

echo.

:: Verificar Python y dependencias
echo 🐍 Verificando Python...
python --version 2>nul
if %ERRORLEVEL% neq 0 (
    echo ❌ Python no está instalado o no está en PATH
    echo 💡 Instala Python desde https://python.org
    pause
    exit /b 1
)

echo ✅ Python disponible
echo.

:: Instalar dependencias si es necesario
echo 📦 Verificando dependencias...
python -c "import flask, flask_cors" 2>nul
if %ERRORLEVEL% neq 0 (
    echo 📥 Instalando dependencias necesarias...
    pip install flask flask-cors
    echo ✅ Dependencias instaladas
) else (
    echo ✅ Dependencias ya instaladas
)

echo.

:: Verificar si el puerto está libre
echo 🔍 Verificando disponibilidad del puerto 8000...
netstat -an | find "0.0.0.0:8000" >nul 2>&1
if %ERRORLEVEL% equ 0 (
    echo ⚠️ El puerto 8000 ya está en uso
    echo 🔄 Intentando detener procesos existentes...
    
    :: Buscar y terminar procesos Python que usen el puerto
    for /f "tokens=5" %%a in ('netstat -ano ^| find ":8000"') do (
        echo 🛑 Terminando proceso %%a...
        taskkill /PID %%a /F >nul 2>&1
    )
    
    timeout /t 2 /nobreak >nul
)

echo ✅ Puerto 8000 disponible
echo.

:: Crear archivo de bloqueo para evitar múltiples instancias
echo %DATE% %TIME% > aria_running.lock

echo 🚀 Iniciando servidor ARIA...
echo.
echo ================================================================================
echo 🌐 ARIA estará disponible en:
echo    Interfaz Web: http://localhost:8000
echo    API REST:     http://localhost:8000/api/
echo.
echo ⏹️ Presiona Ctrl+C para detener el servidor
echo ================================================================================
echo.

:: Iniciar el servidor con manejo de errores
python backend\src\aria_server_final.py

:: Limpiar al terminar
if exist aria_running.lock del aria_running.lock

echo.
echo 👋 ARIA se ha detenido
echo 📊 Sesión finalizada: %DATE% %TIME%
echo.
pause