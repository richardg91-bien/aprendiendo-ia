@echo off
chcp 65001 >nul
title ARIA - Iniciando Sistema con Navegador
color 0B

echo.
echo ===============================================
echo    🤖 ARIA - Asistente IA Futurista 🤖
echo ===============================================
echo.
echo 🚀 Iniciando sistema completo...
echo.

REM Cambiar al directorio del proyecto
cd /d "%~dp0"

REM Limpiar procesos anteriores
echo 🧹 Limpiando procesos anteriores...
taskkill /F /IM python.exe >nul 2>&1
taskkill /F /IM node.exe >nul 2>&1
timeout /t 3 >nul

echo.
echo 🔧 Iniciando Backend Flask...
start "ARIA Backend" /min cmd /c "cd backend && python src/main_stable.py && pause"

echo ⏳ Esperando Backend (10 segundos)...
timeout /t 10 >nul

REM Verificar backend
:check_backend
curl -s -o nul -w "%%{http_code}" http://localhost:8000/api/status | findstr "200" >nul
if %errorlevel% neq 0 (
    echo ⏳ Backend aún iniciando...
    timeout /t 2 >nul
    goto check_backend
)
echo ✅ Backend listo!

echo.
echo 🎨 Iniciando Frontend React...
start "ARIA Frontend" /min cmd /c "cd frontend && npm start"

echo ⏳ Esperando Frontend (15 segundos)...
timeout /t 15 >nul

REM Detectar puerto del frontend
set FRONTEND_PORT=
:detect_frontend
curl -s -o nul -w "%%{http_code}" http://localhost:3000 >nul 2>&1
if %errorlevel% equ 0 (
    set FRONTEND_PORT=3000
    goto frontend_found
)

curl -s -o nul -w "%%{http_code}" http://localhost:3001 >nul 2>&1
if %errorlevel% equ 0 (
    set FRONTEND_PORT=3001
    goto frontend_found
)

echo ⏳ Frontend aún iniciando...
timeout /t 3 >nul
goto detect_frontend

:frontend_found
echo ✅ Frontend listo en puerto %FRONTEND_PORT%!

echo.
echo 🎉 ¡ARIA completamente listo!
echo.
echo 🌐 Abriendo ARIA en el navegador...
echo.

REM Abrir el navegador
start "" "http://localhost:%FRONTEND_PORT%"

echo ===============================================
echo     ✨ ARIA FUNCIONANDO CORRECTAMENTE ✨
echo ===============================================
echo.
echo 🔗 URLs disponibles:
echo    • Principal: http://localhost:%FRONTEND_PORT%
echo    • API:       http://localhost:8000
echo.
echo 💡 ARIA está ejecutándose:
echo    • ✅ Backend Flask: Puerto 8000
echo    • ✅ Frontend React: Puerto %FRONTEND_PORT%
echo    • ✅ Aprendizaje Autónomo: ACTIVO
echo    • ✅ Navegador: ABIERTO
echo.
echo 🔴 Para CERRAR ARIA: Cierra esta ventana
echo.

REM Minimizar ventana después de 5 segundos
echo ⏳ Minimizando en 5 segundos...
timeout /t 5 >nul
powershell -window minimized -command ""

:keep_alive
echo %time% - 🤖 ARIA ejecutándose...
timeout /t 60 >nul
goto keep_alive