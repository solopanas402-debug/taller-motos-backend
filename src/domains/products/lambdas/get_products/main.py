import json

from repositories.product_repository import ProductRepository
from use_cases.product_use_cases import ProductUseCase
from db.db_client import DBClient


def lambda_handler(event, context):
    print(f'event: {event}')
    print(f'context: {context}')

    db_client = DBClient().get_client()
    repository = ProductRepository(db_client)
    usecase = ProductUseCase(repository)
    products = []

    try:
        products = usecase.get_all_products()
        print(f'Productos recuperados: {products}')
    except Exception as e:
        print(f'Error al consultar los productos: {e}')
        return {
            "statusCode": 501,
            "body": json.dumps({
                "message": "A ocurrido un problema al consultar los productos",
                # "input": event
            })
        }

    # response = dbClient.table("products").select("*").execute()
    # print(f'RESPUESTA DE BD PRODUCTOS: {response}')

    return {
        "statusCode": 200,
        "body": json.dumps({
            "data": products,
            # "input": event
        })
    }
