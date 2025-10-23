@echo off
title ARIA - Inicio Rapido
color 0A

echo.
echo 🚀 ARIA - INICIO RAPIDO
echo =====================
echo.

:: Verificar si ya está ejecutándose
echo 🔍 Verificando si ARIA ya está ejecutándose...
netstat -an | find ":3000" >nul
if %errorlevel% == 0 (
    echo ✅ ARIA ya está ejecutándose!
    echo 🌐 Abriendo en el navegador...
    start http://localhost:3000
    echo.
    echo 💡 Si no se abre, ve manualmente a: http://localhost:3000
    pause
    exit
)

netstat -an | find ":5002" >nul
if %errorlevel% == 0 (
    echo ⚠️  Backend ejecutándose, iniciando solo frontend...
    cd frontend
    start "ARIA Frontend" cmd /k "npm start"
    timeout /t 10 /nobreak
    start http://localhost:3000
    exit
)

echo 📱 ARIA no está ejecutándose. Iniciando...
echo.
echo ⏳ Esto tomará unos segundos...
start "ARIA Iniciador" cmd /k "C:\Users\richa\OneDrive\Desktop\aprendiendo-ia\INICIAR_ARIA_COMPLETO.bat"

echo.
echo ✅ Iniciador ejecutándose en otra ventana
echo ⏳ Esperando 15 segundos...
timeout /t 15 /nobreak

echo 🌐 Abriendo ARIA...
start http://localhost:3000

echo.
echo 🎉 ¡ARIA debería estar ejecutándose!
echo 💡 Si no funciona, usa el iniciador completo
pause