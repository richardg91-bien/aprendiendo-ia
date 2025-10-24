#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
🔍 AUDITORÍA COMPLETA DE SUPABASE
=================================

Script para revisar exhaustivamente el estado de Supabase
"""

import os
import sys
import json
from datetime import datetime
from dotenv import load_dotenv
from supabase import create_client

def main():
    print("🔍 AUDITORÍA COMPLETA DE SUPABASE")
    print("=" * 50)
    
    # Cargar variables de entorno
    load_dotenv()
    
    supabase_url = os.getenv('SUPABASE_URL')
    supabase_key = os.getenv('SUPABASE_ANON_KEY')
    
    if not supabase_url or not supabase_key:
        print("❌ Variables de entorno no encontradas")
        return False
    
    print(f"🌐 URL: {supabase_url}")
    print(f"🔑 Key: {supabase_key[:20]}...")
    
    try:
        # Conectar a Supabase
        supabase = create_client(supabase_url, supabase_key)
        print("✅ Conexión establecida")
        
        # === 1. REVISIÓN DE TABLAS ===
        print("\n" + "="*50)
        print("📊 1. REVISIÓN DE TABLAS")
        print("="*50)
        
        tables_expected = [
            'aria_conversations',
            'aria_knowledge', 
            'aria_api_relations',
            'aria_emotions',
            'aria_knowledge_summary',
            'aria_embeddings',
            'aria_knowledge_vectors',
            'aria_concept_relations'
        ]
        
        table_results = {}
        
        for table in tables_expected:
            try:
                # Verificar existencia y estructura
                response = supabase.table(table).select('*').limit(1).execute()
                count_response = supabase.table(table).select('id').execute()
                
                table_results[table] = {
                    'exists': True,
                    'count': len(count_response.data),
                    'sample': response.data[0] if response.data else None,
                    'error': None
                }
                
                print(f"✅ {table}: {len(count_response.data)} registros")
                
            except Exception as e:
                table_results[table] = {
                    'exists': False,
                    'count': 0,
                    'sample': None,
                    'error': str(e)
                }
                print(f"❌ {table}: Error - {str(e)[:50]}...")
        
        # === 2. PRUEBA DE FUNCIONALIDAD ===
        print("\n" + "="*50)
        print("🧪 2. PRUEBA DE FUNCIONALIDAD")
        print("="*50)
        
        # Test de escritura y lectura
        test_results = {}
        
        # Test aria_conversations
        try:
            test_conv = {
                'user_message': 'Test de auditoría',
                'aria_response': 'Respuesta de prueba',
                'session_id': 'audit_test',
                'user_emotion': 'curious',
                'aria_emotion': 'helpful'
            }
            
            insert_response = supabase.table('aria_conversations').insert(test_conv).execute()
            
            # Leer de vuelta
            read_response = supabase.table('aria_conversations')\
                .select('*')\
                .eq('session_id', 'audit_test')\
                .execute()
            
            # Limpiar
            supabase.table('aria_conversations')\
                .delete()\
                .eq('session_id', 'audit_test')\
                .execute()
            
            test_results['conversations'] = '✅ Lectura/Escritura OK'
            print("✅ aria_conversations: Funcional")
            
        except Exception as e:
            test_results['conversations'] = f'❌ Error: {e}'
            print(f"❌ aria_conversations: {e}")
        
        # Test aria_embeddings (si existe)
        if table_results['aria_embeddings']['exists']:
            try:
                test_embedding = {
                    'texto': 'Test de embedding',
                    'embedding': [0.1] * 384,  # Vector de 384 dimensiones
                    'categoria': 'test_audit',
                    'origen': 'audit'
                }
                
                embed_response = supabase.table('aria_embeddings').insert(test_embedding).execute()
                
                # Limpiar
                supabase.table('aria_embeddings')\
                    .delete()\
                    .eq('categoria', 'test_audit')\
                    .execute()
                
                test_results['embeddings'] = '✅ Embeddings OK'
                print("✅ aria_embeddings: Funcional")
                
            except Exception as e:
                test_results['embeddings'] = f'❌ Error: {e}'
                print(f"❌ aria_embeddings: {e}")
        
        # === 3. ANÁLISIS DE DATOS ===
        print("\n" + "="*50)
        print("📈 3. ANÁLISIS DE DATOS")
        print("="*50)
        
        # Últimas conversaciones
        try:
            recent_convs = supabase.table('aria_conversations')\
                .select('user_message, created_at')\
                .order('created_at', desc=True)\
                .limit(5)\
                .execute()
            
            print("💬 Últimas 5 conversaciones:")
            for conv in recent_convs.data:
                timestamp = conv['created_at'][:19]
                message = conv['user_message'][:40]
                print(f"   {timestamp}: {message}...")
                
        except Exception as e:
            print(f"❌ Error obteniendo conversaciones: {e}")
        
        # Conocimiento más confiable
        try:
            top_knowledge = supabase.table('aria_knowledge')\
                .select('concept, confidence')\
                .order('confidence', desc=True)\
                .limit(5)\
                .execute()
            
            print("\n🧠 Top 5 conocimientos:")
            for item in top_knowledge.data:
                concept = item['concept']
                confidence = item.get('confidence', 0)
                print(f"   {concept}: {confidence:.2f}")
                
        except Exception as e:
            print(f"❌ Error obteniendo conocimiento: {e}")
        
        # === 4. VERIFICACIÓN DE INTEGRIDAD ===
        print("\n" + "="*50)
        print("🔒 4. VERIFICACIÓN DE INTEGRIDAD")
        print("="*50)
        
        integrity_issues = []
        
        # Verificar referencias
        try:
            # Verificar que las conversaciones tengan session_id
            no_session = supabase.table('aria_conversations')\
                .select('id')\
                .is_('session_id', 'null')\
                .execute()
            
            if no_session.data:
                integrity_issues.append(f"Conversaciones sin session_id: {len(no_session.data)}")
            
            # Verificar conocimiento sin confianza
            no_confidence = supabase.table('aria_knowledge')\
                .select('id')\
                .is_('confidence', 'null')\
                .execute()
            
            if no_confidence.data:
                integrity_issues.append(f"Conocimiento sin confianza: {len(no_confidence.data)}")
                
        except Exception as e:
            integrity_issues.append(f"Error verificando integridad: {e}")
        
        if integrity_issues:
            print("⚠️ Problemas de integridad encontrados:")
            for issue in integrity_issues:
                print(f"   • {issue}")
        else:
            print("✅ Integridad de datos: OK")
        
        # === 5. RESUMEN EJECUTIVO ===
        print("\n" + "="*50)
        print("📋 5. RESUMEN EJECUTIVO")
        print("="*50)
        
        tables_working = sum(1 for t in table_results.values() if t['exists'])
        total_records = sum(t['count'] for t in table_results.values() if t['exists'])
        
        print(f"📊 Tablas funcionando: {tables_working}/{len(tables_expected)}")
        print(f"📈 Total de registros: {total_records}")
        print(f"🧪 Funcionalidad: {len([t for t in test_results.values() if '✅' in t])}/{len(test_results)} tests OK")
        print(f"🔒 Integridad: {'✅ OK' if not integrity_issues else f'⚠️ {len(integrity_issues)} problemas'}")
        
        # Estado general
        if tables_working == len(tables_expected) and not integrity_issues:
            status = "🟢 EXCELENTE"
        elif tables_working >= 6:
            status = "🟡 BUENO"
        else:
            status = "🔴 NECESITA ATENCIÓN"
        
        print(f"\n🎯 ESTADO GENERAL: {status}")
        
        # === 6. GENERAR REPORTE ===
        report = {
            'timestamp': datetime.now().isoformat(),
            'connection': {'url': supabase_url, 'status': 'connected'},
            'tables': table_results,
            'functionality_tests': test_results,
            'integrity_issues': integrity_issues,
            'summary': {
                'tables_working': tables_working,
                'total_tables': len(tables_expected),
                'total_records': total_records,
                'status': status
            }
        }
        
        with open('supabase_audit_report.json', 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        print(f"\n📄 Reporte detallado guardado: supabase_audit_report.json")
        
        return tables_working >= 6
        
    except Exception as e:
        print(f"❌ Error general en auditoría: {e}")
        return False

if __name__ == "__main__":
    success = main()
    print(f"\n{'🎉 Auditoría completada exitosamente' if success else '⚠️ Se encontraron problemas que requieren atención'}")
    input("\nPresiona Enter para continuar...")