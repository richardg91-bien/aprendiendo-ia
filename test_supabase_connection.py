#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Test de conexión simple a Supabase
"""

import os
import sys
from dotenv import load_dotenv
from supabase import create_client, Client

def main():
    print("🔗 PROBANDO CONEXIÓN A SUPABASE...")
    
    # Cargar variables de entorno
    load_dotenv()
    
    supabase_url = os.getenv('SUPABASE_URL')
    supabase_key = os.getenv('SUPABASE_KEY')
    
    if not supabase_url or not supabase_key:
        print("❌ Error: Variables SUPABASE_URL y SUPABASE_KEY no encontradas")
        print("   Verifica tu archivo .env")
        return False
    
    print(f"📍 URL: {supabase_url}")
    print(f"🔑 Key: {supabase_key[:20]}...")
    
    try:
        # Crear cliente
        supabase: Client = create_client(supabase_url, supabase_key)
        print("✅ Cliente Supabase creado")
        
        # Test simple: obtener datos de aria_conversations (si existe)
        response = supabase.table('aria_conversations').select('*').limit(1).execute()
        print(f"✅ Conexión exitosa! Tablas accesibles")
        
        # Verificar tablas existentes
        existing_tables = supabase.rpc('get_table_names').execute()
        print(f"📊 Respuesta de tablas: {existing_tables}")
        
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        print(f"   Tipo: {type(e).__name__}")
        return False
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)