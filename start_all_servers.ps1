# 🚀 ARIA SYSTEM - INICIADOR COMPLETO DE SERVIDORES (PowerShell)
# ================================================================

param(
    [switch]$NoBrowser,
    [switch]$BackendOnly,
    [string]$Port = "8000"
)

# Configuración de colores
$Host.UI.RawUI.WindowTitle = "ARIA System Server Launcher"

# Funciones auxiliares
function Write-Status {
    param($Message, $Type = "Info")
    $colors = @{
        "Info" = "White"
        "Success" = "Green"
        "Warning" = "Yellow"
        "Error" = "Red"
        "Header" = "Cyan"
    }
    Write-Host $Message -ForegroundColor $colors[$Type]
}

function Test-Port {
    param($Port)
    try {
        $connection = New-Object System.Net.Sockets.TcpClient
        $connection.Connect("127.0.0.1", $Port)
        $connection.Close()
        return $true
    }
    catch {
        return $false
    }
}

function Stop-ProcessOnPort {
    param($Port)
    try {
        $processes = Get-NetTCPConnection -LocalPort $Port -ErrorAction SilentlyContinue
        foreach ($process in $processes) {
            $pid = $process.OwningProcess
            Stop-Process -Id $pid -Force -ErrorAction SilentlyContinue
            Write-Status "🔧 Proceso en puerto $Port detenido (PID: $pid)" "Warning"
        }
    }
    catch {
        # Puerto no está en uso
    }
}

# Banner inicial
Clear-Host
Write-Status "🚀 ARIA SYSTEM - INICIADOR COMPLETO DE SERVIDORES" "Header"
Write-Status "====================================================" "Header"
Write-Status "🤖 Iniciando todos los servidores del sistema ARIA" "Info"
Write-Status "====================================================" "Header"
Write-Host ""

# Variables de configuración
$ProjectDir = $PSScriptRoot
$BackendDir = Join-Path $ProjectDir "backend\src"
$FrontendDir = Join-Path $ProjectDir "frontend"
$DataDir = Join-Path $ProjectDir "data"

Write-Status "📍 Directorio del proyecto: $ProjectDir" "Info"
Write-Host ""

# Verificar Python
Write-Status "🔍 Verificando Python..." "Info"
try {
    $pythonVersion = python --version 2>&1
    if ($LASTEXITCODE -eq 0) {
        $pythonCmd = "python"
        Write-Status "✅ Python encontrado: $pythonVersion" "Success"
    } else {
        throw "Python no encontrado"
    }
}
catch {
    try {
        $pythonVersion = py --version 2>&1
        if ($LASTEXITCODE -eq 0) {
            $pythonCmd = "py"
            Write-Status "✅ Python encontrado: $pythonVersion" "Success"
        } else {
            throw "Python no encontrado"
        }
    }
    catch {
        Write-Status "❌ Python no está instalado o no está en PATH" "Error"
        Write-Status "💡 Instala Python desde https://python.org" "Warning"
        Read-Host "Presiona Enter para salir"
        exit 1
    }
}

# Verificar Node.js
Write-Status "🔍 Verificando Node.js..." "Info"
try {
    $nodeVersion = node --version 2>&1
    if ($LASTEXITCODE -eq 0) {
        $nodeAvailable = $true
        Write-Status "✅ Node.js encontrado: $nodeVersion" "Success"
    } else {
        throw "Node.js no encontrado"
    }
}
catch {
    $nodeAvailable = $false
    Write-Status "⚠️ Node.js no encontrado (opcional para frontend)" "Warning"
}

# Activar entorno virtual si existe
$venvPath = Join-Path $ProjectDir "venv\Scripts\Activate.ps1"
if (Test-Path $venvPath) {
    Write-Status "🐍 Activando entorno virtual..." "Info"
    try {
        & $venvPath
        Write-Status "✅ Entorno virtual activado" "Success"
    }
    catch {
        Write-Status "⚠️ Error activando entorno virtual, usando Python del sistema" "Warning"
    }
} else {
    Write-Status "⚠️ Entorno virtual no encontrado, usando Python del sistema" "Warning"
}

# Crear directorios necesarios
Write-Host ""
Write-Status "📁 Creando directorios necesarios..." "Info"
@("data", "data\logs", "backend\data") | ForEach-Object {
    $dir = Join-Path $ProjectDir $_
    if (!(Test-Path $dir)) {
        New-Item -ItemType Directory -Path $dir -Force | Out-Null
        Write-Status "📁 Creado: $_" "Info"
    }
}

# Instalar dependencias del backend
Write-Host ""
Write-Status "📦 Verificando dependencias del backend..." "Info"
$requirementsPath = Join-Path $ProjectDir "backend\requirements.txt"
if (Test-Path $requirementsPath) {
    Push-Location (Join-Path $ProjectDir "backend")
    try {
        Write-Status "🔄 Instalando dependencias de Python..." "Info"
        & $pythonCmd -m pip install -r requirements.txt --quiet --disable-pip-version-check
        if ($LASTEXITCODE -eq 0) {
            Write-Status "✅ Dependencias de Python instaladas" "Success"
        } else {
            Write-Status "⚠️ Algunos paquetes podrían no haberse instalado correctamente" "Warning"
        }
    }
    catch {
        Write-Status "⚠️ Error instalando dependencias de Python" "Warning"
    }
    finally {
        Pop-Location
    }
} else {
    Write-Status "⚠️ Archivo requirements.txt no encontrado" "Warning"
}

# Instalar dependencias del frontend
if ($nodeAvailable -and !$BackendOnly) {
    Write-Host ""
    Write-Status "📦 Verificando dependencias del frontend..." "Info"
    $packageJsonPath = Join-Path $FrontendDir "package.json"
    if (Test-Path $packageJsonPath) {
        $nodeModulesPath = Join-Path $FrontendDir "node_modules"
        if (!(Test-Path $nodeModulesPath)) {
            Push-Location $FrontendDir
            try {
                Write-Status "🔄 Instalando dependencias de Node.js..." "Info"
                npm install --silent
                Write-Status "✅ Dependencias de Node.js instaladas" "Success"
            }
            catch {
                Write-Status "⚠️ Error instalando dependencias de Node.js" "Warning"
            }
            finally {
                Pop-Location
            }
        } else {
            Write-Status "✅ Dependencias de Node.js ya instaladas" "Success"
        }
    } else {
        Write-Status "⚠️ Archivo package.json no encontrado en frontend" "Warning"
    }
}

Write-Host ""
Write-Status "🚀 INICIANDO SERVIDORES..." "Header"
Write-Status "============================" "Header"

# Verificar y liberar puertos
Write-Status "🔍 Verificando puertos disponibles..." "Info"

# Puerto del backend
if (Test-Port $Port) {
    Write-Status "⚠️ Puerto $Port ya está en uso" "Warning"
    Write-Status "💡 Liberando puerto $Port..." "Info"
    Stop-ProcessOnPort $Port
    Start-Sleep -Seconds 2
}

# Puerto del frontend
if ($nodeAvailable -and !$BackendOnly) {
    if (Test-Port 3000) {
        Write-Status "⚠️ Puerto 3000 ya está en uso" "Warning"
        Write-Status "💡 Liberando puerto 3000..." "Info"
        Stop-ProcessOnPort 3000
        Start-Sleep -Seconds 2
    }
}

# Iniciar servidor backend
Write-Host ""
Write-Status "🖥️ SERVIDOR 1: BACKEND (Puerto $Port)" "Header"
Write-Status "=====================================" "Header"

# Buscar archivo principal del backend
$mainFiles = @("main_stable.py", "main.py", "app.py")
$mainFile = $null

foreach ($file in $mainFiles) {
    $filePath = Join-Path $BackendDir $file
    if (Test-Path $filePath) {
        $mainFile = $file
        Write-Status "✅ Archivo principal encontrado: $mainFile" "Success"
        break
    }
}

if (!$mainFile) {
    Write-Status "❌ No se encontró archivo principal del backend" "Error"
    Read-Host "Presiona Enter para salir"
    exit 1
}

# Iniciar backend en nueva ventana
Write-Status "🚀 Iniciando servidor backend..." "Info"
$backendScript = @"
Set-Location '$BackendDir'
Write-Host '🤖 ARIA Backend Server' -ForegroundColor Cyan
Write-Host 'Puerto: $Port' -ForegroundColor Green
Write-Host 'Archivo: $mainFile' -ForegroundColor Green
Write-Host ''
& '$pythonCmd' '$mainFile'
Read-Host 'Presiona Enter para cerrar'
"@

$backendJob = Start-Process powershell -ArgumentList "-NoExit", "-Command", $backendScript -PassThru

# Esperar a que el backend esté listo
Write-Status "⏳ Esperando a que el backend esté listo..." "Info"
Start-Sleep -Seconds 5

# Verificar si el backend está funcionando
$backendReady = $false
for ($i = 0; $i -lt 10; $i++) {
    try {
        $response = Invoke-WebRequest -Uri "http://127.0.0.1:$Port/api/status" -TimeoutSec 3 -UseBasicParsing
        if ($response.StatusCode -eq 200) {
            $backendReady = $true
            Write-Status "✅ Backend está funcionando correctamente" "Success"
            break
        }
    }
    catch {
        Start-Sleep -Seconds 2
    }
}

if (!$backendReady) {
    Write-Status "⚠️ Backend puede estar iniciando aún..." "Warning"
}

# Iniciar servidor frontend
if ($nodeAvailable -and !$BackendOnly) {
    $packageJsonPath = Join-Path $FrontendDir "package.json"
    if (Test-Path $packageJsonPath) {
        Write-Host ""
        Write-Status "🌐 SERVIDOR 2: FRONTEND (Puerto 3000)" "Header"
        Write-Status "======================================" "Header"
        
        $startServerPath = Join-Path $FrontendDir "start-server.js"
        if (Test-Path $startServerPath) {
            Write-Status "🚀 Iniciando frontend con servidor personalizado..." "Info"
            $frontendScript = @"
Set-Location '$FrontendDir'
Write-Host '🌐 ARIA Frontend Server' -ForegroundColor Cyan
Write-Host 'Puerto: 3000' -ForegroundColor Green
Write-Host ''
node start-server.js
Read-Host 'Presiona Enter para cerrar'
"@
        } else {
            Write-Status "🚀 Iniciando frontend con React..." "Info"
            $frontendScript = @"
Set-Location '$FrontendDir'
Write-Host '🌐 ARIA Frontend Server' -ForegroundColor Cyan
Write-Host 'Puerto: 3000' -ForegroundColor Green
Write-Host ''
npm start
Read-Host 'Presiona Enter para cerrar'
"@
        }
        
        $frontendJob = Start-Process powershell -ArgumentList "-NoExit", "-Command", $frontendScript -PassThru
        
        Write-Status "⏳ Esperando a que el frontend esté listo..." "Info"
        Start-Sleep -Seconds 8
    }
} else {
    Write-Host ""
    Write-Status "⚠️ Frontend no disponible" "Warning"
    Write-Status "💡 El backend seguirá funcionando con su interfaz web integrada" "Info"
}

# Mostrar información de acceso
Write-Host ""
Write-Status "🎉 SERVIDORES INICIADOS EXITOSAMENTE" "Header"
Write-Status "====================================" "Header"

Write-Host ""
Write-Status "🌐 ACCESO AL SISTEMA:" "Header"
Write-Status "----------------------" "Header"
Write-Status "🖥️  Backend API:     http://127.0.0.1:$Port" "Info"
Write-Status "🎨  Interfaz Web:    http://127.0.0.1:$Port" "Info"
if ($nodeAvailable -and !$BackendOnly -and (Test-Path (Join-Path $FrontendDir "package.json"))) {
    Write-Status "🚀  Frontend React:  http://127.0.0.1:3000" "Info"
}

Write-Host ""
Write-Status "📊 ENDPOINTS DISPONIBLES:" "Header"
Write-Status "-------------------------" "Header"
Write-Status "🔍  Estado:           http://127.0.0.1:$Port/api/status" "Info"
Write-Status "💬  Chat normal:      http://127.0.0.1:$Port/api/chat" "Info"
Write-Status "🚀  Chat futurista:   http://127.0.0.1:$Port/api/chat/futuristic" "Info"
Write-Status "🌐  Datos en nube:    http://127.0.0.1:$Port/api/cloud/stats" "Info"
Write-Status "🎭  Emociones:        http://127.0.0.1:$Port/api/cloud/emotions/recent" "Info"

Write-Host ""
Write-Status "🎭 SISTEMA EMOCIONAL ACTIVO:" "Header"
Write-Status "---------------------------" "Header"
Write-Status "🔵  Azul = Normal/Interacción" "Info"
Write-Status "🟢  Verde = Aprendiendo" "Info"
Write-Status "🔴  Rojo = Frustrada" "Info"
Write-Status "🟡  Dorado = Feliz" "Info"
Write-Status "🟣  Púrpura = Pensando" "Info"

# Abrir navegador automáticamente
if (!$NoBrowser) {
    Write-Host ""
    Write-Status "🌐 Abriendo navegador..." "Info"
    Start-Process "http://127.0.0.1:$Port"
}

Write-Host ""
Write-Status "🛠️ COMANDOS ÚTILES:" "Header"
Write-Status "-------------------" "Header"
Write-Status "🧪  Probar sistema:   python demo_futuristic_aria.py" "Info"
Write-Status "📖  Ver guías:        README.md, GUIA_BASE_DATOS_NUBE.md" "Info"
Write-Status "🔄  Reiniciar:        .\start_all_servers.ps1" "Info"

Write-Host ""
Write-Status "💡 CONSEJOS:" "Header"
Write-Status "------------" "Header"
Write-Status "• Las ventanas de servidor se abrieron por separado" "Info"
Write-Status "• Puedes minimizarlas pero NO las cierres" "Warning"
Write-Status "• Para detener: cierra las ventanas de servidor" "Info"
Write-Status "• Los logs aparecen en las ventanas de servidor" "Info"

Write-Host ""
Write-Status "⚠️ IMPORTANTE:" "Header"
Write-Status "--------------" "Header"
$envPath = Join-Path $ProjectDir ".env"
if (!(Test-Path $envPath)) {
    Write-Status "🔧 Para funcionalidad completa, configura tu archivo .env" "Warning"
    Write-Status "📖 Consulta GUIA_BASE_DATOS_NUBE.md para base de datos gratuita" "Info"
}

Write-Host ""
Write-Status "🎉 ¡ARIA está lista para usar!" "Success"
Write-Status "🤖 Tu asistente futurista te espera en: http://127.0.0.1:$Port" "Success"

Write-Host ""
Write-Status "📝 Presiona cualquier tecla para salir (los servidores seguirán funcionando)" "Info"
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")

Write-Host ""
Write-Status "👋 Mantén las ventanas de servidor abiertas para que ARIA funcione" "Info"
Write-Status "🚀 ¡Disfruta tu asistente del futuro!" "Success"