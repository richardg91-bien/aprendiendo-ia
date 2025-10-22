"""
Documentación: Sistema de Voz Spock para ARIA
"""

# 🎙️ Sistema de Síntesis de Voz Spock - ARIA

## 🚀 **Funcionalidad Implementada**

### **✅ Características del Sistema de Voz:**
- **Personalidad Spock:** Transforma respuestas para sonar lógicas y formales
- **Síntesis de Voz:** Usa Windows SAPI para text-to-speech
- **Frases Características:** Incluye saludos, despedidas y expresiones típicas de Spock
- **Transformación de Texto:** Convierte lenguaje coloquial a formal
- **Ejecución Asíncrona:** No bloquea el servidor mientras habla

### **✅ Endpoints de API Disponibles:**

#### **1. Control de Voz:**
```http
POST /api/voice/toggle
Content-Type: application/json

{
  "enabled": true/false
}
```

#### **2. Prueba de Voz:**
```http
POST /api/voice/test
Content-Type: application/json

{
  "text": "Texto a pronunciar"
}
```

#### **3. Saludo Spock:**
```http
POST /api/voice/greeting
```

#### **4. Configuración de Voz:**
```http
POST /api/voice/settings
Content-Type: application/json

{
  "speed": 2
}
```

### **✅ Integración en Chat:**
- El chat ahora incluye síntesis de voz automática
- Respuestas se pronuncian con estilo Spock
- Indicadores de "pensando" con voz
- Control on/off por conversación

## 🎯 **Cómo Usar el Sistema de Voz**

### **1. Chat con Voz (Automático):**
- Las respuestas se pronuncian automáticamente
- Estilo lógico y formal de Spock
- Transformación de texto inteligente

### **2. Control Manual:**
```javascript
// Activar/desactivar voz
fetch('/api/voice/toggle', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ enabled: true })
});

// Prueba de voz
fetch('/api/voice/test', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ text: "Fascinante" })
});
```

## 🎨 **Transformaciones de Texto Spock**

### **Ejemplos de Transformaciones:**
- `"no sé"` → `"no poseo esa información"`
- `"creo que"` → `"mi análisis sugiere que"`
- `"interesante"` → `"fascinante"`
- `"hola"` → `"saludo"`
- `"adiós"` → `"vida larga y próspera"`

### **Frases Características:**
- **Saludos:** "Saludo, humano", "Fascinante. ¿En qué puedo asistirle?"
- **Despedidas:** "Vida larga y próspera", "Que la lógica les acompañe"
- **Procesamiento:** "Analizando información disponible..."

## 🔧 **Configuración Técnica**

### **Archivos Creados:**
- `backend/src/spock_voice_system.py` - Sistema principal con pyttsx3
- `backend/src/spock_voice_simple.py` - Sistema fallback con Windows SAPI
- `backend/src/test_spock_voice.py` - Script de pruebas

### **Dependencias Agregadas:**
- `pyttsx3==2.90` - Síntesis de voz multiplataforma

### **Integración en main.py:**
- Imports dinámicos con fallback
- Endpoints de API para control
- Integración en función de chat

## 🎉 **Estado Actual**

### **✅ Funcionando:**
- ✅ Sistema de voz cargado exitosamente
- ✅ Servidor ejecutándose en http://localhost:8000
- ✅ API endpoints disponibles
- ✅ Transformación de texto estilo Spock
- ✅ Ejecución asíncrona sin bloqueos

### **🔄 Próximos Pasos:**
1. **Frontend:** Agregar botón de control de voz en la interfaz
2. **Configuración:** Panel de ajustes de velocidad y volumen
3. **Personalización:** Más frases y estilos de Spock
4. **Optimización:** Mejor manejo de errores

## 🚀 **Cómo Probar**

### **1. Desde la Interfaz Web:**
1. Abre http://localhost:8000
2. Escribe un mensaje en el chat
3. ARIA responderá con voz de Spock automáticamente

### **2. Desde API directamente:**
```bash
# Activar voz
curl -X POST http://localhost:8000/api/voice/toggle \
  -H "Content-Type: application/json" \
  -d '{"enabled": true}'

# Prueba de voz
curl -X POST http://localhost:8000/api/voice/test \
  -H "Content-Type: application/json" \
  -d '{"text": "Fascinante. El sistema está funcionando."}'
```

¡El sistema de voz Spock está completamente integrado y funcionando!