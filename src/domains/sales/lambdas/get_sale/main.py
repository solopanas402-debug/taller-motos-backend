import json

from db.db_client import DBClient
from repositories.sale_repository import SaleRepository
from use_cases.sale_use_case import SaleUseCase


db_client = DBClient.get_client()
repository = SaleRepository(db_client)
use_case = SaleUseCase(repository)


def lambda_handler(event, context):
    print(f"event: {event}")
    print(f"context: {context}")
    params = event.get("queryStringParameters") or {}
    page = int(params.get("page", 1))
    limit = int(params.get("limit", 10))
    search = params.get("search")
    try:
        result = use_case.get_sales(page, limit, search)
        return {"statusCode": 200, "body": json.dumps(result)}
    except Exception as e:
        return {"statusCode": 500, "body": json.dumps({"message": str(e)})}


