import json
from repositories.customer_repository import CustomerRepository
from use_cases.customer_use_cases import CustomerUseCase

repository = CustomerRepository()
use_case = CustomerUseCase(repository)

def lambda_handler(event, context):
    print(f'event: {event}')
    print(f'context: {context}')
    params = event.get("queryStringParameters") or {}
    page = int(params.get("page", 1))
    limit = int(params.get("limit", 10))
    search = params.get("search")
    try:
        result = use_case.get_customers(page, limit, search)
        return {
            "statusCode": 200,
            "body": json.dumps(result)
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"message": str(e)})
        }
