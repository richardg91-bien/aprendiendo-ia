#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
🔧 APLICADOR DE CORRECCIÓN PARA aria_conversations
================================================

Este script aplica la corrección necesaria para aria_conversations
usando las capacidades limitadas de la API de Supabase
"""

import os
import sys
from dotenv import load_dotenv
from supabase import create_client

def main():
    print("🔧 APLICANDO CORRECCIÓN A aria_conversations")
    print("=" * 50)
    
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
        
        print("\n🔍 Verificando estado actual de aria_conversations...")
        
        # Verificar si las columnas existen
        missing_columns = []
        
        test_data = {
            'user_message': 'Test de columnas',
            'aria_response': 'Test response',
            'session_id': 'column_test_temp',
            'user_emotion': 'curious',
            'aria_emotion': 'helpful'
        }
        
        try:
            # Intentar insertar con todas las columnas
            response = supabase.table('aria_conversations').insert(test_data).execute()
            print("✅ Todas las columnas necesarias ya existen")
            
            # Limpiar el registro de prueba
            supabase.table('aria_conversations').delete().eq('session_id', 'column_test_temp').execute()
            
            print("\n🎉 No se requiere corrección - estructura correcta")
            return True
            
        except Exception as e:
            error_msg = str(e)
            if 'Could not find the' in error_msg and 'column' in error_msg:
                if 'user_emotion' in error_msg:
                    missing_columns.append('user_emotion')
                if 'aria_emotion' in error_msg:
                    missing_columns.append('aria_emotion')
                
                print(f"⚠️ Columnas faltantes detectadas: {missing_columns}")
        
        if missing_columns:
            print(f"\\n📋 INSTRUCCIONES PARA CORRECCIÓN MANUAL:")
            print("=" * 50)
            print("1. Ve a tu Dashboard de Supabase:")
            print("   https://supabase.com/dashboard")
            print("\\n2. Selecciona tu proyecto")
            print("\\n3. Ve a 'SQL Editor'")
            print("\\n4. Ejecuta este comando SQL:")
            print("\\n" + "="*50)
            
            if 'user_emotion' in missing_columns:
                print("ALTER TABLE public.aria_conversations")
                print("ADD COLUMN IF NOT EXISTS user_emotion VARCHAR(50) DEFAULT 'neutral';")
                print()
            
            if 'aria_emotion' in missing_columns:
                print("ALTER TABLE public.aria_conversations")
                print("ADD COLUMN IF NOT EXISTS aria_emotion VARCHAR(50) DEFAULT 'helpful';")
                print()
                
            print("-- Actualizar registros existentes")
            print("UPDATE public.aria_conversations")
            print("SET user_emotion = 'curious'")
            print("WHERE user_emotion IS NULL;")
            print()
            print("UPDATE public.aria_conversations")
            print("SET aria_emotion = 'helpful'")
            print("WHERE aria_emotion IS NULL;")
            
            print("="*50)
            print("\\n5. Después de ejecutar, prueba ARIA nuevamente")
            
            print("\\n📄 ALTERNATIVA: Usa el archivo CORREGIR_CONVERSATIONS.sql")
            print("   que contiene exactamente estos comandos")
        
        return len(missing_columns) == 0
        
    except Exception as e:
        print(f"❌ Error general: {e}")
        return False

if __name__ == "__main__":
    success = main()
    
    if success:
        print("\\n🎉 aria_conversations está correctamente configurada")
        print("✅ ARIA está listo para usar completamente")
    else:
        print("\\n⚠️ Se requiere corrección manual en Supabase")
        print("📋 Sigue las instrucciones mostradas arriba")
    
    input("\\nPresiona Enter para continuar...")