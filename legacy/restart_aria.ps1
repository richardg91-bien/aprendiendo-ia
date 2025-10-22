# ARIA - Script de Reinicio Completo (PowerShell)
# Automatiza el proceso completo de inicio del sistema ARIA

param(
    [switch]$SkipFrontend = $false,
    [switch]$Verbose = $false
)

function Write-AriaMessage {
    param($Message, $Type = "Info")
    
    $timestamp = Get-Date -Format "HH:mm:ss"
    switch ($Type) {
        "Success" { Write-Host "[$timestamp] ✅ $Message" -ForegroundColor Green }
        "Error"   { Write-Host "[$timestamp] ❌ $Message" -ForegroundColor Red }
        "Warning" { Write-Host "[$timestamp] ⚠️  $Message" -ForegroundColor Yellow }
        "Info"    { Write-Host "[$timestamp] ℹ️  $Message" -ForegroundColor Cyan }
        default   { Write-Host "[$timestamp] $Message" }
    }
}

function Stop-ProcessesByName {
    param([string[]]$ProcessNames)
    
    $killed = @()
    foreach ($name in $ProcessNames) {
        $processes = Get-Process -Name $name -ErrorAction SilentlyContinue
        foreach ($proc in $processes) {
            try {
                $proc.Kill()
                $killed += "$($proc.Name) (PID: $($proc.Id))"
            }
            catch {
                if ($Verbose) {
                    Write-AriaMessage "No se pudo eliminar proceso $($proc.Name): $($_.Exception.Message)" "Warning"
                }
            }
        }
    }
    return $killed
}

function Stop-ProcessesByPort {
    param([int[]]$Ports)
    
    $killed = @()
    foreach ($port in $Ports) {
        $connections = netstat -ano | Select-String ":$port.*LISTENING"
        foreach ($conn in $connections) {
            $parts = $conn.ToString().Split(' ', [StringSplitOptions]::RemoveEmptyEntries)
            if ($parts.Count -ge 5) {
                $pid = $parts[-1]
                try {
                    $proc = Get-Process -Id $pid -ErrorAction SilentlyContinue
                    if ($proc) {
                        $proc.Kill()
                        $killed += "$($proc.Name) en puerto $port (PID: $pid)"
                    }
                }
                catch {
                    if ($Verbose) {
                        Write-AriaMessage "No se pudo eliminar proceso en puerto $port (PID: $pid): $($_.Exception.Message)" "Warning"
                    }
                }
            }
        }
    }
    return $killed
}

function Test-AriaDependencies {
    Write-AriaMessage "Verificando dependencias..."
    
    # Verificar estructura de directorios
    $requiredDirs = @("backend", "backend\src")
    foreach ($dir in $requiredDirs) {
        if (-not (Test-Path $dir)) {
            Write-AriaMessage "Directorio $dir no encontrado" "Error"
            return $false
        }
    }
    
    # Verificar archivo principal
    if (-not (Test-Path "backend\src\main.py")) {
        Write-AriaMessage "backend\src\main.py no encontrado" "Error"
        return $false
    }
    
    Write-AriaMessage "Dependencias verificadas correctamente" "Success"
    return $true
}

function Build-Frontend {
    if ($SkipFrontend) {
        Write-AriaMessage "Omitiendo construcción del frontend (parámetro -SkipFrontend)" "Info"
        return $true
    }
    
    if (-not (Test-Path "frontend")) {
        Write-AriaMessage "Frontend no encontrado, omitiendo construcción" "Info"
        return $true
    }
    
    Write-AriaMessage "Construyendo frontend..."
    
    if (-not (Test-Path "frontend\package.json")) {
        Write-AriaMessage "package.json no encontrado en frontend" "Warning"
        return $true
    }
    
    try {
        Push-Location "frontend"
        $result = & npm run build 2>&1
        Pop-Location
        
        if ($LASTEXITCODE -eq 0) {
            Write-AriaMessage "Frontend construido exitosamente" "Success"
            return $true
        } else {
            Write-AriaMessage "Error al construir frontend: $result" "Warning"
            return $true  # No bloqueante
        }
    }
    catch {
        Write-AriaMessage "Error inesperado al construir frontend: $($_.Exception.Message)" "Warning"
        Pop-Location
        return $true
    }
}

function Start-AriaServer {
    Write-AriaMessage "Iniciando servidor ARIA..."
    
    # Activar entorno virtual si existe
    if (Test-Path "venv\Scripts\Activate.ps1") {
        Write-AriaMessage "Activando entorno virtual..."
        & .\venv\Scripts\Activate.ps1
        Write-AriaMessage "Entorno virtual activado" "Success"
    } elseif (Test-Path "Scripts\Activate.ps1") {
        Write-AriaMessage "Activando entorno virtual..."
        & .\Scripts\Activate.ps1
        Write-AriaMessage "Entorno virtual activado" "Success"
    } else {
        Write-AriaMessage "No se encontró entorno virtual, usando Python del sistema" "Warning"
    }
    
    # Cambiar al directorio backend y ejecutar servidor
    try {
        Push-Location "backend"
        & python src\main.py
        Pop-Location
    }
    catch {
        Write-AriaMessage "Error al ejecutar servidor: $($_.Exception.Message)" "Error"
        Pop-Location
        return $false
    }
    finally {
        if ((Get-Location).Path -ne $PWD.Path) {
            Pop-Location
        }
    }
    
    return $true
}

# Script principal
Clear-Host
Write-Host "╔══════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║              🔄 REINICIO COMPLETO DE ARIA               ║" -ForegroundColor Cyan
Write-Host "║              Sistema de Inteligencia Artificial         ║" -ForegroundColor Cyan
Write-Host "╚══════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

# Verificar directorio correcto
if (-not (Test-AriaDependencies)) {
    Write-AriaMessage "Asegúrate de ejecutar desde el directorio raíz de ARIA" "Error"
    exit 1
}

# Detener procesos anteriores
Write-AriaMessage "Deteniendo procesos anteriores..."

# Eliminar procesos Python y Node
$killedByName = Stop-ProcessesByName @("python", "node")
if ($killedByName.Count -gt 0) {
    Write-AriaMessage "Procesos eliminados: $($killedByName -join ', ')" "Success"
}

# Eliminar procesos en puertos específicos
$killedByPort = Stop-ProcessesByPort @(8000, 5000, 3000)
if ($killedByPort.Count -gt 0) {
    Write-AriaMessage "Procesos en puertos eliminados: $($killedByPort -join ', ')" "Success"
}

if ($killedByName.Count -eq 0 -and $killedByPort.Count -eq 0) {
    Write-AriaMessage "No había procesos anteriores ejecutándose" "Success"
}

# Esperar un momento para que los procesos terminen
Start-Sleep -Seconds 2

# Construir frontend
if (-not (Build-Frontend)) {
    Write-AriaMessage "Problema con el frontend, pero continuando..." "Warning"
}

Write-Host ""
Write-AriaMessage "📡 Servidor disponible en: http://localhost:8000"
Write-AriaMessage "🌐 Interfaz web en: http://localhost:8000"
Write-AriaMessage "🔗 API disponible en: http://localhost:8000/api/"
Write-Host ""
Write-AriaMessage "⚠️  Presiona Ctrl+C para detener el servidor"
Write-Host ""

# Iniciar servidor
try {
    $success = Start-AriaServer
    
    Write-Host ""
    Write-AriaMessage "Proceso de reinicio completado" "Info"
    Write-AriaMessage "🔄 Para reiniciar, ejecuta este script nuevamente" "Info"
    
    if (-not $success) {
        exit 1
    }
}
catch {
    Write-AriaMessage "Reinicio cancelado por el usuario" "Info"
    exit 0
}