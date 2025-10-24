@echo off
chcp 65001 >nul
echo 🎨 Creando iconos visibles de ARIA en el escritorio...
echo.

REM Crear archivo VBS para generar iconos
echo Set objShell = CreateObject("WScript.Shell") > "%TEMP%\aria_icons.vbs"
echo Set objDesktop = objShell.SpecialFolders("Desktop") >> "%TEMP%\aria_icons.vbs"
echo. >> "%TEMP%\aria_icons.vbs"
echo REM Icono principal con emoji robot >> "%TEMP%\aria_icons.vbs"
echo Set objShortcut1 = objShell.CreateShortcut(objDesktop ^& "\🤖 ARIA Asistente IA.lnk") >> "%TEMP%\aria_icons.vbs"
echo objShortcut1.TargetPath = "%CD%\ARIA_Desktop.bat" >> "%TEMP%\aria_icons.vbs"
echo objShortcut1.WorkingDirectory = "%CD%" >> "%TEMP%\aria_icons.vbs"
echo objShortcut1.Description = "🤖 ARIA - Tu Asistente de IA Personal con Supabase" >> "%TEMP%\aria_icons.vbs"
echo objShortcut1.IconLocation = "C:\Windows\System32\imageres.dll,76" >> "%TEMP%\aria_icons.vbs"
echo objShortcut1.Save >> "%TEMP%\aria_icons.vbs"
echo. >> "%TEMP%\aria_icons.vbs"
echo REM Icono de inicio rápido >> "%TEMP%\aria_icons.vbs"
echo Set objShortcut2 = objShell.CreateShortcut(objDesktop ^& "\🚀 ARIA Inicio Rápido.lnk") >> "%TEMP%\aria_icons.vbs"
echo objShortcut2.TargetPath = "%CD%\Iniciar_ARIA.bat" >> "%TEMP%\aria_icons.vbs"
echo objShortcut2.WorkingDirectory = "%CD%" >> "%TEMP%\aria_icons.vbs"
echo objShortcut2.Description = "🚀 Iniciar ARIA directamente - Un clic y listo" >> "%TEMP%\aria_icons.vbs"
echo objShortcut2.IconLocation = "C:\Windows\System32\shell32.dll,21" >> "%TEMP%\aria_icons.vbs"
echo objShortcut2.Save >> "%TEMP%\aria_icons.vbs"
echo. >> "%TEMP%\aria_icons.vbs"
echo REM Icono de inteligencia artificial >> "%TEMP%\aria_icons.vbs"
echo Set objShortcut3 = objShell.CreateShortcut(objDesktop ^& "\🧠 ARIA Intelligence.lnk") >> "%TEMP%\aria_icons.vbs"
echo objShortcut3.TargetPath = "%CD%\ARIA_Desktop.bat" >> "%TEMP%\aria_icons.vbs"
echo objShortcut3.WorkingDirectory = "%CD%" >> "%TEMP%\aria_icons.vbs"
echo objShortcut3.Description = "🧠 ARIA - Inteligencia Artificial Avanzada" >> "%TEMP%\aria_icons.vbs"
echo objShortcut3.IconLocation = "C:\Windows\System32\shell32.dll,13" >> "%TEMP%\aria_icons.vbs"
echo objShortcut3.Save >> "%TEMP%\aria_icons.vbs"
echo. >> "%TEMP%\aria_icons.vbs"
echo REM Icono de control >> "%TEMP%\aria_icons.vbs"
echo Set objShortcut4 = objShell.CreateShortcut(objDesktop ^& "\🎯 ARIA Control.lnk") >> "%TEMP%\aria_icons.vbs"
echo objShortcut4.TargetPath = "%CD%\ARIA_Desktop.bat" >> "%TEMP%\aria_icons.vbs"
echo objShortcut4.WorkingDirectory = "%CD%" >> "%TEMP%\aria_icons.vbs"
echo objShortcut4.Description = "🎯 Panel de Control Completo de ARIA" >> "%TEMP%\aria_icons.vbs"
echo objShortcut4.IconLocation = "C:\Windows\System32\shell32.dll,137" >> "%TEMP%\aria_icons.vbs"
echo objShortcut4.Save >> "%TEMP%\aria_icons.vbs"
echo. >> "%TEMP%\aria_icons.vbs"
echo REM Icono de sistema >> "%TEMP%\aria_icons.vbs"
echo Set objShortcut5 = objShell.CreateShortcut(objDesktop ^& "\⚡ ARIA System.lnk") >> "%TEMP%\aria_icons.vbs"
echo objShortcut5.TargetPath = "%CD%\Iniciar_ARIA.bat" >> "%TEMP%\aria_icons.vbs"
echo objShortcut5.WorkingDirectory = "%CD%" >> "%TEMP%\aria_icons.vbs"
echo objShortcut5.Description = "⚡ Sistema ARIA - Acceso Ultra Rápido" >> "%TEMP%\aria_icons.vbs"
echo objShortcut5.IconLocation = "C:\Windows\System32\imageres.dll,1" >> "%TEMP%\aria_icons.vbs"
echo objShortcut5.Save >> "%TEMP%\aria_icons.vbs"

echo ✅ Script VBS generado, ejecutando...
cscript //nologo "%TEMP%\aria_icons.vbs"

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ████████████████████████████████████████████████████████████████
    echo                   🎉 ICONOS CREADOS EXITOSAMENTE
    echo ████████████████████████████████████████████████████████████████
    echo.
    echo 📍 Se han creado 5 iconos visibles en tu escritorio:
    echo.
    echo    🤖 "🤖 ARIA Asistente IA.lnk"      - Panel completo principal
    echo    🚀 "🚀 ARIA Inicio Rápido.lnk"     - Inicio directo y rápido
    echo    🧠 "🧠 ARIA Intelligence.lnk"      - Versión inteligencia
    echo    🎯 "🎯 ARIA Control.lnk"           - Panel de control
    echo    ⚡ "⚡ ARIA System.lnk"            - Acceso ultra rápido
    echo.
    echo 🎨 Cada icono tiene un emoji distintivo para fácil identificación
    echo 🖼️ Todos usan iconos del sistema de Windows para mejor visibilidad
    echo 🎯 Diferentes opciones para diferentes necesidades de uso
    echo.
    echo ✨ ¡ARIA ahora es súper visible en tu escritorio!
) else (
    echo ❌ Error al crear los iconos
)

echo.
echo 🧹 Limpiando archivos temporales...
del "%TEMP%\aria_icons.vbs" 2>nul

echo.
pause