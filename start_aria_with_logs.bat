@echo off
:: 📝 ARIA LOG HELPER - Versión Windows
:: ===================================
:: Helper para capturar logs en Windows sin usar 'tee'

echo 🤖 ARIA SERVER - %date% %time%
echo ✅ Entorno virtual activado

:: Crear directorio de logs si no existe
if not exist "logs" mkdir logs

:: Generar nombre de archivo de log con timestamp
for /f "tokens=2-4 delims=/ " %%a in ('date /t') do (set mydate=%%c%%a%%b)
for /f "tokens=1-2 delims=/:" %%a in ("%TIME%") do (set mytime=%%a%%b)
set logfile=logs\aria_server_%mydate%_%mytime%.log

:: Iniciar servidor con logging
echo 📝 Guardando logs en: %logfile%
echo ========================================== > %logfile%
echo ARIA SERVER INICIADO - %date% %time% >> %logfile%
echo ========================================== >> %logfile%

:: Ejecutar servidor y capturar output
python aria_integrated_server.py 2>&1 | findstr /R ".*" >> %logfile%

echo.
echo 📋 Logs guardados en: %logfile%
pause