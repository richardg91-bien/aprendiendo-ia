@echo off
chcp 65001 >nul
title 🤖 ARIA Desktop - Panel de Control

:MENU
cls
echo.
echo ████████████████████████████████████████████████████████████████
echo                    🤖 ARIA DESKTOP - PANEL DE CONTROL
echo ████████████████████████████████████████████████████████████████
echo.
echo                    Selecciona una opción:
echo.
echo    1. 🚀 Iniciar ARIA (Servidor + Navegador)
echo    2. 🌐 Solo abrir interfaz web (si ya está ejecutándose)
echo    3. 🖥️  Conectar por Escritorio Remoto
echo    4. 📊 Diagnóstico del sistema
echo    5. 🔧 Reinstalar dependencias
echo    6. 📁 Abrir carpeta del proyecto
echo    7. 📝 Ver logs
echo    8. ❌ Salir
echo.
echo ████████████████████████████████████████████████████████████████
echo.
set /p choice="Introduce tu elección (1-8): "

if "%choice%"=="1" goto START_ARIA
if "%choice%"=="2" goto OPEN_WEB
if "%choice%"=="3" goto REMOTE_DESKTOP
if "%choice%"=="4" goto DIAGNOSTICS
if "%choice%"=="5" goto REINSTALL
if "%choice%"=="6" goto OPEN_FOLDER
if "%choice%"=="7" goto VIEW_LOGS
if "%choice%"=="8" goto EXIT

echo ❌ Opción no válida. Presiona cualquier tecla para continuar...
pause >nul
goto MENU

:START_ARIA
cls
echo ████████████████████████████████████████████████████████████████
echo                        🚀 INICIANDO ARIA
echo ████████████████████████████████████████████████████████████████
echo.

cd /d "C:\Users\richa\OneDrive\Desktop\aprendiendo-ia"

if exist "venv\Scripts\activate.bat" (
    echo ✅ Activando entorno virtual...
    call venv\Scripts\activate.bat
) else (
    echo ⚠️  Usando Python global...
)

echo ✅ Verificando servidor...
cd src

echo ✅ Abriendo navegador en 3 segundos...
timeout /t 3 /nobreak >nul
start "" "http://localhost:8000"

echo ✅ Iniciando servidor ARIA...
echo.
echo 🌐 Interfaz web: http://localhost:8000
echo 🖥️  Escritorio remoto: 192.168.0.55:3389
echo 🛑 Presiona Ctrl+C para detener
echo.
python aria_servidor_superbase.py

echo.
echo 🛑 Servidor detenido. Presiona cualquier tecla para volver al menú...
pause >nul
goto MENU

:OPEN_WEB
echo ✅ Abriendo interfaz web de ARIA...
start "" "http://localhost:8000"
timeout /t 2 /nobreak >nul
goto MENU

:REMOTE_DESKTOP
cls
echo ████████████████████████████████████████████████████████████████
echo                    🖥️  ESCRITORIO REMOTO
echo ████████████████████████████████████████████████████████████████
echo.
echo 📡 Información de conexión:
echo.
echo    🌐 Dirección IP: 192.168.0.55
echo    🔌 Puerto: 3389 (RDP)
echo    👤 Usuario: [tu usuario de Windows]
echo    🗝️  Contraseña: [tu contraseña]
echo.
echo 💡 Opciones de conexión:
echo    1. Escritorio remoto de Windows (mstsc)
echo    2. TeamViewer
echo    3. AnyDesk
echo.
set /p rdp_choice="¿Abrir cliente de escritorio remoto? (s/n): "
if /i "%rdp_choice%"=="s" (
    echo ✅ Abriendo cliente de escritorio remoto...
    mstsc /v:192.168.0.55
)
echo.
pause
goto MENU

:DIAGNOSTICS
cls
echo ████████████████████████████████████████████████████████████████
echo                      📊 DIAGNÓSTICO
echo ████████████████████████████████████████████████████████████████
echo.
cd /d "C:\Users\richa\OneDrive\Desktop\aprendiendo-ia"
echo ✅ Ejecutando diagnóstico...
python diagnostico_aria.py
echo.
echo ✅ Diagnóstico completado.
pause
goto MENU

:REINSTALL
cls
echo ████████████████████████████████████████████████████████████████
echo                  🔧 REINSTALAR DEPENDENCIAS
echo ████████████████████████████████████████████████████████████████
echo.
cd /d "C:\Users\richa\OneDrive\Desktop\aprendiendo-ia"
echo ✅ Reinstalando dependencias...
pip install -r requirements.txt --force-reinstall
echo.
echo ✅ Dependencias reinstaladas.
pause
goto MENU

:OPEN_FOLDER
echo ✅ Abriendo carpeta del proyecto...
explorer "C:\Users\richa\OneDrive\Desktop\aprendiendo-ia"
timeout /t 1 /nobreak >nul
goto MENU

:VIEW_LOGS
cls
echo ████████████████████████████████████████████████████████████████
echo                        📝 LOGS
echo ████████████████████████████████████████████████████████████████
echo.
cd /d "C:\Users\richa\OneDrive\Desktop\aprendiendo-ia"
if exist "data\logs\aria_startup.log" (
    echo 📄 Últimas líneas del log:
    echo.
    type "data\logs\aria_startup.log" | more
) else (
    echo ⚠️  No se encontraron logs
)
echo.
pause
goto MENU

:EXIT
echo.
echo 👋 ¡Hasta luego! Que tengas un buen día.
timeout /t 2 /nobreak >nul
exit