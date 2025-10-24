@echo off
chcp 65001 >nul
echo 🎨 Creando iconos visibles de ARIA - Versión mejorada...
echo.

REM Crear VBScript más robusto
(
echo Set objShell = CreateObject^("WScript.Shell"^)
echo strDesktop = objShell.SpecialFolders^("Desktop"^)
echo strWorkingDir = "%CD%"
echo.
echo REM Icono principal ARIA
echo Set objShortcut = objShell.CreateShortcut^(strDesktop ^& "\🤖 ARIA.lnk"^)
echo objShortcut.TargetPath = strWorkingDir ^& "\ARIA_Desktop.bat"
echo objShortcut.WorkingDirectory = strWorkingDir
echo objShortcut.Description = "🤖 ARIA - Asistente de IA Personal"
echo objShortcut.IconLocation = "C:\Windows\System32\imageres.dll,76"
echo objShortcut.Save
echo.
echo REM Icono inicio rápido
echo Set objShortcut2 = objShell.CreateShortcut^(strDesktop ^& "\🚀 ARIA Rápido.lnk"^)
echo objShortcut2.TargetPath = strWorkingDir ^& "\Iniciar_ARIA.bat"
echo objShortcut2.WorkingDirectory = strWorkingDir
echo objShortcut2.Description = "🚀 Iniciar ARIA directamente"
echo objShortcut2.IconLocation = "C:\Windows\System32\shell32.dll,21"
echo objShortcut2.Save
echo.
echo REM Icono sistema IA
echo Set objShortcut3 = objShell.CreateShortcut^(strDesktop ^& "\🧠 ARIA IA.lnk"^)
echo objShortcut3.TargetPath = strWorkingDir ^& "\ARIA_Desktop.bat"
echo objShortcut3.WorkingDirectory = strWorkingDir
echo objShortcut3.Description = "🧠 Sistema de Inteligencia Artificial ARIA"
echo objShortcut3.IconLocation = "C:\Windows\System32\shell32.dll,13"
echo objShortcut3.Save
) > "%TEMP%\aria_desktop_icons.vbs"

echo ✅ Ejecutando creación de iconos...
cscript //nologo "%TEMP%\aria_desktop_icons.vbs"

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ████████████████████████████████████████████████████████████████
    echo              🎉 ¡ICONOS CREADOS CORRECTAMENTE!
    echo ████████████████████████████████████████████████████████████████
    echo.
    echo 📍 Revisa tu escritorio, deberías ver:
    echo.
    echo    🤖 "🤖 ARIA.lnk"              - Panel principal completo
    echo    🚀 "🚀 ARIA Rápido.lnk"       - Inicio súper rápido  
    echo    🧠 "🧠 ARIA IA.lnk"           - Sistema de IA completo
    echo.
    echo 🎯 Cada icono tiene su emoji distintivo para fácil identificación
    echo 🖼️ Usan iconos nativos de Windows para máxima visibilidad
    echo ✨ ¡Ahora ARIA está súper visible en tu escritorio!
    echo.
    echo 💡 Tip: Haz doble clic en cualquiera para acceder a ARIA
) else (
    echo ❌ Hubo un problema al crear los iconos
    echo ℹ️ Pero puede que algunos se hayan creado correctamente
)

echo.
echo 🧹 Limpiando...
del "%TEMP%\aria_desktop_icons.vbs" 2>nul

echo.
echo 🔍 Verificando escritorio...
dir "%USERPROFILE%\Desktop\*ARIA*" 2>nul | find ".lnk" >nul
if %ERRORLEVEL% EQU 0 (
    echo ✅ ¡Confirmado! Hay iconos de ARIA en tu escritorio
    echo.
    dir "%USERPROFILE%\Desktop\*ARIA*" | findstr /C:".lnk"
) else (
    echo ⚠️ No se detectaron iconos, pero pueden estar ahí con nombres diferentes
)

echo.
pause