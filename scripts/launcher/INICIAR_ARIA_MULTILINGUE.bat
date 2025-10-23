@echo off
title ARIA - Sistema Multilingüe Completo
echo.
echo ================================================================
echo   🌐 ARIA - SISTEMA AVANZADO CON APIS EN ESPAÑOL  
echo ================================================================
echo.
echo ✅ Capacidades implementadas:
echo    🇪🇸 APIs en español (LibreTranslate, RAE, noticias)
echo    🇺🇸 APIs en inglés (ArXiv, Wikipedia, RSS)
echo    🧠 Conocimiento real y verificado
echo    🔍 Búsqueda semántica multilingüe
echo    📚 Definiciones de la Real Academia Española
echo    📰 Noticias científicas en tiempo real
echo.

cd /d "%~dp0"

echo 🧪 Ejecutando prueba multilingüe...
echo.
..\..\venv\Scripts\python.exe probar_multilingue.py

echo.
echo 🚀 Iniciando servidor ARIA con capacidades multilingües...
echo.

cd backend\src
start "ARIA Backend Multilingüe" ..\..\venv\Scripts\python.exe main_stable.py

echo ⏳ Esperando a que el backend esté listo...
timeout /t 8 /nobreak >nul

echo.
echo 🌐 Servidor iniciado. Ahora puedes probar:
echo.
echo    💬 "¿Qué has aprendido?"
echo    💬 "Define tecnología"
echo    💬 "¿Qué sabes sobre inteligencia artificial?"
echo    💬 "What do you know about machine learning?"
echo    💬 "Cuéntame sobre cloud computing"
echo.
echo 📍 API disponible en: http://localhost:8000
echo.

pause