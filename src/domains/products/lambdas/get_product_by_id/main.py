import json

from repositories.product_repository import ProductRepository
from use_cases.product_use_cases import ProductUseCase
from db.db_client import DBClient


def lambda_handler(event, context):
    print(f'event: {event}')
    print(f'context: {context}')

    parameters = event.get('queryStringParameters', None)

    if parameters is None:
        return {
            "statusCode": 400,
            "body": json.dumps({
                "message": f"Se debe proporcionar el id del producto",
            })
        }

    id = parameters['id_product']

    db_client = DBClient().get_client()
    repository = ProductRepository(db_client)
    usecase = ProductUseCase(repository)

    product = None

    try:
        product = usecase.get_product_by_id(id)

        print(f'Product recuperado: {product}')

        if product is None:
            return {
                "statusCode": 200,
                "body": json.dumps({
                    "message": f"No se ha encontrado producto con id: {id}",
                })
            }

        print(f'Productos recuperado: {product}')
    except Exception as e:
        print(f'Error al consultar los productos: {e}')
        return {
            "statusCode": 400,
            "body": json.dumps({
                "message": f"El id del producto no es compatible con el formato uuid: {id}",
            })
        }

    return {
        "statusCode": 200,
        "body": json.dumps({
            "data": product,
            # "input": event
        })
    }
