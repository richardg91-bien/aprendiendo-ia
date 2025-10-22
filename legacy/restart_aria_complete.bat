@echo off
title ARIA - Sistema de Reinicio Completo
color 0A

echo.
echo ╔══════════════════════════════════════════════════════════╗
echo ║              🔄 REINICIO COMPLETO DE ARIA               ║
echo ║              Sistema de Inteligencia Artificial         ║
echo ╚══════════════════════════════════════════════════════════╝
echo.

REM Detener todos los procesos Python y Node existentes
echo 🛑 Deteniendo procesos anteriores...
taskkill /F /IM python.exe 2>nul
taskkill /F /IM node.exe 2>nul
timeout /t 2 >nul

REM Limpiar puertos específicos si están ocupados
echo 🧹 Liberando puertos...
for /f "tokens=5" %%a in ('netstat -aon ^| findstr ":8000.*LISTENING"') do taskkill /F /PID %%a 2>nul
for /f "tokens=5" %%a in ('netstat -aon ^| findstr ":5000.*LISTENING"') do taskkill /F /PID %%a 2>nul
for /f "tokens=5" %%a in ('netstat -aon ^| findstr ":3000.*LISTENING"') do taskkill /F /PID %%a 2>nul

echo ✅ Procesos anteriores detenidos
echo.

REM Verificar que estemos en el directorio correcto
if not exist "backend\src\main.py" (
    echo ❌ Error: No se encontró backend/src/main.py
    echo 💡 Asegúrate de ejecutar desde el directorio raíz de ARIA
    pause
    exit /b 1
)

REM Activar entorno virtual
echo 🔧 Activando entorno virtual...
if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\activate.bat
    echo ✅ Entorno virtual activado
) else if exist ".\Scripts\activate.bat" (
    call .\Scripts\activate.bat
    echo ✅ Entorno virtual activado
) else (
    echo ⚠️  No se encontró entorno virtual, usando Python del sistema
)

echo.

REM Construir frontend si existe
if exist "frontend" (
    echo 🏗️  Construyendo frontend...
    cd frontend
    if exist "package.json" (
        call npm run build >nul 2>&1
        if errorlevel 1 (
            echo ⚠️  Error al construir frontend, continuando...
        ) else (
            echo ✅ Frontend construido exitosamente
        )
    )
    cd ..
)

echo.
echo 🚀 Iniciando servidor ARIA...
echo.
echo 📡 Servidor disponible en: http://localhost:8000
echo 🌐 Interfaz web en: http://localhost:8000
echo 🔗 API disponible en: http://localhost:8000/api/
echo.
echo ⚠️  Presiona Ctrl+C para detener el servidor
echo.

REM Iniciar servidor
python backend\src\main.py

echo.
echo 👋 Servidor ARIA detenido
echo 🔄 Para reiniciar, ejecuta este archivo nuevamente
pause