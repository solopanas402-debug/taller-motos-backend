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
                "message": "Se debe proporcionar el cuerpo de la petición"
            })
        }

    request_body = json.loads(request_body)

    print(f'request_body: {request_body}')

    validated_data = validate_and_convert_product_fields(request_body)

    # Crear instancia del producto
    product = Product(
        id_product=generate_uuid_hex(),
        code=validated_data["code"],
        name=validated_data["name"],
        description=validated_data["description"],
        price=validated_data["price"],
        discount=validated_data.get("discount", 0.0),
        stock=validated_data["stock"],
        min_stock=validated_data.get("min_stock", 0),
        max_stock=validated_data.get("max_stock", 0),
        id_supplier=validated_data["id_supplier"],
        id_category=validated_data.get("id_category", ""),
        id_brand=validated_data.get("id_brand", ""),
        model=validated_data.get("model", ""),
        active=validated_data.get("active", True),
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc)
    )

    return product


def validate_and_convert_product_fields(data: dict) -> dict:
    """
    Valida y convierte los tipos de datos del producto.
    """

    # Tipos esperados
    schema = {
        str: ['code', 'name', 'description', 'id_supplier', 'id_category', 'id_brand', 'model'],
        int: ['stock', 'min_stock', 'max_stock'],
        (int, float): ['price', 'discount'],
        bool: ['active']
    }

    # Reglas de validación
    field_rules = {
        'code': {'required': True},
        'name': {'required': True},
        'description': {'required': True},
        'id_supplier': {'required': True},
        'price': {'required': True, 'allow_zero': False},
        'stock': {'required': True, 'allow_zero': True},
        'discount': {'required': False, 'allow_zero': True},
        'min_stock': {'required': False, 'allow_zero': True},
        'max_stock': {'required': False, 'allow_zero': True},
        'id_category': {'required': False},
        'id_brand': {'required': False},
        'model': {'required': False},
        'active': {'required': False}
    }

    # Validar campos
    validation_exception.validate_fields(data, schema, context="producto", field_rules=field_rules)

    # Conversión de datos numéricos
    converted = data.copy()
    for field in ['price', 'discount']:
        value = converted.get(field)
        if value is None or value == '':
            converted[field] = 0.0 if field == 'discount' else None
        else:
            try:
                converted[field] = float(value)
            except (TypeError, ValueError):
                raise validation_exception.ValidationException(
                    f"El campo {field} debe ser un número válido"
                )

    # Validaciones personalizadas
    validate_business_rules(converted)

    return converted


def validate_business_rules(data: dict):
    """
    Reglas de negocio personalizadas
    """
    min_stock = data.get('min_stock', 0)
    max_stock = data.get('max_stock', 0)
    if min_stock > 0 and max_stock > 0 and min_stock > max_stock:
        raise validation_exception.ValidationException(
            "El stock mínimo no puede ser mayor al stock máximo"
        )

    price = data.get('price', 0)
    if price <= 0:
        raise validation_exception.ValidationException(
            "El precio debe ser mayor a 0"
        )

    discount = data.get('discount', 0)
    if discount < 0 or discount > 100:
        raise validation_exception.ValidationException(
            "El descuento debe estar entre 0 y 100"
        )
