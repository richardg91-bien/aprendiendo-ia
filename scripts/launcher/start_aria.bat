@echo off
echo.
echo ╔══════════════════════════════════════════════════════════╗
echo ║                    🚀 ARIA v2.0                         ║
echo ║              Sistema de Inteligencia Artificial         ║
echo ║                  ✨ ESTRUCTURA LIMPIA                    ║
echo ╚══════════════════════════════════════════════════════════╝
echo.
echo 🎯 Iniciando ARIA desde estructura organizada y limpia...
echo.

REM Verificar que estamos en el directorio correcto
if not exist "backend\src\main.py" (
    echo ❌ Error: No se encuentra el archivo principal
    echo 📁 Asegúrate de ejecutar este script desde la raíz del proyecto
    pause
    exit /b 1
)

REM Activar entorno virtual
echo 🔄 Activando entorno virtual...
call .\venv\Scripts\activate.bat
if errorlevel 1 (
    echo ❌ Error: No se pudo activar el entorno virtual
    echo 💡 Ejecuta: python -m venv venv
    pause
    exit /b 1
)

echo ✅ Entorno virtual activado
echo 🛑 Deteniendo procesos anteriores...
taskkill /F /IM python.exe 2>nul
taskkill /F /IM node.exe 2>nul
timeout /t 2 >nul

echo.
echo 🚀 Iniciando servidor ARIA...
echo.
echo 📡 Servidor disponible en: http://localhost:8000
echo 🌐 Interfaz web en: http://localhost:8000
echo 🔗 API disponible en: http://localhost:8000/api/
echo 📁 Estructura organizada: ✅
echo.
echo ⚠️  Presiona Ctrl+C para detener el servidor
echo.

REM Ejecutar desde la estructura limpia
python backend\src\main.py

echo.
echo 👋 Servidor ARIA detenido
echo 📊 Logs disponibles en: data\logs\
pause