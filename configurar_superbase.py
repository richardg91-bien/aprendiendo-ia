#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔧 Configurador Automático de ARIA Super Base
Configura automáticamente la integración con Supabase
"""

import os
import json
import shutil
from datetime import datetime
from typing import Dict, Any

class ARIASupabaseConfigurator:
    """Configurador automático de Supabase para ARIA"""
    
    def __init__(self):
        self.project_root = os.path.dirname(os.path.dirname(__file__))
        self.env_file = os.path.join(self.project_root, '.env')
        self.env_template = os.path.join(self.project_root, '.env.template')
        self.config_file = os.path.join(self.project_root, 'supabase_config.json')
        
    def setup_environment(self):
        """Configurar archivo de variables de entorno"""
        print("🔧 Configurando variables de entorno...")
        
        # Verificar si ya existe .env
        if os.path.exists(self.env_file):
            backup_file = f"{self.env_file}.backup.{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            shutil.copy2(self.env_file, backup_file)
            print(f"💾 Backup creado: {backup_file}")
        
        # Copiar template si no existe .env
        if not os.path.exists(self.env_file) and os.path.exists(self.env_template):
            shutil.copy2(self.env_template, self.env_file)
            print(f"📋 Archivo .env creado desde template")
        
        # Configuración por defecto de Supabase
        default_config = {
            'SUPABASE_URL': 'https://cggxjweagmeirqpdzypn.supabase.co',
            'SUPABASE_ANON_KEY': '',
            'ARIA_ENVIRONMENT': 'development',
            'ARIA_DEBUG': 'true',
            'ARIA_SESSION_TIMEOUT': '3600',
            'ARIA_MAX_CONVERSATIONS': '1000'
        }
        
        # Leer configuración actual
        current_config = {}
        if os.path.exists(self.env_file):
            with open(self.env_file, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#') and '=' in line:
                        key, value = line.split('=', 1)
                        current_config[key] = value
        
        # Actualizar con valores por defecto si no existen
        updated = False
        for key, value in default_config.items():
            if key not in current_config:
                current_config[key] = value
                updated = True
        
        # Escribir configuración actualizada
        if updated:
            with open(self.env_file, 'w', encoding='utf-8') as f:
                f.write("# 🗄️ ARIA Super Base - Configuración\n")
                f.write(f"# Generado automáticamente: {datetime.now().isoformat()}\n\n")
                
                for key, value in current_config.items():
                    f.write(f"{key}={value}\n")
                
                f.write("\n# Agregar tus claves de API aquí:\n")
                f.write("# SUPABASE_ANON_KEY=tu_clave_aqui\n")
                f.write("# OPENAI_API_KEY=tu_openai_key_aqui\n")
                f.write("# GOOGLE_API_KEY=tu_google_key_aqui\n")
            
            print("✅ Archivo .env actualizado")
        else:
            print("✅ Configuración ya existe")
    
    def create_database_schema(self):
        """Crear esquema SQL para las tablas de ARIA"""
        schema_sql = """
-- 🗄️ ARIA Super Base - Esquema de Base de Datos
-- Crear tablas necesarias para el funcionamiento de ARIA

-- Tabla de conocimiento general
CREATE TABLE IF NOT EXISTS aria_knowledge (
    id SERIAL PRIMARY KEY,
    concept VARCHAR(255) UNIQUE NOT NULL,
    description TEXT,
    category VARCHAR(100) DEFAULT 'general',
    confidence FLOAT DEFAULT 0.5 CHECK (confidence >= 0 AND confidence <= 1),
    source VARCHAR(255) DEFAULT 'conversation',
    tags TEXT[],
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Índices para búsqueda rápida
CREATE INDEX IF NOT EXISTS idx_aria_knowledge_concept ON aria_knowledge(concept);
CREATE INDEX IF NOT EXISTS idx_aria_knowledge_category ON aria_knowledge(category);
CREATE INDEX IF NOT EXISTS idx_aria_knowledge_confidence ON aria_knowledge(confidence DESC);

-- Tabla de relaciones con APIs
CREATE TABLE IF NOT EXISTS aria_api_relations (
    id SERIAL PRIMARY KEY,
    api_name VARCHAR(255) NOT NULL,
    api_type VARCHAR(100) NOT NULL,
    endpoint VARCHAR(500) NOT NULL,
    method VARCHAR(10) DEFAULT 'GET',
    description TEXT,
    status VARCHAR(50) DEFAULT 'active',
    last_used TIMESTAMP WITH TIME ZONE,
    success_rate FLOAT DEFAULT 1.0 CHECK (success_rate >= 0 AND success_rate <= 1),
    response_time_avg FLOAT DEFAULT 0,
    usage_count INTEGER DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    metadata JSONB DEFAULT '{}'::jsonb
);

-- Índices para APIs
CREATE INDEX IF NOT EXISTS idx_aria_api_type ON aria_api_relations(api_type);
CREATE INDEX IF NOT EXISTS idx_aria_api_status ON aria_api_relations(status);
CREATE INDEX IF NOT EXISTS idx_aria_api_success_rate ON aria_api_relations(success_rate DESC);

-- Tabla de conversaciones
CREATE TABLE IF NOT EXISTS aria_conversations (
    id SERIAL PRIMARY KEY,
    user_message TEXT NOT NULL,
    aria_response TEXT NOT NULL,
    emotion_state VARCHAR(50) DEFAULT 'neutral',
    confidence FLOAT DEFAULT 0.8 CHECK (confidence >= 0 AND confidence <= 1),
    apis_used JSONB DEFAULT '[]'::jsonb,
    knowledge_accessed JSONB DEFAULT '[]'::jsonb,
    session_id VARCHAR(100) DEFAULT 'default',
    user_id VARCHAR(100),
    language VARCHAR(10) DEFAULT 'es',
    response_time FLOAT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Índices para conversaciones
CREATE INDEX IF NOT EXISTS idx_aria_conv_session ON aria_conversations(session_id);
CREATE INDEX IF NOT EXISTS idx_aria_conv_user ON aria_conversations(user_id);
CREATE INDEX IF NOT EXISTS idx_aria_conv_created ON aria_conversations(created_at DESC);

-- Tabla de sesiones de aprendizaje
CREATE TABLE IF NOT EXISTS aria_learning_sessions (
    id SERIAL PRIMARY KEY,
    topic VARCHAR(255),
    source_type VARCHAR(100),
    knowledge_gained INTEGER DEFAULT 0,
    apis_discovered INTEGER DEFAULT 0,
    concepts_learned TEXT[],
    session_duration FLOAT,
    success_indicators JSONB DEFAULT '{}'::jsonb,
    quality_score FLOAT DEFAULT 0.5,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Tabla de estadísticas de uso
CREATE TABLE IF NOT EXISTS aria_usage_stats (
    id SERIAL PRIMARY KEY,
    date DATE DEFAULT CURRENT_DATE,
    conversations_count INTEGER DEFAULT 0,
    knowledge_queries INTEGER DEFAULT 0,
    api_calls INTEGER DEFAULT 0,
    new_knowledge INTEGER DEFAULT 0,
    avg_response_time FLOAT DEFAULT 0,
    user_satisfaction FLOAT DEFAULT 0.5,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(date)
);

-- Tabla de configuración del sistema
CREATE TABLE IF NOT EXISTS aria_system_config (
    key VARCHAR(100) PRIMARY KEY,
    value TEXT,
    description TEXT,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Insertar configuración por defecto
INSERT INTO aria_system_config (key, value, description) VALUES
('version', '2.0.0', 'Versión de ARIA')
ON CONFLICT (key) DO NOTHING;

INSERT INTO aria_system_config (key, value, description) VALUES
('max_knowledge_entries', '10000', 'Máximo número de entradas de conocimiento')
ON CONFLICT (key) DO NOTHING;

INSERT INTO aria_system_config (key, value, description) VALUES
('default_confidence', '0.5', 'Nivel de confianza por defecto')
ON CONFLICT (key) DO NOTHING;

-- Función para actualizar timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Triggers para actualizar timestamps automáticamente
DROP TRIGGER IF EXISTS update_aria_knowledge_updated_at ON aria_knowledge;
CREATE TRIGGER update_aria_knowledge_updated_at 
    BEFORE UPDATE ON aria_knowledge 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Vistas útiles
CREATE OR REPLACE VIEW aria_knowledge_summary AS
SELECT 
    category,
    COUNT(*) as total_concepts,
    AVG(confidence) as avg_confidence,
    MAX(updated_at) as last_updated
FROM aria_knowledge 
GROUP BY category;

CREATE OR REPLACE VIEW aria_api_performance AS
SELECT 
    api_type,
    COUNT(*) as total_apis,
    AVG(success_rate) as avg_success_rate,
    AVG(response_time_avg) as avg_response_time,
    SUM(usage_count) as total_usage
FROM aria_api_relations 
WHERE status = 'active'
GROUP BY api_type;

-- Comentarios sobre las tablas
COMMENT ON TABLE aria_knowledge IS 'Almacena el conocimiento aprendido por ARIA';
COMMENT ON TABLE aria_api_relations IS 'Registra las APIs y servicios externos que usa ARIA';
COMMENT ON TABLE aria_conversations IS 'Historial completo de conversaciones';
COMMENT ON TABLE aria_learning_sessions IS 'Registro de sesiones de aprendizaje automático';
COMMENT ON TABLE aria_usage_stats IS 'Estadísticas diarias de uso del sistema';
COMMENT ON TABLE aria_system_config IS 'Configuración del sistema ARIA';
"""
        
        schema_file = os.path.join(self.project_root, 'database_schema.sql')
        with open(schema_file, 'w', encoding='utf-8') as f:
            f.write(schema_sql)
        
        print(f"✅ Esquema SQL creado: {schema_file}")
        return schema_file
    
    def create_supabase_config(self):
        """Crear archivo de configuración JSON para Supabase"""
        config = {
            "project_info": {
                "project_id": "cggxjweagmeirqpdzypn",
                "project_name": "ARIA Super Base",
                "region": "us-west-1",
                "created_at": datetime.now().isoformat()
            },
            "database": {
                "host": "db.cggxjweagmeirqpdzypn.supabase.co",
                "port": 5432,
                "database": "postgres",
                "schema": "public"
            },
            "api": {
                "url": "https://cggxjweagmeirqpdzypn.supabase.co",
                "rest_endpoint": "/rest/v1/",
                "realtime_endpoint": "/realtime/v1/",
                "storage_endpoint": "/storage/v1/"
            },
            "features": {
                "auth_enabled": True,
                "realtime_enabled": True,
                "storage_enabled": True,
                "edge_functions_enabled": True
            },
            "aria_specific": {
                "max_knowledge_entries": 10000,
                "conversation_retention_days": 365,
                "api_timeout_seconds": 30,
                "batch_insert_size": 100,
                "enable_caching": True,
                "cache_ttl_seconds": 300
            },
            "security": {
                "row_level_security": True,
                "api_rate_limiting": True,
                "encryption_at_rest": True
            }
        }
        
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Configuración JSON creada: {self.config_file}")
        return config
    
    def install_dependencies(self):
        """Instalar dependencias necesarias"""
        print("📦 Verificando dependencias...")
        
        dependencies = [
            'supabase',
            'python-dotenv',
            'asyncio',
            'psycopg2-binary'
        ]
        
        try:
            import subprocess
            import sys
            
            for dep in dependencies:
                try:
                    __import__(dep.replace('-', '_'))
                    print(f"✅ {dep} ya está instalado")
                except ImportError:
                    print(f"📦 Instalando {dep}...")
                    subprocess.check_call([sys.executable, "-m", "pip", "install", dep])
                    print(f"✅ {dep} instalado correctamente")
                    
        except Exception as e:
            print(f"⚠️ Error instalando dependencias: {e}")
            print("📝 Instalar manualmente con:")
            for dep in dependencies:
                print(f"   pip install {dep}")
    
    def test_connection(self):
        """Probar conexión con Supabase"""
        print("🔗 Probando conexión con Supabase...")
        
        try:
            # Cargar variables de entorno
            from dotenv import load_dotenv
            load_dotenv(self.env_file)
            
            url = os.getenv('SUPABASE_URL')
            key = os.getenv('SUPABASE_ANON_KEY')
            
            if not url:
                print("❌ URL de Supabase no configurada")
                return False
                
            if not key or key == 'tu_clave_anonima_aqui':
                print("⚠️ Clave anónima de Supabase no configurada")
                print("   Configura SUPABASE_ANON_KEY en el archivo .env")
                return False
            
            # Intentar importar y conectar
            from supabase import create_client
            supabase = create_client(url, key)
            
            # Prueba simple
            result = supabase.table('aria_knowledge').select("count", count="exact").execute()
            print(f"✅ Conexión exitosa - Registros de conocimiento: {result.count or 0}")
            return True
            
        except ImportError:
            print("❌ Supabase no está instalado")
            return False
        except Exception as e:
            print(f"❌ Error de conexión: {e}")
            return False
    
    def run_full_setup(self):
        """Ejecutar configuración completa"""
        print("🚀 Iniciando configuración completa de ARIA Super Base...")
        print("=" * 60)
        
        try:
            # Paso 1: Configurar entorno
            self.setup_environment()
            print()
            
            # Paso 2: Instalar dependencias
            self.install_dependencies()
            print()
            
            # Paso 3: Crear esquema
            schema_file = self.create_database_schema()
            print()
            
            # Paso 4: Crear configuración
            config = self.create_supabase_config()
            print()
            
            # Paso 5: Probar conexión
            connection_ok = self.test_connection()
            print()
            
            # Resumen final
            print("📋 RESUMEN DE CONFIGURACIÓN:")
            print("=" * 40)
            print(f"✅ Variables de entorno: {self.env_file}")
            print(f"✅ Esquema SQL: {schema_file}")
            print(f"✅ Configuración JSON: {self.config_file}")
            print(f"{'✅' if connection_ok else '⚠️ '} Conexión Supabase: {'OK' if connection_ok else 'Pendiente'}")
            
            if not connection_ok:
                print("\n🔧 PASOS SIGUIENTES:")
                print("1. Obtén tu clave anónima de Supabase")
                print("2. Actualiza SUPABASE_ANON_KEY en .env")
                print("3. Ejecuta el esquema SQL en tu proyecto Supabase")
                print("4. Vuelve a probar la conexión")
            else:
                print("\n🎉 ¡ARIA Super Base configurado correctamente!")
                print("   Puedes usar aria_superbase.py en tus aplicaciones")
            
            return connection_ok
            
        except Exception as e:
            print(f"❌ Error en configuración: {e}")
            return False


def main():
    """Función principal"""
    print("🗄️ ARIA Super Base - Configurador Automático")
    print("=" * 50)
    
    configurator = ARIASupabaseConfigurator()
    success = configurator.run_full_setup()
    
    if success:
        print("\n🚀 ¡Configuración completada exitosamente!")
    else:
        print("\n⚠️ Configuración parcial - Revisar pasos pendientes")
    
    return success


if __name__ == "__main__":
    main()