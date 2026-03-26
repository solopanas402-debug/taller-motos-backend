#!/usr/bin/env python3
"""
Script para actualizar imports relativos a absolutos en todos los lambdas
"""
import os
import re
from pathlib import Path

def fix_imports_in_file(filepath):
    """Actualiza los imports en un archivo"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    
    # Obtener el dominio desde la ruta del archivo
    # Ejemplo: src/domains/customers/lambdas/get_customers/main.py -> customers
    parts = Path(filepath).parts
    if 'domains' in parts:
        domain_idx = parts.index('domains')
        domain = parts[domain_idx + 1]
        lambda_name = parts[domain_idx + 3]  # get_customers, add_customer, etc.
        
        # Reemplazar imports de use_cases
        content = re.sub(
            r'^from use_cases\.(\w+) import',
            f'from domains.{domain}.lambdas.{lambda_name}.use_cases.\\1 import',
            content,
            flags=re.MULTILINE
        )
        
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
    """Busca y actualiza todos los archivos main.py en lambdas"""
    src_dir = Path('src/domains')
    count = 0
    
    for main_file in src_dir.rglob('lambdas/*/main.py'):
        if fix_imports_in_file(main_file):
            count += 1
    
    print(f"\n✨ Total de archivos actualizados: {count}")

if __name__ == '__main__':
    main()
