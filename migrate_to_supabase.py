#!/usr/bin/env python3
"""
📊 MIGRAR CONOCIMIENTO GEOGRÁFICO A SUPABASE
===========================================

Transferir todo el conocimiento de la base de datos local a Supabase
para que el sistema RAG use Supabase como fuente principal.
"""

import os
import sys
import sqlite3
from datetime import datetime
from pathlib import Path

# Agregar el directorio del proyecto al path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def migrate_local_knowledge_to_supabase():
    """Migrar conocimiento de SQLite local a Supabase"""
    
    print("📊 MIGRANDO CONOCIMIENTO LOCAL A SUPABASE")
    print("=" * 50)
    
    try:
        # Conectar a la base de datos local
        db_path = Path("config/knowledge_base.db")
        if not db_path.exists():
            print("❌ Base de datos local no encontrada")
            return False
        
        # Conectar a Supabase
        from aria_enhanced_connector import get_enhanced_connector
        cloud_connector = get_enhanced_connector()
        print("✅ Conectado a Supabase")
        
        # Leer conocimiento local
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT concept, description, category, tags, created_at, updated_at
            FROM knowledge
        """)
        
        local_knowledge = cursor.fetchall()
        conn.close()
        
        print(f"📚 Conocimiento local encontrado: {len(local_knowledge)} entradas")
        
        # Obtener conocimiento actual de Supabase
        current_supabase_knowledge = cloud_connector.get_knowledge()
        existing_concepts = {item.get('concept', '').lower() for item in current_supabase_knowledge}
        
        print(f"📊 Conocimiento actual en Supabase: {len(current_supabase_knowledge)} entradas")
        
        # Migrar cada entrada
        migrated_count = 0
        skipped_count = 0
        
        for concept, description, category, tags, created_at, updated_at in local_knowledge:
            
            # Verificar si ya existe en Supabase
            if concept.lower() in existing_concepts:
                print(f"  ⚠️ Ya existe en Supabase: {concept}")
                skipped_count += 1
                continue
            
            try:
                # Agregar a Supabase usando el método correcto
                success = cloud_connector.store_knowledge(
                    concept=concept,
                    description=description,
                    category=category or 'general',
                    confidence=0.9  # Alta confianza para datos migrados
                )
                
                if success:
                    print(f"  ✅ Migrado: {concept} ({category})")
                    migrated_count += 1
                else:
                    print(f"  ❌ Error migrando: {concept}")
            
            except Exception as e:
                print(f"  ❌ Error con {concept}: {e}")
        
        print(f"\n📊 RESUMEN DE MIGRACIÓN:")
        print(f"   ✅ Entradas migradas: {migrated_count}")
        print(f"   ⚠️ Ya existían: {skipped_count}")
        print(f"   📈 Total en local: {len(local_knowledge)}")
        
        # Verificar estado final de Supabase
        final_supabase_knowledge = cloud_connector.get_knowledge()
        print(f"   🎯 Total final en Supabase: {len(final_supabase_knowledge)}")
        
        return migrated_count > 0
        
    except Exception as e:
        print(f"❌ Error en migración: {e}")
        import traceback
        traceback.print_exc()
        return False

def verify_geographic_knowledge_in_supabase():
    """Verificar que el conocimiento geográfico esté en Supabase"""
    
    print("\n🔍 VERIFICANDO CONOCIMIENTO GEOGRÁFICO EN SUPABASE")
    print("=" * 55)
    
    try:
        from aria_enhanced_connector import get_enhanced_connector
        cloud_connector = get_enhanced_connector()
        
        # Obtener todo el conocimiento
        all_knowledge = cloud_connector.get_knowledge()
        
        # Buscar conocimiento geográfico
        geographic_keywords = ['roma', 'italia', 'imperio romano', 'coliseo', 'vaticano', 'paris', 'madrid', 'londres']
        
        geographic_knowledge = []
        for item in all_knowledge:
            concept = item.get('concept', '').lower()
            description = item.get('description', '').lower()
            
            for keyword in geographic_keywords:
                if keyword in concept or keyword in description:
                    geographic_knowledge.append(item)
                    break
        
        print(f"📍 Conocimiento geográfico en Supabase: {len(geographic_knowledge)} entradas")
        
        # Mostrar las entradas encontradas
        categories = {}
        for item in geographic_knowledge:
            concept = item.get('concept', 'Sin concepto')
            category = item.get('category', 'general')
            
            if category not in categories:
                categories[category] = []
            categories[category].append(concept)
        
        print("\n📑 Por categorías:")
        for category, concepts in categories.items():
            print(f"   🏷️ {category}: {len(concepts)} entradas")
            for concept in concepts[:3]:  # Mostrar solo las primeras 3
                print(f"      • {concept}")
            if len(concepts) > 3:
                print(f"      ... y {len(concepts) - 3} más")
        
        # Verificar conocimiento específico sobre Roma
        roma_knowledge = [item for item in all_knowledge 
                         if 'roma' in item.get('concept', '').lower() 
                         or 'roma' in item.get('description', '').lower()]
        
        print(f"\n🏛️ Conocimiento específico sobre Roma: {len(roma_knowledge)} entradas")
        for item in roma_knowledge:
            print(f"   • {item.get('concept', 'Sin concepto')} ({item.get('category', 'general')})")
        
        return len(geographic_knowledge) > 0
        
    except Exception as e:
        print(f"❌ Error verificando Supabase: {e}")
        return False

def update_rag_system_to_prioritize_supabase():
    """Actualizar el sistema RAG para priorizar Supabase"""
    
    print("\n🔧 CONFIGURANDO RAG PARA PRIORIZAR SUPABASE")
    print("=" * 50)
    
    try:
        # Leer la configuración RAG actual
        config_path = Path("config/rag_config.json")
        
        if config_path.exists():
            import json
            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
        else:
            config = {}
        
        # Actualizar prioridades para favorecer Supabase
        config["source_priorities"] = {
            "supabase_knowledge": 1,      # Máxima prioridad
            "local_knowledge_db": 2,      # Segunda prioridad
            "conversation_memory": 3,     # Memoria conversacional
            "document_sources": 4,        # Documentos locales
            "api_sources": 5,             # APIs externas
            "web_sources": 6,             # Fuentes web
            "local_knowledge_fallback": 7 # Fallback local
        }
        
        # Configurar umbral de confianza más bajo para Supabase
        config["rag_settings"] = config.get("rag_settings", {})
        config["rag_settings"]["supabase_confidence_threshold"] = 0.2  # Más permisivo
        config["rag_settings"]["local_db_confidence_threshold"] = 0.3
        config["rag_settings"]["fallback_confidence_threshold"] = 0.5
        
        # Configurar búsqueda más agresiva en Supabase
        config["supabase_search"] = {
            "use_fuzzy_matching": True,
            "search_in_description": True,
            "search_in_category": True,
            "max_results": 10,
            "boost_exact_matches": 0.3
        }
        
        # Guardar configuración actualizada
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        
        print("✅ Configuración RAG actualizada")
        print("   🎯 Supabase: Prioridad máxima")
        print("   📊 Umbral de confianza reducido")
        print("   🔍 Búsqueda fuzzy habilitada")
        
        return True
        
    except Exception as e:
        print(f"❌ Error actualizando configuración: {e}")
        return False

def test_supabase_knowledge_access():
    """Probar acceso al conocimiento de Supabase"""
    
    print("\n🧪 PROBANDO ACCESO A CONOCIMIENTO SUPABASE")
    print("=" * 45)
    
    try:
        from aria_enhanced_connector import get_enhanced_connector
        cloud_connector = get_enhanced_connector()
        
        # Consultas de prueba
        test_queries = ['roma', 'italia', 'imperio romano', 'amor', 'inteligencia artificial']
        
        for query in test_queries:
            print(f"\n🔍 Probando: '{query}'")
            
            # Obtener todo el conocimiento
            all_knowledge = cloud_connector.get_knowledge()
            
            # Buscar coincidencias
            matches = []
            for item in all_knowledge:
                concept = item.get('concept', '').lower()
                description = item.get('description', '').lower()
                
                if query.lower() in concept or query.lower() in description:
                    relevance = 1.0 if query.lower() in concept else 0.5
                    matches.append((item, relevance))
            
            matches.sort(key=lambda x: x[1], reverse=True)
            
            print(f"   📊 Resultados: {len(matches)}")
            for item, relevance in matches[:3]:
                concept = item.get('concept', 'Sin concepto')
                category = item.get('category', 'general')
                print(f"   • {concept} ({category}) - relevancia: {relevance}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error probando Supabase: {e}")
        return False

def main():
    """Función principal"""
    
    print("🚀 CONFIGURANDO SUPABASE COMO FUENTE PRINCIPAL RAG")
    print("=" * 60)
    
    try:
        # 1. Migrar conocimiento local a Supabase
        migration_success = migrate_local_knowledge_to_supabase()
        
        # 2. Verificar conocimiento geográfico en Supabase
        verification_success = verify_geographic_knowledge_in_supabase()
        
        # 3. Actualizar configuración RAG
        config_success = update_rag_system_to_prioritize_supabase()
        
        # 4. Probar acceso a Supabase
        test_success = test_supabase_knowledge_access()
        
        print(f"\n🎯 RESUMEN DE CONFIGURACIÓN:")
        print(f"   📊 Migración: {'✅' if migration_success else '❌'}")
        print(f"   🔍 Verificación: {'✅' if verification_success else '❌'}")
        print(f"   ⚙️ Configuración: {'✅' if config_success else '❌'}")
        print(f"   🧪 Pruebas: {'✅' if test_success else '❌'}")
        
        if all([verification_success, config_success, test_success]):
            print("\n🎉 SUPABASE CONFIGURADO COMO FUENTE PRINCIPAL")
            print("✅ El sistema RAG ahora usará Supabase primero")
            print("🏛️ Conocimiento geográfico disponible en la nube")
            print("🚀 Reinicia el servidor para aplicar cambios")
        else:
            print("\n⚠️ Algunas configuraciones fallaron")
            
    except Exception as e:
        print(f"\n❌ Error general: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()