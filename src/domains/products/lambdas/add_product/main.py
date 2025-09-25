import json

from exceptions.validation_exception import ValidationException
from load_initial_parameters import load_initial_parameters
from repositories.product_repository import ProductRepository
from use_cases.product_use_cases import ProductUseCase
from db.db_client import DBClient

db_client = DBClient().get_client()
repository = ProductRepository(db_client)
usecase = ProductUseCase(repository)


def lambda_handler(event, context):
    try:
        product = load_initial_parameters(event)

        response_product = usecase.add_product(product)

        print(f'Productos recuperado: {response_product}')
        return {
            "statusCode": 201,
            "body": json.dumps({
                "data": response_product,
                # "input": event
            })
        }

    except ValidationException as e:
        return {
            "statusCode": 500,
            "body": json.dumps({
                "message": str(e),
            })
        }

    except Exception as e:
        print(f'Error al registrar el producto {e}')
        return {
            "statusCode": 501,
            "body": json.dumps({
                "message": f'No se ha podido registrar el producto',
            })
        }
