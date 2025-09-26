import json
from use_cases.supplier_use_case import SupplierUseCase
from decorators.lambda_decorators import cors_enabled, auth_required
from decorators.role_required import role_required
from decorators.get_endpoint import get_endpoint
from repositories.supplier_repository import SupplierRepository
from db.db_client import DBClient

# Inicialización de dependencias
db_client = DBClient.get_client()
repository = SupplierRepository(db_client)
use_case = SupplierUseCase(repository)

@cors_enabled
@auth_required
@role_required(["ADMIN", "VENDEDOR"])  # Solo estos roles pueden consultar proveedores
@get_endpoint(entity_name="proveedores", max_limit_admin=100, max_limit_other=50)
def lambda_handler(event, context):
    print(f'event: {event}')
    print(f'context: {context}')
    
    # Obtener parámetros validados del decorador
    validated_params = event.get("validated_params", {})
    page = validated_params.get("page", 1)
    limit = validated_params.get("limit", 10)
    search = validated_params.get("search")
    
    # Ejecutar caso de uso
    result = use_case.get_suppliers(page, limit, search)
    
    return result