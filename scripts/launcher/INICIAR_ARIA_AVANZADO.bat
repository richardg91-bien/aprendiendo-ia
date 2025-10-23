@echo off
chcp 65001 >nul
title ARIA - Sistema Avanzado de Aprendizaje

echo.
echo ================================================================================
echo 🚀 ARIA - SISTEMA DE APRENDIZAJE AUTÓNOMO AVANZADO
echo ================================================================================
echo.
echo ✨ SUPERANDO LIMITACIONES ANTERIORES:
echo    ❌ YA NO es un sistema simulado
echo    ✅ Acceso a internet en tiempo real
echo    ✅ Fuentes externas verificadas (Wikipedia, ArXiv, RSS)
echo    ✅ Análisis de contenido web inteligente
echo    ✅ Conocimiento real y actualizado
echo.
echo ================================================================================

:: Verificar entorno virtual
if not exist "venv\Scripts\python.exe" (
    echo ❌ Entorno virtual no encontrado
    echo 💡 Ejecuta: python -m venv venv
    pause
    exit /b 1
)

:: Activar entorno virtual
echo 🔧 Activando entorno virtual...
call venv\Scripts\activate.bat

:: Limpiar procesos anteriores
echo 🧹 Limpiando procesos anteriores...
taskkill /f /im python.exe 2>nul
taskkill /f /im node.exe 2>nul
timeout /t 2 /nobreak >nul

:: Verificar dependencias críticas
echo 🔍 Verificando dependencias avanzadas...
venv\Scripts\python.exe -c "import feedparser, beautifulsoup4, lxml, requests; print('✅ Dependencias OK')" 2>nul
if errorlevel 1 (
    echo ⚠️ Instalando dependencias del sistema avanzado...
    venv\Scripts\python.exe -m pip install feedparser beautifulsoup4 lxml requests
    if errorlevel 1 (
        echo ❌ Error instalando dependencias
        pause
        exit /b 1
    )
)

:: Iniciar ARIA con sistema avanzado
echo.
echo 🚀 Iniciando ARIA con capacidades avanzadas...
venv\Scripts\python.exe start_aria_advanced.py

:: En caso de error
if errorlevel 1 (
    echo.
    echo ❌ Error durante el inicio
    echo 💡 Revisa el log anterior para más detalles
    pause
)

echo.
echo 👋 ARIA finalizado
pause