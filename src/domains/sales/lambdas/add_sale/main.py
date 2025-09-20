import json

from db.db_client import DBClient
from load_initial_parameter import load_initial_parameters
from repositories.sale_detail_repository import SaleDetailRepository
from repositories.sale_repository import SaleRepository
from use_cases.sale_use_case import SaleUseCase

db_client = DBClient.get_client()
sale_repository = SaleRepository(db_client)
sale_detail_repository = SaleDetailRepository(db_client)
use_case = SaleUseCase(sale_repository, sale_detail_repository)


def lambda_handler(event, context):
    try:
        sale_data = load_initial_parameters(event)
        response_sale = use_case.add_sale(sale_data)

        return {
            "statusCode": 201,
            "body": json.dumps(response_sale)
        }

    except ValueError as ve:
        return {
            "statusCode": 400,
            "body": json.dumps({
                "message": str(ve),
            }),
        }

    except TypeError as te:
        return {
            "statusCode": 400,
            "body": json.dumps({
                "message": str(te)
            })
        }

    except Exception as e:
        print(f'Error al registrar la venta: {e}')
        return {
            "statusCode": 501,
            "body": json.dumps({
                "message": str(e),
            }),
        }
