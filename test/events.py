import json

events = {
    "customers_get": {
        "httpMethod": "GET",
        "path": "/customers",
        "queryStringParameters": {"id": "123"}
    },
    "mechanics_get": {
        "httpMethod": "POST",
        "path": "/mechanics",
        "body": json.dumps({"order_id": "456", "product": "Zapatos"})
    },
    "products_get": {
        "httpMethod": "POST",
        "path": "/products",
        "body": json.dumps({"order_id": "456", "product": "Zapatos"})
    },
    "providers_get": {
        "httpMethod": "providers",
        "path": "/orders",
        "body": json.dumps({"order_id": "456", "product": "Zapatos"})
    }
}
