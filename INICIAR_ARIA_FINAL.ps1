# 🚀 ARIA - Launcher PowerShell Final
# Launcher robusto para ARIA con manejo completo de errores

# Configurar consola
$Host.UI.RawUI.WindowTitle = "ARIA - Asistente IA Futurista"
$Host.UI.RawUI.BackgroundColor = "Black"
$Host.UI.RawUI.ForegroundColor = "Green"
Clear-Host

# Función para escribir con colores
function Write-ColorOutput {
    param(
        [string]$Message,
        [string]$Color = "Green"
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
                Write-ColorOutput "🛑 Deteniendo proceso PID: $procId" "Yellow"
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
Write-ColorOutput "🤖 ARIA - ASISTENTE IA FUTURISTA" "Cyan"
Write-ColorOutput "================================================================================"
Write-ColorOutput "🌟 Iniciando sistema completo..." "Yellow"
Write-ColorOutput ""

# Verificar ubicación
$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
$serverPath = Join-Path $scriptPath "backend\src\aria_server_final.py"

if (-not (Test-Path $serverPath)) {
    Write-ColorOutput "❌ Error: No se encuentra el servidor ARIA" "Red"
    Write-ColorOutput "💡 Ejecuta este script desde la carpeta raíz del proyecto" "Yellow"
    Write-ColorOutput ""
    Read-Host "Presiona Enter para salir"
    exit 1
}

Set-Location $scriptPath
Write-ColorOutput "📂 Directorio: $(Get-Location)" "Cyan"
Write-ColorOutput ""

# Activar entorno virtual
$venvPaths = @("venv\Scripts\Activate.ps1", ".venv\Scripts\Activate.ps1")
$venvActivated = $false

foreach ($venvPath in $venvPaths) {
    if (Test-Path $venvPath) {
        Write-ColorOutput "🔧 Activando entorno virtual..." "Yellow"
        try {
            & $venvPath
            Write-ColorOutput "✅ Entorno virtual activado" "Green"
            $venvActivated = $true
            break
        }
        catch {
            Write-ColorOutput "⚠️ Error activando entorno virtual, continuando..." "Yellow"
        }
    }
}

if (-not $venvActivated) {
    Write-ColorOutput "⚠️ No se encontró entorno virtual, usando Python global" "Yellow"
}

Write-ColorOutput ""

# Verificar Python
Write-ColorOutput "🐍 Verificando Python..." "Yellow"
if (-not (Test-Command "python")) {
    Write-ColorOutput "❌ Python no está instalado o no está en PATH" "Red"
    Write-ColorOutput "💡 Instala Python desde https://python.org" "Yellow"
    Read-Host "Presiona Enter para salir"
    exit 1
}

$pythonVersion = python --version 2>&1
Write-ColorOutput "✅ $pythonVersion disponible" "Green"
Write-ColorOutput ""

# Verificar e instalar dependencias
Write-ColorOutput "📦 Verificando dependencias..." "Yellow"
$dependencyCheck = python -c "import flask, flask_cors; print('OK')" 2>&1

if ($dependencyCheck -notmatch "OK") {
    Write-ColorOutput "📥 Instalando dependencias necesarias..." "Yellow"
    try {
        & python -m pip install flask flask-cors --quiet
        Write-ColorOutput "✅ Dependencias instaladas correctamente" "Green"
    }
    catch {
        Write-ColorOutput "❌ Error instalando dependencias" "Red"
        Write-ColorOutput "💡 Intenta ejecutar manualmente: pip install flask flask-cors" "Yellow"
        Read-Host "Presiona Enter para continuar de todos modos"
    }
}
else {
    Write-ColorOutput "✅ Dependencias ya instaladas" "Green"
}

Write-ColorOutput ""

# Verificar puerto 8000
Write-ColorOutput "🔍 Verificando puerto 8000..." "Yellow"
try {
    $portInUse = Get-NetTCPConnection -LocalPort 8000 -ErrorAction SilentlyContinue
    if ($portInUse) {
        Write-ColorOutput "⚠️ Puerto 8000 en uso, liberando..." "Yellow"
        Stop-ProcessOnPort -Port 8000
    }
    Write-ColorOutput "✅ Puerto 8000 disponible" "Green"
}
catch {
    Write-ColorOutput "✅ Puerto 8000 parece estar disponible" "Green"
}

Write-ColorOutput ""

# Crear archivo de bloqueo
$lockFile = "aria_running.lock"
"$(Get-Date)" | Out-File -FilePath $lockFile -Encoding UTF8

# Mostrar información de acceso
Write-ColorOutput "🚀 Iniciando servidor ARIA..." "Yellow"
Write-ColorOutput ""
Write-ColorOutput "================================================================================"
Write-ColorOutput "🌐 ARIA estará disponible en:" "Cyan"
Write-ColorOutput "   Interfaz Web: http://localhost:8000" "White"
Write-ColorOutput "   API REST:     http://localhost:8000/api/" "White"
Write-ColorOutput "   Estado:       http://localhost:8000/api/status" "White"
Write-ColorOutput ""
Write-ColorOutput "⏹️ Presiona Ctrl+C para detener el servidor" "Yellow"
Write-ColorOutput "================================================================================"
Write-ColorOutput ""

# Configurar manejo de Ctrl+C
$null = Register-EngineEvent PowerShell.Exiting -Action {
    if (Test-Path "aria_running.lock") {
        Remove-Item "aria_running.lock" -Force -ErrorAction SilentlyContinue
    }
    Write-Host "`n👋 ARIA se ha detenido correctamente" -ForegroundColor Yellow
}

# Iniciar servidor con manejo de errores
try {
    & python $serverPath
}
catch {
    Write-ColorOutput "`n❌ Error ejecutando ARIA: $_" "Red"
}
finally {
    # Limpiar archivo de bloqueo
    if (Test-Path $lockFile) {
        Remove-Item $lockFile -Force -ErrorAction SilentlyContinue
    }
    
    Write-ColorOutput ""
    Write-ColorOutput "👋 ARIA se ha detenido" "Yellow"
    Write-ColorOutput "📊 Sesión finalizada: $(Get-Date)" "Cyan"
    Write-ColorOutput ""
    Read-Host "Presiona Enter para salir"
}