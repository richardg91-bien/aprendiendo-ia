@echo off
echo 🚀 ARIA FUTURISTIC SYSTEM - INICIO RÁPIDO
echo ==========================================
echo.

echo 🔍 Verificando Python...
python --version
if errorlevel 1 (
    echo ❌ Python no encontrado. Instala Python primero.
    pause
    exit /b 1
)

echo.
echo 📦 Instalando dependencias...
pip install -r backend/requirements.txt

echo.
echo 🧠 Iniciando servidor de ARIA...
echo 🌐 La interfaz estará disponible en: http://127.0.0.1:8000
echo 🚀 Modo futurista activado por defecto
echo.

echo 🎭 COLORES EMOCIONALES:
echo    🔵 Azul = Normal/Interacción
echo    🟢 Verde = Aprendiendo
echo    🔴 Rojo = Frustrada
echo    🟡 Dorado = Feliz
echo    🟣 Púrpura = Pensando
echo.

echo ⚠️  IMPORTANTE: Para usar la base de datos en la nube:
echo    1. Configura tu archivo .env con credenciales de Supabase
echo    2. Ver guía completa en: GUIA_BASE_DATOS_NUBE.md
echo.

echo 🚀 Iniciando ARIA...
python main_stable.py

pause