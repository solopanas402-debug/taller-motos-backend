#!/usr/bin/env python3
"""
Script para reemplazar .range() por .limit().offset() en repositories
"""
import re
from pathlib import Path

def fix_range_in_file(filepath):
    """Reemplaza .range(offset, offset + limit - 1) por .limit(limit).offset(offset)"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    
    # Patrón para encontrar .range(offset, offset + limit - 1)
    # Captura diferentes variaciones
    patterns = [
        (r'\.range\(offset,\s*offset\s*\+\s*limit\s*-\s*1\)', '.limit(limit).offset(offset)'),
        (r'\.range\(\s*offset\s*,\s*offset\s*\+\s*limit\s*-\s*1\s*\)', '.limit(limit).offset(offset)'),
    ]
    
    for pattern, replacement in patterns:
        content = re.sub(pattern, replacement, content)
    
    # Si hubo cambios, guardar el archivo
    if content != original_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ Actualizado: {filepath}")
        return True
    
    return False

def main():
    """Busca y actualiza todos los archivos repository"""
    src_dir = Path('src/domains')
    count = 0
    
    for repo_file in src_dir.rglob('repositories/*.py'):
        if repo_file.name != '__init__.py':
            if fix_range_in_file(repo_file):
                count += 1
    
    print(f"\n✨ Total de archivos actualizados: {count}")

if __name__ == '__main__':
    main()
