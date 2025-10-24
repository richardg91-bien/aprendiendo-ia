"""
Pruebas unitarias para backend/services/texto.py
"""
import pytest
from backend.services import texto

def test_generar_respuesta():
    prompt = "Hola, ¿cómo estás?"
    respuesta = texto.generar_respuesta(prompt)
    assert isinstance(respuesta, str)
    assert len(respuesta) > 0
