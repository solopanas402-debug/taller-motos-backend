import json
from datetime import datetime, timezone
from entities.product import Product
from exceptions import validation_exception
from utils.uuid_generator import generate_uuid_hex


def load_initial_parameters(event):
    print(f'Begin load_initial_parameters')
    print(f'Event: {event}')

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

    validate_product_fields(request_body)

    product = Product(id_product=generate_uuid_hex(), code=request_body["code"], name=request_body["name"],
                      description=request_body["description"], price=float(request_body["price"]),
                      stock=int(request_body["stock"]), min_stock=int(request_body.get("min_stock", 0)),
                      max_stock=int(request_body.get("max_stock", 0)),
                      id_supplier=request_body["id_supplier"],
                      id_category=request_body.get("id_category", ""),
                      id_brand=request_body.get("id_brand", ""),
                      model=request_body.get("model", ""),
                      active=True,
                      created_at=datetime.now(timezone.utc),
                      updated_at=datetime.now(timezone.utc))

    return product


def validate_product_fields(product: dict):
    required_fields = {
        str: ['code', 'name', 'description', 'id_supplier', 'id_category', 'id_brand'],
        int: ['stock', 'min_stock', 'max_stock'],
        float: ['price'],
        bool: ['active']
    }

    validation_exception.validate_fields(product, required_fields, )
