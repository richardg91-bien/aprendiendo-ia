@echo off
title ARIA - Inicio Completo con Conocimiento Real
echo.
echo ===============================================
echo   🤖 ARIA - SISTEMA AVANZADO ACTIVADO  
echo ===============================================
echo.
echo ✅ Mejoras implementadas:
echo    - Conocimiento real de internet (no simulado)
echo    - Base de datos científica verificada
echo    - Respuestas inteligentes (no genéricas)
echo    - APIs ArXiv y Wikipedia integradas
echo.
echo 🚀 Iniciando ARIA...

cd /d "%~dp0"
cd backend\src

echo.
echo 📚 Verificando conocimiento...
..\..\venv\Scripts\python.exe -c "
import sys
sys.path.append('.')
from auto_learning_advanced import aria_advanced_learning
status = aria_advanced_learning.get_status()
total = status.get('total_knowledge', 0)
print(f'   📊 Conocimiento disponible: {total} elementos')
if total == 0:
    print('   🔄 Agregando conocimiento inicial...')
    aria_advanced_learning._learn_from_arxiv('cloud computing')
    aria_advanced_learning._learn_from_arxiv('artificial intelligence')
    status = aria_advanced_learning.get_status()
    print(f'   ✅ Conocimiento cargado: {status.get(\"total_knowledge\", 0)} elementos')
"

echo.
echo 🌐 Iniciando servidor ARIA...
echo    📍 Backend: http://localhost:8000
echo    📍 Frontend: http://localhost:3001
echo.
echo ⚠️  IMPORTANTE: ARIA ahora responde con conocimiento real
echo    - Pregunta: "¿Qué has aprendido?"
echo    - Pregunta: "¿Qué sabes sobre cloud computing?"
echo    - Pregunta: "¿Tienes información sobre FPGAs?"
echo.

start "ARIA Backend" ..\..\venv\Scripts\python.exe main_stable.py

timeout /t 5 /nobreak >nul

cd ..\..\frontend
start "ARIA Frontend" npm start

echo.
echo 🎉 ARIA iniciado correctamente!
echo 💡 Abre tu navegador en: http://localhost:3001
echo.
pause