# 🚀 ARIA - Launcher Completo (Backend + Frontend Moderno)
# Inicia tanto el servidor Python como la interfaz React moderna

param(
    [switch]$BackendOnly,
    [switch]$FrontendOnly,
    [int]$BackendPort = 8000,
    [int]$FrontendPort = 3000
)

# Configurar consola
$Host.UI.RawUI.WindowTitle = "ARIA - Sistema Completo con Interfaz Moderna"
$Host.UI.RawUI.BackgroundColor = "Black"
$Host.UI.RawUI.ForegroundColor = "Cyan"
Clear-Host

# Función para escribir con colores
function Write-ColorOutput {
    param(
        [string]$Message,
        [string]$Color = "Cyan"
    )
    Write-Host $Message -ForegroundColor $Color
}

# Función para verificar comandos
function Test-Command {
    param([string]$Command)
    $null = Get-Command $Command -ErrorAction SilentlyContinue
    return $?
}

# Función para detener procesos en puerto
function Stop-ProcessOnPort {
    param([int]$Port)
    
    try {
        $processes = Get-NetTCPConnection -LocalPort $Port -ErrorAction SilentlyContinue
        if ($processes) {
            foreach ($process in $processes) {
                $procId = $process.OwningProcess
                Write-ColorOutput "🛑 Liberando puerto $Port (PID: $procId)" "Yellow"
                Stop-Process -Id $procId -Force -ErrorAction SilentlyContinue
            }
            Start-Sleep -Seconds 2
        }
    }
    catch {
        Write-ColorOutput "⚠️ No se pudieron detener procesos automáticamente" "Yellow"
    }
}

# Banner de inicio
Write-ColorOutput ""
Write-ColorOutput "================================================================================"
Write-ColorOutput "🤖 ARIA - SISTEMA COMPLETO CON INTERFAZ MODERNA" "Magenta"
Write-ColorOutput "================================================================================"
Write-ColorOutput "🚀 Iniciando Backend (Python/Flask) + Frontend (React/Material-UI)" "Cyan"
Write-ColorOutput "🎨 Interfaz futurista con animaciones y cara de robot" "Yellow"
Write-ColorOutput "🧠 Sistema de IA avanzado con aprendizaje en tiempo real" "Green"
Write-ColorOutput ""

# Verificar ubicación
$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
$backendPath = Join-Path $scriptPath "backend\src\aria_server_final.py"
$frontendPath = Join-Path $scriptPath "frontend"
$packageJsonPath = Join-Path $frontendPath "package.json"

Write-ColorOutput "📂 Verificando estructura del proyecto..." "Cyan"

if (-not (Test-Path $backendPath)) {
    Write-ColorOutput "❌ Error: No se encuentra el servidor backend" "Red"
    Write-ColorOutput "💡 Ejecuta este script desde la carpeta raíz del proyecto" "Yellow"
    Read-Host "Presiona Enter para salir"
    exit 1
}

if (-not (Test-Path $packageJsonPath)) {
    Write-ColorOutput "❌ Error: No se encuentra el frontend React" "Red"
    Write-ColorOutput "💡 La carpeta frontend/ debe contener package.json" "Yellow"
    Read-Host "Presiona Enter para salir"
    exit 1
}

Write-ColorOutput "✅ Backend encontrado: aria_server_final.py" "Green"
Write-ColorOutput "✅ Frontend encontrado: React con Material-UI" "Green"

Set-Location $scriptPath
Write-ColorOutput "📂 Directorio de trabajo: $(Get-Location)" "Cyan"
Write-ColorOutput ""

# Verificar y activar entorno virtual para Python
if (-not $FrontendOnly) {
    Write-ColorOutput "🐍 Configurando entorno Python..." "Yellow"
    
    $venvPaths = @("venv\Scripts\Activate.ps1", ".venv\Scripts\Activate.ps1")
    $venvActivated = $false

    foreach ($venvPath in $venvPaths) {
        if (Test-Path $venvPath) {
            Write-ColorOutput "🔧 Activando entorno virtual..." "Yellow"
            try {
                & $venvPath
                Write-ColorOutput "✅ Entorno virtual Python activado" "Green"
                $venvActivated = $true
                break
            }
            catch {
                Write-ColorOutput "⚠️ Error activando entorno virtual, usando Python global" "Yellow"
            }
        }
    }

    # Verificar Python
    if (-not (Test-Command "python")) {
        Write-ColorOutput "❌ Python no está disponible" "Red"
        Write-ColorOutput "💡 Instala Python desde https://python.org" "Yellow"
        Read-Host "Presiona Enter para salir"
        exit 1
    }

    $pythonVersion = python --version 2>&1
    Write-ColorOutput "✅ $pythonVersion disponible" "Green"

    # Verificar dependencias Python
    Write-ColorOutput "📦 Verificando dependencias Python..." "Yellow"
    $dependencyCheck = python -c "import flask, flask_cors; print('OK')" 2>&1

    if ($dependencyCheck -notmatch "OK") {
        Write-ColorOutput "📥 Instalando dependencias Python..." "Yellow"
        try {
            & python -m pip install flask flask-cors --quiet
            Write-ColorOutput "✅ Dependencias Python instaladas" "Green"
        }
        catch {
            Write-ColorOutput "❌ Error instalando dependencias Python" "Red"
            Read-Host "Presiona Enter para continuar de todos modos"
        }
    }
    else {
        Write-ColorOutput "✅ Dependencias Python verificadas" "Green"
    }
}

# Verificar Node.js para React
if (-not $BackendOnly) {
    Write-ColorOutput ""
    Write-ColorOutput "⚛️ Configurando entorno React..." "Yellow"
    
    if (-not (Test-Command "node")) {
        Write-ColorOutput "❌ Node.js no está instalado" "Red"
        Write-ColorOutput "💡 Instala Node.js desde https://nodejs.org" "Yellow"
        Read-Host "Presiona Enter para salir"
        exit 1
    }

    $nodeVersion = node --version 2>&1
    Write-ColorOutput "✅ Node.js $nodeVersion disponible" "Green"

    if (-not (Test-Command "npm")) {
        Write-ColorOutput "❌ npm no está disponible" "Red"
        Write-ColorOutput "💡 npm debe instalarse con Node.js" "Yellow"
        Read-Host "Presiona Enter para salir"
        exit 1
    }

    $npmVersion = npm --version 2>&1
    Write-ColorOutput "✅ npm $npmVersion disponible" "Green"

    # Verificar e instalar dependencias React
    Write-ColorOutput "📦 Verificando dependencias React..." "Yellow"
    Set-Location $frontendPath
    
    if (-not (Test-Path "node_modules")) {
        Write-ColorOutput "📥 Instalando dependencias React (esto puede tomar unos minutos)..." "Yellow"
        try {
            & npm install
            Write-ColorOutput "✅ Dependencias React instaladas" "Green"
        }
        catch {
            Write-ColorOutput "❌ Error instalando dependencias React" "Red"
            Write-ColorOutput "💡 Intenta ejecutar 'npm install' manualmente en la carpeta frontend/" "Yellow"
            Read-Host "Presiona Enter para continuar"
        }
    }
    else {
        Write-ColorOutput "✅ Dependencias React verificadas" "Green"
    }
    
    Set-Location $scriptPath
}

Write-ColorOutput ""
Write-ColorOutput "🔍 Liberando puertos..." "Yellow"

# Liberar puertos
Stop-ProcessOnPort -Port $BackendPort
Stop-ProcessOnPort -Port $FrontendPort

Write-ColorOutput "✅ Puertos $BackendPort y $FrontendPort disponibles" "Green"
Write-ColorOutput ""

# Variables para jobs
$BackendJob = $null
$FrontendJob = $null

# Función para limpiar al salir
function Cleanup {
    Write-ColorOutput "`n🛑 Deteniendo servicios..." "Yellow"
    
    if ($BackendJob) {
        Stop-Job $BackendJob -ErrorAction SilentlyContinue
        Remove-Job $BackendJob -ErrorAction SilentlyContinue
        Write-ColorOutput "✅ Backend detenido" "Green"
    }
    
    if ($FrontendJob) {
        Stop-Job $FrontendJob -ErrorAction SilentlyContinue  
        Remove-Job $FrontendJob -ErrorAction SilentlyContinue
        Write-ColorOutput "✅ Frontend detenido" "Green"
    }
    
    Stop-ProcessOnPort -Port $BackendPort
    Stop-ProcessOnPort -Port $FrontendPort
    
    Write-ColorOutput "👋 ARIA se ha detenido completamente" "Cyan"
}

# Configurar manejo de Ctrl+C
$null = Register-EngineEvent PowerShell.Exiting -Action { Cleanup }

try {
    # Iniciar Backend
    if (-not $FrontendOnly) {
        Write-ColorOutput "🚀 Iniciando Backend ARIA en puerto $BackendPort..." "Magenta"
        
        $BackendJob = Start-Job -ScriptBlock {
            param($ServerPath, $Port)
            Set-Location (Split-Path $ServerPath -Parent)
            & python (Split-Path $ServerPath -Leaf)
        } -ArgumentList $backendPath, $BackendPort
        
        Write-ColorOutput "✅ Backend iniciado en background" "Green"
        Start-Sleep -Seconds 3
    }

    # Iniciar Frontend
    if (-not $BackendOnly) {
        Write-ColorOutput "🎨 Iniciando Frontend React en puerto $FrontendPort..." "Magenta"
        
        $FrontendJob = Start-Job -ScriptBlock {
            param($FrontendPath, $Port)
            Set-Location $FrontendPath
            $env:PORT = $Port
            & npm start
        } -ArgumentList $frontendPath, $FrontendPort
        
        Write-ColorOutput "✅ Frontend React iniciado en background" "Green"
        Start-Sleep -Seconds 5
    }

    Write-ColorOutput ""
    Write-ColorOutput "================================================================================"
    Write-ColorOutput "🎉 ARIA SISTEMA COMPLETO INICIADO EXITOSAMENTE" "Green"
    Write-ColorOutput "================================================================================"
    
    if (-not $FrontendOnly) {
        Write-ColorOutput "🔧 Backend (API): http://localhost:$BackendPort" "White"
        Write-ColorOutput "   📊 Estado: http://localhost:$BackendPort/api/status" "Gray"
        Write-ColorOutput "   💬 Chat: POST http://localhost:$BackendPort/api/chat" "Gray"
    }
    
    if (-not $BackendOnly) {
        Write-ColorOutput "🎨 Frontend (Interfaz Moderna): http://localhost:$FrontendPort" "White"
        Write-ColorOutput "   🤖 Cara de Robot Animada" "Gray"
        Write-ColorOutput "   🎭 Emociones de IA en Tiempo Real" "Gray"
        Write-ColorOutput "   📚 Panel de Aprendizaje Avanzado" "Gray"
        Write-ColorOutput "   🌐 Búsqueda Web Integrada" "Gray"
    }
    
    Write-ColorOutput ""
    Write-ColorOutput "🌟 Características de la Interfaz Moderna:" "Cyan"
    Write-ColorOutput "   ✨ Animaciones fluidas con Framer Motion" "White"
    Write-ColorOutput "   🎨 Material-UI con tema futurista" "White"  
    Write-ColorOutput "   🤖 Robot face con expresiones dinámicas" "White"
    Write-ColorOutput "   📊 Indicadores de estado en tiempo real" "White"
    Write-ColorOutput "   🧠 Panel de entrenamiento neural" "White"
    Write-ColorOutput "   🔍 Capacidades de búsqueda web" "White"
    Write-ColorOutput ""
    Write-ColorOutput "⏹️ Presiona Ctrl+C para detener ambos servicios" "Yellow"
    Write-ColorOutput "================================================================================"
    
    # Esperar hasta que el usuario presione Ctrl+C
    while ($true) {
        Start-Sleep -Seconds 1
        
        # Verificar si los jobs están ejecutándose
        if ($BackendJob -and $BackendJob.State -eq "Failed") {
            Write-ColorOutput "❌ El backend ha fallado" "Red"
            break
        }
        
        if ($FrontendJob -and $FrontendJob.State -eq "Failed") {
            Write-ColorOutput "❌ El frontend ha fallado" "Red"
            break
        }
    }
}
catch {
    Write-ColorOutput "`n❌ Error durante la ejecución: $_" "Red"
}
finally {
    Cleanup
    Write-ColorOutput "`n📊 Sesión finalizada: $(Get-Date)" "Cyan"
    Read-Host "Presiona Enter para salir"
}