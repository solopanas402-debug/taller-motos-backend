import json
import logging
from use_cases.sale_use_case import SaleUseCase
from decorators.lambda_decorators import cors_enabled, cognito_auth_required, debug_event
from decorators.validate_pagination_and_search import validate_pagination_and_search
from repositories.sale_repository import SaleRepository
from db.db_client import DBClient
from utils.response_utils import ResponseUtils  # Add this import

# Configure logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Inicialización de dependencias
db_client = DBClient.get_client()
repository = SaleRepository(db_client)
use_case = SaleUseCase(repository)

@cors_enabled
# @cognito_auth_required
@debug_event
# @validate_pagination_and_search()
def lambda_handler(event, context):
    logger.info(f'=== GET SALES HANDLER STARTED ===')
    logger.info(f'Event received: {event}')
    logger.info(f'Context: {context.function_name}, Request ID: {context.aws_request_id}')

    try:
        # Obtener los parámetros de la query string
        query_params = event.get("queryStringParameters", {}) or {}
        logger.info(f'Query string parameters: {query_params}')
        
        # Obtener el recordType y payment_method
        record_type = query_params.get("recordType", None)
        payment_method = query_params.get("payment_method", None)
        logger.info(f'Extracted filters - record_type: {record_type}, payment_method: {payment_method}')
        
        # Obtener parámetros validados o usar los de la query string como respaldo
        validated_params = event.get("validated_params", {})
        page = int(validated_params.get("page") or query_params.get("page", 1))
        limit = int(validated_params.get("limit") or query_params.get("limit", 10))
        search = validated_params.get("search") or query_params.get("search", "")
        logger.info(f'Pagination params - page: {page}, limit: {limit}, search: {search}')
        
        # Asegurarse de que page y limit sean números válidos
        page = max(1, page)
        limit = max(1, min(50, limit))
        logger.info(f'Validated pagination - page: {page}, limit: {limit}')

        # 1. Llamas al use case
        logger.info(f'Calling use_case.get_sales with parameters: page={page}, limit={limit}, search={search}, record_type={record_type}, payment_method={payment_method}')
        result = use_case.get_sales(page, limit, search, record_type, payment_method)
        logger.info(f'Use case returned successfully. Result keys: {result.keys()}')

        # 2. Envuelves el resultado
        response = ResponseUtils.success_response(result)
        logger.info(f'=== GET SALES HANDLER COMPLETED SUCCESSFULLY ===')
        return response
    
    except Exception as e:
        logger.error(f'ERROR in lambda_handler: {type(e).__name__}: {str(e)}', exc_info=True)
        raise
