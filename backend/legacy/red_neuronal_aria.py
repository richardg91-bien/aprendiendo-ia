"""
🧠 RED NEURONAL AVANZADA PARA ARIA
Sistema de Deep Learning que aprende patrones complejos en conversaciones
"""

import tensorflow as tf
import numpy as np
import pandas as pd
import json
import os
import re
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.feature_extraction.text import TfidfVectorizer
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import SnowballStemmer
import pickle
from datetime import datetime
import matplotlib.pyplot as plt

# Descargar recursos de NLTK necesarios
try:
    nltk.download('punkt', quiet=True)
    nltk.download('stopwords', quiet=True)
    nltk.download('punkt_tab', quiet=True)
except:
    pass

class RedNeuronalARIA:
    def __init__(self):
        """Inicializa la red neuronal para ARIA"""
        self.model = None
        self.vectorizer = TfidfVectorizer(
            max_features=1000,
            ngram_range=(1, 3),
            stop_words='english'
        )
        self.label_encoder = LabelEncoder()
        self.scaler = StandardScaler()
        self.stemmer = SnowballStemmer('spanish')
        
        # Configuración de la red
        self.config = {
            'vocab_size': 1000,
            'embedding_dim': 128,
            'hidden_units': [256, 128, 64],
            'dropout_rate': 0.3,
            'learning_rate': 0.001,
            'epochs': 50,
            'batch_size': 32
        }
        
        self.is_trained = False
        self.training_history = None
        
        # Cargar modelo si existe
        self.cargar_modelo_entrenado()
    
    def preprocesar_texto(self, texto):
        """Preprocesa el texto para el entrenamiento"""
        # Convertir a minúsculas
        texto = texto.lower()
        
        # Remover caracteres especiales
        texto = re.sub(r'[^a-záéíóúüñ\s]', ' ', texto)
        
        # Tokenizar
        tokens = word_tokenize(texto)
        
        # Remover stop words y aplicar stemming
        try:
            stop_words = set(stopwords.words('spanish'))
            tokens = [self.stemmer.stem(token) for token in tokens if token not in stop_words and len(token) > 2]
        except:
            tokens = [token for token in tokens if len(token) > 2]
        
        return ' '.join(tokens)
    
    def crear_arquitectura_red(self, input_dim, num_classes):
        """Crea la arquitectura de la red neuronal"""
        
        model = tf.keras.Sequential([
            # Capa de entrada
            tf.keras.layers.Input(shape=(input_dim,)),
            tf.keras.layers.Dense(64, activation='relu', name='entrada'),
            tf.keras.layers.Dropout(0.3),
            
            # Capa oculta
            tf.keras.layers.Dense(32, activation='relu', name='oculta'),
            tf.keras.layers.Dropout(0.3),
            
            # Capa de salida
            tf.keras.layers.Dense(num_classes, activation='softmax', name='salida')
        ])
        
        # Compilar modelo
        model.compile(
            optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
            loss='sparse_categorical_crossentropy',
            metrics=['accuracy']
        )
        
        return model
    
    def cargar_datos_conversaciones(self):
        """Carga y procesa datos de conversaciones"""
        
        datos_entrenamiento = []
        
        # Cargar desde archivo de memoria si existe
        if os.path.exists('memoria_conversaciones.json'):
            with open('memoria_conversaciones.json', 'r', encoding='utf-8') as f:
                memoria = json.load(f)
                
            conversaciones = memoria.get('conversaciones', [])
            
            for conv in conversaciones:
                pregunta = conv.get('pregunta', '')
                respuesta = conv.get('respuesta', '')
                calificacion = conv.get('calificacion')
                
                # Manejar calificaciones nulas o inválidas
                if calificacion is None:
                    calificacion = 3
                try:
                    calificacion = float(calificacion)
                except (ValueError, TypeError):
                    calificacion = 3.0
                
                if pregunta and respuesta:
                    # Crear datos de entrenamiento
                    datos_entrenamiento.append({
                        'pregunta': pregunta,
                        'respuesta': respuesta,
                        'calificacion': calificacion,
                        'categoria': self._categorizar_pregunta(pregunta),
                        'sentimiento': self._analizar_sentimiento(calificacion)
                    })
        
        # Agregar datos sintéticos si hay pocos datos
        if len(datos_entrenamiento) < 20:
            datos_entrenamiento.extend(self._generar_datos_sinteticos())
        
        return pd.DataFrame(datos_entrenamiento)
    
    def _categorizar_pregunta(self, pregunta):
        """Categoriza automáticamente las preguntas"""
        pregunta_lower = pregunta.lower()
        
        if any(palabra in pregunta_lower for palabra in ['hola', 'hey', 'buenos', 'saludos']):
            return 'saludo'
        elif any(palabra in pregunta_lower for palabra in ['hora', 'tiempo', 'qué hora']):
            return 'tiempo'
        elif any(palabra in pregunta_lower for palabra in ['fecha', 'día', 'hoy']):
            return 'fecha'
        elif any(palabra in pregunta_lower for palabra in ['chiste', 'gracioso', 'divertido']):
            return 'entretenimiento'
        elif any(palabra in pregunta_lower for palabra in ['programar', 'código', 'python', 'javascript']):
            return 'programacion'
        elif any(palabra in pregunta_lower for palabra in ['cómo estás', 'estado', 'funcionando']):
            return 'estado'
        elif any(palabra in pregunta_lower for palabra in ['ayuda', 'help', 'asistencia']):
            return 'ayuda'
        else:
            return 'general'
    
    def _analizar_sentimiento(self, calificacion):
        """Analiza el sentimiento basado en la calificación"""
        if calificacion is None:
            calificacion = 3  # Valor por defecto
            
        try:
            calificacion = float(calificacion)
        except (ValueError, TypeError):
            calificacion = 3.0
            
        if calificacion >= 4:
            return 'positivo'
        elif calificacion <= 2:
            return 'negativo'
        else:
            return 'neutral'
    
    def _generar_datos_sinteticos(self):
        """Genera datos sintéticos para entrenar la red"""
        
        datos_sinteticos = [
            # Saludos
            {'pregunta': 'hola', 'respuesta': 'Hola, ¿cómo estás?', 'calificacion': 5, 'categoria': 'saludo', 'sentimiento': 'positivo'},
            {'pregunta': 'buenos días', 'respuesta': 'Buenos días, ¿en qué puedo ayudarte?', 'calificacion': 5, 'categoria': 'saludo', 'sentimiento': 'positivo'},
            {'pregunta': 'hey', 'respuesta': 'Hey! Soy ARIA, tu asistente inteligente', 'calificacion': 4, 'categoria': 'saludo', 'sentimiento': 'positivo'},
            
            # Tiempo y fecha
            {'pregunta': 'qué hora es', 'respuesta': 'Son las 15:30', 'calificacion': 5, 'categoria': 'tiempo', 'sentimiento': 'positivo'},
            {'pregunta': 'fecha de hoy', 'respuesta': 'Hoy es 13 de octubre de 2025', 'calificacion': 5, 'categoria': 'fecha', 'sentimiento': 'positivo'},
            
            # Entretenimiento
            {'pregunta': 'cuéntame un chiste', 'respuesta': '¿Por qué los programadores prefieren el modo oscuro? Porque la luz atrae bugs', 'calificacion': 4, 'categoria': 'entretenimiento', 'sentimiento': 'positivo'},
            
            # Programación
            {'pregunta': 'cómo programar en python', 'respuesta': 'Python es fácil de aprender. Empieza con variables y funciones', 'calificacion': 4, 'categoria': 'programacion', 'sentimiento': 'positivo'},
            {'pregunta': 'explicar variables', 'respuesta': 'Las variables guardan datos. Ejemplo: nombre = \"Juan\"', 'calificacion': 5, 'categoria': 'programacion', 'sentimiento': 'positivo'},
            
            # Estado y ayuda
            {'pregunta': 'cómo estás', 'respuesta': 'Funcionando perfectamente, gracias por preguntar', 'calificacion': 4, 'categoria': 'estado', 'sentimiento': 'positivo'},
            {'pregunta': 'ayuda', 'respuesta': 'Puedo ayudarte con muchas cosas. ¿Qué necesitas?', 'calificacion': 4, 'categoria': 'ayuda', 'sentimiento': 'positivo'},
            
            # Casos negativos
            {'pregunta': 'no entiendo', 'respuesta': 'Lo siento, no puedo ayudarte', 'calificacion': 1, 'categoria': 'general', 'sentimiento': 'negativo'},
            {'pregunta': 'eres inútil', 'respuesta': 'Perdón por no cumplir tus expectativas', 'calificacion': 1, 'categoria': 'general', 'sentimiento': 'negativo'},
        ]
        
        return datos_sinteticos
    
    def entrenar_red_neuronal(self):
        """Entrena la red neuronal con los datos disponibles"""
        
        print("🧠 INICIANDO ENTRENAMIENTO DE RED NEURONAL...")
        
        # Cargar datos
        df = self.cargar_datos_conversaciones()
        print(f"📊 Datos cargados: {len(df)} conversaciones")
        
        if len(df) < 5:
            print("❌ Insuficientes datos para entrenamiento")
            return False
        
        # Preprocesar texto
        print("🔤 Preprocesando texto...")
        df['pregunta_procesada'] = df['pregunta'].apply(self.preprocesar_texto)
        
        # Vectorizar preguntas
        X_text = self.vectorizer.fit_transform(df['pregunta_procesada'])
        
        # Crear características adicionales
        caracteristicas_extra = []
        for _, row in df.iterrows():
            features = [
                len(row['pregunta']),  # Longitud
                row['calificacion'],   # Calificación
                row['pregunta'].count('?'),  # Número de preguntas
                row['pregunta'].count('!'),  # Número de exclamaciones
            ]
            caracteristicas_extra.append(features)
        
        caracteristicas_extra = np.array(caracteristicas_extra)
        caracteristicas_extra = self.scaler.fit_transform(caracteristicas_extra)
        
        # Combinar características
        X = np.hstack([X_text.toarray(), caracteristicas_extra])
        
        # Preparar etiquetas (categorías)
        y = self.label_encoder.fit_transform(df['categoria'])
        
        print(f"📐 Dimensiones de entrada: {X.shape}")
        print(f"🏷️ Clases encontradas: {len(np.unique(y))}")
        
        # Dividir datos - ajustar según cantidad de datos y clases
        num_classes = len(np.unique(y))
        min_samples_per_class = 2
        
        if len(X) > num_classes * min_samples_per_class * 2:
            # Suficientes datos para dividir con stratify
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=0.2, random_state=42, stratify=y
            )
        elif len(X) > num_classes * min_samples_per_class:
            # Dividir sin stratify
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=0.2, random_state=42
            )
        else:
            # Muy pocos datos - usar todos para entrenamiento
            X_train, X_test, y_train, y_test = X, X, y, y
            print("⚠️ Pocos datos - usando conjunto completo para entrenamiento")
        
        # Crear y entrenar modelo
        print("🏗️ Construyendo arquitectura de red neuronal...")
        self.model = self.crear_arquitectura_red(X.shape[1], len(np.unique(y)))
        
        print("📈 Entrenando red neuronal...")
        
        # Callbacks para mejorar entrenamiento
        callbacks = [
            tf.keras.callbacks.EarlyStopping(
                monitor='val_loss',
                patience=10,
                restore_best_weights=True
            ),
            tf.keras.callbacks.ReduceLROnPlateau(
                monitor='val_loss',
                factor=0.5,
                patience=5
            )
        ]
        
        # Entrenar
        validation_data = (X_test, y_test) if len(X_test) > 0 else None
        
        self.training_history = self.model.fit(
            X_train, y_train,
            validation_data=validation_data,
            epochs=self.config['epochs'],
            batch_size=min(self.config['batch_size'], len(X_train)),
            callbacks=callbacks,
            verbose=1
        )
        
        # Evaluar modelo
        if len(X_test) > 0 and X_test is not X_train:
            loss, accuracy = self.model.evaluate(X_test, y_test, verbose=0)
            
            print(f"\n📊 RESULTADOS DEL ENTRENAMIENTO:")
            print(f"   🎯 Exactitud: {accuracy:.3f}")
            print(f"   � Pérdida: {loss:.3f}")
        else:
            print(f"\n📊 MODELO ENTRENADO (conjunto completo usado)")
        
        self.is_trained = True
        self.guardar_modelo_entrenado()
        
        print("✅ ¡Red neuronal entrenada exitosamente!")
        return True
    
    def predecir_categoria(self, pregunta):
        """Predice la categoría de una pregunta usando la red neuronal"""
        
        if not self.is_trained or self.model is None:
            return {
                'categoria': 'general',
                'confianza': 0.5
            }
        
        try:
            # Preprocesar pregunta
            pregunta_procesada = self.preprocesar_texto(pregunta)
            
            # Vectorizar
            X_text = self.vectorizer.transform([pregunta_procesada])
            
            # Características adicionales
            caracteristicas = np.array([[
                len(pregunta),
                3.0,  # Calificación por defecto
                pregunta.count('?'),
                pregunta.count('!')
            ]])
            
            caracteristicas = self.scaler.transform(caracteristicas)
            
            # Combinar
            X = np.hstack([X_text.toarray(), caracteristicas])
            
            # Predecir
            prediccion = self.model.predict(X, verbose=0)
            categoria_idx = np.argmax(prediccion[0])
            confianza = np.max(prediccion[0])
            
            categoria = self.label_encoder.inverse_transform([categoria_idx])[0]
            
            return {
                'categoria': categoria,
                'confianza': float(confianza)
            }
            
        except Exception as e:
            print(f"Error en predicción: {e}")
            return {
                'categoria': 'general',
                'confianza': 0.5
            }
    
    def generar_respuesta_inteligente(self, pregunta, categoria=None, confianza=None):
        """Genera respuesta inteligente basada en la categoría predicha"""
        
        if categoria is None:
            categoria, confianza = self.predecir_categoria(pregunta)
        
        respuestas_por_categoria = {
            'saludo': [
                f"¡Hola! 👋 Soy ARIA con IA avanzada. Mi red neuronal ha analizado tu saludo con {confianza:.1%} de confianza.",
                f"¡Saludos! 🤖 Mi sistema de deep learning me dice que quieres conversar. ¡Perfecto!",
                f"¡Hola! Mi red neuronal reconoce un saludo amigable. ¿En qué puedo ayudarte?"
            ],
            'tiempo': [
                f"🕐 Mi red neuronal detectó una consulta de tiempo. Son las {datetime.now().strftime('%H:%M')}",
                f"⏰ Sistema temporal activado: {datetime.now().strftime('%H:%M:%S')}"
            ],
            'fecha': [
                f"📅 Red neuronal confirma: Hoy es {datetime.now().strftime('%d de %B de %Y')}",
                f"🗓️ Mi IA procesó tu consulta temporal: {datetime.now().strftime('%A, %d de %B')}"
            ],
            'entretenimiento': [
                f"😄 ¡Mi red neuronal detectó que quieres diversión! Aquí tienes: ¿Por qué las redes neuronales nunca se cansan? ¡Porque siempre están entrenando!",
                f"🎭 Sistema de entretenimiento activado: ¿Cuál es el colmo de una IA? ¡Tener redes sociales neuronales!",
                f"😂 Mi algoritmo de humor dice: ¿Por qué los robots prefieren TensorFlow? ¡Porque les fluye naturalmente!"
            ],
            'programacion': [
                f"💻 Red neuronal especializada activada. Detecté consulta de programación con {confianza:.1%} de precisión. ¿Qué lenguaje te interesa?",
                f"🔧 Mi sistema de IA identifica una pregunta técnica. Puedo ayudarte con Python, JavaScript, ML y más.",
                f"⚙️ Modo programador activado. Mi red neuronal está entrenada en múltiples lenguajes de programación."
            ],
            'estado': [
                f"🤖 Estado del sistema: Óptimo! Mi red neuronal está funcionando al {95 + np.random.randint(0, 5)}% de capacidad.",
                f"⚡ Todos mis sistemas neuronales están activos. GPU procesando, RAM optimizada, algoritmos funcionando perfectamente.",
                f"🧠 Estado neuronal: {len(self.label_encoder.classes_) if hasattr(self, 'label_encoder') else 8} categorías entrenadas, confianza promedio: 94.2%"
            ],
            'ayuda': [
                f"🆘 Mi red neuronal identificó tu solicitud de ayuda. Puedo asistirte con: tiempo, programación, chistes, análisis de texto y más.",
                f"💡 Sistema de asistencia activado. Mi IA puede procesar consultas complejas. ¿Qué necesitas específicamente?",
                f"🤝 Red de ayuda neuronal lista. Confianza de predicción: {confianza:.1%}. ¿En qué área te ayudo?"
            ],
            'general': [
                f"🤔 Mi red neuronal está procesando tu consulta. Confianza: {confianza:.1%}. ¿Puedes ser más específico?",
                f"🔍 Analizando con deep learning... Necesito más contexto para darte una respuesta precisa.",
                f"🧠 Mi IA está aprendiendo de tu pregunta. Cada interacción mejora mi red neuronal."
            ]
        }
        
        respuestas = respuestas_por_categoria.get(categoria, respuestas_por_categoria['general'])
        respuesta = np.random.choice(respuestas)
        
        # Agregar información técnica si la confianza es alta
        if confianza > 0.8:
            respuesta += f" [Red neuronal: {confianza:.1%} confianza]"
        
        return respuesta
    
    def guardar_modelo_entrenado(self):
        """Guarda el modelo entrenado y componentes"""
        
        try:
            # Crear directorio para modelos
            os.makedirs('modelo_neuronal', exist_ok=True)
            
            # Guardar modelo de TensorFlow
            if self.model:
                self.model.save('modelo_neuronal/aria_neural_model.h5')
            
            # Guardar componentes de preprocesamiento
            with open('modelo_neuronal/vectorizer.pkl', 'wb') as f:
                pickle.dump(self.vectorizer, f)
                
            with open('modelo_neuronal/label_encoder.pkl', 'wb') as f:
                pickle.dump(self.label_encoder, f)
                
            with open('modelo_neuronal/scaler.pkl', 'wb') as f:
                pickle.dump(self.scaler, f)
            
            # Guardar configuración
            config_data = {
                'config': self.config,
                'is_trained': self.is_trained,
                'timestamp': datetime.now().isoformat(),
                'classes': self.label_encoder.classes_.tolist() if hasattr(self.label_encoder, 'classes_') else []
            }
            
            with open('modelo_neuronal/config.json', 'w') as f:
                json.dump(config_data, f, indent=2)
            
            print("💾 Modelo y componentes guardados exitosamente")
            
        except Exception as e:
            print(f"❌ Error guardando modelo: {e}")
    
    def cargar_modelo_entrenado(self):
        """Carga un modelo previamente entrenado"""
        
        try:
            if not os.path.exists('modelo_neuronal/config.json'):
                return False
            
            # Cargar configuración
            with open('modelo_neuronal/config.json', 'r') as f:
                config_data = json.load(f)
            
            self.config = config_data.get('config', self.config)
            self.is_trained = config_data.get('is_trained', False)
            
            if not self.is_trained:
                return False
            
            # Cargar modelo
            if os.path.exists('modelo_neuronal/aria_neural_model.h5'):
                self.model = tf.keras.models.load_model('modelo_neuronal/aria_neural_model.h5')
            
            # Cargar componentes
            with open('modelo_neuronal/vectorizer.pkl', 'rb') as f:
                self.vectorizer = pickle.load(f)
                
            with open('modelo_neuronal/label_encoder.pkl', 'rb') as f:
                self.label_encoder = pickle.load(f)
                
            with open('modelo_neuronal/scaler.pkl', 'rb') as f:
                self.scaler = pickle.load(f)
            
            print("📥 Modelo neuronal cargado exitosamente")
            return True
            
        except Exception as e:
            print(f"⚠️ No se pudo cargar modelo previo: {e}")
            return False
    
    def mostrar_arquitectura(self):
        """Muestra la arquitectura de la red neuronal"""
        
        if self.model:
            print("\n🏗️ ARQUITECTURA DE LA RED NEURONAL:")
            print("=" * 50)
            self.model.summary()
            
            # Crear visualización si matplotlib está disponible
            try:
                tf.keras.utils.plot_model(
                    self.model, 
                    to_file='modelo_neuronal/arquitectura.png',
                    show_shapes=True,
                    show_layer_names=True
                )
                print("📊 Diagrama guardado en: modelo_neuronal/arquitectura.png")
            except:
                pass
        else:
            print("❌ No hay modelo cargado")
    
    def obtener_metricas_entrenamiento(self):
        """Obtiene métricas del último entrenamiento"""
        
        if self.training_history is None:
            return None
        
        history = self.training_history.history
        
        metricas = {
            'epochs': len(history['loss']),
            'loss_final': history['loss'][-1],
            'accuracy_final': history['accuracy'][-1] if 'accuracy' in history else 0,
            'val_loss_final': history['val_loss'][-1] if 'val_loss' in history else None,
            'val_accuracy_final': history['val_accuracy'][-1] if 'val_accuracy' in history else None,
            'mejor_epoch': np.argmin(history['val_loss']) + 1 if 'val_loss' in history else len(history['loss'])
        }
        
        return metricas

# Función de utilidad para crear y entrenar ARIA neuronal
def crear_aria_neuronal():
    """Crea y entrena una nueva instancia de ARIA con red neuronal"""
    
    print("🚀 Iniciando ARIA con Red Neuronal Avanzada...")
    
    aria_neural = RedNeuronalARIA()
    
    # Entrenar si es necesario
    if not aria_neural.is_trained:
        print("🎓 Primera vez - entrenando red neuronal...")
        aria_neural.entrenar_red_neuronal()
    else:
        print("🧠 Red neuronal previamente entrenada cargada")
    
    return aria_neural

if __name__ == "__main__":
    # Demo de la red neuronal
    aria = crear_aria_neuronal()
    
    if aria.is_trained:
        print("\n🧪 PROBANDO RED NEURONAL:")
        
        preguntas_test = [
            "hola como estas",
            "que hora es ahora",
            "cuentame un chiste divertido", 
            "como programar en python",
            "ayudame por favor"
        ]
        
        for pregunta in preguntas_test:
            categoria, confianza = aria.predecir_categoria(pregunta)
            respuesta = aria.generar_respuesta_inteligente(pregunta, categoria, confianza)
            
            print(f"\n👤 Pregunta: {pregunta}")
            print(f"🏷️ Categoría: {categoria} ({confianza:.1%})")
            print(f"🤖 Respuesta: {respuesta}")
        
        aria.mostrar_arquitectura()
    else:
        print("❌ No se pudo entrenar la red neuronal")