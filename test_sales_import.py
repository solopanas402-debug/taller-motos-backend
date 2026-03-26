#!/usr/bin/env python3
"""
Test de importación del sales lambda
"""
import sys
import os

# Configurar paths como lo hace lambda_wrapper
sys.path.insert(0, os.path.abspath('layers/shared'))
sys.path.insert(0, os.path.abspath('src'))

from dotenv import load_dotenv
load_dotenv()

print("Paths configurados correctamente")
print(f"sys.path[0]: {sys.path[0]}")
print(f"sys.path[1]: {sys.path[1]}")

try:
    print("\n1. Importando DBClient...")
    from db.db_client import DBClient
    print("   ✅ DBClient importado")
    
    print("\n2. Importando SaleRepository...")
    from domains.sales.lambdas.get_sales.repositories.sale_repository import SaleRepository
    print("   ✅ SaleRepository importado")
    
    print("\n3. Importando SaleUseCase...")
    from domains.sales.lambdas.get_sales.use_cases.sale_use_case import SaleUseCase
    print("   ✅ SaleUseCase importado")
    
    print("\n4. Creando instancias...")
    db_client = DBClient.get_client()
    print("   ✅ db_client creado")
    
    repository = SaleRepository(db_client)
    print("   ✅ repository creado")
    
    use_case = SaleUseCase(repository)
    print("   ✅ use_case creado")
    
    print("\n5. Importando el módulo main completo...")
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "test_sales_main",
        "src/domains/sales/lambdas/get_sales/main.py"
    )
    module = importlib.util.module_from_spec(spec)
    sys.modules["test_sales_main"] = module
    spec.loader.exec_module(module)
    print("   ✅ Módulo main cargado exitosamente")
    
    print("\n✅ TODO FUNCIONA CORRECTAMENTE")
    
except Exception as e:
    print(f"\n❌ ERROR: {e}")
    import traceback
    traceback.print_exc()
