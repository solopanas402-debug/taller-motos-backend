import json
import uuid
from datetime import datetime, timezone
from utils.response_utils import ResponseUtils


ALLOWED_FIELDS = [
    "status",
    "fault_description",
    "diagnosis",
    "priority",
    "notes",
    "delivery_date",
    "estimated_cost",
    "final_cost",
    "id_mechanic",
]

VALID_STATUSES = ["pending", "in-progress", "completed", "cancelled"]


def load_initial_parameters(event):
    print(f'Begin load_initial_parameters (update_repair)')

    path_parameters = event.get('pathParameters', None)
    if path_parameters is None or 'id' not in path_parameters:
        return ResponseUtils.bad_request_response(
            "Se debe proporcionar el ID de la reparación en la ruta"
        )

    id_repair = path_parameters['id']
    if not id_repair or id_repair.strip() == '':
        return ResponseUtils.bad_request_response(
            "El ID de la reparación no puede estar vacío"
        )

    body = event.get('body', None)
    if not body:
        return ResponseUtils.bad_request_response(
            "El cuerpo de la petición es obligatorio"
        )

    try:
        data = json.loads(body) if isinstance(body, str) else body
    except json.JSONDecodeError:
        return ResponseUtils.bad_request_response(
            "El cuerpo de la petición no tiene un formato JSON válido"
        )

    if not data:
        return ResponseUtils.bad_request_response(
            "Se debe proporcionar al menos un campo para actualizar"
        )

    # Validate status if provided
    if 'status' in data:
        if data['status'] not in VALID_STATUSES:
            return ResponseUtils.bad_request_response(
                f"El campo 'status' debe ser uno de: {', '.join(VALID_STATUSES)}"
            )

    update_data = {field: data[field] for field in ALLOWED_FIELDS if field in data}

    if not update_data and 'products' not in data:
        return ResponseUtils.bad_request_response(
            "No se proporcionaron campos válidos para actualizar"
        )

    if update_data:
        update_data['updated_at'] = datetime.now(timezone.utc).isoformat()

    # Process products/materials if provided
    materials = None
    if 'products' in data:
        raw_products = data['products']
        if not isinstance(raw_products, list):
            return ResponseUtils.bad_request_response("El campo 'products' debe ser una lista")

        materials = []
        for p in raw_products:
            qty = int(p.get("quantity", 1))
            price = float(p.get("unit_price", p.get("price", 0)))
            discount = float(p.get("discount", 0))
            subtotal = round(qty * price * (1 - discount / 100), 2)
            materials.append({
                "id_repair_material": str(uuid.uuid4()).replace('-', ''),
                "id_repair": id_repair,
                "id_product": p.get("id_product"),
                "quantity": qty,
                "unit_price": price,
                "discount": discount,
                "subtotal": subtotal,
            })

        # Auto set status to in-progress when materials are added
        if materials and 'status' not in update_data:
            update_data['status'] = 'in-progress'
            update_data['updated_at'] = datetime.now(timezone.utc).isoformat()

    return id_repair, update_data, materials
