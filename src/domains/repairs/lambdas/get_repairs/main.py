import json

from db.db_client import DBClient
from repositories.repair_repository import RepairRepository
from use_cases.repair_use_case import RepairUseCase


db_client = DBClient.get_client()
repository = RepairRepository(db_client)
use_case = RepairUseCase(repository)


def lambda_handler(event, context):
    print(f"event: {event}")
    print(f"context: {context}")
    params = event.get("queryStringParameters") or {}
    page = int(params.get("page", 1))
    limit = int(params.get("limit", 10))
    search = params.get("search")
    try:
        result = use_case.get_repairs(page, limit, search)
        return {"statusCode": 200, "body": json.dumps(result)}
    except Exception as e:
        return {"statusCode": 500, "body": json.dumps({"message": str(e)})}


