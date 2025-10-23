# ARIA - Restaurar Icono del Escritorio (Version Simple)
# Script PowerShell simplificado para crear acceso directo

Clear-Host
Write-Host ""
Write-Host "================================================================================"
Write-Host "ARIA - RESTAURADOR DE ICONO DEL ESCRITORIO" -ForegroundColor Cyan
Write-Host "================================================================================"
Write-Host ""

# Obtener rutas
$projectPath = (Get-Location).Path
$desktopPath = [Environment]::GetFolderPath("Desktop")

Write-Host "Directorio del proyecto: $projectPath" -ForegroundColor Green
Write-Host "Escritorio: $desktopPath" -ForegroundColor Green
Write-Host ""

# Verificar archivos de ARIA
$launchers = @(
    @{ File = "ARIA_MENU_PRINCIPAL.bat"; Name = "ARIA - Menu Principal" },
    @{ File = "INICIAR_ARIA_FINAL.bat"; Name = "ARIA - Launcher" },
    @{ File = "INICIAR_ARIA_FINAL.ps1"; Name = "ARIA - PowerShell" }
)

$selectedLauncher = $null
foreach ($launcher in $launchers) {
    $launcherPath = Join-Path $projectPath $launcher.File
    if (Test-Path $launcherPath) {
        $selectedLauncher = $launcher
        $selectedLauncher.Path = $launcherPath
        break
    }
}

if (-not $selectedLauncher) {
    Write-Host "ERROR: No se encontraron archivos de ARIA" -ForegroundColor Red
    Write-Host "Ejecuta este script desde la carpeta del proyecto ARIA" -ForegroundColor Yellow
    Read-Host "Presiona Enter para salir"
    exit 1
}

Write-Host "Launcher encontrado: $($selectedLauncher.File)" -ForegroundColor Green
Write-Host ""

# Crear acceso directo
try {
    $shortcutName = $selectedLauncher.Name
    $shortcutPath = Join-Path $desktopPath "$shortcutName.lnk"
    
    # Eliminar acceso directo existente
    if (Test-Path $shortcutPath) {
        Remove-Item $shortcutPath -Force
        Write-Host "Acceso directo anterior eliminado" -ForegroundColor Yellow
    }
    
    # Crear objeto COM
    $WshShell = New-Object -ComObject WScript.Shell
    $Shortcut = $WshShell.CreateShortcut($shortcutPath)
    
    # Configurar acceso directo
    $Shortcut.TargetPath = $selectedLauncher.Path
    $Shortcut.WorkingDirectory = $projectPath
    $Shortcut.Description = "ARIA - Asistente de Inteligencia Artificial"
    
    # Buscar icono
    $iconPaths = @(
        (Join-Path $projectPath "assets\icons\aria_icon.ico"),
        (Join-Path $projectPath "assets\aria.ico"),
        (Join-Path $projectPath "aria_icon.ico")
    )
    
    $iconFound = $false
    foreach ($iconPath in $iconPaths) {
        if (Test-Path $iconPath) {
            $Shortcut.IconLocation = $iconPath
            Write-Host "Icono personalizado encontrado: $iconPath" -ForegroundColor Green
            $iconFound = $true
            break
        }
    }
    
    if (-not $iconFound) {
        $Shortcut.IconLocation = "shell32.dll,1"
        Write-Host "Usando icono del sistema" -ForegroundColor Yellow
    }
    
    # Guardar acceso directo
    $Shortcut.Save()
    
    # Verificar creación
    if (Test-Path $shortcutPath) {
        Write-Host ""
        Write-Host "================================================================================"
        Write-Host "EXITO: ICONO DE ARIA RESTAURADO" -ForegroundColor Green
        Write-Host "================================================================================"
        Write-Host "Acceso directo creado: $shortcutName.lnk" -ForegroundColor Green
        Write-Host "Ubicacion: $desktopPath" -ForegroundColor Cyan
        Write-Host ""
        Write-Host "Funcionalidades de ARIA:" -ForegroundColor Cyan
        Write-Host "  - Interfaz web interactiva" -ForegroundColor White
        Write-Host "  - Chat con IA avanzada" -ForegroundColor White
        Write-Host "  - Sistema de aprendizaje" -ForegroundColor White
        Write-Host "  - APIs REST completas" -ForegroundColor White
        Write-Host ""
        Write-Host "Haz doble clic en el icono para iniciar ARIA" -ForegroundColor Yellow
    } else {
        throw "No se pudo verificar la creacion del acceso directo"
    }
    
} catch {
    Write-Host ""
    Write-Host "================================================================================"
    Write-Host "ERROR: NO SE PUDO CREAR EL ICONO" -ForegroundColor Red
    Write-Host "================================================================================"
    Write-Host "Error: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host ""
    Write-Host "Posibles soluciones:" -ForegroundColor Yellow
    Write-Host "  1. Ejecutar como administrador" -ForegroundColor White
    Write-Host "  2. Verificar permisos del escritorio" -ForegroundColor White
    Write-Host "  3. Comprobar antivirus" -ForegroundColor White
} finally {
    # Limpiar objetos COM
    if ($WshShell) {
        [System.Runtime.Interopservices.Marshal]::ReleaseComObject($WshShell) | Out-Null
    }
}

Write-Host ""
Write-Host "================================================================================"
Read-Host "Presiona Enter para continuar"