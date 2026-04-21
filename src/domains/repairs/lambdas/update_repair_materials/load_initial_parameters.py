import json
import uuid
from utils.response_utils import ResponseUtils


def load_initial_parameters(event):
    path_parameters = event.get('pathParameters', None)
    if not path_parameters or 'id' not in path_parameters:
        return ResponseUtils.bad_request_response("Se debe proporcionar el ID de la reparación")

    id_repair = path_parameters['id'].strip()
    if not id_repair:
        return ResponseUtils.bad_request_response("El ID de la reparación no puede estar vacío")

    body = event.get('body', None)
    if body is None:
        return ResponseUtils.bad_request_response("El cuerpo de la petición es obligatorio")

    try:
        data = json.loads(body) if isinstance(body, str) else body
    except json.JSONDecodeError:
        return ResponseUtils.bad_request_response("JSON inválido")

    raw_products = data.get('products', [])
    if not isinstance(raw_products, list):
        return ResponseUtils.bad_request_response("El campo 'products' debe ser una lista")

    materials = []
    for p in raw_products:
        if not p.get('id_product'):
            return ResponseUtils.bad_request_response("Cada producto debe tener 'id_product'")
        qty = int(p.get('quantity', 1))
        price = float(p.get('unit_price', p.get('price', 0)))
        discount = float(p.get('discount', 0))
        subtotal = round(qty * price * (1 - discount / 100), 2)
        materials.append({
            "id_repair_material": str(uuid.uuid4()).replace('-', ''),
            "id_repair": id_repair,
            "id_product": p['id_product'],
            "quantity": qty,
            "unit_price": price,
            "discount": discount,
            "subtotal": subtotal,
        })

    return id_repair, materials
