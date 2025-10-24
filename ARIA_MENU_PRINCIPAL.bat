@echo off
:: 🎯 ARIA - MENÚ PRINCIPAL FINAL
:: Acceso a todas las funcionalidades de ARIA

title ARIA - Asistente IA Futurista - Menú Principal
color 0B

:MENU_PRINCIPAL
cls
echo.
echo ================================================================================
echo 🤖 ARIA - ASISTENTE IA FUTURISTA - MENU PRINCIPAL
echo ================================================================================
echo 🌟 Versión: 1.0.0 Estable
echo 🚀 Estado: Completamente Funcional
echo.
echo 🎯 OPCIONES DISPONIBLES:
echo.
echo    [1] 🚀 Iniciar ARIA (Servidor Principal)
echo    [2] 🎨 Iniciar ARIA con Interfaz Moderna (React)
echo    [3] 🧪 Ejecutar Pruebas Completas
echo    [4] 🌐 ARIA Completo (Supabase + Google Cloud + Web)
echo    [5] 📊 Ver Estado del Sistema
echo    [6] 📁 Explorar Estructura del Proyecto
echo    [7] 📚 Ver Documentación
echo    [8] 🔧 Herramientas de Diagnóstico
echo    [9] 🆘 Ayuda y Soporte
echo    [0] 🏁 Salir
echo.
echo ================================================================================

set /p opcion="🎯 Selecciona una opción [0-9]: "

if "%opcion%"=="1" goto INICIAR_ARIA
if "%opcion%"=="2" goto INICIAR_ARIA_MODERNO
if "%opcion%"=="3" goto EJECUTAR_PRUEBAS
if "%opcion%"=="4" goto ABRIR_WEB
if "%opcion%"=="5" goto VER_ESTADO
if "%opcion%"=="6" goto EXPLORAR_PROYECTO
if "%opcion%"=="7" goto VER_DOCUMENTACION
if "%opcion%"=="8" goto HERRAMIENTAS
if "%opcion%"=="9" goto AYUDA
if "%opcion%"=="0" goto SALIR

echo ❌ Opción inválida. Presiona cualquier tecla para continuar...
pause >nul
goto MENU_PRINCIPAL

:INICIAR_ARIA
cls
echo 🚀 Iniciando ARIA...
echo ================================================================================
call INICIAR_ARIA_FINAL.bat
goto MENU_PRINCIPAL

:INICIAR_ARIA_MODERNO
cls
echo 🎨 Iniciando ARIA con Interfaz Moderna...
echo ================================================================================
echo 🚀 Backend Flask + Frontend React
echo 🤖 Cara de robot animada
echo 🎭 Emociones de IA en tiempo real
echo ✨ Animaciones fluidas con Material-UI
echo 🌐 Interfaz disponible en: http://localhost:3000
echo.
call INICIAR_ARIA_COMPLETO.ps1
goto MENU_PRINCIPAL

:EJECUTAR_PRUEBAS
cls
echo 🧪 Ejecutando Pruebas Completas...
echo ================================================================================
echo ⚠️ Asegúrate de que ARIA esté ejecutándose en otra ventana
echo.
pause
python backend\src\test_aria_completo.py
echo.
echo ✅ Pruebas completadas. Presiona cualquier tecla para continuar...
pause >nul
goto MENU_PRINCIPAL

:ABRIR_WEB
cls
echo 🌐 Iniciando ARIA con Conexiones Completas...
echo ================================================================================
echo 🔗 Conectando a Supabase y Google Cloud...
echo 🚀 Iniciando servidor integrado...
echo ⚡ Activando interfaz moderna...
echo.

:: Activar entorno virtual
echo 📦 Activando entorno virtual...
call venv_new\Scripts\activate.bat

:: Verificar conexiones
echo 🔍 Verificando configuración...
python -c "from dotenv import load_dotenv; import os; load_dotenv(); print('✅ Supabase:', 'Configurado' if os.getenv('SUPABASE_URL') else '❌ Falta config'); print('✅ Google Cloud:', 'Configurado' if os.getenv('GOOGLE_CLOUD_API_KEY') else '❌ Falta config')"

echo.
echo 🚀 Iniciando ARIA Integrado con todas las conexiones...
echo 📊 Estado: Conectando a Supabase y Google Cloud
echo 🌐 Interfaz disponible en: http://localhost:5000
echo ⚡ Modo: Completo con IA avanzada
echo.

:: Iniciar servidor integrado en una ventana nueva (mantener la ventana abierta)
echo 🚀 Iniciando servidor en ventana separada con logging...
start "ARIA Integrated Server" cmd /k "echo 🤖 ARIA SERVER - %date% %time% && venv_new\Scripts\activate && echo ✅ Entorno virtual activado && python aria_integrated_server.py 2>&1"

:: Dar más tiempo inicial para que el servidor arranque
echo ⏳ Dando tiempo inicial al servidor para arrancar...
timeout /t 3 /nobreak >nul

:: Esperar y reintentar comprobación del servidor (hasta ~20s)
echo ⏳ Esperando que el servidor se inicie (reintentos extendidos)...
powershell -Command "for($i=0;$i -lt 20;$i++){ try{$response = Invoke-RestMethod -Uri 'http://localhost:5000/api/status' -TimeoutSec 3; Write-Host \"✅ Servidor respondió correctamente en intento $($i+1)\"; exit 0 } catch{ if($i -lt 5) { Write-Host \"⏳ Intento $($i+1): Esperando...\" } else { Write-Host \"🔍 Intento $($i+1): $($_.Exception.Message)\" } } Start-Sleep -Seconds 1 }; Write-Host \"❌ Servidor no respondió después de 20 intentos\"; exit 1"

if %ERRORLEVEL% equ 0 (
    echo ✅ Servidor iniciado correctamente
) else (
    echo ⚠️ No se pudo verificar el servidor en localhost:5000
    echo 💡 Posibles causas:
    echo    - El servidor está iniciando (normal, espera un momento más)
    echo    - Puerto 5000 está ocupado por otra aplicación
    echo    - Error en la configuración del entorno virtual
    echo    - Dependencias faltantes (Flask, etc.)
    echo.
    echo 🔍 Revisa la ventana del servidor para ver mensajes de error detallados
)

echo.
echo 🌐 Abriendo interfaz web moderna...
start http://localhost:5000

echo.
echo ================================================================================
echo 🎉 ¡ARIA INICIADO EN SEGUNDO PLANO!
echo ================================================================================
echo.
echo 🔗 Características activas (según configuración):
echo    - Servidor integrado en puerto 5000 (ventana separada)
echo    - Conexión a Supabase (si `SUPABASE_URL` configurada)
echo    - Integración con Google Cloud (si `GOOGLE_CLOUD_API_KEY` configurada)
echo.
echo 🌐 Interfaz web: http://localhost:5000
echo 📊 Estado del sistema: http://localhost:5000/api/status
echo.
echo ================================================================================
echo 🤔 ¿Qué quieres hacer ahora?
echo ================================================================================
echo.
echo    [1] 🔙 Volver al menú principal
echo    [2] 🏁 Salir (mantener servidor ejecutándose)
echo.
set /p siguiente="Selecciona [1-2]: "

if "%siguiente%"=="1" goto MENU_PRINCIPAL
if "%siguiente%"=="2" exit /b 0

echo ❌ Opción inválida. Saliendo...
timeout /t 2 /nobreak >nul
exit /b 0

:VER_ESTADO
cls
echo 📊 Verificando Estado del Sistema...
echo ================================================================================
curl -X GET "http://localhost:8000/api/status" 2>nul
if %ERRORLEVEL% neq 0 (
    echo ❌ ARIA no está ejecutándose
    echo 💡 Usa la opción 1 para iniciarlo
) else (
    echo ✅ ARIA está funcionando correctamente
)
echo.
pause
goto MENU_PRINCIPAL

:EXPLORAR_PROYECTO
cls
echo 📁 Estructura del Proyecto...
echo ================================================================================
type ESTRUCTURA_ORGANIZADA.md 2>nul
if %ERRORLEVEL% neq 0 (
    echo 📂 Archivos principales:
    echo    - backend\src\aria_server_final.py  (Servidor principal)
    echo    - INICIAR_ARIA_FINAL.bat           (Launcher)
    echo    - ARIA_COMPLETAMENTE_FUNCIONAL.md  (Documentación)
)
echo.
pause
goto MENU_PRINCIPAL

:VER_DOCUMENTACION
cls
echo 📚 Documentación de ARIA...
echo ================================================================================
echo.
echo 📖 Documentos disponibles:
echo    - ARIA_COMPLETAMENTE_FUNCIONAL.md (Estado y funcionalidades)
echo    - README_ARIA.md                  (Guía de usuario)
echo    - docs\                           (Documentación técnica)
echo.
echo 🌐 APIs disponibles:
echo    - GET  /api/status     (Estado del sistema)
echo    - POST /api/chat       (Conversación)
echo    - GET  /api/knowledge  (Base de conocimiento)
echo    - GET  /api/history    (Historial)
echo    - POST /api/learn      (Enseñar conceptos)
echo.
pause
goto MENU_PRINCIPAL

:HERRAMIENTAS
cls
echo 🔧 Herramientas de Diagnóstico...
echo ================================================================================
echo.
echo 🔍 Verificando dependencias...
python -c "import flask, flask_cors; print('✅ Dependencias OK')" 2>nul
if %ERRORLEVEL% neq 0 (
    echo ❌ Faltan dependencias. Instalando...
    pip install flask flask-cors
)

echo.
echo 🔍 Verificando puerto 8000...
netstat -an | find "0.0.0.0:8000" >nul 2>&1
if %ERRORLEVEL% equ 0 (
    echo ✅ Puerto 8000 en uso (ARIA probablemente ejecutándose)
) else (
    echo ℹ️ Puerto 8000 libre
)

echo.
echo 🔍 Verificando archivos principales...
if exist "backend\src\aria_server_final.py" (
    echo ✅ Servidor principal encontrado
) else (
    echo ❌ Servidor principal no encontrado
)

if exist "INICIAR_ARIA_FINAL.bat" (
    echo ✅ Launcher encontrado
) else (
    echo ❌ Launcher no encontrado
)

echo.
pause
goto MENU_PRINCIPAL

:AYUDA
cls
echo 🆘 Ayuda y Soporte...
echo ================================================================================
echo.
echo 🎯 GUÍA RÁPIDA:
echo.
echo 1. 🚀 INICIAR ARIA:
echo    - Ejecuta opción 1 o INICIAR_ARIA_FINAL.bat
echo    - Espera a ver "Running on http://127.0.0.1:8000"
echo    - Visita http://localhost:8000 en tu navegador
echo.
echo 2. 💬 USAR EL CHAT:
echo    - Abre la interfaz web
echo    - Usa los botones de prueba
echo    - O envía POST a /api/chat con {"message": "tu mensaje"}
echo.
echo 3. 🧪 PROBAR FUNCIONALIDADES:
echo    - Usa la opción 2 para ejecutar todas las pruebas
echo    - Verifica que todas pasen
echo.
echo 4. 🛠️ SOLUCIONAR PROBLEMAS:
echo    - Usa la opción 7 para diagnóstico
echo    - Verifica que Python esté instalado
echo    - Asegúrate de que el puerto 8000 esté libre
echo.
echo 5. 📞 CONTACTO:
echo    - Revisa ARIA_COMPLETAMENTE_FUNCIONAL.md
echo    - Consulta la documentación en docs/
echo.
pause
goto MENU_PRINCIPAL

:SALIR
cls
echo.
echo 👋 Gracias por usar ARIA - Asistente IA Futurista
echo 🌟 ¡Hasta la próxima!
echo.
timeout /t 2 /nobreak >nul
exit

:EOF