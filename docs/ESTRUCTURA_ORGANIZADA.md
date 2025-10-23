# 📁 Estructura Organizada del Proyecto ARIA

## 🎯 Nueva Organización de Archivos

### 📂 **assets/**
- **icons/** - Todos los iconos PNG e ICO de ARIA
  - `aria_icon.ico`, `aria_icon_*.png`
  - `aria_icon_premium.ico`, `aria_icon_advanced.ico`

### 📂 **backend/**
- Código del servidor backend
- APIs y lógica principal de ARIA

### 📂 **frontend/**
- Interfaz de usuario web
- Componentes React y archivos estáticos

### 📂 **config/**
- Archivos de configuración del proyecto
- Variables de entorno y configuraciones

### 📂 **data/**
- Datos del proyecto y bases de datos locales

### 📂 **docs/**
- Documentación del proyecto

### 📂 **scripts/**

#### 📁 **aria/**
- `aria_estable.py` - Versión estable de ARIA
- `aria_google_cloud_integration.py` - Integración con Google Cloud
- `aria_servidor_multilingue.py` - Servidor multilingüe
- `aria_test_server.py` - Servidor de pruebas
- `aria_oauth_flow_example.py` - Ejemplo de flujo OAuth

#### 📁 **demo/**
- `demo_*.py` - Archivos de demostración
- `explicacion_*.py` - Archivos explicativos
- `explorar_*.py` - Scripts de exploración
- `ejemplo_*.py` - Scripts de ejemplo

#### 📁 **launcher/**
- `INICIAR_*.bat` - Scripts de inicio por lotes
- `*.ps1` - Scripts de PowerShell
- `*.vbs` - Scripts VBS
- `start_*.py` - Scripts de inicio en Python
- `menu_*.py` - Scripts de menú

#### 📁 **setup/**
- `configurar_*.py` - Scripts de configuración
- `configure_*.py` - Scripts de configuración
- `setup_*.py` - Scripts de instalación
- `instalar_*.py` - Scripts de instalación
- `crear_*.py` - Scripts de creación
- `create_*.py` - Scripts de creación
- `guia_*.py` - Scripts de guía

#### 📁 **test/**
- `test_*.py` - Scripts de prueba
- `probar_*.py` - Scripts de prueba
- `prueba_*.py` - Scripts de prueba
- `verificar_*.py` - Scripts de verificación
- `verify_*.py` - Scripts de verificación
- `check_*.py` - Scripts de verificación
- `diagnose_*.py` - Scripts de diagnóstico

### 📂 **updates/**
- `actualizar_*.py` - Scripts de actualización

### 📂 **reports/**
- `*.json` - Reportes y configuraciones en JSON
- Reportes de Google Cloud y verificaciones

### 📂 **legacy/**
- Archivos obsoletos y versiones anteriores

## 🚀 Ventajas de esta Organización

1. **📋 Claridad**: Cada tipo de archivo tiene su lugar específico
2. **🔍 Facilidad de búsqueda**: Los archivos están categorizados por función
3. **🛠️ Mantenimiento**: Más fácil mantener y actualizar el proyecto
4. **👥 Colaboración**: Otros desarrolladores pueden entender la estructura rápidamente
5. **📈 Escalabilidad**: Fácil agregar nuevos archivos en las categorías correctas

## 📝 Archivos Principales en la Raíz

- `README.md` - Documentación principal
- `README_ARIA.md` - Documentación específica de ARIA
- `.env*` - Variables de entorno
- `.gitignore` - Archivos ignorados por Git
- Documentos markdown de estado y guías

## 🎯 Próximos Pasos

1. Verificar que todos los archivos estén en su lugar correcto
2. Actualizar rutas en scripts que referencien archivos movidos
3. Probar que todos los scripts funcionen con la nueva estructura
4. Actualizar documentación con las nuevas rutas

---
*Organización completada el {{ fecha_actual }}*