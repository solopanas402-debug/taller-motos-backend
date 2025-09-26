import json
from decorators.lambda_decorators import cors_enabled, auth_required
from decorators.role_required import role_required
from decorators.get_endpoint import get_endpoint
from db.db_client import DBClient
from repositories.repair_repository import RepairRepository
from use_cases.repair_use_case import RepairUseCase

# Inicialización de dependencias
db_client = DBClient.get_client()
repository = RepairRepository(db_client)
use_case = RepairUseCase(repository)

@cors_enabled
@auth_required
@role_required(["ADMIN", "MECANICO", "VENDEDOR"])  # Estos roles pueden consultar reparaciones
@get_endpoint(entity_name="reparaciones", max_limit_admin=100, max_limit_other=50)
def lambda_handler(event, context):
    print(f"event: {event}")
    print(f"context: {context}")
    
    # Obtener parámetros validados del decorador
    validated_params = event.get("validated_params", {})
    page = validated_params.get("page", 1)
    limit = validated_params.get("limit", 10)
    search = validated_params.get("search")
    
    # Ejecutar caso de uso
    result = use_case.get_repairs(page, limit, search)
    
    return result


