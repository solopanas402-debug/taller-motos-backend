import json

from events import events
from lambdas import get_lambda


class Context:
    def __init__(self):
        self.function_name = "local-lambda-test"
        self.memory_limit_in_mb = 128
        self.invoked_function_arn = "arn:aws:lambda:local:test"
        self.aws_request_id = "1234"


context = Context()


def run(lambda_name, event_name):
    # if lambda_name not in LAMBDA_MODULES:
    #     raise ValueError(f"Lambda '{lambda_name}' no encontrada")
    if event_name not in events:
        print(f"Evento '{event_name}' no encontrado.")
        return

    # lambda_function = lambdas[lambda_name]
    lambda_function = get_lambda(lambda_name)
    event = events[event_name]

    print(f"\n=== Ejecutando {lambda_name} con evento {event_name} ===\n")
    result = lambda_function(event, context)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    # lambda_name = "add_product"
    resource_name = "get_suppliers"
    run(resource_name, resource_name)
    # run("orders_post", "orders_post")
