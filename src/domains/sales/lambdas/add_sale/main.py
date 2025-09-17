import json

from db.db_client import DBClient
from load_initial_parameter import load_initial_parameters
from repositories.sale_detail_repository import SaleDetailRepository
from repositories.sale_repository import SaleRepository
from use_cases.sale_use_case import SaleUseCase

# from repositories.customer_repository import CustomerRepository
# from repositories.seller_repository import SellerRepository
# from use_cases.customer_use_case import CustomerUseCase
# from use_cases.seller_use_case import SellerUseCase

db_client = DBClient.get_client()
sale_repository = SaleRepository(db_client)
sale_detail_repository = SaleDetailRepository(db_client)
use_case = SaleUseCase(sale_repository, sale_detail_repository)


def lambda_handler(event, context):
    try:
        sale_data = load_initial_parameters(event)

        # customer_repository = CustomerRepository(db_client)
        # customer_use_case = CustomerUseCase(customer_repository)
        # is_customer_exists = customer_use_case.is_customer_exists(sale_data["sale"]["id_customer"])
        # if not is_customer_exists:
        #     return {
        #         "statusCode": 400,
        #         "body": json.dumps({"message": f"El cliente con id {sale_data["sale"]["id_customer"]} no existe"})
        #     }
        # seller_repository = SellerRepository(db_client)
        # seller_use_case = SellerUseCase(seller_repository)
        # is_seller_exists = seller_use_case.is_seller_exists(sale_data["sale"]["id_seller"])
        # if not is_seller_exists:
        #     return {
        #         "statusCode": 400,
        #         "body": json.dumps({"message": f"El vendedor con id {sale_data["sale"]["id_seller"]} no existe"})
        #     }
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
