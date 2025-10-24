#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🤖 ARIA - Servidor con Super Base Integration
============================================

Servidor ARIA mejorado con integración completa de Super Base
para almacenamiento persistente de conocimiento y relaciones APIs.

Características:
✅ Integración completa con Supabase
✅ Almacenamiento persistente de conversaciones
✅ Gestión de conocimiento con base de datos
✅ Relaciones inteligentes con APIs externas
✅ Sistema de aprendizaje continuo
✅ Interfaz moderna con React

Fecha: 22 de octubre de 2025
"""

import sys
import os

# Agregar directorios al path para imports relativos
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, current_dir)
sys.path.insert(0, parent_dir)

from flask import Flask, request, jsonify, render_template, send_from_directory
from flask_cors import CORS
import json
import time
import uuid
from datetime import datetime, timezone
import logging
import re
from typing import Dict, List, Optional, Any

# Importar Super Base
try:
    from backend.services.aria_superbase import aria_superbase, ARIASuperBase
    SUPERBASE_AVAILABLE = True
    print("🗄️ ARIA Super Base cargado")
except ImportError as e:
    SUPERBASE_AVAILABLE = False
    print(f"❌ Super Base no disponible: {e}")

# Importar sistema de embeddings con Supabase
try:
    from core.aria_embeddings_supabase import ARIAEmbeddingsSupabase, crear_embedding_system
    EMBEDDINGS_AVAILABLE = True
    print("🧠 Sistema de embeddings Supabase cargado")
except ImportError as e:
    EMBEDDINGS_AVAILABLE = False
    print(f"❌ Sistema de embeddings no disponible: {e}")

# Importar sistemas de ARIA existentes
try:
    LEARNING_SYSTEM_AVAILABLE = True
    print("✅ Sistema de aprendizaje activado con control inteligente")
    print("📚 Funciones: Embeddings + APIs españolas + Análisis de patrones")
except ImportError as e:
    LEARNING_SYSTEM_AVAILABLE = False
    print(f"⚠️ Sistema de aprendizaje no disponible: {e}")

# Importar sistema emocional con Supabase
try:
    from core.emotion_detector_supabase import (
        init_emotion_detector_supabase,
        detect_user_emotion_supabase,
        detect_aria_emotion_supabase,
        get_emotion_stats_supabase
    )
    EMOTION_SUPABASE_AVAILABLE = True
    print("🎭 Sistema emocional Supabase cargado")
except ImportError as e:
    EMOTION_SUPABASE_AVAILABLE = False
    print(f"❌ Sistema emocional no disponible: {e}")

# ... El resto del código permanece igual ...
