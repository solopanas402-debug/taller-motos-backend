#!/usr/bin/env python3
"""
Script para actualizar imports en use_cases
"""
import os
import re
from pathlib import Path

def fix_imports_in_file(filepath):
    """Actualiza los imports en un archivo use_case"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    
    # Obtener el dominio desde la ruta del archivo
    # Ejemplo: src/domains/customers/lambdas/get_customers/use_cases/customer_use_case.py -> customers
    parts = Path(filepath).parts
    if 'domains' in parts and 'use_cases' in parts:
        domain_idx = parts.index('domains')
        domain = parts[domain_idx + 1]
        lambda_name = parts[domain_idx + 3]  # get_customers, add_customer, etc.
        
        # Reemplazar imports de repositories
        content = re.sub(
            r'^from repositories\.(\w+) import',
            f'from domains.{domain}.lambdas.{lambda_name}.repositories.\\1 import',
            content,
            flags=re.MULTILINE
        )
        
        # Si hubo cambios, guardar el archivo
        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✅ Actualizado: {filepath}")
            return True
    
    return False

def main():
    """Busca y actualiza todos los archivos en use_cases"""
    src_dir = Path('src/domains')
    count = 0
    
    for use_case_file in src_dir.rglob('use_cases/*.py'):
        if use_case_file.name != '__init__.py':
            if fix_imports_in_file(use_case_file):
                count += 1
    
    print(f"\n✨ Total de archivos actualizados: {count}")

if __name__ == '__main__':
    main()
