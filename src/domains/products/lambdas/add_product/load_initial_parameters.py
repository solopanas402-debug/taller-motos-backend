import json
import uuid
from datetime import datetime, timezone
from entities.product import Product
from utils.validators import validate_length, validate_quantity


def load_initial_parameters(event, context):
    print(f'event: {event}')
    print(f'context: {context}')

    request_body = event.get('body', None)

    if request_body is None:
        return {
            "statusCode": 400,
            "body": json.dumps({
                "message": "Se debe proporcinar el cuerpo de la peticion"
            })
        }

    request_body = json.loads(request_body)

    print(f'request_body: {request_body}')

    validate_fields(request_body)

    product = Product(id=str(uuid.uuid4()), code=request_body["code"], name=request_body["name"],
                      description=request_body["description"], price=float(request_body["price"]),
                      stock=int(request_body["stock"]), min_stock=int(request_body.get("min_stock", 0)),
                      provider_id=request_body["provider_id"],
                      category=request_body.get("category", ""),
                      brand=request_body.get("brand", ""),
                      is_active=True,
                      created_at=datetime.now(timezone.utc),
                      updated_at=datetime.now(timezone.utc))

    return product


def validate_fields(product:dict):
    required_fields = {
        'str' : ['code', 'name', 'description', 'provider_id', 'category', 'brand'],
        'int': ['stock', 'min_stock'],
        'float': ['price'],
        'bool': ['is_active']
    }

    for type, fields in required_fields.items():
        for field in fields:
            if field not in product:
                raise ValueError(f"El campo '{field}' es obligatorio.")
            value = product[field]

            if type == 'str' and not isinstance(value, str):
                raise TypeError(f"El campo '{field}' debe ser una cadena de caracteres.")
            if type == 'int' and not isinstance(value, int):
                raise TypeError(f"El campo '{field}' debe ser entero.")
            if type == 'float' and not isinstance(value, (float, int)):
                raise TypeError(f"El campo '{field}' debe ser decimal (float).")
            if type == 'bool' and not isinstance(value, bool):
                raise TypeError(f"El campo '{field}' debe ser booleano.")

            if type == 'str':
                validate_length(field, value, min_len=1, max_len=255)
            if type in ['int', 'float']:
                validate_quantity(field, value)




