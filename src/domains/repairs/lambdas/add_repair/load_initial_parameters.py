import json
from datetime import datetime

from exceptions import validation_exception
from utils.uuid_generator import generate_uuid_hex, generate_short_numeric


def load_initial_parameters(event) -> dict:
    print("Begin loading_initial_parameters")
    print(f"Event: {event}")

    requestBody = event.get("body", None)
    if requestBody is None:
        return {
            "statusCode": 400,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"message": "Se debe proporcionar el cuerpo de la peticion"})
        }

    requestBody = json.loads(requestBody)
    print(f"Request body: {requestBody}")
    validate_fields(requestBody)

    return generate_repair_data(requestBody)


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
        "materials": materials
    }

    return repair_data
