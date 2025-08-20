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
        "queryStringParameters": {"id": "0d319f34-8197-4940-9473-8ae7c9dbb27b"}
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
            "provider_id": "51cae105-eea6-4cc5-a9f9-3e9692b5c7b1",
            "category": "Pruebas",
            "brand": "PRUEBA",
            "is_active": True,
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
