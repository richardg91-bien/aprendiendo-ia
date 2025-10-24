# Script PowerShell para crear iconos de ARIA muy visibles en el escritorio
# Ejecutar: .\Crear_Icono_Visible.ps1

Write-Host "🎨 Creando iconos de ARIA muy visibles para el escritorio..." -ForegroundColor Cyan

# Obtener ruta del escritorio
$DesktopPath = [Environment]::GetFolderPath("Desktop")
$ProjectPath = Get-Location
$WshShell = New-Object -comObject WScript.Shell

Write-Host ""
Write-Host "📍 Escritorio: $DesktopPath" -ForegroundColor Yellow
Write-Host "📁 Proyecto: $ProjectPath" -ForegroundColor Yellow
Write-Host ""

# Array de iconos a crear con diferentes estilos
$Shortcuts = @(
    @{
        Name = "🤖 ARIA Asistente IA"
        Target = "ARIA_Desktop.bat"
        Description = "🤖 ARIA - Asistente de IA Personal - Panel Completo"
        Icon = "C:\Windows\System32\shell32.dll,13"  # Icono de computadora
    },
    @{
        Name = "🚀 ARIA Inicio Rápido"
        Target = "Iniciar_ARIA.bat"
        Description = "🚀 Iniciar ARIA directamente - Un clic y listo"
        Icon = "C:\Windows\System32\shell32.dll,21"  # Icono de aplicación
    },
    @{
        Name = "🧠 ARIA Intelligence"
        Target = "ARIA_Desktop.bat"
        Description = "🧠 ARIA - Inteligencia Artificial con Supabase"
        Icon = "C:\Windows\System32\imageres.dll,76"  # Icono de cerebro/inteligencia
    },
    @{
        Name = "⚡ ARIA Quick Launch"
        Target = "Iniciar_ARIA.bat"
        Description = "⚡ Lanzamiento rápido de ARIA - Servidor automático"
        Icon = "C:\Windows\System32\imageres.dll,1"   # Icono de rayo
    },
    @{
        Name = "🎯 ARIA Control Panel"
        Target = "ARIA_Desktop.bat"
        Description = "🎯 Panel de control completo de ARIA"
        Icon = "C:\Windows\System32\shell32.dll,137"  # Icono de configuración
    }
)

# Crear cada acceso directo
foreach ($ShortcutInfo in $Shortcuts) {
    $ShortcutPath = Join-Path $DesktopPath ($ShortcutInfo.Name + ".lnk")
    
    try {
        $Shortcut = $WshShell.CreateShortcut($ShortcutPath)
        $Shortcut.TargetPath = Join-Path $ProjectPath $ShortcutInfo.Target
        $Shortcut.WorkingDirectory = $ProjectPath
        $Shortcut.Description = $ShortcutInfo.Description
        $Shortcut.IconLocation = $ShortcutInfo.Icon
        $Shortcut.WindowStyle = 1
        $Shortcut.Save()
        
        Write-Host "✅ Creado: $($ShortcutInfo.Name)" -ForegroundColor Green
    }
    catch {
        Write-Host "❌ Error creando: $($ShortcutInfo.Name)" -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "🎨 Creando icono adicional con PowerShell personalizado..." -ForegroundColor Magenta

# Crear un icono especial con icono de sistema más visible
$SpecialShortcut = Join-Path $DesktopPath "🌟 ARIA AI System.lnk"
$Special = $WshShell.CreateShortcut($SpecialShortcut)
$Special.TargetPath = Join-Path $ProjectPath "ARIA_Desktop.bat"
$Special.WorkingDirectory = $ProjectPath
$Special.Description = "🌟 ARIA - Sistema de Inteligencia Artificial Avanzado"
$Special.IconLocation = "C:\Windows\System32\DDORes.dll,2"  # Icono especial del sistema
$Special.Save()

Write-Host "✅ Icono especial creado: 🌟 ARIA AI System" -ForegroundColor Green

Write-Host ""
Write-Host "🎯 Intentando crear icono con imagen personalizada..." -ForegroundColor Cyan

# Intentar crear un archivo ICO simple usando PowerShell
try {
    $IconScript = @"
Add-Type -AssemblyName System.Drawing
`$bitmap = New-Object System.Drawing.Bitmap(32, 32)
`$graphics = [System.Drawing.Graphics]::FromImage(`$bitmap)
`$graphics.Clear([System.Drawing.Color]::Blue)
`$font = New-Object System.Drawing.Font("Arial", 14, [System.Drawing.FontStyle]::Bold)
`$brush = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::White)
`$graphics.DrawString("AI", `$font, `$brush, 2, 8)
`$graphics.Dispose()
`$iconPath = "$ProjectPath\aria_icon.ico"
if (Test-Path `$iconPath) { Remove-Item `$iconPath }
`$bitmap.Save(`$iconPath, [System.Drawing.Imaging.ImageFormat]::Icon)
Write-Host "✅ Icono personalizado creado: aria_icon.ico" -ForegroundColor Green
"@
    
    Invoke-Expression $IconScript
    
    # Crear acceso directo con icono personalizado
    if (Test-Path "$ProjectPath\aria_icon.ico") {
        $CustomShortcut = Join-Path $DesktopPath "🎨 ARIA Custom.lnk"
        $Custom = $WshShell.CreateShortcut($CustomShortcut)
        $Custom.TargetPath = Join-Path $ProjectPath "ARIA_Desktop.bat"
        $Custom.WorkingDirectory = $ProjectPath
        $Custom.Description = "🎨 ARIA - Con icono personalizado azul"
        $Custom.IconLocation = "$ProjectPath\aria_icon.ico"
        $Custom.Save()
        
        Write-Host "✅ Icono personalizado aplicado: 🎨 ARIA Custom" -ForegroundColor Green
    }
}
catch {
    Write-Host "⚠️ No se pudo crear icono personalizado, usando iconos del sistema" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "████████████████████████████████████████████████████████████████" -ForegroundColor Green
Write-Host "                    🎉 ICONOS CREADOS EXITOSAMENTE" -ForegroundColor Green
Write-Host "████████████████████████████████████████████████████████████████" -ForegroundColor Green
Write-Host ""
Write-Host "📍 Iconos creados en tu escritorio:" -ForegroundColor Cyan
Write-Host ""

foreach ($ShortcutInfo in $Shortcuts) {
    Write-Host "   🔗 $($ShortcutInfo.Name).lnk" -ForegroundColor White
}
Write-Host "   🔗 🌟 ARIA AI System.lnk" -ForegroundColor White

if (Test-Path "$ProjectPath\aria_icon.ico") {
    Write-Host "   🔗 🎨 ARIA Custom.lnk (con icono personalizado)" -ForegroundColor White
}

Write-Host ""
Write-Host "🎯 Características de los iconos:" -ForegroundColor Yellow
Write-Host "   • Diferentes estilos visuales para elegir" -ForegroundColor White
Write-Host "   • Iconos con emojis para fácil identificación" -ForegroundColor White
Write-Host "   • Descripciones detalladas al pasar el mouse" -ForegroundColor White
Write-Host "   • Todos conectados a ARIA con opciones diferentes" -ForegroundColor White
Write-Host ""
Write-Host "✨ ¡ARIA ahora es súper visible en tu escritorio!" -ForegroundColor Magenta
Write-Host ""

Read-Host "Presiona Enter para continuar..."