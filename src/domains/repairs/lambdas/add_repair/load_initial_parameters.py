import base64
import json
import os
import re
from datetime import datetime
from requests_toolbelt.multipart import decoder

from exceptions import validation_exception
from utils.uuid_generator import generate_uuid_hex, generate_short_numeric

import logging

logging.basicConfig(filename='event.log', level=logging.DEBUG)


def load_initial_parameters(event) -> dict:
    print("Begin loading_initial_parameters")

    requestBody = format_data(event)

    print(f"Request body: {requestBody}")
    validate_fields(requestBody)

    return generate_repair_data(requestBody)


def format_data(event) -> dict:
    print("Begin format_data")

    headers = {k.lower(): v for k, v in (event.get("headers") or {}).items()}
    content_type = headers.get("content-type", "")
    body = event.get("body")

    if body is None:
        return {
            "statusCode": 400,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"message": "Se debe proporcionar el cuerpo de la petición"})
        }

    if event.get("isBase64Encoded", False):
        body_bytes = base64.b64decode(body)
    else:
        body_bytes = body if isinstance(body, (bytes, bytearray)) else body.encode()

    result = {}
    photos = []

    if "multipart/form-data" in content_type.lower():
        multipart_data = decoder.MultipartDecoder(body_bytes, content_type)

        for idx, part in enumerate(multipart_data.parts):
            disposition = part.headers.get(b"Content-Disposition", b"").decode(errors="ignore")
            name_match = re.search(r'name="([^"]+)"', disposition) or re.search(r'name=([^;]+)', disposition)
            part_name = name_match.group(1).strip('" ') if name_match else None
            filename_match = re.search(r'filename="([^"]+)"', disposition)
            filename = filename_match.group(1) if filename_match else None

            if part_name in ("payload", "body"):
                try:
                    payload_str = part.content.decode("utf-8")
                    payload = json.loads(payload_str)
                    result.update(payload)
                except Exception as e:
                    print(f"[format_data] Error parseando JSON: {e}")
            elif part_name == "photos" or filename:
                photos.append({
                    "filename": filename,
                    "content": part.content
                })

    else:
        try:
            result = json.loads(body_bytes.decode("utf-8"))
        except Exception as e:
            print(f"[format_data] Error parseando JSON raw: {e}")
            result = {}

    if photos:
        result["photos"] = photos

    logging.debug(f"IMAGES: {photos}")


    return result


def validate_fields(request_body: dict):
    print("Begin validate_fields")
    
    # Define optional rules
    optional_rule = {"required": False}
    allow_zero_rule = {"allow_zero": True, "required": False}
    
    # 1. Root level requirements
    # 'labor' and 'products' are now optional from frontend perspective
    required_fields = {
        dict: ["repair", "vehicle"]
    }
    validation_exception.validate_fields(request_body, required_fields)

    # ... (vehicle validations were here)
    vehicle = request_body["vehicle"]
    vehicle_schema = {
        str: ["id_customer", "license_plate", "brand", "model", "color"],
        int: ["year", "mileage"]
    }
    vehicle_rules = {
        "color": optional_rule,
        "year": optional_rule,
        "mileage": allow_zero_rule
    }
    validation_exception.validate_fields(vehicle, vehicle_schema, context="vehículo", field_rules=vehicle_rules)

    # 3. Repair validations
    repair = request_body["repair"]
    repair_schema = {
        str: ["id_mechanic", "fault_description", "diagnosis", "status", "priority", "notes", "id_created_by", "entry_date", "delivery_date"],
        (float, int): ["estimated_cost", "final_cost"]
    }
    repair_rules = {
        "diagnosis": optional_rule,
        "delivery_date": optional_rule,
        "final_cost": allow_zero_rule,
        "notes": optional_rule,
        "estimated_cost": allow_zero_rule,
        "priority": optional_rule
    }
    validation_exception.validate_fields(repair, repair_schema, context="reparación", field_rules=repair_rules)

    # 4. Labor validations (Optional section)
    labor = request_body.get("labor")
    if labor:
        labor_schema = {
            str: ["id_service_type", "start_date", "completion_date"],
            int: ["actual_hours"],
            (float, int): ["agreed_price"],
            bool: ["completed"]
        }
        labor_rules = {
            "id_service_type": optional_rule,
            "start_date": optional_rule,
            "completion_date": optional_rule,
            "actual_hours": allow_zero_rule,
            "agreed_price": allow_zero_rule,
            "completed": optional_rule
        }
        validation_exception.validate_fields(labor, labor_schema, context="mano de obra", field_rules=labor_rules)

    # 5. Products validation (Optional)
    products = request_body.get("products")
    if products:
        product_fields = {
            str: ['id_product'],
            int: ['quantity', 'stock'],
            (float, int): ['unit_price', 'discount']
        }
        field_rules_products = {
            "discount": {"allow_zero": True},
        }
        for idx, product in enumerate(products, start=1):
            if not isinstance(product, dict):
                raise ValueError(f"Cada producto debe ser un objeto válido (error en producto {idx})")
            validation_exception.validate_fields(product, product_fields, context=f"el producto {idx}", field_rules=field_rules_products)


def generate_repair_data(request_body: dict) -> dict:
    print("Begin generate_repair_data")

    id_vehicle = request_body["vehicle"].get("id_vehicle", generate_uuid_hex())
    id_repair = generate_uuid_hex()
    
    vehicle_req = request_body["vehicle"]
    vehicle = {
        "id_vehicle": id_vehicle,
        "id_customer": vehicle_req["id_customer"],
        "license_plate": vehicle_req["license_plate"],
        "brand": vehicle_req["brand"],
        "model": vehicle_req["model"],
        "year": vehicle_req.get("year"),
        "color": vehicle_req.get("color", ""),
        "mileage": vehicle_req.get("mileage", 0),
        "active": True
    }

    repair_req = request_body["repair"]
    labor_req = request_body.get("labor", {})
    
    repair = {
        "id_repair": id_repair,
        "order_number": generate_short_numeric(),
        "id_vehicle": vehicle["id_vehicle"],
        "id_mechanic": repair_req["id_mechanic"],
        "fault_description": repair_req["fault_description"],
        "diagnosis": repair_req.get("diagnosis", ""),
        "status": repair_req["status"],
        "priority": repair_req.get("priority", "medium"),
        "entry_date": repair_req["entry_date"],
        "start_date": labor_req.get("start_date"),
        "completion_date": labor_req.get("completion_date"),
        "delivery_date": repair_req.get("delivery_date"),
        "notes": repair_req.get("notes", ""),
        "estimated_cost": repair_req.get("estimated_cost", 0.0),
        "final_cost": repair_req.get("final_cost", 0.0),
        "id_created_by": repair_req["id_created_by"],
    }

    labor = {
        "id_repair_service": generate_uuid_hex(),
        "id_repair": id_repair,
        "id_service_type": labor_req.get("id_service_type", "53ec546e-c0c8-4b37-b554-0eefab310602"),
        "start_date": labor_req.get("start_date"),
        "completion_date": labor_req.get("completion_date"),
        "actual_hours": labor_req.get("actual_hours", 0),
        "agreed_price": labor_req.get("agreed_price", 0.0),
        "completed": labor_req.get("completed", False)
    }

    materials = []
    products_req = request_body.get("products", [])
    for product in products_req:
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
    }

    if request_body.get("photos"):
        repair_data["photos"] = request_body["photos"]

    return repair_data