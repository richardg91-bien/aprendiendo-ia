@echo off
:: Script directo para crear acceso directo de ARIA usando PowerShell embebido

title ARIA - Creando Icono
echo.
echo ================================================================================
echo ARIA - CREANDO ICONO EN EL ESCRITORIO
echo ================================================================================
echo.

:: Verificar archivos de ARIA
if exist "ARIA_MENU_PRINCIPAL.bat" (
    set "LAUNCHER=ARIA_MENU_PRINCIPAL.bat"
    set "NAME=ARIA - Menu Principal"
) else if exist "INICIAR_ARIA_FINAL.bat" (
    set "LAUNCHER=INICIAR_ARIA_FINAL.bat"
    set "NAME=ARIA - Launcher"
) else (
    echo ERROR: No se encontraron archivos de ARIA
    pause
    exit /b 1
)

echo Creando acceso directo para: %LAUNCHER%
echo.

:: Usar PowerShell embebido para crear el acceso directo
powershell -Command ^
"$desktop = [Environment]::GetFolderPath('Desktop'); ^
$shell = New-Object -ComObject WScript.Shell; ^
$shortcut = $shell.CreateShortcut(\"$desktop\ARIA - Asistente IA.lnk\"); ^
$shortcut.TargetPath = \"%CD%\%LAUNCHER%\"; ^
$shortcut.WorkingDirectory = \"%CD%\"; ^
$shortcut.Description = 'ARIA - Asistente de Inteligencia Artificial'; ^
$shortcut.IconLocation = 'shell32.dll,1'; ^
$shortcut.Save(); ^
Write-Host 'Acceso directo creado exitosamente' -ForegroundColor Green"

echo.
echo ================================================================================
echo VERIFICANDO CREACION...
echo ================================================================================

:: Verificar que se creó
powershell -Command "Test-Path ([Environment]::GetFolderPath('Desktop') + '\ARIA - Asistente IA.lnk')" >nul 2>&1

if %ERRORLEVEL% equ 0 (
    echo.
    echo ✅ EXITO: Icono de ARIA creado en el escritorio
    echo 📁 Nombre: ARIA - Asistente IA.lnk
    echo 🚀 Haz doble clic para iniciar ARIA
    echo.
    echo Funcionalidades disponibles:
    echo   - Interfaz web interactiva
    echo   - Chat con IA avanzada
    echo   - Sistema de aprendizaje
    echo   - APIs REST completas
) else (
    echo.
    echo ❌ ERROR: No se pudo crear el icono
    echo 💡 Intenta ejecutar como administrador
)

echo.
echo ================================================================================
pause