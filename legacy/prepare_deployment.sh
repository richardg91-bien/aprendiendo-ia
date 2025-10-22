#!/bin/bash
# Script de preparación para deployment

echo "🚀 Preparando ARIA para deployment..."

# Crear directorio de logs si no existe
mkdir -p logs

# Verificar que todas las dependencias estén instaladas
echo "📦 Verificando dependencias..."
pip install -r backend/requirements.txt

# Verificar estructura de archivos
echo "📁 Verificando estructura de archivos..."
files_required=(
    "backend/src/main.py"
    "backend/src/feedback_system.py"
    "backend/requirements.txt"
    "railway.json"
    "Procfile"
    "database_schema.sql"
)

for file in "${files_required[@]}"; do
    if [ -f "$file" ]; then
        echo "✅ $file - OK"
    else
        echo "❌ $file - FALTA"
        exit 1
    fi
done

# Verificar que el frontend esté construido
if [ -d "frontend/build" ]; then
    echo "✅ Frontend build - OK"
else
    echo "🔧 Construyendo frontend..."
    cd frontend && npm run build && cd ..
fi

# Verificar sintaxis Python
echo "🐍 Verificando sintaxis Python..."
python -m py_compile backend/src/main.py
python -m py_compile backend/src/feedback_system.py

echo "✅ ¡ARIA está listo para deployment!"
echo ""
echo "📋 Próximos pasos:"
echo "1. Subir código a GitHub"
echo "2. Configurar Supabase"
echo "3. Crear proyecto en Railway"
echo "4. Configurar variables de entorno"
echo "5. ¡Disfrutar tu ARIA en la nube! 🌩️"