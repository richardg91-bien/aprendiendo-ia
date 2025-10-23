@echo off
chcp 65001 > nul
cls

echo.
echo ===============================================
echo    🤖 ARIA - Asistente IA Futurista 🤖
echo ===============================================
echo.
echo 🚀 Iniciando sistema ESTABLE...
echo.

REM Cambiar al directorio del proyecto
cd /d "C:\Users\richa\OneDrive\Desktop\aprendiendo-ia"

echo 🧹 Limpiando procesos anteriores...
taskkill /F /IM python.exe 2>nul
taskkill /F /IM node.exe 2>nul

echo.
echo 🔧 Iniciando Backend ARIA Estable...

REM Activar entorno virtual
call venv\Scripts\activate.bat

REM Cambiar al directorio del código fuente
cd backend\src

echo ⏳ Iniciando servidor en puerto 8000...
echo.
echo 🌐 Una vez iniciado, abre: http://localhost:8000
echo 📊 API Status: http://localhost:8000/api/status
echo 💬 Para probar chat usa PowerShell:
echo    Invoke-RestMethod -Uri "http://localhost:8000/api/chat" -Method POST -ContentType "application/json" -Body '{\"message\":\"Hola ARIA\"}'
echo.
echo ⏹️ Presiona Ctrl+C para detener el servidor
echo ===============================================
echo.

REM Iniciar servidor ultra simple y estable
python main_ultra_simple_working.py

echo.
echo 👋 Servidor ARIA detenido
pause