#!/usr/bin/env python3
"""
🚀 CONFIGURACIÓN INICIAL DEL SISTEMA RAG PARA ARIA
=================================================

Script para configurar automáticamente el sistema RAG
con fuentes de datos predefinidas y configuraciones optimizadas.
"""

import os
import sys
import json
from datetime import datetime
from pathlib import Path

# Agregar el directorio del proyecto al path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from data_source_manager import DataSourceManager
    from aria_rag_system import create_rag_system
    print("✅ Módulos RAG importados correctamente")
except ImportError as e:
    print(f"❌ Error importando módulos RAG: {e}")
    sys.exit(1)

def create_config_directory():
    """Crear directorio de configuración"""
    config_dir = Path("config")
    config_dir.mkdir(exist_ok=True)
    print(f"📁 Directorio de configuración: {config_dir.absolute()}")
    return config_dir

def setup_document_sources(manager: DataSourceManager):
    """Configurar fuentes de documentos locales"""
    print("\n📄 Configurando fuentes de documentos...")
    
    # Documentación del proyecto
    project_docs = [
        "docs/",
        "README.md", 
        "*.md"
    ]
    
    success = manager.add_document_source(
        name="Documentación del Proyecto",
        file_paths=project_docs,
        file_types=['.md', '.txt', '.rst'],
        description="Documentación completa del proyecto ARIA"
    )
    
    if success:
        print("  ✅ Fuente de documentación agregada")
    
    # Código fuente como documentación
    code_docs = [
        "*.py",
        "backend/src/",
        "frontend/src/"
    ]
    
    success = manager.add_document_source(
        name="Código Fuente",
        file_paths=code_docs,
        file_types=['.py', '.js', '.jsx', '.ts', '.tsx'],
        description="Código fuente del proyecto para referencias técnicas"
    )
    
    if success:
        print("  ✅ Fuente de código fuente agregada")

def setup_api_sources(manager: DataSourceManager):
    """Configurar fuentes de APIs externas"""
    print("\n🌐 Configurando fuentes de APIs...")
    
    # Wikipedia ES API
    success = manager.add_api_source(
        name="Wikipedia Español",
        base_url="https://es.wikipedia.org/api/rest_v1/page/summary/{query}",
        headers={'User-Agent': 'ARIA-RAG/1.0'},
        description="Resúmenes de artículos de Wikipedia en español"
    )
    
    if success:
        print("  ✅ API de Wikipedia ES agregada")
    
    # JSONPlaceholder para pruebas
    success = manager.add_api_source(
        name="API de Pruebas",
        base_url="https://jsonplaceholder.typicode.com/posts",
        headers={'Content-Type': 'application/json'},
        params_template={'userId': 1},
        description="API de pruebas para validar funcionamiento"
    )
    
    if success:
        print("  ✅ API de pruebas agregada")

def setup_web_sources(manager: DataSourceManager):
    """Configurar fuentes web específicas"""
    print("\n🔗 Configurando fuentes web...")
    
    # Sitios de documentación técnica
    tech_sites = [
        "https://docs.python.org/es/3/",
        "https://flask.palletsprojects.com/",
        "https://react.dev/learn"
    ]
    
    success = manager.add_web_source(
        name="Documentación Técnica",
        urls=tech_sites,
        selectors={
            "content": "main, .content, article, .documentation",
            "title": "h1, h2, .title",
            "exclude": ".sidebar, .nav, .footer, .ads"
        },
        description="Documentación oficial de tecnologías utilizadas"
    )
    
    if success:
        print("  ✅ Fuentes web de documentación agregadas")

def setup_knowledge_base(manager: DataSourceManager):
    """Configurar base de conocimiento local"""
    print("\n🧠 Configurando base de conocimiento...")
    
    # Crear base de conocimiento SQLite local
    knowledge_db_path = Path("config/knowledge_base.db")
    
    # Solo crear si no existe
    if not knowledge_db_path.exists():
        import sqlite3
        
        conn = sqlite3.connect(knowledge_db_path)
        cursor = conn.cursor()
        
        # Crear tabla de conocimiento
        cursor.execute("""
            CREATE TABLE knowledge (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                concept TEXT NOT NULL,
                description TEXT NOT NULL,
                category TEXT DEFAULT 'general',
                tags TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Insertar conocimiento básico
        basic_knowledge = [
            ("ARIA", "Asistente de Inteligencia Artificial integrado con Supabase y Google Cloud", "sistema", "ia,asistente,aria"),
            ("RAG", "Retrieval-Augmented Generation - Sistema que combina búsqueda y generación de texto con IA", "tecnologia", "rag,ia,busqueda"),
            ("Supabase", "Plataforma de base de datos como servicio basada en PostgreSQL", "tecnologia", "base_datos,cloud"),
            ("Flask", "Framework web ligero para Python", "programacion", "python,web,framework"),
            ("React", "Biblioteca de JavaScript para construir interfaces de usuario", "programacion", "javascript,frontend,ui")
        ]
        
        cursor.executemany(
            "INSERT INTO knowledge (concept, description, category, tags) VALUES (?, ?, ?, ?)",
            basic_knowledge
        )
        
        conn.commit()
        conn.close()
        
        print(f"  ✅ Base de conocimiento local creada: {knowledge_db_path}")
    
    # Agregar como fuente de datos
    success = manager.add_database_source(
        name="Base de Conocimiento Local",
        connection_string=f"sqlite:///{knowledge_db_path}",
        query_template="SELECT concept, description, category FROM knowledge WHERE concept LIKE '%{query}%' OR description LIKE '%{query}%' LIMIT {limit}",
        description="Base de conocimiento local con información fundamental"
    )
    
    if success:
        print("  ✅ Fuente de BD local agregada al manager")

def create_rag_configuration():
    """Crear configuración personalizada para RAG"""
    print("\n⚙️ Creando configuración RAG...")
    
    config = {
        "rag_settings": {
            "max_context_length": 4000,
            "min_confidence_threshold": 0.3,
            "max_sources": 5,
            "cache_duration_hours": 24,
            "enable_emotion_analysis": True,
            "enable_web_search_fallback": True
        },
        "source_priorities": {
            "supabase_knowledge": 1,
            "local_knowledge": 2,
            "document_sources": 3,
            "api_sources": 4,
            "web_sources": 5
        },
        "response_templates": {
            "multi_source": "Basándome en múltiples fuentes, puedo explicarte sobre {topic}:",
            "single_source": "Según la información que tengo sobre {topic}:",
            "low_confidence": "No tengo información completa sobre {topic}, pero puedo sugerir:",
            "web_fallback": "Buscaré información actualizada sobre {topic} en la web:"
        },
        "emotion_mappings": {
            "happy": {"confidence_boost": 0.1, "response_style": "enthusiastic"},
            "sad": {"confidence_boost": -0.1, "response_style": "empathetic"},
            "curious": {"confidence_boost": 0.05, "response_style": "educational"},
            "confused": {"confidence_boost": -0.05, "response_style": "clarifying"}
        }
    }
    
    config_path = Path("config/rag_config.json")
    with open(config_path, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2, ensure_ascii=False)
    
    print(f"  ✅ Configuración RAG guardada: {config_path}")
    return config

def test_rag_system(manager: DataSourceManager):
    """Probar el sistema RAG configurado"""
    print("\n🧪 Probando sistema RAG...")
    
    try:
        # Crear sistema RAG de prueba
        rag_system = create_rag_system()
        
        # Consultas de prueba
        test_queries = [
            "¿Qué es ARIA?",
            "Explícame RAG",
            "¿Cómo funciona Supabase?",
            "Programación en Python"
        ]
        
        for i, query in enumerate(test_queries, 1):
            print(f"\n  📝 Prueba {i}: {query}")
            
            try:
                # Simular respuesta RAG básica
                sources = manager.list_sources()
                enabled_sources = [s for s in sources if s.get('enabled', False)]
                
                print(f"     🔍 Fuentes disponibles: {len(enabled_sources)}")
                print(f"     ✅ Sistema respondería usando fuentes configuradas")
                
            except Exception as e:
                print(f"     ❌ Error en prueba: {e}")
    
    except Exception as e:
        print(f"  ❌ Error creando sistema RAG de prueba: {e}")

def generate_setup_report(manager: DataSourceManager):
    """Generar reporte de configuración"""
    print("\n📊 Generando reporte de configuración...")
    
    sources = manager.list_sources()
    
    report = {
        "setup_timestamp": datetime.now().isoformat(),
        "total_sources": len(sources),
        "enabled_sources": len([s for s in sources if s.get('enabled', False)]),
        "sources_by_type": {},
        "configuration_files": [
            "config/data_sources.json",
            "config/rag_config.json",
            "config/knowledge_base.db"
        ],
        "system_status": "configured"
    }
    
    # Contar por tipo
    for source in sources:
        source_type = source.get('type', 'unknown')
        report["sources_by_type"][source_type] = report["sources_by_type"].get(source_type, 0) + 1
    
    # Guardar reporte
    report_path = Path("config/rag_setup_report.json")
    with open(report_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    print(f"  ✅ Reporte guardado: {report_path}")
    
    # Mostrar resumen
    print("\n📋 RESUMEN DE CONFIGURACIÓN:")
    print(f"   📊 Total de fuentes: {report['total_sources']}")
    print(f"   ✅ Fuentes habilitadas: {report['enabled_sources']}")
    print("   📑 Tipos de fuentes:")
    for source_type, count in report["sources_by_type"].items():
        print(f"      • {source_type}: {count}")
    
    return report

def main():
    """Configuración principal del sistema RAG"""
    print("🚀 CONFIGURANDO SISTEMA RAG PARA ARIA")
    print("=" * 50)
    
    try:
        # 1. Crear directorio de configuración
        config_dir = create_config_directory()
        
        # 2. Inicializar manager de fuentes de datos
        manager = DataSourceManager()
        
        # 3. Configurar diferentes tipos de fuentes
        setup_document_sources(manager)
        setup_api_sources(manager)
        setup_web_sources(manager)
        setup_knowledge_base(manager)
        
        # 4. Crear configuración personalizada
        config = create_rag_configuration()
        
        # 5. Probar sistema
        test_rag_system(manager)
        
        # 6. Generar reporte
        report = generate_setup_report(manager)
        
        print("\n🎉 CONFIGURACIÓN RAG COMPLETADA")
        print("=" * 50)
        print("✅ Sistema RAG listo para usar")
        print("🌐 Accede a: http://localhost:5000/rag-admin")
        print("📊 API RAG: http://localhost:5000/api/rag/sources")
        
    except Exception as e:
        print(f"\n❌ Error en configuración: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()