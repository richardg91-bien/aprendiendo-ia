#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔧 Verificador de Configuración de Variables de Entorno - ARIA
Script para verificar y validar todas las configuraciones de entorno
"""

import os
import sys
from pathlib import Path
from typing import Dict, List, Tuple
import json

class EnvConfigVerifier:
    def __init__(self):
        self.base_path = Path(__file__).parent.parent.parent
        self.config_issues = []
        self.config_warnings = []
        self.config_ok = []
        
    def check_env_files(self) -> Dict[str, bool]:
        """Verifica la existencia de archivos .env"""
        print("🔍 Verificando archivos de configuración...")
        
        env_files = {
            '.env': self.base_path / '.env',
            '.env.example': self.base_path / '.env.example',
            '.env.production': self.base_path / '.env.production',
            'config/env/.env': self.base_path / 'config' / 'env' / '.env',
            'config/env/.env.example': self.base_path / 'config' / 'env' / '.env.example',
        }
        
        results = {}
        for name, path in env_files.items():
            exists = path.exists()
            results[name] = exists
            
            if exists:
                self.config_ok.append(f"✅ {name} encontrado")
            else:
                if name == '.env':
                    self.config_issues.append(f"❌ {name} NO encontrado - ¡REQUERIDO!")
                else:
                    self.config_warnings.append(f"⚠️ {name} no encontrado")
        
        return results
    
    def load_env_file(self, file_path: Path) -> Dict[str, str]:
        """Carga variables de un archivo .env"""
        env_vars = {}
        if file_path.exists():
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith('#') and '=' in line:
                            key, value = line.split('=', 1)
                            env_vars[key.strip()] = value.strip()
            except Exception as e:
                self.config_issues.append(f"❌ Error leyendo {file_path}: {e}")
        return env_vars
    
    def check_required_variables(self) -> Dict[str, bool]:
        """Verifica variables de entorno requeridas"""
        print("\n🔑 Verificando variables de entorno requeridas...")
        
        required_vars = {
            # Configuración básica del servidor
            'PORT': 'Puerto del servidor',
            'DEBUG': 'Modo de depuración',
            
            # Base de datos
            'SUPABASE_URL': 'URL de Supabase',
            'SUPABASE_ANON_KEY': 'Clave anónima de Supabase',
            
            # Google Cloud (opcional pero recomendado)
            'GOOGLE_CLOUD_PROJECT_ID': 'ID del proyecto de Google Cloud',
        }
        
        optional_vars = {
            'SUPABASE_SERVICE_ROLE_KEY': 'Clave de servicio de Supabase',
            'GOOGLE_APPLICATION_CREDENTIALS': 'Credenciales de Google Cloud',
            'OPENAI_API_KEY': 'Clave de API de OpenAI',
            'NODE_ENV': 'Entorno de Node.js',
            'ARIA_VOICE_ENABLED': 'Voz de ARIA habilitada',
            'ARIA_LEARNING_MODE': 'Modo de aprendizaje de ARIA',
            'PARENTAL_CONTROLS': 'Controles parentales',
        }
        
        # Cargar variables del archivo .env principal
        env_file = self.base_path / '.env'
        env_vars = self.load_env_file(env_file)
        
        # También verificar variables del sistema
        system_env_vars = dict(os.environ)
        all_vars = {**env_vars, **system_env_vars}
        
        results = {}
        
        # Verificar variables requeridas
        for var, description in required_vars.items():
            exists = var in all_vars and all_vars[var].strip()
            results[var] = exists
            
            if exists:
                self.config_ok.append(f"✅ {var}: {description}")
            else:
                self.config_issues.append(f"❌ {var} NO configurado - {description}")
        
        # Verificar variables opcionales
        for var, description in optional_vars.items():
            exists = var in all_vars and all_vars[var].strip()
            
            if exists:
                self.config_ok.append(f"✅ {var}: {description}")
            else:
                self.config_warnings.append(f"⚠️ {var} no configurado - {description} (opcional)")
        
        return results
    
    def check_file_permissions(self) -> bool:
        """Verifica permisos de archivos .env"""
        print("\n🔒 Verificando permisos de archivos...")
        
        env_file = self.base_path / '.env'
        if env_file.exists():
            try:
                # Verificar que se puede leer
                with open(env_file, 'r') as f:
                    f.read(1)
                self.config_ok.append("✅ Permisos de lectura correctos para .env")
                return True
            except PermissionError:
                self.config_issues.append("❌ Sin permisos de lectura para .env")
                return False
        return False
    
    def validate_variable_formats(self) -> Dict[str, bool]:
        """Valida el formato de variables específicas"""
        print("\n🔍 Validando formatos de variables...")
        
        env_file = self.base_path / '.env'
        env_vars = self.load_env_file(env_file)
        
        validations = {}
        
        # Validar PORT
        if 'PORT' in env_vars:
            try:
                port = int(env_vars['PORT'])
                if 1000 <= port <= 65535:
                    self.config_ok.append(f"✅ PORT válido: {port}")
                    validations['PORT'] = True
                else:
                    self.config_issues.append(f"❌ PORT fuera de rango: {port}")
                    validations['PORT'] = False
            except ValueError:
                self.config_issues.append(f"❌ PORT no es un número: {env_vars['PORT']}")
                validations['PORT'] = False
        
        # Validar SUPABASE_URL
        if 'SUPABASE_URL' in env_vars:
            url = env_vars['SUPABASE_URL']
            if url.startswith('https://') and '.supabase.co' in url:
                self.config_ok.append("✅ SUPABASE_URL formato válido")
                validations['SUPABASE_URL'] = True
            else:
                self.config_warnings.append("⚠️ SUPABASE_URL formato inusual")
                validations['SUPABASE_URL'] = False
        
        # Validar DEBUG
        if 'DEBUG' in env_vars:
            debug = env_vars['DEBUG'].lower()
            if debug in ['true', 'false', '1', '0']:
                self.config_ok.append(f"✅ DEBUG válido: {debug}")
                validations['DEBUG'] = True
            else:
                self.config_warnings.append(f"⚠️ DEBUG valor inusual: {debug}")
                validations['DEBUG'] = False
        
        return validations
    
    def check_sensitive_data_exposure(self) -> List[str]:
        """Verifica que datos sensibles no estén expuestos"""
        print("\n🛡️ Verificando exposición de datos sensibles...")
        
        sensitive_vars = [
            'SUPABASE_SERVICE_ROLE_KEY',
            'OPENAI_API_KEY',
            'DATABASE_PASSWORD',
            'SECRET_KEY',
            'PRIVATE_KEY'
        ]
        
        exposed_vars = []
        
        # Verificar que .env esté en .gitignore
        gitignore_path = self.base_path / '.gitignore'
        if gitignore_path.exists():
            try:
                with open(gitignore_path, 'r') as f:
                    gitignore_content = f.read()
                    if '.env' in gitignore_content:
                        self.config_ok.append("✅ .env está en .gitignore")
                    else:
                        self.config_issues.append("❌ .env NO está en .gitignore - ¡RIESGO DE SEGURIDAD!")
            except Exception:
                self.config_warnings.append("⚠️ No se pudo verificar .gitignore")
        
        return exposed_vars
    
    def generate_report(self) -> Dict:
        """Genera un reporte completo de la configuración"""
        print("\n" + "="*60)
        print("📊 REPORTE DE CONFIGURACIÓN DE ENTORNO")
        print("="*60)
        
        # Ejecutar todas las verificaciones
        env_files = self.check_env_files()
        required_vars = self.check_required_variables()
        permissions = self.check_file_permissions()
        validations = self.validate_variable_formats()
        security = self.check_sensitive_data_exposure()
        
        # Mostrar resultados
        print(f"\n✅ CONFIGURACIONES CORRECTAS ({len(self.config_ok)}):")
        for item in self.config_ok:
            print(f"  {item}")
        
        if self.config_warnings:
            print(f"\n⚠️ ADVERTENCIAS ({len(self.config_warnings)}):")
            for item in self.config_warnings:
                print(f"  {item}")
        
        if self.config_issues:
            print(f"\n❌ PROBLEMAS CRÍTICOS ({len(self.config_issues)}):")
            for item in self.config_issues:
                print(f"  {item}")
        
        # Calcular puntuación
        total_checks = len(self.config_ok) + len(self.config_warnings) + len(self.config_issues)
        score = (len(self.config_ok) / total_checks * 100) if total_checks > 0 else 0
        
        print(f"\n🎯 PUNTUACIÓN DE CONFIGURACIÓN: {score:.1f}%")
        
        if score >= 90:
            print("🎉 ¡Excelente! Configuración muy completa")
        elif score >= 70:
            print("👍 Buena configuración, algunas mejoras menores")
        elif score >= 50:
            print("⚠️ Configuración funcional pero necesita mejoras")
        else:
            print("❌ Configuración incompleta, se requieren correcciones")
        
        # Generar reporte en JSON
        report = {
            'timestamp': str(Path(__file__).stat().st_mtime),
            'score': score,
            'env_files': env_files,
            'required_vars': required_vars,
            'validations': validations,
            'permissions': permissions,
            'config_ok': self.config_ok,
            'config_warnings': self.config_warnings,
            'config_issues': self.config_issues
        }
        
        return report
    
    def save_report(self, report: Dict, filename: str = "env_config_report.json"):
        """Guarda el reporte en un archivo JSON"""
        report_path = self.base_path / 'reports' / filename
        
        try:
            report_path.parent.mkdir(exist_ok=True)
            with open(report_path, 'w', encoding='utf-8') as f:
                json.dump(report, f, indent=2, ensure_ascii=False)
            print(f"\n📄 Reporte guardado en: {report_path}")
        except Exception as e:
            print(f"❌ Error guardando reporte: {e}")

def main():
    """Función principal"""
    print("🔧 VERIFICADOR DE CONFIGURACIÓN DE ENTORNO - ARIA")
    print("=" * 60)
    
    verifier = EnvConfigVerifier()
    report = verifier.generate_report()
    verifier.save_report(report)
    
    # Determinar código de salida
    if verifier.config_issues:
        print(f"\n❌ Se encontraron {len(verifier.config_issues)} problemas críticos")
        sys.exit(1)
    elif verifier.config_warnings:
        print(f"\n⚠️ Se encontraron {len(verifier.config_warnings)} advertencias")
        sys.exit(0)
    else:
        print("\n✅ ¡Todas las configuraciones están correctas!")
        sys.exit(0)

if __name__ == "__main__":
    main()