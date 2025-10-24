# Script PowerShell para crear acceso directo de ARIA en el escritorio
# Ejecutar como administrador para mejores resultados

$DesktopPath = [Environment]::GetFolderPath("Desktop")
$ProjectPath = "C:\Users\richa\OneDrive\Desktop\aprendiendo-ia"
$ShortcutPath = Join-Path $DesktopPath "🤖 ARIA Asistente IA.lnk"

Write-Host "🚀 Creando acceso directo de ARIA en el escritorio..." -ForegroundColor Cyan

# Crear objeto WScript.Shell
$WshShell = New-Object -comObject WScript.Shell

# Crear el acceso directo
$Shortcut = $WshShell.CreateShortcut($ShortcutPath)
$Shortcut.TargetPath = Join-Path $ProjectPath "ARIA_Desktop.bat"
$Shortcut.WorkingDirectory = $ProjectPath
$Shortcut.Description = "🤖 ARIA - Asistente de IA Personal con Panel de Control"
$Shortcut.IconLocation = "C:\Windows\System32\shell32.dll,13"  # Icono de computadora
$Shortcut.WindowStyle = 1  # Ventana normal
$Shortcut.Save()

Write-Host "✅ Acceso directo creado exitosamente:" -ForegroundColor Green
Write-Host "   📍 Ubicación: $ShortcutPath" -ForegroundColor Yellow
Write-Host "   🎯 Apunta a: ARIA_Desktop.bat" -ForegroundColor Yellow
Write-Host ""
Write-Host "🎉 ¡Ya puedes hacer doble clic en el escritorio para abrir ARIA!" -ForegroundColor Green
Write-Host ""
Write-Host "📋 Funciones disponibles desde el acceso directo:" -ForegroundColor Cyan
Write-Host "   🚀 Iniciar ARIA completo" -ForegroundColor White
Write-Host "   🌐 Abrir solo la interfaz web" -ForegroundColor White
Write-Host "   🖥️  Conectar por escritorio remoto" -ForegroundColor White
Write-Host "   📊 Diagnóstico del sistema" -ForegroundColor White
Write-Host "   🔧 Reinstalar dependencias" -ForegroundColor White
Write-Host ""

# Intentar también crear el acceso directo simple
$SimpleShortcutPath = Join-Path $DesktopPath "🚀 Iniciar ARIA.lnk"
$SimpleShortcut = $WshShell.CreateShortcut($SimpleShortcutPath)
$SimpleShortcut.TargetPath = Join-Path $ProjectPath "Iniciar_ARIA.bat"
$SimpleShortcut.WorkingDirectory = $ProjectPath
$SimpleShortcut.Description = "🚀 Iniciar ARIA directamente"
$SimpleShortcut.IconLocation = "C:\Windows\System32\shell32.dll,21"  # Icono de aplicación
$SimpleShortcut.WindowStyle = 1
$SimpleShortcut.Save()

Write-Host "✅ También se creó acceso directo de inicio rápido:" -ForegroundColor Green
Write-Host "   📍 🚀 Iniciar ARIA.lnk" -ForegroundColor Yellow
Write-Host ""
Write-Host "🎯 Recomendación: Usa '🤖 ARIA Asistente IA' para el panel completo" -ForegroundColor Magenta
Write-Host "                 Usa '🚀 Iniciar ARIA' para inicio directo" -ForegroundColor Magenta

Read-Host "`nPresiona Enter para continuar..."