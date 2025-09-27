import json
from use_cases.supplier_use_case import SupplierUseCase
from decorators.lambda_decorators import cors_enabled, cognito_auth_required , debug_event
from decorators.get_endpoint import get_endpoint
from repositories.supplier_repository import SupplierRepository
from db.db_client import DBClient
from utils.response_utils import ResponseUtils  # Add this import

# Inicialización de dependencias
db_client = DBClient.get_client()
repository = SupplierRepository(db_client)
use_case = SupplierUseCase(repository)

@cors_enabled
@cognito_auth_required
@debug_event
@get_endpoint(entity_name="proveedores")
def lambda_handler(event, context):
    print(f'event: {event}')
    print(f'context: {context}')
    
    validated_params = event.get("validated_params", {})
    page = validated_params.get("page", 1)
    limit = validated_params.get("limit", 10)
    search = validated_params.get("search")
    
    # 1. Llamas al use case
    result = use_case.get_suppliers(page, limit, search)

    # 2. Envuelves el resultado
    return ResponseUtils.success_response(result)
