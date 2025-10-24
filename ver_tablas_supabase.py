#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
🔍 EXPLORADOR DE TABLAS SUPABASE
==============================

Script para ver todas las tablas de ARIA en Supabase
"""

import os
import sys
from dotenv import load_dotenv
from supabase import create_client

def main():
    print("🔍 EXPLORADOR DE TABLAS SUPABASE")
    print("=" * 40)
    
    # Cargar variables de entorno
    load_dotenv()
    
    supabase_url = os.getenv('SUPABASE_URL')
    supabase_key = os.getenv('SUPABASE_ANON_KEY')
    
    if not supabase_url or not supabase_key:
        print("❌ Variables de entorno no encontradas")
        return
    
    try:
        # Conectar a Supabase
        supabase = create_client(supabase_url, supabase_key)
        print("✅ Conectado a Supabase")
        
        print("\n📊 TABLAS DE ARIA:")
        print("-" * 30)
        
        # Lista de tablas esperadas
        tables = [
            'aria_conversations',
            'aria_knowledge', 
            'aria_api_relations',
            'aria_emotions',
            'aria_knowledge_summary',
            'aria_embeddings',
            'aria_knowledge_vectors',
            'aria_concept_relations'
        ]
        
        for table in tables:
            try:
                # Intentar obtener el conteo de registros
                response = supabase.table(table).select('id').execute()
                count = len(response.data)
                status = "✅" if count >= 0 else "❌"
                print(f"{status} {table}: {count} registros")
                
            except Exception as e:
                print(f"❌ {table}: No existe o error ({str(e)[:50]}...)")
        
        print("\n🔍 ÚLTIMAS CONVERSACIONES:")
        print("-" * 30)
        try:
            response = supabase.table('aria_conversations')\
                .select('id, user_message, created_at')\
                .order('created_at', desc=True)\
                .limit(5)\
                .execute()
            
            for conv in response.data:
                timestamp = conv['created_at'][:19]
                message = conv['user_message'][:50]
                print(f"• {timestamp}: {message}...")
                
        except Exception as e:
            print(f"❌ Error obteniendo conversaciones: {e}")
        
        print("\n📚 CONOCIMIENTO ALMACENADO:")
        print("-" * 30)
        try:
            response = supabase.table('aria_knowledge')\
                .select('concept, confidence')\
                .order('confidence', desc=True)\
                .limit(10)\
                .execute()
            
            for item in response.data:
                concept = item['concept']
                confidence = item.get('confidence', 0)
                print(f"• {concept}: {confidence:.2f}")
                
        except Exception as e:
            print(f"❌ Error obteniendo conocimiento: {e}")
            
    except Exception as e:
        print(f"❌ Error general: {e}")

if __name__ == "__main__":
    main()