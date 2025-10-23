@echo off
chcp 65001 >nul
REM 🚀 ARIA - Iniciador Rápido y Simple
echo 🚀 ARIA - Iniciador Rápido y Simple
echo ===================================
echo 🤖 Asistente IA del Futuro
echo ===================================
echo.

cd /d "%~dp0"

REM Verificar Python
echo 🔍 Verificando Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python no encontrado
    echo 💡 Instala Python desde https://python.org
    pause
    exit /b 1
)
echo ✅ Python encontrado

REM Activar entorno virtual si existe
if exist "venv\Scripts\activate.bat" (
    echo 🐍 Activando entorno virtual...
    call "venv\Scripts\activate.bat"
    echo ✅ Entorno virtual activado
) else (
    echo ⚠️ Entorno virtual no encontrado
)

REM Crear directorios necesarios
echo 📁 Creando directorios...
mkdir data 2>nul
mkdir data\logs 2>nul
mkdir backend\data 2>nul
echo ✅ Directorios creados

REM Verificar archivo principal
if not exist "backend\src\main_stable.py" (
    echo ❌ Archivo principal no encontrado: backend\src\main_stable.py
    echo 💡 Verifica que estés en el directorio correcto
    pause
    exit /b 1
)

REM Instalar dependencias básicas
echo 📦 Instalando dependencias...
cd backend
python -m pip install --upgrade pip --quiet
python -m pip install flask flask-cors requests aiohttp python-dotenv --quiet
if errorlevel 1 (
    echo ⚠️ Algunas dependencias podrían faltar
) else (
    echo ✅ Dependencias básicas instaladas
)

REM Liberar puerto 8000 si está ocupado
echo 🔍 Verificando puerto 8000...
netstat -an | findstr ":8000 " >nul
if not errorlevel 1 (
    echo ⚠️ Puerto 8000 ocupado, intentando liberar...
    for /f "tokens=5" %%a in ('netstat -ano ^| findstr ":8000 "') do (
        taskkill /PID %%a /F >nul 2>&1
    )
    timeout /t 2 >nul
)

REM Iniciar servidor
echo.
echo 🚀 Iniciando ARIA...
echo 🌐 Interfaz disponible en: http://127.0.0.1:8000
echo 🎭 Sistema emocional activado
echo.
echo ⚠️ IMPORTANTE: NO cierres esta ventana mientras uses ARIA
echo.
cd src

REM Iniciar con manejo de errores
python main_stable.py
if errorlevel 1 (
    echo.
    echo ❌ Error al iniciar ARIA
    echo 💡 Ejecuta 'python diagnose_system.py' para más información
)

echo.
echo 🛑 ARIA se ha detenido
pause