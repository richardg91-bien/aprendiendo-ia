@echo off
:: Script para limpiar iconos duplicados de ARIA y dejar solo uno

title ARIA - Limpieza de Iconos
echo.
echo ================================================================================
echo ARIA - LIMPIEZA DE ICONOS DUPLICADOS
echo ================================================================================
echo.

:: Listar iconos existentes
echo Iconos de ARIA encontrados en el escritorio:
powershell -Command "Get-ChildItem ([Environment]::GetFolderPath('Desktop')) -Name '*ARIA*'" | findstr ".lnk"

echo.
echo Limpiando iconos duplicados...

:: Eliminar iconos duplicados (conservar el principal)
powershell -Command ^
"$desktop = [Environment]::GetFolderPath('Desktop'); ^
$files = @('ARIA - Menu Principal.lnk', 'ARIA Asistente IA.lnk'); ^
foreach ($file in $files) { ^
    $path = Join-Path $desktop $file; ^
    if (Test-Path $path) { ^
        Remove-Item $path -Force; ^
        Write-Host \"Eliminado: $file\" -ForegroundColor Yellow ^
    } ^
}"

echo.
echo Verificando estado final...
powershell -Command "Get-ChildItem ([Environment]::GetFolderPath('Desktop')) -Name '*ARIA*'" | findstr ".lnk"

echo.
echo ================================================================================
echo ✅ LIMPIEZA COMPLETADA
echo ================================================================================
echo.
echo 📋 Estado final:
echo   - Icono principal: ARIA - Asistente IA.lnk
echo   - Ubicacion: Escritorio
echo   - Funcion: Abrir menu principal de ARIA
echo.
echo 🚀 Haz doble clic en el icono para usar ARIA
echo.
echo ================================================================================
pause