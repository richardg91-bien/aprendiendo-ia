@echo off
:: 🎨 ARIA - Acceso Directo a Interfaz Moderna
:: Inicia ARIA con la interfaz React moderna

title ARIA - Interfaz Moderna
color 0B

echo.
echo ================================================================================
echo 🎨 ARIA - INICIANDO CON INTERFAZ MODERNA
echo ================================================================================
echo 🚀 Backend Flask + Frontend React
echo 🤖 Cara de robot animada
echo 🎭 Emociones de IA en tiempo real
echo ✨ Animaciones fluidas
echo.

:: Cambiar al directorio del proyecto
cd /d "%~dp0"

:: Verificar archivos necesarios
if not exist "INICIAR_ARIA_COMPLETO.ps1" (
    echo ❌ Error: No se encuentra el launcher completo
    pause
    exit /b 1
)

echo 🔧 Iniciando sistema completo...
echo.

:: Ejecutar el launcher PowerShell completo
powershell -ExecutionPolicy Bypass -File "INICIAR_ARIA_COMPLETO.ps1"

echo.
echo 👋 ARIA se ha detenido
pause