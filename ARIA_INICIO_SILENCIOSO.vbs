' ==========================================
' 🚀 ARIA - Iniciador Silencioso (VBS)
' ==========================================
' Este script inicia ARIA sin mostrar ventanas de comandos

Dim objShell, fso, projectPath, pythonPath

' Crear objeto Shell
Set objShell = CreateObject("WScript.Shell")
Set fso = CreateObject("Scripting.FileSystemObject")

' Rutas del proyecto
projectPath = "C:\Users\richa\OneDrive\Desktop\aprendiendo-ia"
pythonPath = projectPath & "\venv\Scripts\python.exe"

' Verificar que el proyecto existe
If Not fso.FolderExists(projectPath) Then
    MsgBox "❌ No se encontró el proyecto ARIA en: " & projectPath, vbCritical, "Error - ARIA"
    WScript.Quit
End If

' Mostrar mensaje de inicio
objShell.Popup "🚀 Iniciando ARIA..." & vbNewLine & vbNewLine & "✅ Backend" & vbNewLine & "✅ Frontend" & vbNewLine & "✅ Supabase", 3, "ARIA - Sistema IA", vbInformation

' Cambiar al directorio del proyecto
objShell.CurrentDirectory = projectPath

' 1. Iniciar Backend (ventana oculta)
objShell.Run """" & pythonPath & """ backend\src\main_stable.py", 0, False

' Esperar 5 segundos
WScript.Sleep 5000

' 2. Cambiar al directorio frontend
objShell.CurrentDirectory = projectPath & "\frontend"

' Verificar si node_modules existe
If Not fso.FolderExists(projectPath & "\frontend\node_modules") Then
    ' Instalar dependencias si no existen
    objShell.Popup "📥 Instalando dependencias del frontend..." & vbNewLine & "Esto puede tomar unos minutos la primera vez.", 3, "ARIA - Configuración", vbInformation
    objShell.Run "cmd /c npm install", 0, True
End If

' 3. Iniciar Frontend (ventana oculta)
objShell.Run "cmd /c npm start", 0, False

' Esperar 15 segundos para que todo inicie
WScript.Sleep 15000

' 4. Abrir navegador
objShell.Run "http://localhost:3000"

' Mostrar mensaje final
objShell.Popup "🎉 ¡ARIA iniciado correctamente!" & vbNewLine & vbNewLine & "🌐 Se abrió en tu navegador" & vbNewLine & "🔗 http://localhost:3000" & vbNewLine & vbNewLine & "💡 Todo funciona en segundo plano", 5, "ARIA - Sistema IA", vbInformation