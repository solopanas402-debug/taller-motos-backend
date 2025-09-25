import json
import uuid
from datetime import datetime, timezone

from entities.gender import Gender
from entities.identification_type import IdentificationType
from src.domains.customers.entities.customer import Customer
from utils.validators import validate_length

def load_initial_parameters(event):
    print('Begin load_initial_parameters')
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

    # Validar campos requeridos
    validate_customer_fields(request_body)

    # Obtener campos opcionales con default None
    address = request_body.get("address")
    phone = request_body.get("phone")
    email = request_body.get("email")
    identification_type = request_body.get("identification_type")
    birth_date_str = request_body.get("birth_date")
    gender = request_body.get("gender")

    # Validar enums si están presentes
    if identification_type and identification_type not in IdentificationType._value2member_map_:
        raise TypeError(f"El campo 'identification_type' debe ser uno de los siguientes valores: {[e.value for e in IdentificationType]}")

    if gender and gender not in Gender._value2member_map_:
        raise TypeError(f"El campo 'gender' debe ser uno de los siguientes valores: {[e.value for e in Gender]}")

    # Parsear birth_date si viene
    birth_date = None
    if birth_date_str:
        try:
            birth_date = datetime.strptime(birth_date_str, "%Y-%m-%d").date()
        except ValueError:
            raise ValueError("El campo 'birth_date' debe tener el formato 'YYYY-MM-DD'")

    # Crear el objeto Customer
    customer = Customer(
        id_customer=str(uuid.uuid4()),
        id_number=request_body["id_number"],
        name=request_body["name"],
        surname=request_body["surname"],
        address=address,
        phone=phone,
        email=email,
        identification_type=identification_type,
        birth_date=birth_date,
        gender=gender,
        active=True,
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc)
    )

    return customer


def validate_customer_fields(customer: dict):
    required_fields = ['id_number', 'name', 'surname']

    for field in required_fields:
        if field not in customer or customer[field] is None:
            raise ValueError(f"El campo '{field}' es obligatorio.")

        value = customer[field]
        if not isinstance(value, str):
            raise TypeError(f"El campo '{field}' debe ser una cadena de caracteres.")

        validate_length(field, value, min_len=1, max_len=255)