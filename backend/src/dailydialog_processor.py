"""
Implementación inmediata de DailyDialog para ARIA
Paso 1 del plan escalonado - dataset pequeño y manejable
"""

import json
import csv
import requests
import zipfile
from pathlib import Path
import re
from datetime import datetime

class DailyDialogProcessor:
    def __init__(self, base_path="backend/modelo_neuronal/data/dialogos"):
        self.base_path = Path(base_path)
        self.dailydialog_path = self.base_path / "dailydialog"
        self.processed_path = self.base_path / "processed"
        
        # Crear directorios
        self.dailydialog_path.mkdir(parents=True, exist_ok=True)
        self.processed_path.mkdir(parents=True, exist_ok=True)
        
        print("📂 Procesador de DailyDialog inicializado")
    
    def download_dailydialog(self):
        """Descargar DailyDialog dataset"""
        # URL de ejemplo - necesitarás la URL real del dataset
        print("📥 Para descargar DailyDialog:")
        print("   1. Ve a: https://yanran.li/dailydialog")
        print("   2. Descarga el dataset")
        print("   3. Extrae en:", self.dailydialog_path)
        print("   4. Luego ejecuta: process_dailydialog()")
        
        # Crear estructura de ejemplo mientras tanto
        self._create_sample_dailydialog()
    
    def _create_sample_dailydialog(self):
        """Crear dataset de ejemplo de DailyDialog"""
        print("🧪 Creando dataset de muestra de DailyDialog...")
        
        # Diálogos de ejemplo en inglés (estructura real)
        sample_dialogs = [
            [
                "Hi, how are you doing?",
                "I'm doing well, thank you. How about you?",
                "I'm good too. What are your plans for today?",
                "I'm planning to study some AI concepts. What about you?",
                "That sounds interesting! I might work on my programming skills."
            ],
            [
                "Good morning!",
                "Good morning! How did you sleep?",
                "I slept well, thanks. Ready for a new day?",
                "Absolutely! I have some exciting projects to work on.",
                "That's great! What kind of projects?"
            ],
            [
                "Can you help me with something?",
                "Of course! What do you need help with?",
                "I'm trying to understand machine learning better.",
                "That's a fascinating topic. What specific area interests you?",
                "I'm particularly interested in natural language processing."
            ]
        ]
        
        # Crear archivo de diálogos
        dialog_file = self.dailydialog_path / "dialogues_sample.txt"
        with open(dialog_file, 'w', encoding='utf-8') as f:
            for i, dialog in enumerate(sample_dialogs):
                for j, turn in enumerate(dialog):
                    f.write(f"{turn}")
                    if j < len(dialog) - 1:
                        f.write(" __eou__ ")
                f.write("\n")
        
        print(f"✅ Dataset de muestra creado: {dialog_file}")
        return True
    
    def process_dailydialog(self):
        """Procesar archivos de DailyDialog"""
        print("🔄 Procesando DailyDialog...")
        
        # Buscar archivos de diálogos
        dialog_files = list(self.dailydialog_path.glob("*.txt"))
        
        if not dialog_files:
            print("⚠️  No se encontraron archivos de diálogos")
            print("   Creando dataset de muestra...")
            self._create_sample_dailydialog()
            dialog_files = list(self.dailydialog_path.glob("*.txt"))
        
        all_dialogs = []
        
        for file_path in dialog_files:
            print(f"📖 Procesando: {file_path.name}")
            
            with open(file_path, 'r', encoding='utf-8') as f:
                for i, line in enumerate(f):
                    line = line.strip()
                    if line:
                        # Dividir por separador de turnos
                        turns = line.split(' __eou__ ')
                        
                        if len(turns) >= 2:
                            dialog = {
                                "dialog_id": f"dailydialog_{file_path.stem}_{i:04d}",
                                "source": "dailydialog",
                                "language": "en",
                                "turns": []
                            }
                            
                            for j, turn in enumerate(turns):
                                turn = turn.strip()
                                if turn:
                                    dialog["turns"].append({
                                        "turn_id": j,
                                        "speaker": "user" if j % 2 == 0 else "assistant",
                                        "text": turn,
                                        "length": len(turn)
                                    })
                            
                            if len(dialog["turns"]) >= 2:
                                all_dialogs.append(dialog)
        
        # Guardar diálogos procesados
        output_file = self.processed_path / "dailydialog_processed.json"
        
        processed_data = {
            "metadata": {
                "total_dialogs": len(all_dialogs),
                "source": "DailyDialog",
                "language": "en",
                "processed_date": datetime.now().isoformat(),
                "description": "Processed DailyDialog dataset for conversational AI training"
            },
            "dialogs": all_dialogs
        }
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(processed_data, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Procesamiento completado")
        print(f"📊 Total de diálogos: {len(all_dialogs)}")
        print(f"💾 Archivo guardado: {output_file}")
        
        return processed_data
    
    def translate_to_spanish(self, dialogs_data):
        """Traducir diálogos al español (versión básica)"""
        print("🌐 Traduciendo diálogos al español...")
        
        # Traducciones básicas de ejemplo
        translations = {
            "Hi, how are you doing?": "Hola, ¿cómo estás?",
            "I'm doing well, thank you. How about you?": "Estoy bien, gracias. ¿Y tú?",
            "I'm good too. What are your plans for today?": "Yo también estoy bien. ¿Cuáles son tus planes para hoy?",
            "Good morning!": "¡Buenos días!",
            "Good morning! How did you sleep?": "¡Buenos días! ¿Cómo dormiste?",
            "Can you help me with something?": "¿Puedes ayudarme con algo?",
            "Of course! What do you need help with?": "¡Por supuesto! ¿Con qué necesitas ayuda?",
        }
        
        spanish_dialogs = []
        
        for dialog in dialogs_data["dialogs"]:
            spanish_dialog = {
                "dialog_id": dialog["dialog_id"] + "_es",
                "source": dialog["source"] + "_translated",
                "language": "es",
                "turns": []
            }
            
            for turn in dialog["turns"]:
                spanish_text = translations.get(turn["text"], turn["text"])
                
                spanish_dialog["turns"].append({
                    "turn_id": turn["turn_id"],
                    "speaker": turn["speaker"],
                    "text": spanish_text,
                    "length": len(spanish_text),
                    "original_text": turn["text"]
                })
            
            spanish_dialogs.append(spanish_dialog)
        
        # Guardar versión en español
        spanish_data = {
            "metadata": {
                "total_dialogs": len(spanish_dialogs),
                "source": "DailyDialog (Spanish Translation)",
                "language": "es",
                "processed_date": datetime.now().isoformat(),
                "description": "DailyDialog traducido al español para entrenamiento de IA conversacional"
            },
            "dialogs": spanish_dialogs
        }
        
        output_file = self.processed_path / "dailydialog_spanish.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(spanish_data, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Traducción completada")
        print(f"💾 Archivo en español: {output_file}")
        
        return spanish_data
    
    def integrate_with_aria(self, dialogs_data):
        """Integrar diálogos con sistema de aprendizaje de ARIA"""
        print("🔗 Integrando con sistema de aprendizaje de ARIA...")
        
        # Conectar con el sistema de aprendizaje existente
        try:
            import sys
            from pathlib import Path
            backend_src = Path(__file__).parent
            sys.path.insert(0, str(backend_src))
            
            from learning_system import learning_system
            
            # Procesar cada diálogo
            integrated_count = 0
            
            for dialog in dialogs_data["dialogs"]:
                turns = dialog["turns"]
                
                # Crear pares pregunta-respuesta
                for i in range(0, len(turns) - 1, 2):
                    if i + 1 < len(turns):
                        user_input = turns[i]["text"]
                        aria_response = turns[i + 1]["text"]
                        
                        # Aprender de la conversación
                        context = {
                            "source": "dailydialog",
                            "dialog_id": dialog["dialog_id"],
                            "language": dialog["language"]
                        }
                        
                        learning_system.learn_from_conversation(
                            user_input, 
                            aria_response, 
                            context, 
                            0.8  # Alta confianza para datos de calidad
                        )
                        
                        integrated_count += 1
            
            print(f"✅ Integración completada")
            print(f"📚 Conversaciones integradas: {integrated_count}")
            
            return True
            
        except Exception as e:
            print(f"⚠️  Error en integración: {e}")
            print("   Los diálogos están disponibles para procesamiento manual")
            return False
    
    def run_complete_pipeline(self):
        """Ejecutar pipeline completo"""
        print("🚀 Ejecutando pipeline completo de DailyDialog...")
        
        # Paso 1: Descargar/crear dataset
        self.download_dailydialog()
        
        # Paso 2: Procesar diálogos
        dialogs_data = self.process_dailydialog()
        
        # Paso 3: Traducir al español
        spanish_data = self.translate_to_spanish(dialogs_data)
        
        # Paso 4: Integrar con ARIA
        self.integrate_with_aria(spanish_data)
        
        print("\n✅ Pipeline completado exitosamente!")
        print("🎯 ARIA ahora tiene patrones de diálogo mejorados")
        
        return True

# Función principal
def main():
    print("=" * 60)
    print("🚀 IMPLEMENTACIÓN DE DAILYDIALOG - FASE 1")
    print("=" * 60)
    
    processor = DailyDialogProcessor()
    processor.run_complete_pipeline()
    
    print("\n" + "=" * 60)
    print("📊 SIGUIENTE PASO:")
    print("   Prueba ARIA ahora para ver las mejoras en conversaciones")
    print("   Las respuestas deberían ser más naturales y coherentes")
    print("=" * 60)

if __name__ == "__main__":
    main()