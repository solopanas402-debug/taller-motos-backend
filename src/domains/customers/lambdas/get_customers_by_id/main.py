import json

from repositories.customer_repository import CustomerRepository
from use_cases.customer_use_cases import CustomerUseCase

repository = CustomerRepository()
usecase = CustomerUseCase(repository)


def lambda_handler(event, context):
    print(f'event: {event}')
    print(f'context: {context}')

    parameters = event.get('queryStringParameters', None)

    if parameters is None:
        return {
            "statusCode": 400,
            "body": json.dumps({
                "message": f"Se debe proporcionar el id del cliente",
            })
        }

    id = parameters['id_number']

    customer = None

    try:
        customer = usecase.get_customer_by_id(id)

        print(f'Product recuperado: {customer}')

        if customer is None:
            return {
                "statusCode": 200,
                "body": json.dumps({
                    "message": f"No se ha encontrado cliente con id: {id}",
                })
            }

        print(f'Productos recuperado: {customer}')
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
            "data": customer,
            # "input": event
        })
    }
