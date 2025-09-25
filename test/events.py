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
             "products": [{'id_product': 'a9a57032-1bdc-4dc0-b8b2-b72317c0fff5', 'quantity': 5, 'unit_price': 30.00,
                           'discount': 0.00}, ],
             "subtotal": 150.00, "total": 172.50})
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
            "id_number": "1753532041",
            "name": "Lesly",
            "surname": "Villarruel",
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
