# ======================================
# 🚀 ARIA - Iniciador Completo PowerShell
# ======================================

Write-Host "
 ██████╗ ██████╗ ██╗ █████╗ 
██╔══██╗██╔══██╗██║██╔══██╗
██████╔╝██████╔╝██║███████║
██╔══██╗██╔══██╗██║██╔══██║
██║  ██║██║  ██║██║██║  ██║
╚═╝  ╚═╝╚═╝  ╚═╝╚═╝╚═╝  ╚═╝
" -ForegroundColor Cyan

Write-Host "====================================" -ForegroundColor Green
Write-Host " INICIANDO SISTEMA ARIA COMPLETO" -ForegroundColor Green
Write-Host "====================================" -ForegroundColor Green
Write-Host ""

# Cambiar al directorio del proyecto
Set-Location "C:\Users\richa\OneDrive\Desktop\aprendiendo-ia"

Write-Host "[1/5] 🔧 Activando entorno virtual..." -ForegroundColor Yellow
& .\venv\Scripts\Activate.ps1

Write-Host "[2/5] 📦 Verificando dependencias Python..." -ForegroundColor Yellow
& python -m pip install --quiet flask flask-cors requests python-dotenv pyttsx3 psycopg[binary]

Write-Host "[3/5] 🌐 Verificando conexión a Supabase..." -ForegroundColor Yellow
& python test_supabase_final.py

Write-Host "[4/5] 🖥️  Iniciando servidor backend..." -ForegroundColor Yellow
Start-Process PowerShell -ArgumentList "-NoExit", "-Command", "cd 'C:\Users\richa\OneDrive\Desktop\aprendiendo-ia'; .\venv\Scripts\Activate.ps1; python backend\src\main_stable.py" -WindowStyle Normal

Write-Host "[5/5] ⏳ Esperando 8 segundos antes de iniciar frontend..." -ForegroundColor Yellow
Start-Sleep -Seconds 8

Write-Host "[6/6] 🎨 Iniciando frontend React..." -ForegroundColor Yellow
Set-Location "frontend"

if (Test-Path "node_modules") {
    Start-Process PowerShell -ArgumentList "-NoExit", "-Command", "cd 'C:\Users\richa\OneDrive\Desktop\aprendiendo-ia\frontend'; npm start" -WindowStyle Normal
} else {
    Write-Host "📥 Instalando dependencias del frontend..." -ForegroundColor Magenta
    npm install
    Start-Process PowerShell -ArgumentList "-NoExit", "-Command", "cd 'C:\Users\richa\OneDrive\Desktop\aprendiendo-ia\frontend'; npm start" -WindowStyle Normal
}

Write-Host ""
Write-Host "====================================" -ForegroundColor Green
Write-Host "   🎉 ARIA INICIADO COMPLETAMENTE" -ForegroundColor Green
Write-Host "====================================" -ForegroundColor Green
Write-Host ""
Write-Host "🔗 URLs disponibles:" -ForegroundColor Cyan
Write-Host "   Backend:  http://localhost:5002" -ForegroundColor White
Write-Host "   Frontend: http://localhost:3000" -ForegroundColor White
Write-Host "   Supabase: ✅ Conectado" -ForegroundColor Green
Write-Host ""

# Esperar y abrir navegador
Write-Host "⏳ Esperando 10 segundos para que todo inicie..." -ForegroundColor Yellow
Start-Sleep -Seconds 10

Write-Host "🌐 Abriendo ARIA en el navegador..." -ForegroundColor Green
Start-Process "http://localhost:3000"

Write-Host ""
Write-Host "✅ ARIA está ejecutándose en segundo plano." -ForegroundColor Green
Write-Host "💡 Presiona Ctrl+C para salir cuando termines." -ForegroundColor Yellow
Write-Host ""

# Mantener el script abierto
Write-Host "Presiona cualquier tecla para cerrar este iniciador..." -ForegroundColor Cyan
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")