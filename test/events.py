import json

events = {
    "get_customers": {
        "httpMethod": "GET",
        "path": "/customers",
        "queryStringParameters": {"page": "1", "limit": "5", "search": "Laura"}
    },
    "get_customer_by_id": {
        "httpMethod": "GET",
        "path": "/customers",
        "queryStringParameters": {"id_number": "5647382910567"}
    },
    "get_mechanics": {
        "httpMethod": "POST",
        "path": "/mechanics",
        "body": json.dumps({"order_id": "456", "product": "Zapatos"})
    },
    "get_product_by_id": {
        "httpMethod": "GET",
        "path": "/products",
        "queryStringParameters": {"id_product": "b03196fd-a140-4781-a529-3862119f8b8c"}
    },
    "get_products": {
        "httpMethod": "POST",
        "path": "/products",
        "body": json.dumps({"order_id": "456", "product": "Zapatos"})
    },
    "add_product": {
        "httpMethod": "POST",
        "path": "/products",
        "body": json.dumps({
            "code": "TESTBACK",
            "name": "PRODUCTO BACK",
            "description": "Producto subido desde back",
            "price": 23.50,
            "stock": 10,
            "min_stock": 20,
            "max_stock": 30,
            "id_supplier": "4cfff20a-b6ef-47ec-acda-0daa132af7dc",
            "id_category": "1cda8459-7235-4be5-b3e7-498b0518e3dd",
            "id_brand": "b3b093f4-f05a-41a0-8dd5-5892d7efe05d",
            "model": "Corolla",
            "active": True,
            # "created_at": self.created_at,
            # "updated_at": self.updated_at
        })
    },
    "add_sale": {
        "httpMethod": "POST",
        "path": "/sales",
        "body": json.dumps(
            {"id_customer": "136daed3-3b83-4733-9ea2-2f06bea74ff7", "id_seller": "98abe20d-b97d-4b0f-8a50-386a6d75e47b",
             "products": [
                 {'id_product': 'a9a57032-1bdc-4dc0-b8b2-b72317c0fff5', 'quantity': 5, 'unit_price': 30.00,
                  'stock': 100,
                  'discount': 0.00},
                 {'id_product': 'b03196fd-a140-4781-a529-3862119f8b8c', 'quantity': 3, 'unit_price': 15.00,
                  'stock': 50,
                  'discount': 0.00}, ],
             "subtotal": 150.00, "total": 300.00})
    },
    "add_repair": {
        "httpMethod": "POST",
        "path": "/repair",
        "body": json.dumps({
            "vehicle": {
                "id_customer": "136daed3-3b83-4733-9ea2-2f06bea74ff7",
                "license_plate": "sdfsdfsd",
                "brand": "sdfsdf",
                "model": "sdfsdf",
                "year": 56756,
                "color": "sdfsdf",
                "mileage": 56475675,
                "active": True
            },
            "repair": {
                "id_mechanic": "33c80fa0-f13e-4961-a9aa-ab21fb213c0c",
                "fault_description": "Detalle del dano",
                "diagnosis": "Algo se dano",
                "status": "pending",
                "priority": "high",
                "entry_date": "2025-09-20T14:35:00",
                "delivery_date": "2025-09-20T14:35:00",
                "notes": "El carro esta danado",
                "estimated_cost": 34343.44,
                "final_cost": 34343.44,
                "id_created_by": "98abe20d-b97d-4b0f-8a50-386a6d75e47b",

            },
            "labor": {
                "id_service_type": "98abe20d-b97d-4b0f-8a50-386a6d75e47b",
                "agreed_price": 33.33,
                "actual_hours": 48,
                "completed": False,
                "start_date": "2025-09-23T14:35:00",
                "completion_date": "2025-09-25T14:35:00",
            },
            "products": [
                {'id_product': 'a9a57032-1bdc-4dc0-b8b2-b72317c0fff5', 'quantity': 6, 'unit_price': 30.00,
                 'stock': 90,
                 'discount': 0.00, "subtotal": 180.00, "type": "repair",
                 "usage_date": "2025-09-24T14:35:00", },
                {'id_product': 'b03196fd-a140-4781-a529-3862119f8b8c', 'quantity': 5, 'unit_price': 15.00,
                 'stock': 44,
                 'discount': 0.00, "subtotal": 75.00, "type": "repair", "usage_date": "2025-09-25T14:35:00", }, ],
            "photos": [{}]
        })
    },
    "get_suppliers": {
        "httpMethod": "GET",
        "path": "/orders",
        "body": json.dumps({"order_id": "456", "product": "Zapatos"})
    },
    
    "add_mechanic": {
        "httpMethod": "POST",
        "path": "/mechanics",
        "body": json.dumps({
            "name": "Juan Pérez",
            "phone": "555-1234",
            "email": "juan@example.com"
        })
    },
    "add_customer": {
        "httpMethod": "POST",
        "path": "/customers",
        "body": json.dumps({
            "id_number": "0803473784",
            "name": "Jonathan",
            "surname": "Valencia",
            "address": "La Ermita",
            "phone": "0987621276",
            "email": "lesly123@gmail.com",
            "identification_type": "id_card",
            # "birth_date": "2001-05-21",
            "gender": "female",
            "active": True,
            # "created_at": self.created_at,
            # "updated_at": self.updated_at
        })
    },
    "get_mechanics": {
        "httpMethod": "GET",
        "path": "/mechanics",
        "queryStringParameters": {"page": "1", "limit": "5"}
    }
}
