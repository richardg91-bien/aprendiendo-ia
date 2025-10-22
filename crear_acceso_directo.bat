@echo off
title Creador de Acceso Directo - ARIA

echo.
echo 🖥️ CREANDO ACCESO DIRECTO PARA ARIA
echo ================================

:: Crear acceso directo en el escritorio
set "SCRIPT_DIR=%~dp0"
set "DESKTOP=%USERPROFILE%\Desktop"
set "SHORTCUT_NAME=🚀 ARIA - Asistente IA.lnk"

echo 📁 Directorio del proyecto: %SCRIPT_DIR%
echo 🖥️ Escritorio: %DESKTOP%
echo.

:: Crear archivo VBS temporal para crear el acceso directo
echo Set oWS = WScript.CreateObject("WScript.Shell") > "%TEMP%\CreateShortcut.vbs"
echo sLinkFile = "%DESKTOP%\%SHORTCUT_NAME%" >> "%TEMP%\CreateShortcut.vbs"
echo Set oLink = oWS.CreateShortcut(sLinkFile) >> "%TEMP%\CreateShortcut.vbs"
echo oLink.TargetPath = "%SCRIPT_DIR%INICIAR_ARIA_COMPLETO.bat" >> "%TEMP%\CreateShortcut.vbs"
echo oLink.WorkingDirectory = "%SCRIPT_DIR%" >> "%TEMP%\CreateShortcut.vbs"
echo oLink.Description = "Inicia el sistema completo ARIA con un clic" >> "%TEMP%\CreateShortcut.vbs"
echo oLink.IconLocation = "shell32.dll,137" >> "%TEMP%\CreateShortcut.vbs"
echo oLink.Save >> "%TEMP%\CreateShortcut.vbs"

:: Ejecutar el script VBS
cscript //nologo "%TEMP%\CreateShortcut.vbs"

:: Limpiar archivo temporal
del "%TEMP%\CreateShortcut.vbs"

echo ✅ Acceso directo creado en el escritorio
echo 🔗 Nombre: %SHORTCUT_NAME%
echo.
echo 🎉 ¡Ahora puedes iniciar ARIA con un doble clic desde el escritorio!
echo.
echo 💡 El acceso directo ejecutará:
echo    - Activará el entorno virtual
echo    - Iniciará el servidor backend
echo    - Iniciará el frontend React
echo    - Abrirá ARIA en tu navegador
echo.
pause