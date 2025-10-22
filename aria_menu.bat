@echo off
chcp 65001 >nul
cls

:MENU
echo.
echo 🚀 ARIA SYSTEM - MENÚ PRINCIPAL
echo ================================
echo 🤖 Tu Asistente de IA Futurista
echo ================================
echo.
echo 1. 🚀 Iniciar Todos los Servidores (Recomendado)
echo 2. 🖥️  Iniciar Solo Backend
echo 3. 🧪 Probar Sistema (Demo)
echo 4. 🔍 Diagnóstico del Sistema
echo 5. 📖 Ver Guías de Configuración
echo 6. 🔧 Configuración Rápida
echo 7. 🌐 Abrir Interfaz Web
echo 8. 🛑 Detener Servidores
echo 9. ❌ Salir
echo.

set /p choice="Selecciona una opción (1-9): "

if "%choice%"=="1" goto START_ALL
if "%choice%"=="2" goto START_BACKEND
if "%choice%"=="3" goto DEMO
if "%choice%"=="4" goto DIAGNOSE
if "%choice%"=="5" goto GUIDES
if "%choice%"=="6" goto QUICK_SETUP
if "%choice%"=="7" goto WEB_INTERFACE
if "%choice%"=="8" goto STOP_SERVERS
if "%choice%"=="9" goto EXIT

echo ❌ Opción inválida. Intenta de nuevo.
timeout /t 2 >nul
goto MENU

:START_ALL
cls
echo 🚀 Iniciando todos los servidores...
echo.
call start_all_servers.bat
goto MENU

:START_BACKEND
cls
echo 🖥️ Iniciando solo el backend...
echo.
powershell -ExecutionPolicy Bypass -File "start_all_servers.ps1" -BackendOnly
goto MENU

:DEMO
cls
echo 🧪 Ejecutando demo del sistema...
echo.
python demo_futuristic_aria.py
pause
goto MENU

:DIAGNOSE
cls
echo 🔍 Ejecutando diagnóstico del sistema...
echo.
python diagnose_system.py
goto MENU

:GUIDES
cls
echo 📖 GUÍAS DISPONIBLES:
echo =====================
echo.
echo 1. 📋 README.md - Información general
echo 2. 🌐 GUIA_BASE_DATOS_NUBE.md - Configurar base de datos gratuita
echo 3. 🚀 RESUMEN_SISTEMA_FUTURISTA.md - Resumen completo del sistema
echo 4. 📊 SISTEMA_APRENDIZAJE_AUTONOMO.md - Sistema de aprendizaje
echo.
set /p guide="¿Qué guía quieres ver? (1-4) o Enter para volver: "

if "%guide%"=="1" start notepad README.md
if "%guide%"=="2" start notepad GUIA_BASE_DATOS_NUBE.md  
if "%guide%"=="3" start notepad RESUMEN_SISTEMA_FUTURISTA.md
if "%guide%"=="4" start notepad SISTEMA_APRENDIZAJE_AUTONOMO.md

goto MENU

:QUICK_SETUP
cls
echo 🔧 CONFIGURACIÓN RÁPIDA:
echo ========================
echo.
echo 1. 📦 Instalar dependencias básicas
echo 2. 🐍 Crear entorno virtual
echo 3. 🌐 Configurar archivo .env
echo 4. 📁 Crear directorios necesarios
echo 5. 🔄 Todo lo anterior
echo.
set /p setup="Selecciona opción (1-5) o Enter para volver: "

if "%setup%"=="1" goto INSTALL_DEPS
if "%setup%"=="2" goto CREATE_VENV
if "%setup%"=="3" goto SETUP_ENV
if "%setup%"=="4" goto CREATE_DIRS
if "%setup%"=="5" goto SETUP_ALL

goto MENU

:INSTALL_DEPS
echo 📦 Instalando dependencias...
cd backend
python -m pip install -r requirements.txt
echo ✅ Dependencias instaladas
pause
goto MENU

:CREATE_VENV
echo 🐍 Creando entorno virtual...
python -m venv venv
echo ✅ Entorno virtual creado
echo 💡 Úsalo con: venv\Scripts\activate.bat
pause
goto MENU

:SETUP_ENV
echo 🌐 Configurando archivo .env...
if not exist .env (
    copy .env.example .env
    echo ✅ Archivo .env creado desde plantilla
    echo 💡 Edítalo para configurar tu base de datos
) else (
    echo ⚠️ Archivo .env ya existe
)
notepad .env
goto MENU

:CREATE_DIRS
echo 📁 Creando directorios...
mkdir data 2>nul
mkdir data\logs 2>nul  
mkdir backend\data 2>nul
echo ✅ Directorios creados
pause
goto MENU

:SETUP_ALL
echo 🔄 Configuración completa...
call :CREATE_DIRS
call :CREATE_VENV
call :INSTALL_DEPS
call :SETUP_ENV
echo 🎉 Configuración completa terminada
pause
goto MENU

:WEB_INTERFACE
echo 🌐 Abriendo interfaz web...
start http://127.0.0.1:8000
goto MENU

:STOP_SERVERS
echo 🛑 Deteniendo servidores...
taskkill /f /im python.exe /t >nul 2>&1
taskkill /f /im node.exe /t >nul 2>&1
echo ✅ Servidores detenidos
pause
goto MENU

:EXIT
echo 👋 ¡Hasta luego!
echo 🤖 Gracias por usar ARIA
timeout /t 2 >nul
exit