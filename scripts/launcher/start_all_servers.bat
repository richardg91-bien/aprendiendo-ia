@echo off
chcp 65001 >nul
cls

echo 🚀 ARIA SYSTEM - INICIADOR COMPLETO DE SERVIDORES
echo ====================================================
echo 🤖 Iniciando todos los servidores del sistema ARIA
echo ====================================================
echo.

REM Configurar variables
set PROJECT_DIR=%~dp0
set BACKEND_DIR=%PROJECT_DIR%backend\src
set FRONTEND_DIR=%PROJECT_DIR%frontend
set PYTHON_CMD=python

echo 📍 Directorio del proyecto: %PROJECT_DIR%
echo.

REM Verificar Python
echo 🔍 Verificando Python...
%PYTHON_CMD% --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python no encontrado. Intentando con 'py'...
    set PYTHON_CMD=py
    py --version >nul 2>&1
    if errorlevel 1 (
        echo ❌ Python no está instalado o no está en PATH
        echo 💡 Instala Python desde https://python.org
        pause
        exit /b 1
    )
)
echo ✅ Python encontrado

REM Verificar Node.js
echo 🔍 Verificando Node.js...
node --version >nul 2>&1
if errorlevel 1 (
    echo ⚠️ Node.js no encontrado (opcional para frontend)
    set NODE_AVAILABLE=false
) else (
    echo ✅ Node.js encontrado
    set NODE_AVAILABLE=true
)

REM Activar entorno virtual si existe
if exist "%PROJECT_DIR%venv\Scripts\activate.bat" (
    echo 🐍 Activando entorno virtual...
    call "%PROJECT_DIR%venv\Scripts\activate.bat"
    echo ✅ Entorno virtual activado
) else (
    echo ⚠️ Entorno virtual no encontrado, usando Python del sistema
)

REM Instalar dependencias del backend
echo.
echo 📦 Verificando dependencias del backend...
if exist "%PROJECT_DIR%backend\requirements.txt" (
    echo 🔄 Instalando dependencias de Python...
    cd /d "%PROJECT_DIR%backend"
    %PYTHON_CMD% -m pip install -r requirements.txt --quiet
    if errorlevel 1 (
        echo ⚠️ Algunos paquetes podrían no haberse instalado correctamente
    ) else (
        echo ✅ Dependencias de Python instaladas
    )
) else (
    echo ⚠️ Archivo requirements.txt no encontrado
)

REM Instalar dependencias del frontend
if "%NODE_AVAILABLE%"=="true" (
    echo.
    echo 📦 Verificando dependencias del frontend...
    if exist "%FRONTEND_DIR%\package.json" (
        cd /d "%FRONTEND_DIR%"
        if not exist "node_modules" (
            echo 🔄 Instalando dependencias de Node.js...
            npm install --silent
            echo ✅ Dependencias de Node.js instaladas
        ) else (
            echo ✅ Dependencias de Node.js ya instaladas
        )
    ) else (
        echo ⚠️ Archivo package.json no encontrado en frontend
    )
)

echo.
echo 🚀 INICIANDO SERVIDORES...
echo ============================

REM Crear directorios necesarios
mkdir "%PROJECT_DIR%data" 2>nul
mkdir "%PROJECT_DIR%data\logs" 2>nul
mkdir "%PROJECT_DIR%backend\data" 2>nul

REM Función para verificar si un puerto está en uso
echo 🔍 Verificando puertos disponibles...

REM Verificar puerto 8000 (Backend)
netstat -an | findstr ":8000 " >nul
if not errorlevel 1 (
    echo ⚠️ Puerto 8000 ya está en uso
    echo 💡 Cerrando procesos en puerto 8000...
    for /f "tokens=5" %%a in ('netstat -ano ^| findstr ":8000 "') do (
        taskkill /PID %%a /F >nul 2>&1
    )
    timeout /t 2 >nul
)

REM Verificar puerto 3000 (Frontend)
if "%NODE_AVAILABLE%"=="true" (
    netstat -an | findstr ":3000 " >nul
    if not errorlevel 1 (
        echo ⚠️ Puerto 3000 ya está en uso
        echo 💡 Cerrando procesos en puerto 3000...
        for /f "tokens=5" %%a in ('netstat -ano ^| findstr ":3000 "') do (
            taskkill /PID %%a /F >nul 2>&1
        )
        timeout /t 2 >nul
    )
)

echo.
echo 🖥️ SERVIDOR 1: BACKEND (Puerto 8000)
echo =====================================

REM Verificar archivos principales del backend
if exist "%BACKEND_DIR%\main_stable.py" (
    echo ✅ Archivo principal encontrado: main_stable.py
    set MAIN_FILE=main_stable.py
) else if exist "%BACKEND_DIR%\main.py" (
    echo ✅ Archivo principal encontrado: main.py
    set MAIN_FILE=main.py
) else (
    echo ❌ No se encontró archivo principal del backend
    echo 💡 Buscando alternativas...
    if exist "%BACKEND_DIR%\app.py" (
        set MAIN_FILE=app.py
    ) else (
        echo ❌ No se encontró ningún archivo principal válido
        pause
        exit /b 1
    )
)

REM Iniciar servidor backend en nueva ventana
echo 🚀 Iniciando servidor backend...
cd /d "%BACKEND_DIR%"
start "ARIA Backend Server" cmd /k "echo 🤖 ARIA Backend Server && echo Puerto: 8000 && echo Archivo: %MAIN_FILE% && echo. && %PYTHON_CMD% %MAIN_FILE%"

REM Esperar a que el backend esté listo
echo ⏳ Esperando a que el backend esté listo...
timeout /t 5 >nul

REM Verificar si el backend está funcionando
echo 🔍 Verificando estado del backend...
%PYTHON_CMD% -c "import requests; requests.get('http://127.0.0.1:8000/api/status', timeout=5)" >nul 2>&1
if errorlevel 1 (
    echo ⚠️ Backend puede estar iniciando aún...
) else (
    echo ✅ Backend está funcionando correctamente
)

if "%NODE_AVAILABLE%"=="true" if exist "%FRONTEND_DIR%\package.json" (
    echo.
    echo 🌐 SERVIDOR 2: FRONTEND (Puerto 3000)
    echo ======================================
    
    cd /d "%FRONTEND_DIR%"
    
    REM Verificar si hay un script de inicio personalizado
    if exist "start-server.js" (
        echo 🚀 Iniciando frontend con servidor personalizado...
        start "ARIA Frontend Server" cmd /k "echo 🌐 ARIA Frontend Server && echo Puerto: 3000 && echo. && node start-server.js"
    ) else (
        echo 🚀 Iniciando frontend con React...
        start "ARIA Frontend Server" cmd /k "echo 🌐 ARIA Frontend Server && echo Puerto: 3000 && echo. && npm start"
    )
    
    echo ⏳ Esperando a que el frontend esté listo...
    timeout /t 8 >nul
) else (
    echo.
    echo ⚠️ Frontend no disponible (Node.js no instalado o package.json no encontrado)
    echo 💡 El backend seguirá funcionando con su interfaz web integrada
)

echo.
echo 🎉 SERVIDORES INICIADOS EXITOSAMENTE
echo ====================================

echo.
echo 🌐 ACCESO AL SISTEMA:
echo ----------------------
echo 🖥️  Backend API:     http://127.0.0.1:8000
echo 🎨  Interfaz Web:    http://127.0.0.1:8000
if "%NODE_AVAILABLE%"=="true" if exist "%FRONTEND_DIR%\package.json" (
    echo 🚀  Frontend React:  http://127.0.0.1:3000
)

echo.
echo 📊 ENDPOINTS DISPONIBLES:
echo -------------------------
echo 🔍  Estado:           http://127.0.0.1:8000/api/status
echo 💬  Chat normal:      http://127.0.0.1:8000/api/chat
echo 🚀  Chat futurista:   http://127.0.0.1:8000/api/chat/futuristic
echo 🌐  Datos en nube:    http://127.0.0.1:8000/api/cloud/stats
echo 🎭  Emociones:        http://127.0.0.1:8000/api/cloud/emotions/recent

echo.
echo 🎭 SISTEMA EMOCIONAL ACTIVO:
echo ---------------------------
echo 🔵  Azul = Normal/Interacción
echo 🟢  Verde = Aprendiendo
echo 🔴  Rojo = Frustrada
echo 🟡  Dorado = Feliz
echo 🟣  Púrpura = Pensando

echo.
echo 🛠️ COMANDOS ÚTILES:
echo -------------------
echo 🧪  Probar sistema:   python demo_futuristic_aria.py
echo 📖  Ver guías:        README.md, GUIA_BASE_DATOS_NUBE.md
echo 🔄  Reiniciar:        Cierra las ventanas y ejecuta este script

echo.
echo 💡 CONSEJOS:
echo ------------
echo • Las ventanas de servidor se abrieron por separado
echo • Puedes minimizarlas pero NO las cierres
echo • Para detener: cierra las ventanas de servidor
echo • Los logs aparecen en las ventanas de servidor

echo.
echo ⚠️ IMPORTANTE:
echo --------------
if not exist "%PROJECT_DIR%.env" (
    echo 🔧 Para funcionalidad completa, configura tu archivo .env
    echo 📖 Consulta GUIA_BASE_DATOS_NUBE.md para base de datos gratuita
    echo.
)

echo 🎉 ¡ARIA está lista para usar!
echo 🤖 Tu asistente futurista te espera en: http://127.0.0.1:8000

echo.
echo 📝 Presiona cualquier tecla para salir (los servidores seguirán funcionando)
pause >nul

echo.
echo 👋 Mantén las ventanas de servidor abiertas para que ARIA funcione
echo 🚀 ¡Disfruta tu asistente del futuro!