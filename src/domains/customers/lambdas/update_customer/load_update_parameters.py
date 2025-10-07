import json
from datetime import datetime, timezone
from utils.response_utils import ResponseUtils


def load_update_parameters(event):
    """
    Loads and validates customer update parameters from the event.
    Returns a tuple: (id_customer, update_data)
    """
    print(f'Begin load_update_parameters')
    print(f'Event: {event}')

    # Get customer ID from path parameters
    path_parameters = event.get('pathParameters', None)
    if path_parameters is None or 'id' not in path_parameters:
        return ResponseUtils.bad_request_response(
            "Se debe proporcionar el ID del cliente en la ruta"
        )

    id_customer = path_parameters['id']
    if not id_customer or id_customer.strip() == '':
        return ResponseUtils.bad_request_response(
            "El ID del cliente no puede estar vacío"
        )

    # Get request body
    body = event.get('body', None)
    if not body:
        return ResponseUtils.bad_request_response(
            "El cuerpo de la petición es obligatorio"
        )

    try:
        data = json.loads(body)
    except json.JSONDecodeError:
        return ResponseUtils.bad_request_response(
            "El cuerpo de la petición no tiene un formato JSON válido"
        )

    print(f'request_body: {data}')

    # Validate that at least one field is provided for update
    if not data:
        return ResponseUtils.bad_request_response(
            "Se debe proporcionar al menos un campo para actualizar"
        )

    # Prepare update data with only allowed fields
    allowed_fields = [
        "id_number", "name", "surname", "address", "phone", 
        "email", "identification_type", "birth_date", "gender", "active"
    ]
    
    update_data = {}
    for field in allowed_fields:
        if field in data:
            update_data[field] = data[field]

    # If no valid fields were provided
    if not update_data:
        return ResponseUtils.bad_request_response(
            "No se proporcionaron campos válidos para actualizar"
        )

    # Validate email format if provided
    if "email" in update_data and update_data["email"]:
        if not validate_email(update_data["email"]):
            return ResponseUtils.bad_request_response(
                "El formato del correo electrónico no es válido"
            )

    # Validate identification_type if provided
    if "identification_type" in update_data and update_data["identification_type"]:
        valid_types = ["RUC", "CEDULA", "PASAPORTE"]
        if update_data["identification_type"] not in valid_types:
            return ResponseUtils.bad_request_response(
                f"El tipo de identificación debe ser uno de: {', '.join(valid_types)}"
            )

    # Validate gender if provided
    if "gender" in update_data and update_data["gender"]:
        valid_genders = ["M", "F", "OTRO"]
        if update_data["gender"] not in valid_genders:
            return ResponseUtils.bad_request_response(
                f"El género debe ser uno de: {', '.join(valid_genders)}"
            )

    # Add updated_at timestamp
    update_data['updated_at'] = datetime.now(timezone.utc).isoformat()

    return id_customer, update_data


def validate_email(email: str) -> bool:
    """Simple email validation"""
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None