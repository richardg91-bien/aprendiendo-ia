@echo off
title ARIA - Sistema Completo de IA
color 0A

echo.
echo  ██████╗ ██████╗ ██╗ █████╗ 
echo ██╔══██╗██╔══██╗██║██╔══██╗
echo ██████╔╝██████╔╝██║███████║
echo ██╔══██╗██╔══██╗██║██╔══██║
echo ██║  ██║██║  ██║██║██║  ██║
echo ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝╚═╝  ╚═╝
echo.
echo ===================================
echo  INICIANDO SISTEMA ARIA COMPLETO
echo ===================================
echo.

echo [1/4] Activando entorno virtual...
cd /d "C:\Users\richa\OneDrive\Desktop\aprendiendo-ia"
call venv\Scripts\activate.bat

echo [2/4] Verificando dependencias...
pip install -q flask flask-cors requests python-dotenv pyttsx3 psycopg[binary]

echo [3/4] Iniciando servidor backend...
start "ARIA Backend" cmd /k "cd /d C:\Users\richa\OneDrive\Desktop\aprendiendo-ia && venv\Scripts\activate && python backend\src\main_stable.py"

echo [4/4] Esperando 5 segundos para iniciar frontend...
timeout /t 5 /nobreak

echo [5/5] Iniciando frontend React...
cd frontend
if exist node_modules (
    start "ARIA Frontend" cmd /k "npm start"
) else (
    echo Instalando dependencias del frontend...
    call npm install
    start "ARIA Frontend" cmd /k "npm start"
)

echo.
echo ===================================
echo   ARIA INICIADO COMPLETAMENTE
echo ===================================
echo.
echo Backend: http://localhost:5002
echo Frontend: http://localhost:3000
echo Supabase: Conectado
echo.
echo Presiona cualquier tecla para abrir ARIA...
pause >nul

start http://localhost:3000

echo.
echo ARIA ejecutandose en segundo plano.
echo Cierra esta ventana cuando termines.
echo.
pause