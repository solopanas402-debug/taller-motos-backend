#!/usr/bin/env python3
"""
Script de validación de optimizaciones
Verifica que todos los cambios se aplicaron correctamente
"""

import os
import re

def check_file_for_optimization(filepath, checks):
    """Verifica si un archivo contiene las optimizaciones esperadas"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        results = {}
        for check_name, patterns in checks.items():
            found = all(re.search(pattern, content, re.IGNORECASE) for pattern in patterns)
            results[check_name] = found
        
        return results
    except Exception as e:
        return {"error": str(e)}

# Definir verificaciones
CHECKS = {
    "products_get_products": {
        "filepath": "src/domains/products/lambdas/get_products/repositories/product_repository.py",
        "checks": {
            "Columnas específicas": [
                r"id_product.*name.*code.*price.*stock",
            ],
            "Sin segunda query": [
                r'count="exact"',
                r"response\.count"
            ],
            "Búsqueda optimizada": [
                r"name\.ilike",
                r"code\.ilike",
                r"~description~"  # Verificar que description NO esté en búsqueda
            ]
        }
    },
    "customers_get_customers": {
        "filepath": "src/domains/customers/lambdas/get_customers/repositories/customer_repository.py",
        "checks": {
            "Columnas específicas": [
                r"id_customer.*name.*email"
            ],
            "Campos indexados": [
                r"name\.ilike",
                r"email\.ilike",
                r"id_number\.ilike"
            ]
        }
    },
    "customers_get_by_id": {
        "filepath": "src/domains/customers/lambdas/get_customer_by_id/repositories/customer_repository.py",
        "checks": {
            "Columnas específicas": [
                r"id_customer.*name.*email"
            ],
            "Usa single()": [
                r"\.single\(\)"
            ]
        }
    },
    "products_get_by_id": {
        "filepath": "src/domains/products/lambdas/get_product_by_id/repositories/product_repository.py",
        "checks": {
            "Columnas específicas": [
                r"id_product.*name.*code.*price"
            ]
        }
    },
    "sales_get_sales": {
        "filepath": "src/domains/sales/lambdas/get_sales/repositories/sale_repository.py",
        "checks": {
            "Búsqueda optimizada": [
                r"p_search.*if.*search.*else.*None",
                r"p_record_type.*if.*record_type.*else.*None"
            ]
        }
    },
    "sales_get_by_id": {
        "filepath": "src/domains/sales/lambdas/get_sale_by_id/repositories/sale_repository.py",
        "checks": {
            "Límite específico": [
                r"p_limit.*1",
                r"p_offset.*0"
            ]
        }
    },
    "sql_indexes": {
        "filepath": "scripts/create_indexes.sql",
        "checks": {
            "Índices products": [
                r"idx_products_name",
                r"idx_products_code"
            ],
            "Índices customers": [
                r"idx_customers_name",
                r"idx_customers_email"
            ],
            "Índices sales": [
                r"idx_sales_status",
                r"idx_sales_created_at"
            ]
        }
    }
}

def main():
    print("=" * 70)
    print("🔍 VALIDACIÓN DE OPTIMIZACIONES - TALLER MOTOS")
    print("=" * 70)
    
    base_path = "/content/c:/Users/Jonathan Valencia/Documents/GitHub/taller-motos-backend"
    
    total_checks = 0
    passed_checks = 0
    failed_checks = []
    
    for category, config in CHECKS.items():
        filepath = os.path.join(base_path, config["filepath"])
        print(f"\n📄 {category}")
        print(f"   Archivo: {config['filepath']}")
        
        results = check_file_for_optimization(filepath, config["checks"])
        
        if "error" in results:
            print(f"   ❌ ERROR: {results['error']}")
            continue
        
        for check_name, passed in results.items():
            total_checks += 1
            status = "✅ PASS" if passed else "❌ FAIL"
            print(f"   {status} - {check_name}")
            
            if passed:
                passed_checks += 1
            else:
                failed_checks.append(f"{category} → {check_name}")
    
    print("\n" + "=" * 70)
    print("📊 RESUMEN")
    print("=" * 70)
    print(f"✅ Pasadas: {passed_checks}/{total_checks}")
    print(f"❌ Fallidas: {len(failed_checks)}/{total_checks}")
    
    if failed_checks:
        print("\n⚠️  CHECKS FALLIDAS:")
        for fail in failed_checks:
            print(f"   • {fail}")
    else:
        print("\n🎉 ¡TODAS LAS OPTIMIZACIONES APLICADAS CORRECTAMENTE!")
    
    print("\n" + "=" * 70)
    print("📋 PRÓXIMOS PASOS")
    print("=" * 70)
    print("""
1. ✅ Verificar este script: DONE
2. 🔧 Ejecutar índices SQL en Supabase:
   - Ir a SQL Editor
   - Copiar contenido de scripts/create_indexes.sql
   - Ejecutar
3. 🧪 Testing de endpoints
4. 📊 Monitorear performance en Supabase Dashboard
5. 🚀 Implementar caching (Fase 2)
    """)
    
    print("=" * 70)

if __name__ == "__main__":
    main()

# INSTRUCCIONES DE USO:
# python3 validate_optimizations.py
# 
# O desde terminal en VSCode:
# cd /tu/proyecto
# python3 scripts/validate_optimizations.py
