import json
import logging
from use_cases.quotation_use_case import QuotationUseCase
from decorators.lambda_decorators import cors_enabled, cognito_auth_required, debug_event
from decorators.validate_pagination_and_search import validate_pagination_and_search
from repositories.quotation_repository import QuotationRepository
from db.db_client import DBClient
from utils.response_utils import ResponseUtils

logger = logging.getLogger()
logger.setLevel(logging.INFO)

db_client = DBClient.get_client()
repository = QuotationRepository(db_client)
use_case = QuotationUseCase(repository)

@cors_enabled
@cognito_auth_required
@debug_event
def lambda_handler(event, context):
    logger.info(f'=== GET QUOTATIONS HANDLER STARTED ===')
    logger.info(f'Event received: {event}')
    logger.info(f'Context: {context.function_name}, Request ID: {context.aws_request_id}')

    try:
        query_params = event.get("queryStringParameters", {}) or {}
        logger.info(f'Query string parameters: {query_params}')
        
        # Force recordType to quotation
        record_type = "quotation"
        payment_method = query_params.get("payment_method", None)
        logger.info(f'Forced record_type: {record_type}, payment_method: {payment_method}')
        
        validated_params = event.get("validated_params", {})
        page = int(validated_params.get("page") or query_params.get("page", 1))
        limit = int(validated_params.get("limit") or query_params.get("limit", 10))
        search = validated_params.get("search") or query_params.get("search", "")
        logger.info(f'Pagination params - page: {page}, limit: {limit}, search: {search}')
        
        page = max(1, page)
        limit = max(1, min(50, limit))
        logger.info(f'Validated pagination - page: {page}, limit: {limit}')

        logger.info(f'Calling use_case.get_quotations with parameters: page={page}, limit={limit}, search={search}, payment_method={payment_method}')
        result = use_case.get_quotations(page, limit, search, record_type, payment_method)
        logger.info(f'Use case returned successfully. Result keys: {result.keys()}')

        response = ResponseUtils.success_response(result)
        logger.info(f'=== GET QUOTATIONS HANDLER COMPLETED SUCCESSFULLY ===')
        return response
    
    except Exception as e:
        logger.error(f'ERROR in lambda_handler: {type(e).__name__}: {str(e)}', exc_info=True)
        raise
