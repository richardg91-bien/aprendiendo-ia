#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🗄️ Creador de Tablas ARIA Super Base
===================================

Script para crear las tablas necesarias en Supabase
para el funcionamiento de ARIA Super Base.

Fecha: 22 de octubre de 2025
"""

import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

try:
    from supabase import create_client, Client
    import psycopg2
    from psycopg2 import sql
    DEPENDENCIES_OK = True
except ImportError as e:
    print(f"❌ Dependencias faltantes: {e}")
    print("Instalar con: pip install supabase psycopg2-binary")
    DEPENDENCIES_OK = False

def create_aria_tables():
    """Crear todas las tablas necesarias para ARIA"""
    if not DEPENDENCIES_OK:
        return False
    
    print("🗄️ Creando tablas de ARIA Super Base...")
    
    # Configuración de conexión
    url = os.getenv('SUPABASE_URL')
    key = os.getenv('SUPABASE_ANON_KEY')
    
    if not url or not key:
        print("❌ Variables de entorno SUPABASE_URL y SUPABASE_ANON_KEY requeridas")
        return False
    
    try:
        # Conectar a Supabase
        supabase = create_client(url, key)
        print(f"✅ Conectado a Supabase: {url}")
        
        # Esquemas SQL para crear las tablas
        tables_sql = [
            # Tabla de conocimiento
            """
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
            """,
            
            # Tabla de relaciones de APIs
            """
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
            """,
            
            # Tabla de conversaciones
            """
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
            """,
            
            # Tabla de sesiones de aprendizaje
            """
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
            """,
            
            # Tabla de estadísticas de uso
            """
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
            """,
            
            # Tabla de configuración del sistema
            """
            CREATE TABLE IF NOT EXISTS aria_system_config (
                key VARCHAR(100) PRIMARY KEY,
                value TEXT,
                description TEXT,
                updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
            );
            """
        ]
        
        # Índices para optimización
        indexes_sql = [
            "CREATE INDEX IF NOT EXISTS idx_aria_knowledge_concept ON aria_knowledge(concept);",
            "CREATE INDEX IF NOT EXISTS idx_aria_knowledge_category ON aria_knowledge(category);",
            "CREATE INDEX IF NOT EXISTS idx_aria_knowledge_confidence ON aria_knowledge(confidence DESC);",
            "CREATE INDEX IF NOT EXISTS idx_aria_api_type ON aria_api_relations(api_type);",
            "CREATE INDEX IF NOT EXISTS idx_aria_api_status ON aria_api_relations(status);",
            "CREATE INDEX IF NOT EXISTS idx_aria_conv_session ON aria_conversations(session_id);",
            "CREATE INDEX IF NOT EXISTS idx_aria_conv_created ON aria_conversations(created_at DESC);"
        ]
        
        # Configuración inicial
        config_sql = [
            """
            INSERT INTO aria_system_config (key, value, description) VALUES
            ('version', '2.0.0', 'Versión de ARIA Super Base')
            ON CONFLICT (key) DO UPDATE SET value = EXCLUDED.value;
            """,
            """
            INSERT INTO aria_system_config (key, value, description) VALUES
            ('max_knowledge_entries', '10000', 'Máximo número de entradas de conocimiento')
            ON CONFLICT (key) DO NOTHING;
            """,
            """
            INSERT INTO aria_system_config (key, value, description) VALUES
            ('default_confidence', '0.5', 'Nivel de confianza por defecto')
            ON CONFLICT (key) DO NOTHING;
            """
        ]
        
        # Obtener la URL de conexión directa a PostgreSQL
        # Necesitamos usar la conexión directa para ejecutar DDL
        database_url = os.getenv('DATABASE_URL')
        if not database_url:
            print("❌ DATABASE_URL no encontrada. Usando método alternativo...")
            # Intentar usar psycopg2 con los datos de Supabase
            database_url = f"postgresql://postgres:[password]@db.{url.split('//')[1].split('.')[0]}.supabase.co:5432/postgres"
            print("⚠️ Necesitarás configurar la contraseña de la base de datos manualmente")
            return False
        
        print("🔗 Conectando directamente a PostgreSQL...")
        
        # Conectar directamente a PostgreSQL
        conn = psycopg2.connect(database_url)
        conn.autocommit = True
        cursor = conn.cursor()
        
        print("✅ Conexión PostgreSQL establecida")
        
        # Crear tablas
        print("📋 Creando tablas...")
        for i, table_sql in enumerate(tables_sql, 1):
            try:
                cursor.execute(table_sql)
                table_name = table_sql.split('IF NOT EXISTS ')[1].split(' ')[0]
                print(f"   ✅ Tabla {i}: {table_name}")
            except Exception as e:
                print(f"   ❌ Error creando tabla {i}: {e}")
        
        # Crear índices
        print("🔍 Creando índices...")
        for i, index_sql in enumerate(indexes_sql, 1):
            try:
                cursor.execute(index_sql)
                print(f"   ✅ Índice {i} creado")
            except Exception as e:
                print(f"   ⚠️ Índice {i}: {e}")
        
        # Insertar configuración inicial
        print("⚙️ Configurando sistema...")
        for i, config in enumerate(config_sql, 1):
            try:
                cursor.execute(config)
                print(f"   ✅ Configuración {i} insertada")
            except Exception as e:
                print(f"   ⚠️ Config {i}: {e}")
        
        # Cerrar conexión
        cursor.close()
        conn.close()
        
        print("\n🎉 ¡Tablas de ARIA Super Base creadas exitosamente!")
        print("✅ La base de datos está lista para usar")
        
        return True
        
    except Exception as e:
        print(f"❌ Error creando tablas: {e}")
        print("\n💡 Pasos alternativos:")
        print("1. Ve a tu panel de Supabase")
        print("2. Abre el SQL Editor")
        print("3. Ejecuta el archivo database_schema.sql")
        return False

def verify_tables():
    """Verificar que las tablas se crearon correctamente"""
    print("\n🔍 Verificando tablas creadas...")
    
    url = os.getenv('SUPABASE_URL')
    key = os.getenv('SUPABASE_ANON_KEY')
    
    try:
        supabase = create_client(url, key)
        
        # Intentar hacer una consulta simple a cada tabla
        tables_to_check = [
            'aria_knowledge',
            'aria_api_relations', 
            'aria_conversations',
            'aria_learning_sessions',
            'aria_usage_stats',
            'aria_system_config'
        ]
        
        for table in tables_to_check:
            try:
                result = supabase.table(table).select("count", count="exact").execute()
                print(f"   ✅ {table}: {result.count} registros")
            except Exception as e:
                print(f"   ❌ {table}: {e}")
        
        print("\n✅ Verificación completada")
        return True
        
    except Exception as e:
        print(f"❌ Error verificando tablas: {e}")
        return False

def main():
    """Función principal"""
    print("🗄️ ARIA SUPER BASE - CREADOR DE TABLAS")
    print("="*50)
    
    if not DEPENDENCIES_OK:
        return False
    
    # Crear tablas
    success = create_aria_tables()
    
    if success:
        # Verificar que funcionan
        verify_tables()
        print("\n🚀 ¡ARIA Super Base está listo para usar!")
    else:
        print("\n⚠️ Revisa la configuración y vuelve a intentar")
    
    return success

if __name__ == "__main__":
    main()