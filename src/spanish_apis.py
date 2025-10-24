#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🇪🇸 ARIA Spanish APIs
=====================

Sistema de APIs españolas para búsquedas web y servicios específicos de España.
Incluye búsquedas en Google, DuckDuckGo, APIs del gobierno español, etc.

Fecha: 24 de octubre de 2025
"""

import requests
import json
import time
from typing import Dict, List, Optional, Any
import urllib.parse
from datetime import datetime
import logging

# Configurar logging
logger = logging.getLogger(__name__)

class ARIASpanishAPIs:
    """Sistema de APIs españolas para ARIA"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        
        # APIs disponibles
        self.apis_config = {
            'duckduckgo': {
                'enabled': True,
                'url': 'https://api.duckduckgo.com/',
                """
                Este archivo ahora solo importa el módulo spanish_apis desde backend/services.
                La lógica principal se encuentra en backend/services/spanish_apis.py
                """

                from backend.services.spanish_apis import *