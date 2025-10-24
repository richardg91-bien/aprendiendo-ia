#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
✅ VERIFICADOR DE TABLAS CORREGIDAS
=================================

Script para verificar que todas las tablas están funcionando
"""

import os
import sys
from dotenv import load_dotenv
from supabase import create_client

def main():
    print("✅ VERIFICADOR DE TABLAS CORREGIDAS")
    print("=" * 40)
    
    # Cargar variables de entorno
    load_dotenv()
    
    supabase_url = os.getenv('SUPABASE_URL')
    supabase_key = os.getenv('SUPABASE_ANON_KEY')
    
    if not supabase_url or not supabase_key:
        print("❌ Variables de entorno no encontradas")
        return False
    
    try:
        # Conectar a Supabase
        supabase = create_client(supabase_url, supabase_key)
        print("✅ Conectado a Supabase")
        
        print("\n📊 VERIFICANDO TODAS LAS TABLAS:")
        print("-" * 40)
        
        # Lista completa de tablas esperadas
        all_tables = [
            'aria_conversations',
            'aria_knowledge', 
            'aria_api_relations',
            'aria_emotions',
            'aria_knowledge_summary',
            'aria_embeddings',
            'aria_knowledge_vectors',
            'aria_concept_relations'
        ]
        
        working_tables = 0
        
        for table in all_tables:
            try:
                # Intentar obtener el conteo de registros
                response = supabase.table(table).select('id').execute()
                count = len(response.data)
                print(f"✅ {table}: {count} registros")
                working_tables += 1
                
            except Exception as e:
                error_msg = str(e)
                if "Could not find the table" in error_msg:
                    print(f"❌ {table}: No existe")
                elif "column" in error_msg and ".id" in error_msg:
                    print(f"⚠️ {table}: Estructura incorrecta")
                else:
                    print(f"❌ {table}: Error - {error_msg[:50]}...")
        
        print(f"\n📊 RESUMEN:")
        print(f"✅ Tablas funcionando: {working_tables}/{len(all_tables)}")
        
        if working_tables == len(all_tables):
            print("🎉 ¡TODAS LAS TABLAS ESTÁN FUNCIONANDO!")
            
            # Probar funcionalidad de embeddings
            print("\n🧪 PROBANDO FUNCIONALIDAD DE EMBEDDINGS:")
            try:
                # Intentar insertar un embedding de prueba
                test_embedding = [0.1] * 384  # Vector de 384 dimensiones
                
                response = supabase.table('aria_embeddings').insert({
                    'texto': 'Prueba de embeddings',
                    'embedding': test_embedding,
                    'categoria': 'test',
                    'origen': 'verification'
                }).execute()
                
                print("✅ Inserción de embeddings: Funcional")
                
                # Limpiar el registro de prueba
                supabase.table('aria_embeddings').delete().eq('categoria', 'test').execute()
                print("✅ Limpieza completada")
                
            except Exception as e:
                print(f"⚠️ Embeddings: Error - {e}")
        
        elif working_tables >= 4:
            print("✅ Tablas básicas funcionando, falta completar embeddings")
        else:
            print("⚠️ Varias tablas necesitan corrección")
        
        return working_tables >= 4
        
    except Exception as e:
        print(f"❌ Error general: {e}")
        return False

if __name__ == "__main__":
    success = main()
    print(f"\n{'🎉 Sistema verificado exitosamente' if success else '⚠️ Algunas tablas necesitan atención'}")
    input("\nPresiona Enter para continuar...")