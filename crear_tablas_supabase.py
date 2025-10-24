#!/usr/bin/env python3
"""
🔧 CREAR TABLAS DE SUPABASE PARA ARIA
====================================

Este script crea automáticamente todas las tablas necesarias
en tu base de datos de Supabase para que ARIA funcione completamente.

Uso:
1. Ejecuta este script con: python crear_tablas_supabase.py
2. O copia y pega el SQL resultante en el SQL Editor de Supabase
"""

import os
import sys
from datetime import datetime

def leer_esquema_sql(archivo):
    """Leer archivo SQL y devolverlo como string"""
    try:
        with open(archivo, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        print(f"❌ No se encontró el archivo: {archivo}")
        return None

def crear_sql_completo():
    """Crear el SQL completo combinando ambos esquemas"""
    
    # Esquema principal
    esquema_principal = leer_esquema_sql('aria_superbase_schema.sql')
    
    # Esquema de emociones
    esquema_emociones = leer_esquema_sql('supabase_emotions_schema.sql')
    
    if not esquema_principal:
        print("❌ Error: No se puede leer el esquema principal")
        return None
    
    if not esquema_emociones:
        print("❌ Error: No se puede leer el esquema de emociones")
        return None
    
    # Combinar ambos esquemas
    sql_completo = f"""-- 🚀 ARIA COMPLETE DATABASE SCHEMA
-- Creado automáticamente el: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
-- ================================================

-- ESQUEMA PRINCIPAL DE ARIA
{esquema_principal}

-- ESQUEMA ADICIONAL PARA INTERFAZ FUTURÍSTICA
{esquema_emociones}

-- ================================================
-- ✅ ESQUEMA COMPLETO DE ARIA LISTO
-- 📊 Incluye: Conocimiento, APIs, Conversaciones, Emociones, Sesiones
-- 🎨 Soporta: Interfaz básica y futurística con cambios de color
-- ================================================
"""
    
    return sql_completo

def guardar_sql_completo(sql_content):
    """Guardar el SQL completo en un archivo"""
    nombre_archivo = f"aria_complete_schema_{datetime.now().strftime('%Y%m%d_%H%M%S')}.sql"
    
    try:
        with open(nombre_archivo, 'w', encoding='utf-8') as f:
            f.write(sql_content)
        
        print(f"✅ SQL completo guardado en: {nombre_archivo}")
        return nombre_archivo
    except Exception as e:
        print(f"❌ Error guardando archivo: {e}")
        return None

def main():
    """Función principal"""
    print("🔧 CREADOR DE TABLAS SUPABASE PARA ARIA")
    print("=" * 50)
    
    # Crear SQL completo
    sql_completo = crear_sql_completo()
    
    if not sql_completo:
        print("❌ Error: No se pudo crear el SQL completo")
        sys.exit(1)
    
    # Guardar archivo
    archivo_sql = guardar_sql_completo(sql_completo)
    
    if archivo_sql:
        print("\n📋 INSTRUCCIONES PARA EJECUTAR EN SUPABASE:")
        print("=" * 50)
        print("1. Ve a tu panel de Supabase: https://supabase.com/dashboard")
        print("2. Selecciona tu proyecto")
        print("3. Ve a 'SQL Editor' en el menú lateral")
        print("4. Crea una nueva consulta")
        print(f"5. Copia y pega el contenido de: {archivo_sql}")
        print("6. Haz clic en 'Run' para ejecutar")
        print("\n🎉 ¡Esto creará todas las tablas necesarias para ARIA!")
        
        # Mostrar también el SQL para copiado directo
        print("\n📜 O COPIA Y PEGA ESTE SQL DIRECTAMENTE:")
        print("=" * 50)
        print(sql_completo)
    
    print("\n✅ Proceso completado")

if __name__ == "__main__":
    main()