@echo off
title ARIA - Iniciando Sistema Completo
echo.
echo ========================================
echo   🤖 ARIA - Asistente IA Futurista
echo ========================================
echo.
echo 🚀 Iniciando sistema completo...
echo.

REM Cambiar al directorio del proyecto
cd /d "%~dp0"

REM Verificar si ya hay procesos ejecutándose
echo 🔍 Verificando procesos existentes...
tasklist /FI "IMAGENAME eq python.exe" 2>nul | find /I /N "python.exe" >nul
if "%ERRORLEVEL%"=="0" (
    echo ⚠️  Detectados procesos Python existentes, finalizando...
    taskkill /F /IM python.exe >nul 2>&1
    timeout /t 2 >nul
)

tasklist /FI "IMAGENAME eq node.exe" 2>nul | find /I /N "node.exe" >nul
if "%ERRORLEVEL%"=="0" (
    echo ⚠️  Detectados procesos Node existentes, finalizando...
    taskkill /F /IM node.exe >nul 2>&1
    timeout /t 2 >nul
)

echo.
echo 🔧 Iniciando Backend Flask...
start "ARIA Backend" /min cmd /c "cd backend && python src/main_stable.py"

echo ⏳ Esperando que el backend se inicialice...
timeout /t 8 >nul

echo.
echo 🎨 Iniciando Frontend React...
start "ARIA Frontend" /min cmd /c "cd frontend && npm start"

echo ⏳ Esperando que el frontend se inicialice...
timeout /t 15 >nul

echo.
echo 🌐 Verificando disponibilidad del sistema...

REM Verificar que el backend esté disponible
:check_backend
curl -s -o nul -w "%%{http_code}" http://localhost:8000/api/status | findstr "200" >nul
if %errorlevel% neq 0 (
    echo ⏳ Esperando backend...
    timeout /t 3 >nul
    goto check_backend
)
echo ✅ Backend listo en puerto 8000

REM Verificar que el frontend esté disponible
:check_frontend
curl -s -o nul -w "%%{http_code}" http://localhost:3000 >nul 2>&1
if %errorlevel% equ 0 (
    set FRONTEND_PORT=3000
    goto frontend_ready
)

curl -s -o nul -w "%%{http_code}" http://localhost:3001 >nul 2>&1
if %errorlevel% equ 0 (
    set FRONTEND_PORT=3001
    goto frontend_ready
)

echo ⏳ Esperando frontend...
timeout /t 3 >nul
goto check_frontend

:frontend_ready
echo ✅ Frontend listo en puerto %FRONTEND_PORT%

echo.
echo 🎉 ¡Sistema ARIA completamente listo!
echo.
echo 🌐 Abriendo ARIA en el navegador...

REM Abrir el navegador automáticamente
start "" "http://localhost:%FRONTEND_PORT%"

echo.
echo ========================================
echo   ✨ ARIA está ejecutándose ✨
echo ========================================
echo.
echo 🔗 URLs de acceso:
echo    • Interfaz Principal: http://localhost:%FRONTEND_PORT%
echo    • API Backend: http://localhost:8000
echo.
echo 💡 Consejos:
echo    • Mantén esta ventana abierta
echo    • Para cerrar ARIA, cierra esta ventana
echo    • El aprendizaje autónomo está ACTIVO
echo.
echo ⌨️  Presiona cualquier tecla para minimizar esta ventana...
pause >nul

REM Minimizar la ventana después de abrir el navegador
powershell -window minimized -command ""

REM Mantener el script ejecutándose hasta que se cierre manualmente
echo 🤖 ARIA está ejecutándose en segundo plano...
echo 🔴 Para DETENER ARIA, cierra esta ventana
echo.
:keep_running
timeout /t 30 >nul
goto keep_running