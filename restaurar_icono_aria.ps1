# 🎯 ARIA - Restaurar Ícono del Escritorio (PowerShell)
# Script para recrear el acceso directo de ARIA en el escritorio

param(
    [switch]$Force,
    [string]$IconPath = ""
)

# Configurar consola
$Host.UI.RawUI.WindowTitle = "ARIA - Restaurador de Ícono"
Clear-Host

function Write-ColorOutput {
    param(
        [string]$Message,
        [string]$Color = "Green"
    )
    Write-Host $Message -ForegroundColor $Color
}

function Create-ARIADesktopShortcut {
    param(
        [string]$ProjectPath,
        [string]$DesktopPath,
        [string]$CustomIconPath = ""
    )
    
    try {
        # Determinar qué launcher usar (prioridad)
        $launchers = @(
            @{
                File = "ARIA_MENU_PRINCIPAL.bat"
                Name = "🤖 ARIA - Asistente IA"
                Description = "ARIA - Asistente de Inteligencia Artificial Futurista"
            },
            @{
                File = "INICIAR_ARIA_FINAL.bat"
                Name = "🤖 ARIA - Launcher"
                Description = "ARIA - Iniciar Asistente de IA"
            },
            @{
                File = "INICIAR_ARIA_FINAL.ps1"
                Name = "🤖 ARIA - PowerShell"
                Description = "ARIA - Iniciar con PowerShell"
            }
        )
        
        $selectedLauncher = $null
        foreach ($launcher in $launchers) {
            $launcherPath = Join-Path $ProjectPath $launcher.File
            if (Test-Path $launcherPath) {
                $selectedLauncher = $launcher
                $selectedLauncher.Path = $launcherPath
                break
            }
        }
        
        if (-not $selectedLauncher) {
            Write-ColorOutput "❌ No se encontraron archivos launcher de ARIA" "Red"
            return $false
        }
        
        Write-ColorOutput "📁 Proyecto: $ProjectPath" "Cyan"
        Write-ColorOutput "🖥️ Escritorio: $DesktopPath" "Cyan"
        Write-ColorOutput "🎯 Launcher: $($selectedLauncher.File)" "Cyan"
        
        # Crear acceso directo
        $shortcutPath = Join-Path $DesktopPath "$($selectedLauncher.Name).lnk"
        
        # Eliminar acceso directo existente si existe y Force está habilitado
        if ((Test-Path $shortcutPath) -and $Force) {
            Remove-Item $shortcutPath -Force
            Write-ColorOutput "🗑️ Acceso directo anterior eliminado" "Yellow"
        } elseif (Test-Path $shortcutPath) {
            Write-ColorOutput "⚠️ Ya existe un acceso directo. Usa -Force para sobrescribir" "Yellow"
            return $false
        }
        
        # Crear objeto COM para el acceso directo
        $WshShell = New-Object -ComObject WScript.Shell
        $Shortcut = $WshShell.CreateShortcut($shortcutPath)
        
        # Configurar propiedades del acceso directo
        $Shortcut.TargetPath = $selectedLauncher.Path
        $Shortcut.WorkingDirectory = $ProjectPath
        $Shortcut.Description = $selectedLauncher.Description
        $Shortcut.WindowStyle = 1  # Normal window
        
        # Configurar ícono
        if ($CustomIconPath -and (Test-Path $CustomIconPath)) {
            $Shortcut.IconLocation = $CustomIconPath
            Write-ColorOutput "🎨 Ícono personalizado: $CustomIconPath" "Green"
        } else {
            # Buscar íconos en el proyecto
            $iconPaths = @(
                (Join-Path $ProjectPath "assets\icons\aria_icon.ico"),
                (Join-Path $ProjectPath "assets\aria.ico"),
                (Join-Path $ProjectPath "aria_icon.ico"),
                (Join-Path $ProjectPath "icon.ico")
            )
            
            $iconFound = $false
            foreach ($iconPath in $iconPaths) {
                if (Test-Path $iconPath) {
                    $Shortcut.IconLocation = $iconPath
                    Write-ColorOutput "🎨 Ícono encontrado: $iconPath" "Green"
                    $iconFound = $true
                    break
                }
            }
            
            if (-not $iconFound) {
                # Usar ícono del sistema para aplicaciones
                $Shortcut.IconLocation = "shell32.dll,1"
                Write-ColorOutput "🎨 Usando ícono del sistema" "Yellow"
            }
        }
        
        # Guardar el acceso directo
        $Shortcut.Save()
        
        # Verificar que se creó
        if (Test-Path $shortcutPath) {
            Write-ColorOutput "✅ Acceso directo creado exitosamente" "Green"
            Write-ColorOutput "🔗 Ubicación: $shortcutPath" "Cyan"
            return $true
        } else {
            Write-ColorOutput "❌ Error: No se pudo crear el acceso directo" "Red"
            return $false
        }
        
    } catch {
        Write-ColorOutput "❌ Error creando acceso directo: $($_.Exception.Message)" "Red"
        return $false
    } finally {
        # Limpiar objetos COM
        if ($WshShell) {
            [System.Runtime.Interopservices.Marshal]::ReleaseComObject($WshShell) | Out-Null
        }
    }
}

function Create-SimpleIcon {
    param(
        [string]$ProjectPath
    )
    
    try {
        # Crear directorio de assets si no existe
        $assetsDir = Join-Path $ProjectPath "assets\icons"
        if (-not (Test-Path $assetsDir)) {
            New-Item -ItemType Directory -Path $assetsDir -Force | Out-Null
            Write-ColorOutput "📁 Directorio de assets creado" "Green"
        }
        
        # Crear un archivo .bat que puede servir como ícono básico
        $iconBat = Join-Path $assetsDir "aria_icon.bat"
        $iconContent = @"
@echo off
rem Este archivo sirve como placeholder para el ícono de ARIA
echo ARIA - Asistente IA Futurista
"@
        Set-Content -Path $iconBat -Value $iconContent -Encoding UTF8
        
        Write-ColorOutput "🎨 Archivo de ícono básico creado" "Green"
        return $iconBat
        
    } catch {
        Write-ColorOutput "⚠️ No se pudo crear archivo de ícono: $($_.Exception.Message)" "Yellow"
        return $null
    }
}

# Script principal
Write-ColorOutput ""
Write-ColorOutput "================================================================================"
Write-ColorOutput "🎯 ARIA - RESTAURADOR DE ÍCONO DEL ESCRITORIO" "Cyan"
Write-ColorOutput "================================================================================"
Write-ColorOutput "🎨 Recreando acceso directo de ARIA en el escritorio..." "Yellow"
Write-ColorOutput ""

# Obtener rutas
$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
$projectPath = $scriptPath
$desktopPath = [Environment]::GetFolderPath("Desktop")

Write-ColorOutput "📊 Información del sistema:" "Cyan"
Write-ColorOutput "   📁 Directorio del proyecto: $projectPath" "White"
Write-ColorOutput "   🖥️ Escritorio: $desktopPath" "White"
Write-ColorOutput ""

# Verificar que estamos en el directorio correcto
$expectedFiles = @("ARIA_MENU_PRINCIPAL.bat", "INICIAR_ARIA_FINAL.bat", "INICIAR_ARIA_FINAL.ps1")
$foundFiles = @()

foreach ($file in $expectedFiles) {
    $filePath = Join-Path $projectPath $file
    if (Test-Path $filePath) {
        $foundFiles += $file
    }
}

if ($foundFiles.Count -eq 0) {
    Write-ColorOutput "❌ No se encontraron archivos de ARIA en este directorio" "Red"
    Write-ColorOutput "💡 Asegúrate de ejecutar este script desde la carpeta del proyecto ARIA" "Yellow"
    Write-ColorOutput ""
    Read-Host "Presiona Enter para salir"
    exit 1
}

Write-ColorOutput "✅ Archivos de ARIA encontrados:" "Green"
foreach ($file in $foundFiles) {
    Write-ColorOutput "   📄 $file" "White"
}
Write-ColorOutput ""

# Crear ícono simple si no existe
if ($IconPath -eq "") {
    $IconPath = Create-SimpleIcon -ProjectPath $projectPath
}

# Crear acceso directo
Write-ColorOutput "🔧 Creando acceso directo..." "Yellow"
$success = Create-ARIADesktopShortcut -ProjectPath $projectPath -DesktopPath $desktopPath -CustomIconPath $IconPath

Write-ColorOutput ""
Write-ColorOutput "================================================================================"

if ($success) {
    Write-ColorOutput "🎉 ¡ÍCONO DE ARIA RESTAURADO EXITOSAMENTE!" "Green"
    Write-ColorOutput "✅ El ícono de ARIA está ahora disponible en tu escritorio" "Green"
    Write-ColorOutput "🚀 Haz doble clic en el ícono para iniciar ARIA" "Cyan"
    Write-ColorOutput ""
    Write-ColorOutput "📋 Funcionalidades disponibles:" "Cyan"
    Write-ColorOutput "   🤖 Interfaz web interactiva" "White"
    Write-ColorOutput "   💬 Chat con IA avanzada" "White"
    Write-ColorOutput "   🧠 Sistema de aprendizaje" "White"
    Write-ColorOutput "   📊 APIs REST completas" "White"
} else {
    Write-ColorOutput "❌ NO SE PUDO RESTAURAR EL ÍCONO" "Red"
    Write-ColorOutput "🔧 Posibles soluciones:" "Yellow"
    Write-ColorOutput "   1. Ejecutar como administrador" "White"
    Write-ColorOutput "   2. Verificar permisos del escritorio" "White"
    Write-ColorOutput "   3. Usar el parámetro -Force para sobrescribir" "White"
    Write-ColorOutput ""
    Write-ColorOutput "💡 Intenta: .\restaurar_icono_aria.ps1 -Force" "Cyan"
}

Write-ColorOutput "================================================================================"
Write-ColorOutput ""
Read-Host "Presiona Enter para continuar"