import json
from db.db_client import DBClient
from repositories.supplier_repository import SupplierRepository
from use_cases.supplier_use_case import SupplierUseCase

db_client = DBClient.get_client()
repository = SupplierRepository(db_client)
use_case = SupplierUseCase(repository)

def lambda_handler(event, context):
    print(f'event: {event}')
    print(f'context: {context}')
    
    params = event.get("queryStringParameters") or {}
    page = int(params.get("page", 1))
    limit = int(params.get("limit", 10))
    search = params.get("search")
    
    try:
        result = use_case.get_suppliers(page, limit, search)
        return {
            "statusCode": 200,
            "body": json.dumps(result, default=str)  # default=str para manejar tipos UUID y datetime
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"message": str(e)})
        }