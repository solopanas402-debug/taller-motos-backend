import json

from repositories.product_repository import ProductRepository
from use_cases.product_use_cases import ProductUseCase
from db.db_client import DBClient

db_client = DBClient().get_client()
repository = ProductRepository(db_client)
usecase = ProductUseCase(repository)


def lambda_handler(event, context):
    print(f"event: {event}")
    print(f"context: {context}")

    params = event.get("queryStringParameters") or {}
    page = int(params.get("page", 1))
    limit = int(params.get("limit", 10))
    search = params.get("search")

    try:
        response = usecase.get_all_products(page, limit, search)
    except Exception as e:
        return {
            "statusCode": 501,
            "body": json.dumps({
                "message": "Ha ocurrido un problema al consultar los productos"
            })
        }

    return {
        "statusCode": 200,
        "body": json.dumps(response)
    }
