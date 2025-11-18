import json
from datetime import datetime, timezone
from utils.response_utils import ResponseUtils


def load_initial_parameters(event):
    """
    Loads and validates supplier update parameters from the event.
    Returns a tuple: (id_supplier, update_data)
    """
    print(f'Begin load_update_parameters')
    print(f'Event: {event}')

    # Get supplier ID from path parameters
    path_parameters = event.get('pathParameters', None)
    if path_parameters is None or 'id' not in path_parameters:
        return ResponseUtils.bad_request_response(
            "Se debe proporcionar el ID de la cotización en la ruta"
        )

    id_sale = path_parameters['id']
    if not id_sale or id_sale.strip() == '':
        return ResponseUtils.bad_request_response(
            "El ID de la cotización no puede estar vacío"
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
        "status",
        "payment_method"
    ]

    update_data = {}
    for field in allowed_fields:
        if field in data:
            # Validar payment_method si está presente
            if field == "payment_method":
                valid_payment_methods = ['cash', 'transfer', 'debit_card', 'credit_card']
                payment_method = data[field].lower() if isinstance(data[field], str) else data[field]
                if payment_method not in valid_payment_methods:
                    return ResponseUtils.bad_request_response(
                        f"El campo 'payment_method' debe ser uno de: {', '.join(valid_payment_methods)}"
                    )
                update_data[field] = payment_method
            else:
                update_data[field] = data[field]

    # If no valid fields were provided
    if not update_data:
        return ResponseUtils.bad_request_response(
            "No se proporcionaron campos válidos para actualizar"
        )

    # Add updated_at timestamp
    update_data['updated_at'] = datetime.now(timezone.utc).isoformat()

    return id_sale, update_data
