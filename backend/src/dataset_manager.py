"""
Sistema de Gestión de Datasets para ARIA
Maneja la descarga, procesamiento y almacenamiento de datasets de entrenamiento
"""

import os
import zipfile
import tarfile
import gzip
import json
import requests
from pathlib import Path
from urllib.parse import urlparse
from tqdm import tqdm
import hashlib
from datetime import datetime
import logging

class DatasetManager:
    def __init__(self, base_path="backend/modelo_neuronal/data"):
        self.base_path = Path(base_path)
        self.base_path.mkdir(parents=True, exist_ok=True)
        
        # Configurar directorios
        self.datasets_config = {
            "voz": {
                "path": self.base_path / "voz",
                "commonvoice": self.base_path / "voz" / "commonvoice",
                "processed": self.base_path / "voz" / "processed"
            },
            "texto": {
                "path": self.base_path / "texto",
                "oscar": self.base_path / "texto" / "oscar",
                "processed": self.base_path / "texto" / "processed"
            },
            "dialogos": {
                "path": self.base_path / "dialogos",
                "dailydialog": self.base_path / "dialogos" / "dailydialog",
                "processed": self.base_path / "dialogos" / "processed"
            }
        }
        
        # Crear directorios
        self._create_directories()
        
        # Configurar logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        
        print("📂 Gestor de Datasets inicializado")
    
    def _create_directories(self):
        """Crear estructura de directorios"""
        for dataset_type, paths in self.datasets_config.items():
            for path in paths.values():
                path.mkdir(parents=True, exist_ok=True)
    
    def check_disk_space(self, required_gb=250):
        """Verificar espacio disponible en disco"""
        import shutil
        total, used, free = shutil.disk_usage(self.base_path)
        free_gb = free // (1024**3)
        
        print(f"💾 Espacio libre: {free_gb} GB")
        print(f"📊 Espacio requerido: {required_gb} GB")
        
        if free_gb < required_gb:
            print(f"⚠️  ADVERTENCIA: Espacio insuficiente!")
            print(f"   Necesitas al menos {required_gb - free_gb} GB adicionales")
            return False
        
        print("✅ Espacio suficiente disponible")
        return True
    
    def download_file(self, url, destination, chunk_size=8192):
        """Descargar archivo con barra de progreso"""
        try:
            response = requests.get(url, stream=True)
            total_size = int(response.headers.get('content-length', 0))
            
            destination = Path(destination)
            destination.parent.mkdir(parents=True, exist_ok=True)
            
            with open(destination, 'wb') as file:
                with tqdm(
                    desc=f"Descargando {destination.name}",
                    total=total_size,
                    unit='B',
                    unit_scale=True,
                    unit_divisor=1024,
                ) as pbar:
                    for chunk in response.iter_content(chunk_size=chunk_size):
                        if chunk:
                            file.write(chunk)
                            pbar.update(len(chunk))
            
            print(f"✅ Descargado: {destination}")
            return True
            
        except Exception as e:
            print(f"❌ Error descargando {url}: {e}")
            return False
    
    def extract_archive(self, archive_path, destination):
        """Extraer archivo comprimido"""
        archive_path = Path(archive_path)
        destination = Path(destination)
        
        try:
            if archive_path.suffix.lower() == '.zip':
                with zipfile.ZipFile(archive_path, 'r') as zip_ref:
                    zip_ref.extractall(destination)
            
            elif archive_path.suffix.lower() in ['.tar', '.tar.gz', '.tgz']:
                with tarfile.open(archive_path, 'r:*') as tar_ref:
                    tar_ref.extractall(destination)
            
            elif archive_path.suffix.lower() == '.gz':
                with gzip.open(archive_path, 'rb') as gz_file:
                    output_path = destination / archive_path.stem
                    with open(output_path, 'wb') as output_file:
                        output_file.write(gz_file.read())
            
            print(f"✅ Extraído: {archive_path} -> {destination}")
            return True
            
        except Exception as e:
            print(f"❌ Error extrayendo {archive_path}: {e}")
            return False
    
    def get_commonvoice_info(self):
        """Obtener información sobre Common Voice"""
        info = {
            "name": "Mozilla Common Voice",
            "description": "Dataset de voz crowdsourced en múltiples idiomas",
            "spanish_version": "Corpus validado en español",
            "estimated_size": "15-30 GB comprimido, 100+ GB descomprimido",
            "url": "https://commonvoice.mozilla.org/es/datasets",
            "format": "TSV + MP3 files",
            "recommended": True,
            "download_steps": [
                "1. Ir a https://commonvoice.mozilla.org/es/datasets",
                "2. Crear cuenta gratuita",
                "3. Seleccionar 'Español' en idioma",
                "4. Descargar 'Corpus validado'",
                "5. Extraer en backend/modelo_neuronal/data/voz/commonvoice/"
            ]
        }
        return info
    
    def get_oscar_info(self):
        """Obtener información sobre OSCAR"""
        info = {
            "name": "OSCAR (Open Super-large Crawled ALMAnaCH coRpus)",
            "description": "Corpus masivo de texto web en múltiples idiomas",
            "spanish_version": "OSCAR 2023 - Spanish subset",
            "estimated_size": "50-200 GB según versión",
            "url": "https://oscar-project.github.io/",
            "format": "JSONL o texto plano",
            "recommended": False,  # Muy grande para empezar
            "download_steps": [
                "1. Ir a https://huggingface.co/datasets/oscar-corpus/OSCAR-2301",
                "2. Seleccionar subset español (es)",
                "3. Descargar versión 'small' para empezar",
                "4. Extraer en backend/modelo_neuronal/data/texto/oscar/"
            ],
            "alternatives": [
                "Wikipedia español (más manejable)",
                "CC-News español",
                "Texto de Common Crawl filtrado"
            ]
        }
        return info
    
    def get_dailydialog_info(self):
        """Obtener información sobre DailyDialog"""
        info = {
            "name": "DailyDialog",
            "description": "Dataset de conversaciones cotidianas en inglés",
            "spanish_version": "No disponible, solo inglés",
            "estimated_size": "~50 MB",
            "url": "https://yanran.li/dailydialog",
            "format": "TXT files con diálogos",
            "recommended": True,
            "download_steps": [
                "1. Ir a https://yanran.li/dailydialog",
                "2. Descargar 'DailyDialog dataset'",
                "3. Extraer en backend/modelo_neuronal/data/dialogos/dailydialog/"
            ],
            "note": "Está en inglés, pero útil para estructura de diálogos"
        }
        return info
    
    def show_dataset_analysis(self):
        """Mostrar análisis completo de datasets"""
        print("=" * 60)
        print("📊 ANÁLISIS DE DATASETS PROPUESTOS")
        print("=" * 60)
        
        datasets = [
            ("Common Voice", self.get_commonvoice_info()),
            ("OSCAR", self.get_oscar_info()),
            ("DailyDialog", self.get_dailydialog_info())
        ]
        
        for name, info in datasets:
            print(f"\n🔍 {name}")
            print("-" * 40)
            print(f"📝 Descripción: {info['description']}")
            print(f"💾 Tamaño estimado: {info['estimated_size']}")
            print(f"📊 Formato: {info['format']}")
            print(f"✅ Recomendado: {'Sí' if info['recommended'] else 'No'}")
            
            if 'note' in info:
                print(f"📌 Nota: {info['note']}")
            
            if 'alternatives' in info:
                print(f"🔄 Alternativas: {', '.join(info['alternatives'])}")
    
    def create_sample_datasets(self):
        """Crear datasets de muestra para pruebas"""
        print("🧪 Creando datasets de muestra para desarrollo...")
        
        # Dataset de voz simulado
        voz_sample = self.datasets_config["voz"]["processed"] / "sample_voice.json"
        voice_data = {
            "metadata": {
                "total_samples": 100,
                "sample_rate": 16000,
                "format": "wav"
            },
            "samples": [
                {
                    "audio_file": f"sample_{i:03d}.wav",
                    "transcript": f"Texto de ejemplo número {i}",
                    "duration": 2.5,
                    "speaker_id": f"speaker_{i%10}"
                }
                for i in range(100)
            ]
        }
        
        with open(voz_sample, 'w', encoding='utf-8') as f:
            json.dump(voice_data, f, indent=2, ensure_ascii=False)
        
        # Dataset de texto simulado
        texto_sample = self.datasets_config["texto"]["processed"] / "sample_text.json"
        text_data = {
            "metadata": {
                "total_sentences": 1000,
                "language": "es"
            },
            "sentences": [
                f"Esta es una oración de ejemplo número {i} para entrenar el modelo de lenguaje."
                for i in range(1000)
            ]
        }
        
        with open(texto_sample, 'w', encoding='utf-8') as f:
            json.dump(text_data, f, indent=2, ensure_ascii=False)
        
        # Dataset de diálogos simulado
        dialogos_sample = self.datasets_config["dialogos"]["processed"] / "sample_dialogs.json"
        dialog_data = {
            "metadata": {
                "total_dialogs": 50,
                "language": "es"
            },
            "dialogs": [
                {
                    "dialog_id": f"dialog_{i:03d}",
                    "turns": [
                        {"speaker": "user", "text": f"Hola, ¿cómo estás? Pregunta {i}"},
                        {"speaker": "assistant", "text": f"Hola, estoy bien gracias. Respuesta {i}"},
                        {"speaker": "user", "text": f"¿Puedes ayudarme con algo? Consulta {i}"},
                        {"speaker": "assistant", "text": f"Por supuesto, ¿en qué puedo ayudarte? Asistencia {i}"}
                    ]
                }
                for i in range(50)
            ]
        }
        
        with open(dialogos_sample, 'w', encoding='utf-8') as f:
            json.dump(dialog_data, f, indent=2, ensure_ascii=False)
        
        print("✅ Datasets de muestra creados")
        print(f"📂 Voz: {voz_sample}")
        print(f"📂 Texto: {texto_sample}")
        print(f"📂 Diálogos: {dialogos_sample}")
    
    def get_current_status(self):
        """Obtener estado actual de datasets"""
        status = {}
        
        for dataset_type, paths in self.datasets_config.items():
            status[dataset_type] = {}
            
            for path_name, path in paths.items():
                if path_name == "path":
                    continue
                    
                files = list(path.glob("*")) if path.exists() else []
                status[dataset_type][path_name] = {
                    "exists": path.exists(),
                    "file_count": len(files),
                    "size_mb": self._get_directory_size(path) if path.exists() else 0
                }
        
        return status
    
    def _get_directory_size(self, path):
        """Calcular tamaño de directorio en MB"""
        try:
            total_size = sum(f.stat().st_size for f in path.rglob('*') if f.is_file())
            return round(total_size / (1024 * 1024), 2)
        except:
            return 0
    
    def show_status_report(self):
        """Mostrar reporte de estado"""
        print("=" * 60)
        print("📊 ESTADO ACTUAL DE DATASETS")
        print("=" * 60)
        
        status = self.get_current_status()
        
        for dataset_type, paths in status.items():
            print(f"\n📁 {dataset_type.upper()}")
            print("-" * 30)
            
            for path_name, info in paths.items():
                icon = "✅" if info["exists"] else "❌"
                print(f"{icon} {path_name}: {info['file_count']} archivos, {info['size_mb']} MB")

# Instancia global del gestor
dataset_manager = DatasetManager()

if __name__ == "__main__":
    # Mostrar análisis y estado
    dataset_manager.show_dataset_analysis()
    dataset_manager.show_status_report()
    
    # Verificar espacio
    dataset_manager.check_disk_space()
    
    # Crear datasets de muestra
    dataset_manager.create_sample_datasets()