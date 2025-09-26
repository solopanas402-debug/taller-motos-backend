import json

from db.db_client import DBClient
from exceptions.validation_exception import ValidationException
from src.domains.bulk_products.lambdas.add_products.load_initial_parameters import load_initial_parameters
from src.domains.bulk_products.lambdas.add_products.repositories.product_repository import ProductRepository
from src.domains.bulk_products.lambdas.add_products.use_cases.product_use_case import ProductUseCase

db_client = DBClient.get_client()
repository = ProductRepository(db_client)
use_case = ProductUseCase(repository)


def lambda_handler(event, context):
    print(f'event: {event}')

    try:
        products = load_initial_parameters(event)
        response = use_case.execute(products)

        return {
            "statusCode": 201,
            "body": json.dumps({
                "data": response,
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
        print(f'Error al registrar la reparacion: {e}')
        return {
            "statusCode": 500,
            "body": json.dumps({
                "message": str(e),
            })
        }
