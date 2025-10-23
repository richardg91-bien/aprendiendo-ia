@echo off
:: 🎯 ARIA - Restaurador de Ícono del Escritorio
:: Script simple para recrear el acceso directo de ARIA

title ARIA - Restaurando Icono
color 0A

echo.
echo ================================================================================
echo 🎯 ARIA - RESTAURADOR DE ICONO DEL ESCRITORIO
echo ================================================================================
echo.

:: Verificar que estamos en el directorio correcto
if not exist "ARIA_MENU_PRINCIPAL.bat" (
    if not exist "INICIAR_ARIA_FINAL.bat" (
        echo ❌ Error: No se encuentran los archivos de ARIA
        echo 💡 Ejecuta este script desde la carpeta del proyecto
        pause
        exit /b 1
    )
)

echo ✅ Archivos de ARIA encontrados
echo.

:: Obtener la ruta del escritorio
for /f "usebackq tokens=3*" %%A in (`reg query "HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders" /v Desktop`) do set DESKTOP=%%A %%B
if "%DESKTOP%"=="" set DESKTOP=%USERPROFILE%\Desktop

echo 📁 Directorio actual: %CD%
echo 🖥️ Escritorio: %DESKTOP%
echo.

:: Crear directorio de assets si no existe
if not exist "assets\icons" mkdir assets\icons

:: Determinar qué launcher usar
set LAUNCHER_FILE=""
set LAUNCHER_NAME="ARIA - Asistente IA"
set LAUNCHER_DESC="ARIA - Asistente de Inteligencia Artificial"

if exist "ARIA_MENU_PRINCIPAL.bat" (
    set LAUNCHER_FILE=ARIA_MENU_PRINCIPAL.bat
    set LAUNCHER_NAME=ARIA - Menu Principal
) else if exist "INICIAR_ARIA_FINAL.bat" (
    set LAUNCHER_FILE=INICIAR_ARIA_FINAL.bat
    set LAUNCHER_NAME=ARIA - Launcher
) else if exist "INICIAR_ARIA_FINAL.ps1" (
    set LAUNCHER_FILE=INICIAR_ARIA_FINAL.ps1
    set LAUNCHER_NAME=ARIA - PowerShell
)

echo 🎯 Launcher seleccionado: %LAUNCHER_FILE%
echo.

:: Crear script VBS para crear el acceso directo
echo 🔧 Creando acceso directo...

set VBS_SCRIPT=%TEMP%\create_aria_shortcut.vbs
set SHORTCUT_PATH=%DESKTOP%\%LAUNCHER_NAME%.lnk

:: Eliminar acceso directo existente si existe
if exist "%SHORTCUT_PATH%" (
    echo 🗑️ Eliminando acceso directo anterior...
    del "%SHORTCUT_PATH%" >nul 2>&1
)

:: Crear script VBS
echo Set oWS = WScript.CreateObject("WScript.Shell") > "%VBS_SCRIPT%"
echo sLinkFile = "%SHORTCUT_PATH%" >> "%VBS_SCRIPT%"
echo Set oLink = oWS.CreateShortcut(sLinkFile) >> "%VBS_SCRIPT%"
echo oLink.TargetPath = "%CD%\%LAUNCHER_FILE%" >> "%VBS_SCRIPT%"
echo oLink.WorkingDirectory = "%CD%" >> "%VBS_SCRIPT%"
echo oLink.Description = "%LAUNCHER_DESC%" >> "%VBS_SCRIPT%"

:: Buscar ícono personalizado
if exist "assets\icons\aria_icon.ico" (
    echo oLink.IconLocation = "%CD%\assets\icons\aria_icon.ico" >> "%VBS_SCRIPT%"
    echo 🎨 Usando ícono personalizado
) else if exist "assets\aria.ico" (
    echo oLink.IconLocation = "%CD%\assets\aria.ico" >> "%VBS_SCRIPT%"
    echo 🎨 Usando ícono de assets
) else (
    echo oLink.IconLocation = "shell32.dll,1" >> "%VBS_SCRIPT%"
    echo 🎨 Usando ícono del sistema
)

echo oLink.Save >> "%VBS_SCRIPT%"

:: Ejecutar script VBS
cscript //nologo "%VBS_SCRIPT%"

:: Limpiar archivo temporal
del "%VBS_SCRIPT%" >nul 2>&1

:: Verificar que se creó el acceso directo
if exist "%SHORTCUT_PATH%" (
    echo.
    echo ================================================================================
    echo 🎉 ¡ICONO DE ARIA RESTAURADO EXITOSAMENTE!
    echo ================================================================================
    echo ✅ Acceso directo creado: %LAUNCHER_NAME%.lnk
    echo 📍 Ubicación: %DESKTOP%
    echo 🚀 Haz doble clic en el ícono para iniciar ARIA
    echo.
    echo 📋 Funcionalidades de ARIA:
    echo    🤖 Interfaz web interactiva
    echo    💬 Chat con IA avanzada  
    echo    🧠 Sistema de aprendizaje
    echo    📊 APIs REST completas
    echo.
    echo ✅ ¡Listo para usar!
) else (
    echo.
    echo ================================================================================
    echo ❌ NO SE PUDO CREAR EL ICONO
    echo ================================================================================
    echo 💡 Posibles soluciones:
    echo    1. Ejecutar como administrador
    echo    2. Verificar permisos del escritorio
    echo    3. Comprobar que el antivirus no bloquee
    echo.
    echo 🔧 Intenta ejecutar este script como administrador
)

echo.
echo ================================================================================
pause