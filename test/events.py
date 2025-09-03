import json

events = {
    "get_customers": {
        "httpMethod": "GET",
        "path": "/customers",
        "queryStringParameters": {"id": "123"}
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
    "get_suppliers": {
        "httpMethod": "providers",
        "path": "/orders",
        "body": json.dumps({"order_id": "456", "product": "Zapatos"})
    }
}
