import json

from repositories.product_repository import ProductRepository
from use_cases.product_use_cases import ProductUseCase
from db.db_client import DBClient

db_client = DBClient().get_client()
repository = ProductRepository(db_client)
usecase = ProductUseCase(repository)


def lambda_handler(event, context):
    print(f'event: {event}')
    print(f'context: {context}')

    try:
        response = usecase.get_all_products()
        print(f'Productos recuperados: {response}')
    except Exception as e:
        print(f'Error al consultar los productos: {e}')
        return {
            "statusCode": 501,
            "body": json.dumps({
                "message": "A ocurrido un problema al consultar los productos",
                # "input": event
            })
        }

    return {
        "statusCode": 200,
        "body": json.dumps({
            "data": response,
            # "input": event
        })
    }
