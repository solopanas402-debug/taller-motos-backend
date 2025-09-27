import json
from use_cases.customer_use_case import CustomerUseCase
from decorators.lambda_decorators import cors_enabled, cognito_auth_required , debug_event

from decorators.validate_pagination_and_search import validate_pagination_and_search
from repositories.customer_repository import CustomerRepository
from db.db_client import DBClient
from utils.response_utils import ResponseUtils

# Inicialización de dependencias
db_client = DBClient.get_client()
repository = CustomerRepository(db_client)
use_case = CustomerUseCase(repository)

@cors_enabled
@cognito_auth_required
@debug_event
@validate_pagination_and_search()
def lambda_handler(event, context):
    print(f'event: {event}')
    print(f'context: {context}')
    
    validated_params = event.get("validated_params", {})
    page = validated_params.get("page", 1)
    limit = validated_params.get("limit", 10)
    search = validated_params.get("search")
    
    # 1. Llamas al use case
    result = use_case.get_customers(page, limit, search)

    # 2. Envuelves el resultado
    return ResponseUtils.success_response(result)