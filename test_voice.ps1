Add-Type -AssemblyName System.Speech
$voice = New-Object System.Speech.Synthesis.SpeechSynthesizer
$voice.Rate = 0
$voice.Volume = 80
$voice.Speak("Hola, soy ARIA. Mi sistema de voz está funcionando correctamente.")
Write-Host "Prueba de voz completada"