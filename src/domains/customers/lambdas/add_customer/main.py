import json

from src.domains.customers.lambdas.add_customer.load_initial_parameter import load_initial_parameters
from src.domains.customers.lambdas.add_customer.repository.customer_repository import CustomerRepository
from src.domains.customers.lambdas.add_customer.use_cases.customer_use_cases import CustomerUseCase

repository = CustomerRepository()
usecase = CustomerUseCase(repository)


def lambda_handler(event, context):
    try:
        customer = load_initial_parameters(event)

        print(f"CLIENTE RESULTANTE: {customer}")

        response_customer = usecase.add_customer(customer)

        if response_customer is None:
            return {
                "statusCode": 501,
                "body": json.dumps({
                    "message": f"No se ha podido registrar el cliente",
                    # "input": event
                })
            }

        print(f'Cliente recuperado: {response_customer}')

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
        print(f'Error al registrar el cliente {e}')
        return {
            "statusCode": 501,
            "body": json.dumps({
                "message": f'No se ha podido registrar el cliente',
                # "input": event
            })
        }

    return {
        "statusCode": 200,
        "body": json.dumps({
            "data": response_customer,
            # "input": event
        })
    }
