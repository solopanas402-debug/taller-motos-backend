import json
import uuid


def load_initial_parameters(event):
    print(f'Begin load_initial_parameters')
    print(f'Event: {event}')

    request_body = event.get('body', None)
    if request_body is None:
        return {
            "statusCode": 400,
            "body": json.dumps({
                "message": "Se debe proporcionar el cuerpo de la petición"
            })
        }

    request_body = json.loads(request_body)
    print(f'request_body: {request_body}')
    validate_fields(request_body)
    sale_date = generate_sale_data(request_body)
    return sale_date


def validate_fields(request_body: dict):
    print("Begin validate_fields")

    required_fields = {
        'str': ['id_customer', 'id_seller'],
        'list': ['products'],
        'float': ['subtotal', 'total'],
    }

    for expected_type, fields in required_fields.items():
        for field in fields:
            if field not in request_body or request_body[field] in [None, "", []]:
                raise ValueError(f"El campo '{field}' es obligatorio y no puede estar vacío")

            value = request_body[field]

            if expected_type == 'str':
                if not isinstance(value, (str, int)) or str(value).strip() == "":
                    raise TypeError(f"El campo '{field}' debe ser una cadena válida")

            elif expected_type == 'list':
                if not isinstance(value, list) or not value:
                    raise TypeError(f"El campo '{field}' debe ser una lista con al menos un elemento")

            elif expected_type == 'float':
                if not isinstance(value, (int, float)):
                    raise TypeError(f"El campo '{field}' debe ser un número")

    product_fields = {
        'str': ['id_product'],
        'int': ['quantity'],
        'float': ['unit_price', 'discount']
    }

    products = request_body["products"]
    for idx, product in enumerate(products, start=1):
        if not isinstance(product, dict):
            raise ValueError(f"Cada producto debe ser un objeto válido (error en producto #{idx})")

        for expected_type, fields in product_fields.items():
            for field in fields:
                if field not in product or product[field] in [None, ""]:
                    raise ValueError(f"El campo '{field}' es obligatorio en producto #{idx}")

                value = product[field]

                if expected_type == 'str':
                    if not isinstance(value, (str, int)) or str(value).strip() == "":
                        raise TypeError(f"El campo '{field}' debe ser un número o cadena válida (producto #{idx})")

                elif expected_type == 'int':
                    if not isinstance(value, int):
                        raise TypeError(f"El campo '{field}' debe ser entero (producto #{idx})")

                elif expected_type == 'float':
                    if not isinstance(value, (int, float)):
                        raise TypeError(f"El campo '{field}' debe ser decimal (producto #{idx})")

    if request_body["total"] < request_body["subtotal"]:
        raise ValueError("El campo 'total' no puede ser menor que 'subtotal'")


def generate_sale_data(request_body: dict) -> dict:
    id_sale = uuid.uuid4().hex
    subtotal = float(request_body["subtotal"])
    total = float(request_body["total"])

    sale = {
        "id_sale": id_sale,
        "invoice_number": uuid.uuid4().int % (10 ** 8),
        "id_customer": request_body["id_customer"],
        "id_seller": request_body["id_seller"],
        "tax": subtotal * 0.15,
        "subtotal": subtotal,
        "total": total,
        "status": "paid"
    }

    details = []
    for product in request_body["products"]:
        quantity = int(product["quantity"])
        unit_price = float(product["unit_price"])
        discount = float(product.get("discount", 0))
        subtotal_product = (unit_price * quantity) - discount

        sale_detail = {
            "id_sale_detail": uuid.uuid4().hex,
            "id_sale": id_sale,
            "id_product": product["id_product"],
            "quantity": quantity,
            "unit_price": unit_price,
            "discount": discount,
            "subtotal": subtotal_product,
        }
        details.append(sale_detail)

    return {
        "sale": sale,
        "details": details
    }


def validate_customer_existance():
    print(f'Begin validate_customer_existance')
