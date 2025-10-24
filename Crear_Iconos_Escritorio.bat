@echo off
chcp 65001 >nul
title 🎨 Creador de Icono ARIA para Escritorio

echo.
echo ████████████████████████████████████████████████████████████████
echo                🎨 CREANDO ICONO ARIA PARA ESCRITORIO
echo ████████████████████████████████████████████████████████████████
echo.

echo 🚀 Paso 1: Creando archivo de icono personalizado...

REM Crear un archivo VBS para generar un icono
echo Set objShell = CreateObject("WScript.Shell") > "%TEMP%\create_aria_icon.vbs"
echo Set objDesktop = objShell.SpecialFolders("Desktop") >> "%TEMP%\create_aria_icon.vbs"
echo Set objShortcut = objShell.CreateShortcut(objDesktop ^& "\🤖 ARIA - Asistente IA.lnk") >> "%TEMP%\create_aria_icon.vbs"
echo objShortcut.TargetPath = "%CD%\ARIA_Desktop.bat" >> "%TEMP%\create_aria_icon.vbs"
echo objShortcut.WorkingDirectory = "%CD%" >> "%TEMP%\create_aria_icon.vbs"
echo objShortcut.Description = "🤖 ARIA - Tu Asistente de IA Personal con Supabase y APIs Españolas" >> "%TEMP%\create_aria_icon.vbs"
echo objShortcut.IconLocation = "C:\Windows\System32\shell32.dll,13" >> "%TEMP%\create_aria_icon.vbs"
echo objShortcut.Save >> "%TEMP%\create_aria_icon.vbs"
echo.
echo Set objShortcut2 = objShell.CreateShortcut(objDesktop ^& "\🚀 Iniciar ARIA Rápido.lnk") >> "%TEMP%\create_aria_icon.vbs"
echo objShortcut2.TargetPath = "%CD%\Iniciar_ARIA.bat" >> "%TEMP%\create_aria_icon.vbs"
echo objShortcut2.WorkingDirectory = "%CD%" >> "%TEMP%\create_aria_icon.vbs"
echo objShortcut2.Description = "🚀 Iniciar ARIA directamente - Servidor + Navegador automático" >> "%TEMP%\create_aria_icon.vbs"
echo objShortcut2.IconLocation = "C:\Windows\System32\shell32.dll,21" >> "%TEMP%\create_aria_icon.vbs"
echo objShortcut2.Save >> "%TEMP%\create_aria_icon.vbs"

echo ✅ Archivo de creación preparado
echo.

echo 🚀 Paso 2: Ejecutando creador de iconos...
cscript //nologo "%TEMP%\create_aria_icon.vbs"

echo.
echo 🚀 Paso 3: Creando icono adicional con PowerShell para mejor visualización...

REM Crear icono adicional con PowerShell
powershell -Command "& {$WshShell = New-Object -comObject WScript.Shell; $Desktop = $WshShell.SpecialFolders('Desktop'); $Shortcut = $WshShell.CreateShortcut($Desktop + '\ARIA AI Assistant.lnk'); $Shortcut.TargetPath = '%CD%\ARIA_Desktop.bat'; $Shortcut.WorkingDirectory = '%CD%'; $Shortcut.Description = 'ARIA - Asistente de Inteligencia Artificial'; $Shortcut.IconLocation = 'C:\Windows\System32\imageres.dll,76'; $Shortcut.Save(); Write-Host 'Icono principal creado'}"

powershell -Command "& {$WshShell = New-Object -comObject WScript.Shell; $Desktop = $WshShell.SpecialFolders('Desktop'); $Shortcut = $WshShell.CreateShortcut($Desktop + '\ARIA Quick Start.lnk'); $Shortcut.TargetPath = '%CD%\Iniciar_ARIA.bat'; $Shortcut.WorkingDirectory = '%CD%'; $Shortcut.Description = 'Inicio rápido de ARIA - Un clic y listo'; $Shortcut.IconLocation = 'C:\Windows\System32\imageres.dll,1'; $Shortcut.Save(); Write-Host 'Icono de inicio rápido creado'}"

echo.
echo 🎯 Paso 4: Creando icono con imagen de robot más visible...

REM Crear un icono más llamativo
powershell -Command "& {$WshShell = New-Object -comObject WScript.Shell; $Desktop = $WshShell.SpecialFolders('Desktop'); $Shortcut = $WshShell.CreateShortcut($Desktop + '\🤖 ARIA IA.lnk'); $Shortcut.TargetPath = '%CD%\ARIA_Desktop.bat'; $Shortcut.WorkingDirectory = '%CD%'; $Shortcut.Description = '🤖 ARIA - Inteligencia Artificial Personal'; $Shortcut.IconLocation = 'C:\Windows\System32\ddores.dll,10'; $Shortcut.Save(); Write-Host 'Icono visual creado'}"

echo.
echo 🌟 Paso 5: Limpiando archivos temporales...
del "%TEMP%\create_aria_icon.vbs" 2>nul

echo.
echo ████████████████████████████████████████████████████████████████
echo                   ✅ ICONOS CREADOS EXITOSAMENTE
echo ████████████████████████████████████████████████████████████████
echo.
echo 🎉 Se han creado varios iconos en tu escritorio:
echo.
echo    🤖 "🤖 ARIA - Asistente IA.lnk"     - Panel completo con emoji
echo    🚀 "🚀 Iniciar ARIA Rápido.lnk"     - Inicio directo con emoji  
echo    💻 "ARIA AI Assistant.lnk"          - Versión en inglés
echo    ⚡ "ARIA Quick Start.lnk"           - Inicio rápido en inglés
echo    🎯 "🤖 ARIA IA.lnk"                - Icono más visible
echo.
echo 💡 Todos los iconos apuntan a ARIA y tienen diferentes iconos visuales
echo 🎨 Usa el que más te guste o tenlos todos para fácil acceso
echo.
echo ✨ ¡ARIA ya está visible en tu escritorio!
echo.
pause