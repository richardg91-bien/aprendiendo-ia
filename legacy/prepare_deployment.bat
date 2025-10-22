@echo off
REM Script de preparación para deployment en Windows

echo 🚀 Preparando ARIA para deployment...

REM Crear directorio de logs si no existe
if not exist "logs" mkdir logs

REM Verificar dependencias
echo 📦 Verificando dependencias...
python -m pip install -r backend\requirements.txt

REM Verificar archivos requeridos
echo 📁 Verificando estructura de archivos...

if exist "backend\src\main.py" (
    echo ✅ main.py - OK
) else (
    echo ❌ main.py - FALTA
    pause
    exit /b 1
)

if exist "backend\src\feedback_system.py" (
    echo ✅ feedback_system.py - OK
) else (
    echo ❌ feedback_system.py - FALTA
    pause
    exit /b 1
)

if exist "railway.json" (
    echo ✅ railway.json - OK
) else (
    echo ❌ railway.json - FALTA
    pause
    exit /b 1
)

REM Verificar sintaxis Python
echo 🐍 Verificando sintaxis Python...
python -m py_compile backend\src\main.py
python -m py_compile backend\src\feedback_system.py

echo.
echo ✅ ¡ARIA está listo para deployment!
echo.
echo 📋 Próximos pasos:
echo 1. Subir código a GitHub
echo 2. Configurar Supabase
echo 3. Crear proyecto en Railway
echo 4. Configurar variables de entorno
echo 5. ¡Disfrutar tu ARIA en la nube! 🌩️
echo.
pause