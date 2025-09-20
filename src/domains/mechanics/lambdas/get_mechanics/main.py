import json
from db.db_client import DBClient
from repositories.mechanic_repository import MechanicRepository
from use_cases.mechanic_use_case import MechanicUseCase

db_client = DBClient.get_client()
repository = MechanicRepository(db_client)
use_case = MechanicUseCase(repository)

def lambda_handler(event, context):
    print(f'event: {event}')
    print(f'context: {context}')
    params = event.get("queryStringParameters") or {}
    page = int(params.get("page", 1))
    limit = int(params.get("limit", 10))
    search = params.get("search")
    try:
        result = use_case.get_mechanics(page, limit, search)
        return {
            "statusCode": 200,
            "body": json.dumps(result)
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"message": str(e)})
        }
