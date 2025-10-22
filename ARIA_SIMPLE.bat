@echo off
title ARIA - Inicio Simple y Funcional
color 0A

echo.
echo 🚀 ARIA - INICIO SIMPLE
echo ====================
echo.

:: Cambiar al directorio del proyecto
cd /d "C:\Users\richa\OneDrive\Desktop\aprendiendo-ia"

:: Activar entorno virtual
call venv\Scripts\activate.bat

echo [1/3] 🖥️ Iniciando servidor backend en puerto 8000...
start "ARIA Backend" cmd /k "venv\Scripts\python.exe backend\src\main_stable.py"

echo [2/3] ⏳ Esperando 8 segundos para que el backend inicie...
timeout /t 8 /nobreak

echo [3/3] 🎨 Iniciando frontend React...
cd frontend
start "ARIA Frontend" cmd /k "set PORT=3000 && npm start"

echo.
echo ✅ ARIA iniciándose...
echo ⏳ Esperando 15 segundos...
timeout /t 15 /nobreak

echo 🌐 Abriendo ARIA...
start http://localhost:3000

echo.
echo 🎉 ¡ARIA debería estar funcionando!
echo 📋 URLs:
echo    Frontend: http://localhost:3000
echo    Backend:  http://localhost:8000
echo.
echo 💡 Si no funciona, verifica las ventanas del terminal que se abrieron
pause