@echo off
echo Creando acceso directo de ARIA en el escritorio...

powershell -Command "& {$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('C:\Users\richa\Desktop\ARIA Asistente IA.lnk'); $Shortcut.TargetPath = 'C:\Users\richa\OneDrive\Desktop\aprendiendo-ia\ARIA_Desktop.bat'; $Shortcut.WorkingDirectory = 'C:\Users\richa\OneDrive\Desktop\aprendiendo-ia'; $Shortcut.Description = 'ARIA - Asistente de IA Personal'; $Shortcut.Save(); Write-Host 'Acceso directo principal creado'}"

powershell -Command "& {$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('C:\Users\richa\Desktop\Iniciar ARIA.lnk'); $Shortcut.TargetPath = 'C:\Users\richa\OneDrive\Desktop\aprendiendo-ia\Iniciar_ARIA.bat'; $Shortcut.WorkingDirectory = 'C:\Users\richa\OneDrive\Desktop\aprendiendo-ia'; $Shortcut.Description = 'Iniciar ARIA directamente'; $Shortcut.Save(); Write-Host 'Acceso directo rapido creado'}"

echo.
echo ✅ Accesos directos creados en el escritorio:
echo    📍 "ARIA Asistente IA.lnk" - Panel completo
echo    📍 "Iniciar ARIA.lnk" - Inicio directo
echo.
echo 🎉 ¡Ya puedes usar ARIA desde tu escritorio!
echo.
pause