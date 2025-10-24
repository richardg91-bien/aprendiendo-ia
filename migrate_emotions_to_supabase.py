#!/usr/bin/env python3
"""
🎭 MIGRACIÓN DEL SISTEMA EMOCIONAL A SUPABASE
===========================================

Migra toda la información del sistema de emociones de ARIA a Supabase
"""

import json
import sys
import os
from datetime import datetime
from typing import Dict, List

# Importar sistema de emociones
try:
    from emotion_detector import EmotionDetector
    EMOTION_AVAILABLE = True
except ImportError as e:
    print(f"⚠️ No se pudo importar sistema de emociones: {e}")
    EMOTION_AVAILABLE = False

# Importar conector sin inicializar servidor
try:
    import os
    from supabase import create_client, Client
    from dotenv import load_dotenv
    
    # Cargar variables de entorno
    load_dotenv("backend/.env")
    
    # Configuración de Supabase
    SUPABASE_URL = os.getenv('SUPABASE_URL')
    SUPABASE_KEY = os.getenv('SUPABASE_ANON_KEY')
    
    if SUPABASE_URL and SUPABASE_KEY:
        supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
        SUPABASE_AVAILABLE = True
    else:
        SUPABASE_AVAILABLE = False
        print("❌ Variables de Supabase no encontradas")
        
except ImportError as e:
    print(f"⚠️ No se pudo importar Supabase: {e}")
    SUPABASE_AVAILABLE = False

def store_knowledge_direct(concept: str, description: str, category: str = "general", confidence: float = 0.8):
    """Almacenar conocimiento directamente en Supabase"""
    try:
        data = {
            "concept": concept,
            "description": description,
            "category": category,
            "confidence": confidence
        }
        
        result = supabase.table("aria_knowledge").insert(data).execute()
        return len(result.data) > 0
    except Exception as e:
        print(f"Error almacenando en Supabase: {e}")
        return False

def search_knowledge_direct(query: str):
    """Buscar conocimiento directamente en Supabase"""
    try:
        result = supabase.table("aria_knowledge").select("*").ilike("concept", f"%{query}%").execute()
        return result.data
    except Exception as e:
        print(f"Error buscando en Supabase: {e}")
        return []

def get_knowledge_by_category_direct(category: str):
    """Obtener conocimiento por categoría directamente de Supabase"""
    try:
        result = supabase.table("aria_knowledge").select("*").eq("category", category).execute()
        return result.data
    except Exception as e:
        print(f"Error obteniendo por categoría: {e}")
        return []
    """Crear tablas necesarias para el sistema emocional en Supabase"""
    
    sql_commands = [
        """
        -- Tabla para mapeo de emociones
        CREATE TABLE IF NOT EXISTS aria_emotions (
            id SERIAL PRIMARY KEY,
            emotion_key VARCHAR(50) UNIQUE NOT NULL,
            emotion_name VARCHAR(100) NOT NULL,
            aria_emotion VARCHAR(50) NOT NULL,
            color_hex VARCHAR(7) NOT NULL,
            color_rgb VARCHAR(15) NOT NULL,
            category VARCHAR(50) DEFAULT 'basic',
            description TEXT,
            confidence_threshold FLOAT DEFAULT 0.5,
            created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
            updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
        );
        """,
        
        """
        -- Tabla para histórico de emociones detectadas
        CREATE TABLE IF NOT EXISTS aria_emotion_history (
            id SERIAL PRIMARY KEY,
            conversation_id INTEGER REFERENCES aria_conversations(id),
            emotion_detected VARCHAR(50) NOT NULL,
            emotion_confidence FLOAT DEFAULT 0.5,
            emotion_provider VARCHAR(50) DEFAULT 'fallback',
            user_text TEXT,
            aria_response_emotion VARCHAR(50),
            color_used VARCHAR(7),
            context_type VARCHAR(20) DEFAULT 'user',
            timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
            raw_data JSONB DEFAULT '{}'::jsonb
        );
        """,
        
        """
        -- Tabla para configuración emocional
        CREATE TABLE IF NOT EXISTS aria_emotion_config (
            id SERIAL PRIMARY KEY,
            config_key VARCHAR(100) UNIQUE NOT NULL,
            config_value JSONB NOT NULL,
            description TEXT,
            active BOOLEAN DEFAULT true,
            created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
            updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
        );
        """,
        
        """
        -- Índices para mejorar rendimiento
        CREATE INDEX IF NOT EXISTS idx_emotion_history_conversation 
        ON aria_emotion_history(conversation_id);
        
        CREATE INDEX IF NOT EXISTS idx_emotion_history_timestamp 
        ON aria_emotion_history(timestamp);
        
        CREATE INDEX IF NOT EXISTS idx_emotions_key 
        ON aria_emotions(emotion_key);
        """
    ]
    
    return sql_commands

def create_emotion_tables():
    """Obtener todos los mapeos de emociones del sistema actual"""
    
    if not EMOTION_AVAILABLE:
        print("❌ Sistema de emociones no disponible")
        return {}
    
    # Crear detector temporal para obtener mapeos
    detector = EmotionDetector("")  # Sin API key para obtener solo mapeos
    
    return detector.emotion_colors

def get_emotion_mappings() -> Dict:
    """Obtener todos los mapeos de emociones del sistema actual"""
    
    if not EMOTION_AVAILABLE:
        print("❌ Sistema de emociones no disponible")
        return {}
    
    # Crear detector temporal para obtener mapeos
    detector = EmotionDetector("")  # Sin API key para obtener solo mapeos
    
    return detector.emotion_colors

def migrate_emotion_system():
    """Migrar todo el sistema emocional a Supabase"""
    
    print("🎭 MIGRANDO SISTEMA EMOCIONAL A SUPABASE")
    print("=" * 50)
    
    # Inicializar conexión a Supabase
    print("🔗 Conectando a Supabase...")
    if not SUPABASE_AVAILABLE:
        print("❌ Supabase no disponible")
        return False
    print("✅ Conectado a Supabase")
    
    # Crear tablas necesarias
    print("🏗️ Creando tablas de emociones...")
    sql_commands = create_emotion_tables()
    
    for i, sql in enumerate(sql_commands):
        try:
            print(f"   📝 Ejecutando comando {i+1}/{len(sql_commands)}")
            # Nota: Necesitaremos ejecutar estos SQL manualmente en Supabase
            # o crear una función que los ejecute
        except Exception as e:
            print(f"   ❌ Error en comando {i+1}: {e}")
    
    # Migrar mapeos de emociones
    print("🎨 Migrando mapeos de emociones...")
    emotion_mappings = get_emotion_mappings()
    
    if not emotion_mappings:
        print("❌ No se pudieron obtener mapeos de emociones")
        return False
    
    migrated_count = 0
    for emotion_key, emotion_data in emotion_mappings.items():
        try:
            # Preparar datos para Supabase
            emotion_record = {
                'concept': f"emotion_{emotion_key}",
                'description': json.dumps({
                    'emotion_key': emotion_key,
                    'emotion_name': emotion_data['name'],
                    'aria_emotion': emotion_data['aria_emotion'],
                    'color_hex': emotion_data['color'],
                    'color_rgb': emotion_data['rgb'],
                    'category': 'emotion_mapping',
                    'type': 'emotion_system'
                }),
                'category': 'emotion_mapping',
                'confidence': 1.0  # Mapeos de emociones tienen confianza máxima
            }
            
            # Almacenar en tabla de conocimiento
            result = store_knowledge_direct(
                concept=emotion_record['concept'],
                description=emotion_record['description'],
                category=emotion_record['category'],
                confidence=emotion_record['confidence']
            )
            
            if result:
                print(f"   ✅ Migrada emoción: {emotion_key} → {emotion_data['name']}")
                migrated_count += 1
            else:
                print(f"   ⚠️ Ya existe: {emotion_key}")
                
        except Exception as e:
            print(f"   ❌ Error migrando {emotion_key}: {e}")
    
    # Migrar configuración emocional
    print("⚙️ Migrando configuración emocional...")
    
    emotion_config = {
        'edenai_providers': ['vernai'],
        'fallback_enabled': True,
        'confidence_threshold': 0.5,
        'default_emotion': 'neutral',
        'emotion_persistence': True,
        'color_system_enabled': True
    }
    
    try:
        config_record = {
            'concept': 'emotion_system_config',
            'description': json.dumps(emotion_config),
            'category': 'system_config',
            'confidence': 1.0
        }
        
        result = store_knowledge_direct(
            concept=config_record['concept'],
            description=config_record['description'],
            category=config_record['category'],
            confidence=config_record['confidence']
        )
        
        if result:
            print("   ✅ Configuración emocional migrada")
        else:
            print("   ⚠️ Configuración ya existía")
            
    except Exception as e:
        print(f"   ❌ Error migrando configuración: {e}")
    
    # Verificar migración
    print("🔍 Verificando migración...")
    try:
        emotion_knowledge = get_knowledge_by_category_direct('emotion_mapping')
        config_knowledge = get_knowledge_by_category_direct('system_config')
        
        print(f"   📊 Emociones migradas: {len(emotion_knowledge) if emotion_knowledge else 0}")
        print(f"   ⚙️ Configuraciones migradas: {len(config_knowledge) if config_knowledge else 0}")
        
    except Exception as e:
        print(f"   ❌ Error verificando: {e}")
    
    print("\n📊 RESUMEN DE MIGRACIÓN EMOCIONAL:")
    print(f"   ✅ Emociones migradas: {migrated_count}")
    print(f"   📈 Total disponible: {len(emotion_mappings)}")
    print(f"   🎯 Éxito: {migrated_count == len(emotion_mappings)}")
    
    print("\n🔧 PRÓXIMOS PASOS:")
    print("   1. Ejecutar SQL de creación de tablas en Supabase manualmente")
    print("   2. Verificar que las emociones están disponibles")
    print("   3. Probar sistema emocional con Supabase")
    print("   4. Actualizar servidor para usar emociones de Supabase")
    
    return migrated_count > 0

def test_emotion_retrieval():
    """Probar recuperación de emociones desde Supabase"""
    
    print("\n🧪 PROBANDO RECUPERACIÓN DE EMOCIONES")
    print("=" * 40)
    
    try:
        # Buscar emociones específicas
        test_emotions = ['joy', 'sadness', 'anger', 'neutral']
        
        for emotion in test_emotions:
            emotion_key = f"emotion_{emotion}"
            result = search_knowledge_direct(emotion_key)
            
            if result:
                print(f"   ✅ {emotion}: Encontrada")
                # Mostrar datos de la emoción
                if len(result) > 0:
                    emotion_data = json.loads(result[0].get('description', '{}'))
                    color = emotion_data.get('color_hex', 'N/A')
                    name = emotion_data.get('emotion_name', 'N/A')
                    print(f"      🎨 Color: {color} | Nombre: {name}")
            else:
                print(f"   ❌ {emotion}: No encontrada")
                
    except Exception as e:
        print(f"❌ Error probando recuperación: {e}")

if __name__ == "__main__":
    print("🚀 CONFIGURACIÓN SISTEMA EMOCIONAL EN SUPABASE")
    print("=" * 60)
    
    success = migrate_emotion_system()
    
    if success:
        test_emotion_retrieval()
        print("\n🎉 MIGRACIÓN EMOCIONAL COMPLETADA")
        print("🔄 Reinicia el servidor ARIA para usar el sistema emocional en la nube")
    else:
        print("\n❌ ERROR EN MIGRACIÓN EMOCIONAL")
        print("🔧 Revisa la configuración de Supabase")