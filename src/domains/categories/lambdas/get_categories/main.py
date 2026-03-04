import logging

from db.db_client import DBClient
from decorators.lambda_decorators import debug_event, cognito_auth_required, cors_enabled
from decorators.validate_pagination_and_search import validate_pagination_and_search
from repositories.category_repository import CategoryRepository
from use_cases.category_use_case import CategoryUseCase
from utils.response_utils import ResponseUtils

# Configure logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Inicialización de dependencias
db_client = DBClient.get_client()
repository = CategoryRepository(db_client)
use_case = CategoryUseCase(repository)

@cors_enabled
@cognito_auth_required
@debug_event
@validate_pagination_and_search()
def lambda_handler(event, context):
    logger.info(f'=== GET CATEGORIES HANDLER STARTED ===')
    logger.info(f'Event received: {event}')
    logger.info(f'Context: {context.function_name}, Request ID: {context.aws_request_id}')

    try:
        # Obtener los parámetros de la query string
        query_params = event.get('queryStringParameters', {}) or {}

        # Obtener parámetros validados o usar los de la query string como respaldo
        validated_params = event.get("validated_params", {})
        page = int(validated_params.get("page") or query_params.get("page", 1))
        limit = int(validated_params.get("limit") or query_params.get("limit", 10))
        search = validated_params.get("search") or query_params.get("search", "")

        # Asegurarse de que page y limit sean números válidos
        page = max(1, page)
        limit = max(1, min(50, limit))

        result = use_case.get_customers(page, limit, search)
        return ResponseUtils.success_response(result)
    except Exception as e:
        logger.error(f'ERROR in lambda_handler: {type(e).__name__}: {str(e)}', exc_info=True)
        raise