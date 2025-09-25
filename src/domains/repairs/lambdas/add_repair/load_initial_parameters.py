import base64
import json
import re
from datetime import datetime
from requests_toolbelt.multipart import decoder

from exceptions import validation_exception
from utils.uuid_generator import generate_uuid_hex, generate_short_numeric


def load_initial_parameters(event) -> dict:
    print("Begin loading_initial_parameters")
    # print(f"Event: {event}")

    # requestBody = event.get("body", None)
    requestBody = format_data(event)

    # requestBody = json.loads(requestBody)
    print(f"Request body: {requestBody}")
    validate_fields(requestBody)

    return generate_repair_data(requestBody)


def format_data(event) -> dict:
    print("Begin format_data")

    headers = {k.lower(): v for k, v in (event.get("headers") or {}).items()}
    content_type = headers.get("content-type")
    body = event.get("body")

    if body is None:
        return {
            "statusCode": 400,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"message": "Se debe proporcionar el cuerpo de la petición"})
        }

    # Decodificar correctamente los bytes
    if event.get("isBase64Encoded", False):
        body_bytes = base64.b64decode(body)
    else:
        body_bytes = body.encode("utf-8")  # ¡no latin-1, ni errors="ignore"!

    # Parse multipart
    multipart_data = decoder.MultipartDecoder(body_bytes, content_type)

    photos = []
    payload = None

    for idx, part in enumerate(multipart_data.parts):
        disposition = part.headers.get(b"Content-Disposition", b"").decode(errors="ignore")

        name_match = re.search(r'name="([^"]+)"', disposition) or re.search(r'name=([^;]+)', disposition)
        part_name = name_match.group(1).strip('" ') if name_match else None

        filename_match = re.search(r'filename="([^"]+)"', disposition)
        filename = filename_match.group(1) if filename_match else None

        if part_name in ("payload", "body"):
            try:
                payload = json.loads(part.text)
            except Exception as e:
                print(f"[format_data] Error parseando JSON: {e}")
                payload = {}
        elif part_name == "photos" or filename:
            photos.append({
                "filename": filename,
                "content": part.content  # bytes puros, listos para Supabase
            })

    result = {}
    if payload:
        result.update(payload)
    if photos:
        result["photos"] = photos

    print("payload presente?:", bool(payload))
    print("cantidad photos:", len(photos))

    return result



def validate_fields(request_body: dict):
    print("Begin validate_fields")
    required_fields = {
        dict: ["repair", "vehicle", "labor"],
        list: ["products", "photos"]
    }

    validation_exception.validate_fields(request_body, required_fields)

    vehicle = request_body["vehicle"]
    vehicle_fields = {
        str: ["id_customer", "license_plate", "brand", "model", "color"],
        int: ["year", "mileage"]
    }

    validation_exception.validate_fields(vehicle, vehicle_fields)

    repair_fields = {
        str: ["id_mechanic", "fault_description", "diagnosis", "status", "priority", "notes", "id_created_by"],
        datetime: ["entry_date"],
        float: ["estimated_cost"]
    }

    repair = request_body["repair"]
    validation_exception.validate_fields(repair, repair_fields)

    labor_fields = {
        str: ["id_service_type"],
        datetime: ["start_date", "completion_date"],
        int: ["actual_hours"],
        float: ["agreed_price"],
        bool: ["completed"]
    }
    labor = request_body["labor"]
    validation_exception.validate_fields(labor, labor_fields)

    product_fields = {
        str: ['id_product'],
        int: ['quantity', 'stock'],
        float: ['unit_price', 'discount']
    }

    field_rules = {
        "discount": {"allow_zero": True},
    }
    products = request_body["products"]
    for idx, product in enumerate(products, start=1):

        if not isinstance(product, dict):
            raise ValueError(f"Cada producto debe ser un objeto válido (error en producto #{idx})")

        validation_exception.validate_fields(product, product_fields, context="products", field_rules=field_rules)
    # photos = request_body["photos"]


def generate_repair_data(request_body: dict) -> dict:
    print("Begin generate_repair_data")

    id_vehicle = request_body["vehicle"].get("id_vehicle", generate_uuid_hex())
    id_repair = generate_uuid_hex()
    vehicle = {
        "id_vehicle": id_vehicle,
        "id_customer": request_body["vehicle"]["id_customer"],
        "license_plate": request_body["vehicle"]["license_plate"],
        "brand": request_body["vehicle"]["brand"],
        "model": request_body["vehicle"]["model"],
        "year": request_body["vehicle"]["year"],
        "color": request_body["vehicle"]["color"],
        "mileage": request_body["vehicle"]["mileage"],
        "active": True
    }

    repair = {
        "id_repair": id_repair,
        "order_number": generate_short_numeric(),
        "id_vehicle": vehicle["id_vehicle"],
        "id_mechanic": request_body["repair"]["id_mechanic"],
        "fault_description": request_body["repair"]["fault_description"],
        "diagnosis": request_body["repair"]["diagnosis"],
        "status": request_body["repair"]["status"],
        "priority": request_body["repair"]["priority"],
        "entry_date": request_body["repair"]["entry_date"],
        "notes": request_body["repair"]["notes"],
        "estimated_cost": request_body["repair"]["estimated_cost"],
        "id_created_by": request_body["repair"]["id_created_by"],
    }

    labor = {
        "id_repair_service": generate_uuid_hex(),
        "id_repair": id_repair,
        **request_body["labor"]
    }

    materials = []

    for product in request_body["products"]:
        material = {
            "id_repair_material": generate_uuid_hex(),
            "id_vehicle": id_vehicle,
            **product,
        }
        materials.append(material)

    repair_data = {
        "repair": repair,
        "vehicle": vehicle,
        "labor": labor,
        "materials": materials,
        "photos": request_body["photos"]
    }

    return repair_data
