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
echo    [2] 🧪 Ejecutar Pruebas Completas
echo    [3] 🌐 Abrir Interfaz Web
echo    [4] 📊 Ver Estado del Sistema
echo    [5] 📁 Explorar Estructura del Proyecto
echo    [6] 📚 Ver Documentación
echo    [7] 🔧 Herramientas de Diagnóstico
echo    [8] 🆘 Ayuda y Soporte
echo    [9] 🏁 Salir
echo.
echo ================================================================================

set /p opcion="🎯 Selecciona una opción [1-9]: "

if "%opcion%"=="1" goto INICIAR_ARIA
if "%opcion%"=="2" goto EJECUTAR_PRUEBAS
if "%opcion%"=="3" goto ABRIR_WEB
if "%opcion%"=="4" goto VER_ESTADO
if "%opcion%"=="5" goto EXPLORAR_PROYECTO
if "%opcion%"=="6" goto VER_DOCUMENTACION
if "%opcion%"=="7" goto HERRAMIENTAS
if "%opcion%"=="8" goto AYUDA
if "%opcion%"=="9" goto SALIR

echo ❌ Opción inválida. Presiona cualquier tecla para continuar...
pause >nul
goto MENU_PRINCIPAL

:INICIAR_ARIA
cls
echo 🚀 Iniciando ARIA...
echo ================================================================================
call INICIAR_ARIA_FINAL.bat
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
echo 🌐 Abriendo Interfaz Web...
echo ================================================================================
start http://localhost:8000
echo ✅ Interfaz web abierta en el navegador
echo 💡 Si no se abre automáticamente, visita: http://localhost:8000
echo.
pause
goto MENU_PRINCIPAL

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