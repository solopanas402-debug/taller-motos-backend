import datetime
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
        "queryStringParameters": {"page": "1", "limit": "5"}
    },
    "get_product_by_id": {
        "httpMethod": "GET",
        "path": "/products",
        "queryStringParameters": {"id_product": "b03196fd-a140-4781-a529-3862119f8b8c"}
    },
    "get_products": {
        "httpMethod": "GET",
        "path": "/products",
        "queryStringParameters": {"page": "1", "limit": "10", "search": ""}
    },
    "add_product": {
        "httpMethod": "POST",
        "path": "/products",
        "body": json.dumps({
            "code": "TESTBACK 2",
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
    "get_repairs": {
        "httpMethod": "GET",
        "path": "/repair",
        "queryStringParameters": {"page": "1", "limit": "5", "search": ""}
    },
    "get_sales": {
        "httpMethod": "GET",
        "path": "/sales",
        "queryStringParameters": {"page": "1", "limit": "5", "search": "", "recordType": "quote"}
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
    "add_products": {
        "httpMethod": "POST",
        "path": "/bulk_products",
        "body": json.dumps([
            {
                "code": "MECH004",
                "name": "Amortiguador trasero",
                "description": "Amortiguador trasero hidráulico para SUV",
                "price": 110.00,
                "stock": 25,
                "min_stock": 8,
                "max_stock": 50,
                "id_supplier": "4cfff20a-b6ef-47ec-acda-0daa132af7dc",
                "id_category": "1cda8459-7235-4be5-b3e7-498b0518e3dd",
                "id_brand": "b3b093f4-f05a-41a0-8dd5-5892d7efe05d",
                "model": "Hilux 2020",
                "active": True
            },
            {
                "code": "MECH005",
                "name": "Correa de distribución",
                "description": "Correa de distribución reforzada de 120 dientes",
                "price": 35.90,
                "stock": 60,
                "min_stock": 15,
                "max_stock": 100,
                "id_supplier": "4cfff20a-b6ef-47ec-acda-0daa132af7dc",
                "id_category": "1cda8459-7235-4be5-b3e7-498b0518e3dd",
                "id_brand": "b3b093f4-f05a-41a0-8dd5-5892d7efe05d",
                "model": "Nissan Sentra",
                "active": True
            },
            {
                "code": "MECH006",
                "name": "Bomba de agua",
                "description": "Bomba de agua metálica para sistema de refrigeración",
                "price": 78.40,
                "stock": 18,
                "min_stock": 5,
                "max_stock": 40,
                "id_supplier": "4cfff20a-b6ef-47ec-acda-0daa132af7dc",
                "id_category": "1cda8459-7235-4be5-b3e7-498b0518e3dd",
                "id_brand": "b3b093f4-f05a-41a0-8dd5-5892d7efe05d",
                "model": "Chevrolet Aveo",
                "active": True
            }
        ])
    },
    "update_product": {
        "httpMethod": "PUT",
        "path": "/products/{id_product}",
        "pathParameters": {
            "id_product": "b03196fd-a140-4781-a529-3862119f8b8c"
        },
        "body": json.dumps({
            "name": "PRODUCTO ACTUALIZADO",
            "description": "Descripción actualizada desde test",
            "price": 45.99,
            "stock": 25,
            "min_stock": 10,
            "max_stock": 50,
            "discount": 15.5,
            "active": True
        })
    },
    
    "update_product_partial": {
        "httpMethod": "PUT",
        "path": "/products/{id_product}",
        "pathParameters": {
            "id_product": "b03196fd-a140-4781-a529-3862119f8b8c"
        },
        "body": json.dumps({
            "price": 99.99,
            "stock": 100
        })
    },
    
    "delete_product": {
        "httpMethod": "DELETE",
        "path": "/products/{id_product}",
        "pathParameters": {
            "id_product": "b03196fd-a140-4781-a529-3862119f8b8c"
        }
    },
    
    "find_product_by_id": {
        "httpMethod": "GET",
        "path": "/products/{id_product}",
        "pathParameters": {
            "id_product": "b03196fd-a140-4781-a529-3862119f8b8c"
        }
    },
        
    "add_customer": {
        "httpMethod": "POST",
        "path": "/customers",
        "body": json.dumps({
            "id_number": "0912345678",
            "name": "Carlos",
            "surname": "Rodríguez Pérez",
            "address": "Av. Principal #123, Guayaquil",
            "phone": "0987654321",
            "email": "carlos.rodriguez@example.com",
            "identification_type": "CEDULA",
            "birth_date": "1985-03-15",
            "gender": "M",
            "active": True
        })
    },
    
    "update_customer": {
        "httpMethod": "PUT",
        "path": "/customers/{id_customer}",
        "pathParameters": {
            "id_customer": "136daed3-3b83-4733-9ea2-2f06bea74ff7"
        },
        "body": json.dumps({
            "name": "Carlos Alberto",
            "surname": "Rodríguez García",
            "address": "Av. Secundaria #456, Guayaquil",
            "phone": "0991234567",
            "email": "carlos.nuevo@example.com",
            "active": True
        })
    },
    
    "update_customer_partial": {
        "httpMethod": "PUT",
        "path": "/customers/{id_customer}",
        "pathParameters": {
            "id_customer": "136daed3-3b83-4733-9ea2-2f06bea74ff7"
        },
        "body": json.dumps({
            "phone": "0998877665",
            "email": "nuevo.email@example.com"
        })
    },
    
    "update_customer_email_only": {
        "httpMethod": "PUT",
        "path": "/customers/{id_customer}",
        "pathParameters": {
            "id_customer": "136daed3-3b83-4733-9ea2-2f06bea74ff7"
        },
        "body": json.dumps({
            "email": "actualizado@example.com"
        })
    },
    
    "delete_customer": {
        "httpMethod": "DELETE",
        "path": "/customers/{id_customer}",
        "pathParameters": {
            "id_customer": "136daed3-3b83-4733-9ea2-2f06bea74ff7"
        }
    },
    
    "find_customer_by_id": {
        "httpMethod": "GET",
        "path": "/customers/{id_customer}",
        "pathParameters": {
            "id_customer": "136daed3-3b83-4733-9ea2-2f06bea74ff7"
        }
    },
}