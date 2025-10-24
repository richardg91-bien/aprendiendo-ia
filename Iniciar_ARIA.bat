@echo off
chcp 65001 >nul
title 🤖 ARIA - Asistente IA Personal

echo.
echo ████████████████████████████████████████████████████████████████
echo                    🤖 ARIA - ASISTENTE IA PERSONAL
echo ████████████████████████████████████████████████████████████████
echo.
echo 🚀 Iniciando ARIA...
echo 📍 Acceso directo desde escritorio
echo ⏱️  Fecha: %date% %time%
echo.
echo ████████████████████████████████████████████████████████████████

REM Cambiar al directorio del proyecto
cd /d "C:\Users\richa\OneDrive\Desktop\aprendiendo-ia"

REM Activar entorno virtual si existe
if exist "venv\Scripts\activate.bat" (
    echo ✅ Activando entorno virtual...
    call venv\Scripts\activate.bat
) else (
    echo ⚠️  Entorno virtual no encontrado, usando Python global
)

REM Verificar que el archivo existe
if not exist "src\aria_servidor_superbase.py" (
    echo ❌ ERROR: No se encuentra el servidor ARIA
    echo    Verifica que estés en el directorio correcto
    pause
    exit /b 1
)

echo ✅ Entrando al directorio src...
cd src

echo ✅ Iniciando servidor ARIA...
echo.
echo 🌐 El servidor se abrirá en: http://localhost:8000
echo 🖥️  Para escritorio remoto usa: 192.168.0.55:3389
echo.
echo ████████████████████████████████████████████████████████████████
echo                     ¡ARIA ESTÁ LISTO!
echo ████████████████████████████████████████████████████████████████
echo.

REM Esperar un momento y abrir el navegador
timeout /t 3 /nobreak >nul
start "" "http://localhost:8000"

REM Iniciar el servidor (esto mantendrá la ventana abierta)
python aria_servidor_superbase.py

REM Si el servidor se cierra, mostrar mensaje
echo.
echo ████████████████████████████████████████████████████████████████
echo                   ARIA SE HA DETENIDO
echo ████████████████████████████████████████████████████████████████
echo.
echo 🛑 El servidor ARIA se ha cerrado
echo 💡 Puedes cerrar esta ventana o presionar cualquier tecla
echo.
pause