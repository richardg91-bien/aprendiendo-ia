#!/usr/bin/env python3
"""
📊 CONFIGURADOR DE FUENTES DE DATOS PARA RAG
===========================================

Permite agregar y gestionar múltiples fuentes de datos:
- Bases de datos personalizadas
- APIs externas
- Documentos locales
- Fuentes web específicas
"""

import os
import json
import sqlite3
import requests
from datetime import datetime
from typing import Dict, List, Any, Optional
from pathlib import Path
import hashlib

class DataSourceManager:
    """Gestor de fuentes de datos para RAG"""
    
    def __init__(self, config_path: str = "config/data_sources.json"):
        self.config_path = config_path
        self.config_dir = Path(config_path).parent
        self.config_dir.mkdir(exist_ok=True)
        
        # Base de datos local para caché
        self.cache_db_path = self.config_dir / "data_cache.db"
        self.init_cache_database()
        
        # Cargar configuración existente
        self.sources_config = self.load_sources_config()
        
        print("📊 Gestor de fuentes de datos inicializado")
    
    def init_cache_database(self):
        """Inicializar base de datos de caché"""
        try:
            conn = sqlite3.connect(self.cache_db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS cached_data (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    source_id TEXT NOT NULL,
                    content_hash TEXT NOT NULL,
                    content TEXT NOT NULL,
                    metadata TEXT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    expires_at DATETIME,
                    access_count INTEGER DEFAULT 0
                )
            """)
            
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_source_hash 
                ON cached_data(source_id, content_hash)
            """)
            
            conn.commit()
            conn.close()
            print("✅ Base de datos de caché inicializada")
            
        except Exception as e:
            print(f"❌ Error inicializando caché: {e}")
    
    def load_sources_config(self) -> Dict:
        """Cargar configuración de fuentes"""
        try:
            if os.path.exists(self.config_path):
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            print(f"⚠️ Error cargando configuración: {e}")
        
        # Configuración por defecto
        return {
            "sources": [],
            "global_settings": {
                "cache_duration_hours": 24,
                "max_cache_size_mb": 100,
                "retry_attempts": 3,
                "timeout_seconds": 30
            }
        }
    
    def save_sources_config(self):
        """Guardar configuración de fuentes"""
        try:
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(self.sources_config, f, indent=2, ensure_ascii=False)
            print("✅ Configuración guardada")
        except Exception as e:
            print(f"❌ Error guardando configuración: {e}")
    
    def add_database_source(self, 
                           name: str, 
                           connection_string: str, 
                           query_template: str,
                           description: str = "") -> bool:
        """Agregar fuente de base de datos"""
        
        source_config = {
            "id": f"db_{len(self.sources_config['sources'])}",
            "name": name,
            "type": "database",
            "description": description,
            "config": {
                "connection_string": connection_string,
                "query_template": query_template,
                "batch_size": 100
            },
            "enabled": True,
            "created_at": datetime.now().isoformat()
        }
        
        self.sources_config["sources"].append(source_config)
        self.save_sources_config()
        
        print(f"✅ Fuente de BD agregada: {name}")
        return True
    
    def add_api_source(self, 
                      name: str, 
                      base_url: str, 
                      headers: Dict = None,
                      params_template: Dict = None,
                      description: str = "") -> bool:
        """Agregar fuente de API externa"""
        
        source_config = {
            "id": f"api_{len(self.sources_config['sources'])}",
            "name": name,
            "type": "api",
            "description": description,
            "config": {
                "base_url": base_url,
                "headers": headers or {},
                "params_template": params_template or {},
                "method": "GET",
                "response_path": "data"  # JSONPath para extraer datos
            },
            "enabled": True,
            "created_at": datetime.now().isoformat()
        }
        
        self.sources_config["sources"].append(source_config)
        self.save_sources_config()
        
        print(f"✅ Fuente de API agregada: {name}")
        return True
    
    def add_document_source(self, 
                           name: str, 
                           file_paths: List[str],
                           file_types: List[str] = None,
                           description: str = "") -> bool:
        """Agregar fuente de documentos locales"""
        
        file_types = file_types or ['.txt', '.md', '.pdf', '.docx']
        
        source_config = {
            "id": f"docs_{len(self.sources_config['sources'])}",
            "name": name,
            "type": "documents",
            "description": description,
            "config": {
                "file_paths": file_paths,
                "file_types": file_types,
                "chunk_size": 1000,
                "overlap_size": 200,
                "encoding": "utf-8"
            },
            "enabled": True,
            "created_at": datetime.now().isoformat()
        }
        
        self.sources_config["sources"].append(source_config)
        self.save_sources_config()
        
        print(f"✅ Fuente de documentos agregada: {name}")
        return True
    
    def add_web_source(self, 
                      name: str, 
                      urls: List[str],
                      selectors: Dict = None,
                      description: str = "") -> bool:
        """Agregar fuente web específica"""
        
        selectors = selectors or {
            "content": "p, div.content, article",
            "title": "h1, h2, .title",
            "exclude": ".ads, .sidebar, .comments"
        }
        
        source_config = {
            "id": f"web_{len(self.sources_config['sources'])}",
            "name": name,
            "type": "web",
            "description": description,
            "config": {
                "urls": urls,
                "selectors": selectors,
                "update_frequency": "daily",
                "respect_robots": True,
                "user_agent": "ARIA-RAG-Bot/1.0"
            },
            "enabled": True,
            "created_at": datetime.now().isoformat()
        }
        
        self.sources_config["sources"].append(source_config)
        self.save_sources_config()
        
        print(f"✅ Fuente web agregada: {name}")
        return True
    
    def query_source(self, source_id: str, query: str, limit: int = 10) -> List[Dict]:
        """Consultar una fuente específica"""
        
        source = self.get_source_by_id(source_id)
        if not source or not source.get('enabled', False):
            return []
        
        # Verificar caché primero
        cached_results = self.get_from_cache(source_id, query)
        if cached_results:
            return cached_results
        
        # Consultar fuente según tipo
        source_type = source.get('type')
        results = []
        
        try:
            if source_type == 'database':
                results = self._query_database_source(source, query, limit)
            elif source_type == 'api':
                results = self._query_api_source(source, query, limit)
            elif source_type == 'documents':
                results = self._query_document_source(source, query, limit)
            elif source_type == 'web':
                results = self._query_web_source(source, query, limit)
            
            # Guardar en caché
            if results:
                self.save_to_cache(source_id, query, results)
            
        except Exception as e:
            print(f"❌ Error consultando {source_id}: {e}")
        
        return results
    
    def _query_database_source(self, source: Dict, query: str, limit: int) -> List[Dict]:
        """Consultar fuente de base de datos"""
        # Implementación básica - requiere librerías específicas según BD
        results = []
        
        # Placeholder para diferentes tipos de BD
        connection_string = source['config']['connection_string']
        
        if 'sqlite' in connection_string.lower():
            results = self._query_sqlite(source, query, limit)
        elif 'postgresql' in connection_string.lower():
            results = self._query_postgresql(source, query, limit)
        
        return results
    
    def _query_sqlite(self, source: Dict, query: str, limit: int) -> List[Dict]:
        """Consultar SQLite"""
        results = []
        
        try:
            db_path = source['config']['connection_string'].replace('sqlite:///', '')
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            # Usar template de consulta
            query_template = source['config']['query_template']
            sql_query = query_template.replace('{query}', query).replace('{limit}', str(limit))
            
            cursor.execute(sql_query)
            rows = cursor.fetchall()
            
            # Convertir a diccionarios
            columns = [desc[0] for desc in cursor.description]
            for row in rows:
                result = dict(zip(columns, row))
                results.append({
                    'content': result.get('content', str(result)),
                    'metadata': {
                        'source': source['name'],
                        'type': 'database',
                        'raw_data': result
                    }
                })
            
            conn.close()
            
        except Exception as e:
            print(f"❌ Error SQLite: {e}")
        
        return results
    
    def _query_api_source(self, source: Dict, query: str, limit: int) -> List[Dict]:
        """Consultar fuente de API"""
        results = []
        
        try:
            config = source['config']
            url = config['base_url']
            headers = config.get('headers', {})
            
            # Preparar parámetros
            params = config.get('params_template', {}).copy()
            params['q'] = query
            params['limit'] = limit
            
            response = requests.get(
                url, 
                headers=headers, 
                params=params,
                timeout=self.sources_config['global_settings']['timeout_seconds']
            )
            
            if response.status_code == 200:
                data = response.json()
                
                # Extraer datos según response_path
                response_path = config.get('response_path', 'data')
                if response_path in data:
                    items = data[response_path]
                    
                    for item in items[:limit]:
                        results.append({
                            'content': item.get('content', str(item)),
                            'metadata': {
                                'source': source['name'],
                                'type': 'api',
                                'raw_data': item
                            }
                        })
            
        except Exception as e:
            print(f"❌ Error API: {e}")
        
        return results
    
    def _query_document_source(self, source: Dict, query: str, limit: int) -> List[Dict]:
        """Consultar documentos locales"""
        results = []
        
        try:
            config = source['config']
            file_paths = config['file_paths']
            file_types = config['file_types']
            
            query_words = set(query.lower().split())
            
            for file_path in file_paths:
                path = Path(file_path)
                
                if path.is_file() and path.suffix in file_types:
                    # Leer archivo
                    content = self._read_document_file(path, config)
                    
                    # Búsqueda simple por palabras clave
                    content_words = set(content.lower().split())
                    relevance = len(query_words & content_words) / len(query_words)
                    
                    if relevance > 0.1:  # Umbral mínimo
                        results.append({
                            'content': content[:1000] + "..." if len(content) > 1000 else content,
                            'metadata': {
                                'source': source['name'],
                                'type': 'document',
                                'file_path': str(path),
                                'relevance': relevance
                            }
                        })
                
                elif path.is_dir():
                    # Buscar en directorio
                    for file in path.rglob('*'):
                        if file.suffix in file_types and len(results) < limit:
                            content = self._read_document_file(file, config)
                            content_words = set(content.lower().split())
                            relevance = len(query_words & content_words) / len(query_words)
                            
                            if relevance > 0.1:
                                results.append({
                                    'content': content[:1000] + "..." if len(content) > 1000 else content,
                                    'metadata': {
                                        'source': source['name'],
                                        'type': 'document',
                                        'file_path': str(file),
                                        'relevance': relevance
                                    }
                                })
            
            # Ordenar por relevancia
            results.sort(key=lambda x: x['metadata']['relevance'], reverse=True)
            
        except Exception as e:
            print(f"❌ Error documentos: {e}")
        
        return results[:limit]
    
    def _read_document_file(self, file_path: Path, config: Dict) -> str:
        """Leer contenido de archivo"""
        try:
            encoding = config.get('encoding', 'utf-8')
            
            if file_path.suffix == '.txt' or file_path.suffix == '.md':
                with open(file_path, 'r', encoding=encoding) as f:
                    return f.read()
            
            # Para otros tipos, retornar placeholder
            return f"Contenido de {file_path.name} (tipo {file_path.suffix} no completamente soportado)"
            
        except Exception as e:
            return f"Error leyendo {file_path}: {e}"
    
    def _query_web_source(self, source: Dict, query: str, limit: int) -> List[Dict]:
        """Consultar fuente web"""
        results = []
        
        try:
            from bs4 import BeautifulSoup
            config = source['config']
            
            for url in config['urls'][:limit]:
                try:
                    headers = {'User-Agent': config.get('user_agent', 'ARIA-RAG-Bot/1.0')}
                    response = requests.get(url, headers=headers, timeout=30)
                    
                    if response.status_code == 200:
                        soup = BeautifulSoup(response.content, 'html.parser')
                        
                        # Extraer contenido según selectores
                        content_selector = config['selectors'].get('content', 'p')
                        content_elements = soup.select(content_selector)
                        
                        content = ' '.join([elem.get_text().strip() for elem in content_elements])
                        
                        # Verificar relevancia
                        if query.lower() in content.lower():
                            results.append({
                                'content': content[:1000] + "..." if len(content) > 1000 else content,
                                'metadata': {
                                    'source': source['name'],
                                    'type': 'web',
                                    'url': url,
                                    'title': soup.title.string if soup.title else 'Sin título'
                                }
                            })
                
                except Exception as e:
                    print(f"⚠️ Error procesando {url}: {e}")
        
        except ImportError:
            print("❌ BeautifulSoup no disponible para scraping web")
        except Exception as e:
            print(f"❌ Error web source: {e}")
        
        return results
    
    def get_source_by_id(self, source_id: str) -> Optional[Dict]:
        """Obtener fuente por ID"""
        for source in self.sources_config['sources']:
            if source['id'] == source_id:
                return source
        return None
    
    def list_sources(self) -> List[Dict]:
        """Listar todas las fuentes configuradas"""
        return self.sources_config['sources']
    
    def enable_source(self, source_id: str) -> bool:
        """Habilitar fuente"""
        source = self.get_source_by_id(source_id)
        if source:
            source['enabled'] = True
            self.save_sources_config()
            return True
        return False
    
    def disable_source(self, source_id: str) -> bool:
        """Deshabilitar fuente"""
        source = self.get_source_by_id(source_id)
        if source:
            source['enabled'] = False
            self.save_sources_config()
            return True
        return False
    
    def get_from_cache(self, source_id: str, query: str) -> Optional[List[Dict]]:
        """Obtener resultados del caché"""
        try:
            query_hash = hashlib.md5(query.encode()).hexdigest()
            
            conn = sqlite3.connect(self.cache_db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT content, metadata FROM cached_data 
                WHERE source_id = ? AND content_hash = ? 
                AND (expires_at IS NULL OR expires_at > datetime('now'))
            """, (source_id, query_hash))
            
            rows = cursor.fetchall()
            conn.close()
            
            if rows:
                results = []
                for content, metadata_json in rows:
                    metadata = json.loads(metadata_json) if metadata_json else {}
                    results.append({
                        'content': content,
                        'metadata': metadata
                    })
                return results
            
        except Exception as e:
            print(f"⚠️ Error accediendo caché: {e}")
        
        return None
    
    def save_to_cache(self, source_id: str, query: str, results: List[Dict]):
        """Guardar resultados en caché"""
        try:
            query_hash = hashlib.md5(query.encode()).hexdigest()
            
            conn = sqlite3.connect(self.cache_db_path)
            cursor = conn.cursor()
            
            # Calcular fecha de expiración
            cache_hours = self.sources_config['global_settings']['cache_duration_hours']
            expires_at = datetime.now().replace(microsecond=0)
            expires_at = expires_at.replace(hour=expires_at.hour + cache_hours)
            
            for result in results:
                cursor.execute("""
                    INSERT OR REPLACE INTO cached_data 
                    (source_id, content_hash, content, metadata, expires_at)
                    VALUES (?, ?, ?, ?, ?)
                """, (
                    source_id,
                    query_hash,
                    result['content'],
                    json.dumps(result.get('metadata', {})),
                    expires_at.isoformat()
                ))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            print(f"⚠️ Error guardando en caché: {e}")
    
    def clear_cache(self, source_id: str = None):
        """Limpiar caché"""
        try:
            conn = sqlite3.connect(self.cache_db_path)
            cursor = conn.cursor()
            
            if source_id:
                cursor.execute("DELETE FROM cached_data WHERE source_id = ?", (source_id,))
                print(f"✅ Caché limpiado para {source_id}")
            else:
                cursor.execute("DELETE FROM cached_data")
                print("✅ Todo el caché limpiado")
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            print(f"❌ Error limpiando caché: {e}")

# Función para crear configuración rápida
def setup_quick_rag_sources(manager: DataSourceManager):
    """Configuración rápida de fuentes RAG comunes"""
    
    print("🚀 Configurando fuentes RAG básicas...")
    
    # 1. Fuente de documentación técnica
    manager.add_document_source(
        name="Documentación Técnica",
        file_paths=["docs/", "README.md"],
        file_types=['.md', '.txt'],
        description="Documentación del proyecto y guías técnicas"
    )
    
    # 2. API de Wikipedia (ejemplo)
    manager.add_api_source(
        name="Wikipedia API",
        base_url="https://es.wikipedia.org/api/rest_v1/page/summary",
        description="Resúmenes de artículos de Wikipedia"
    )
    
    print("✅ Fuentes básicas configuradas")

if __name__ == "__main__":
    # Ejemplo de uso
    manager = DataSourceManager()
    setup_quick_rag_sources(manager)
    
    # Listar fuentes
    sources = manager.list_sources()
    print(f"\n📊 {len(sources)} fuentes configuradas:")
    for source in sources:
        status = "🟢" if source.get('enabled', False) else "🔴"
        print(f"{status} {source['name']} ({source['type']})")