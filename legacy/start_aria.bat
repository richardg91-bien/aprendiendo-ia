@echo off
echo.
echo ╔══════════════════════════════════════════════════════════╗
echo ║                    🚀 ARIA v2.0                         ║
echo ║              Sistema de Inteligencia Artificial         ║
echo ╚══════════════════════════════════════════════════════════╝
echo.
echo 🔄 Iniciando ARIA...
echo.

REM Activar entorno virtual y ejecutar servidor
call .\venv\Scripts\Activate.ps1
if errorlevel 1 (
    echo ❌ Error: No se pudo activar el entorno virtual
    echo 💡 Asegúrate de que el entorno virtual esté creado
    pause
    exit /b 1
)

echo ✅ Entorno virtual activado
echo � Deteniendo procesos anteriores...
taskkill /F /IM python.exe 2>nul
taskkill /F /IM node.exe 2>nul
timeout /t 2 >nul

echo �🚀 Iniciando servidor ARIA...
echo.
echo 📡 Servidor disponible en: http://localhost:8000
echo 🌐 Interfaz web en: http://localhost:8000
echo 🔗 API disponible en: http://localhost:8000/api/
echo.
echo ⚠️  Presiona Ctrl+C para detener el servidor
echo.

python backend\src\main.py

echo.
echo 👋 Servidor ARIA detenido
pause