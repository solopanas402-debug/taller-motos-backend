import json

from load_initial_parameters import load_initial_parameters
from repositories.product_repository import ProductRepository
from use_cases.product_use_cases import ProductUseCase
from db.db_client import DBClient

db_client = DBClient().get_client()
repository = ProductRepository(db_client)
usecase = ProductUseCase(repository)


def lambda_handler(event, context):
    response_product = None
    try:
        product = load_initial_parameters(event)

        # print(f"PRODUCTO RESULTANTE: {product}")

        response_product = usecase.add_product(product)

        if response_product is None:
            return {
                "statusCode": 501,
                "body": json.dumps({
                    "message": f"No se ha podido registrar el producto",
                    # "input": event
                })
            }

        print(f'Productos recuperado: {response_product}')

    except ValueError as ve:
        # Captura errores de validación
        return {
            "statusCode": 400,
            "body": json.dumps({
                "message": str(ve)
            })
        }

    except TypeError as te:
        # Captura errores de validación
        return {
            "statusCode": 400,
            "body": json.dumps({
                "message": str(te)
            })
        }

    except Exception as e:
        print(f'Error al registrar el producto {e}')
        return {
            "statusCode": 501,
            "body": json.dumps({
                "message": f'No se ha podido registrar el producto',
                # "input": event
            })
        }

    return {
        "statusCode": 200,
        "body": json.dumps({
            "data": response_product,
            # "input": event
        })
    }
