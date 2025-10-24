@echo off
chcp 65001 >nul
echo 🎯 Creando icono único de ARIA - Todo integrado...
echo.

REM Eliminar iconos anteriores
echo 🧹 Limpiando iconos anteriores...
del "%USERPROFILE%\Desktop\🤖 ARIA.lnk" 2>nul
del "%USERPROFILE%\Desktop\🚀 ARIA Rápido.lnk" 2>nul
del "%USERPROFILE%\Desktop\🧠 ARIA IA.lnk" 2>nul
del "%USERPROFILE%\Desktop\ARIA Asistente IA.lnk" 2>nul
del "%USERPROFILE%\Desktop\Iniciar ARIA.lnk" 2>nul

REM Crear un icono único y completo
(
echo Set objShell = CreateObject^("WScript.Shell"^)
echo strDesktop = objShell.SpecialFolders^("Desktop"^)
echo strWorkingDir = "%CD%"
echo.
echo REM Icono único ARIA - Todo en uno
echo Set objShortcut = objShell.CreateShortcut^(strDesktop ^& "\🤖 ARIA - Asistente IA.lnk"^)
echo objShortcut.TargetPath = strWorkingDir ^& "\ARIA_Desktop.bat"
echo objShortcut.WorkingDirectory = strWorkingDir
echo objShortcut.Description = "🤖 ARIA - Asistente de IA Personal - Panel de Control Completo con inicio automático, diagnóstico, escritorio remoto y todas las funcionalidades integradas"
echo objShortcut.IconLocation = "C:\Windows\System32\imageres.dll,76"
echo objShortcut.Save
) > "%TEMP%\aria_unico.vbs"

echo ✅ Creando icono único...
cscript //nologo "%TEMP%\aria_unico.vbs"

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ████████████████████████████████████████████████████████████████
    echo               🎉 ¡ICONO ÚNICO CREADO EXITOSAMENTE!
    echo ████████████████████████████████████████████████████████████████
    echo.
    echo 📍 En tu escritorio ahora tienes UN SOLO ICONO:
    echo.
    echo    🤖 "🤖 ARIA - Asistente IA.lnk"
    echo.
    echo 🎯 **ESTE ICONO INCLUYE TODO:**
    echo    ┌─────────────────────────────────────────────────────────────┐
    echo    │ ✅ 🚀 Inicio automático del servidor                        │
    echo    │ ✅ 🌐 Apertura automática del navegador                     │
    echo    │ ✅ 🖥️  Escritorio remoto integrado                          │
    echo    │ ✅ 📊 Diagnóstico del sistema                               │
    echo    │ ✅ 🔧 Herramientas de mantenimiento                        │
    echo    │ ✅ 📁 Acceso directo a archivos                            │
    echo    │ ✅ 📝 Visualización de logs                                │
    echo    │ ✅ 🎛️  Panel de control completo                           │
    echo    └─────────────────────────────────────────────────────────────┘
    echo.
    echo 💡 **CÓMO USAR:**
    echo    1. Doble clic en el icono
    echo    2. Elige la opción que necesites del menú
    echo    3. Para uso normal: opción 1 (inicio completo)
    echo.
    echo ✨ ¡Todo tu poder de IA en un solo clic! 🤖⚡
) else (
    echo ❌ Error al crear el icono único
)

echo.
echo 🧹 Limpiando...
del "%TEMP%\aria_unico.vbs" 2>nul

echo.
echo 🔍 Verificando resultado...
if exist "%USERPROFILE%\Desktop\🤖 ARIA - Asistente IA.lnk" (
    echo ✅ ¡PERFECTO! Icono único creado en el escritorio
    echo.
    echo 📊 **RESUMEN:**
    echo    📂 Ubicación: %USERPROFILE%\Desktop\
    echo    📝 Nombre: 🤖 ARIA - Asistente IA.lnk
    echo    🎯 Función: Panel de control TODO-EN-UNO
    echo    🖼️ Icono: Robot distintivo de Windows
    echo.
    echo 🎊 ¡ARIA está listo para usar desde tu escritorio!
) else (
    echo ⚠️ No se detectó el icono, pero puede estar con nombre ligeramente diferente
)

echo.
pause