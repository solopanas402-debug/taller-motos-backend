import json
from use_cases.product_use_case import ProductUseCase
from decorators.lambda_decorators import cors_enabled, cognito_auth_required, debug_event
from decorators.validate_pagination_and_search import validate_pagination_and_search
from repositories.product_repository import ProductRepository  
from db.db_client import DBClient
from utils.response_utils import ResponseUtils  # Add this import

# Inicialización de dependencias
db_client = DBClient.get_client()
repository = ProductRepository(db_client)
use_case = ProductUseCase(repository)

@cors_enabled
@cognito_auth_required
@debug_event
@validate_pagination_and_search()
def lambda_handler(event, context):
    print(f'event: {event}')
    print(f'context: {context}')
    
    # Obtener los parámetros de la query string
    query_params = event.get('queryStringParameters', {}) or {}
    
    # Obtener parámetros validados o usar los de la query string como respaldo
    validated_params = event.get("validated_params", {})
    page = int(validated_params.get("page") or query_params.get("page", 1))
    limit = int(validated_params.get("limit") or query_params.get("limit", 10))
    search = validated_params.get("search") or query_params.get("search", "")
    
    # Asegurarse de que page y limit sean números válidos
    page = max(1, page)  # página mínima es 1
    limit = max(1, min(50, limit))  # límite entre 1 y 100
    
    # Llamar al use case con los parámetros procesados
    result = use_case.get_all_products(page, limit, search)

    # 2. Envuelves el resultado
    return ResponseUtils.success_response(result)
