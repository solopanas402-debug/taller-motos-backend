import datetime
import json

events = {
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
    "get_customers": {
        "httpMethod": "GET",
        "path": "/customers",
        "queryStringParameters": {"id": "123"}
    },
    "get_customer_by_id": {
        "httpMethod": "GET",
        "path": "/customers/{id}",
        "pathParameters": {
            "id": "2559987b-6a71-48ee-ac76-1919523c49e1"
        }
    },
    "delete_customer": {
        "httpMethod": "DELETE",
        "path": "/customers/{id}",
        "pathParameters": {
            "id": "2559987b-6a71-48ee-ac76-1919523c49e1"
        }
    },
    "update_customer": {
        "httpMethod": "PUT",
        "path": "/customers/{id}",
        "pathParameters": {
            "id": "136daed3-3b83-4733-9ea2-2f06bea74ff7"
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
    "add_mechanic": {
        "httpMethod": "POST",
        "path": "/mechanics",
        "body": json.dumps({
            "name": "Juan Pérez",
            "phone": "555-1234",
            "email": "juan@example.com"
        })
    },
    "get_mechanics": {
        "httpMethod": "POST",
        "path": "/mechanics",
        "queryStringParameters": {"page": "1", "limit": "5"}
    },
    "get_mechanic_by_id": {
        "httpMethod": "GET",
        "path": "/mechanics/{id}",
        "pathParameters": {
            "id": "ebd0acc0-44ab-4e80-9ce2-40981c20f360"
        }
    },
    "delete_mechanic": {
        "httpMethod": "DELETE",
        "path": "/mechanics/{id}",
        "pathParameters": {
            "id": "ec407443-4891-4e61-b7d9-1c2064ba3663"
        }
    },
    "update_mechanic": {
        "httpMethod": "PUT",
        "path": "/mechanics/{id}",
        "pathParameters": {
            "id": "ebd0acc0-44ab-4e80-9ce2-40981c20f360"
        },
        "body": json.dumps({
            "name": "Carlos Alberto",
            "surname": "Rodríguez García",
            "address": "Av. Secundaria #456, Guayaquil",
            "phone": "0991234567",
            "email": "carlos.nuevo@example.com",
            "active": False
        })
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
    "get_products": {
        "httpMethod": "GET",
        "path": "/products",
        "queryStringParameters": {"page": "1", "limit": "10", "search": ""}
    },
    "get_product_by_id": {
        "httpMethod": "GET",
        "path": "/products/{id}",
        "pathParameters": {"id": "b03196fd-a140-4781-a529-3862119f8b8c"}
    },
    "delete_product": {
        "httpMethod": "DELETE",
        "path": "/products/{id}",
        "pathParameters": {
            "id": "b03196fd-a140-4781-a529-3862119f8b8c"
        }
    },
    "update_product": {
        "httpMethod": "PUT",
        "path": "/products/{id}",
        "pathParameters": {
            "id": "b03196fd-a140-4781-a529-3862119f8b8c"
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
    "add_repair": {
        "httpMethod": "POST",
        "path": "/repairs",
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
    "get_repairs": {
        "httpMethod": "GET",
        "path": "/repairs",
        "queryStringParameters": {"page": "1", "limit": "5", "search": ""}
    },
    "get_repair_by_id": {
        "httpMethod": "GET",
        "path": "/repairs/{id}",
        "pathParameters": {"id": "752cd4bd-a61e-4000-b651-ab2d2ac14ae0"}
    },
    "delete_repair": {
        "httpMethod": "DELETE",
        "path": "/repairs/{id}",
        "pathParameters": {
            "id": "b03196fd-a140-4781-a529-3862119f8b8c"
        }
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
    "get_sales": {
        "httpMethod": "GET",
        "path": "/sales",
        "queryStringParameters": {"page": "1", "limit": "5", "search": "", "recordType": "quote"}
    },
    "get_sale_by_id": {
        "httpMethod": "GET",
        "path": "/sales/{id}",
        "pathParameters": {"id": "fdd33220-a805-44d2-b8a0-7a1cfde95d35"}
    },
    "delete_sale": {
        "httpMethod": "DELETE",
        "path": "/sales/{id}",
        "pathParameters": {
            "id": "b03196fd-a140-4781-a529-3862119f8b8c"
        }
    },
    "update_sale": {
        "httpMethod": "PUT",
        "path": "/sales/{id}",
        "pathParameters": {
            "id": "2fcc9e4f-20bd-4b22-9c2a-6685840fefe8"
        },
        "body": json.dumps({
            "status": "pending",
        })
    },
    "add_supplier": {
        "httpMethod": "POST",
        "path": "/suppliers",
        "body": json.dumps(
            {
                "name": "Prueba para eliminar",
                "surname": "Leo te odio no haces bien",
                "main_contact": "Luis Herrera",
                "phone": "555-3344",
                "email": "contacto@autorepuestos.com",
                "address": "Zona Industrial, Edificio 5, Ciudad Norte",
                "ruc": "SUPP789456123",
                "active": True
            })
    },
    "get_suppliers": {
        "httpMethod": "GET",
        "path": "/suppliers",
        "body": json.dumps({"order_id": "456", "product": "Zapatos"})
    },
    "get_supplier_by_id": {
        "httpMethod": "GET",
        "path": "/suppliers/{id}",
        "pathParameters": {"id": "9084837b-74bd-457d-ac6b-15bed6c441ff"}
    },
    "delete_supplier": {
        "httpMethod": "DELETE",
        "path": "/suppliers/{id}",
        "pathParameters": {
            "id": "b03196fd-a140-4781-a529-3862119f8b8c"
        }
    },
    "update_supplier": {
        "httpMethod": "PUT",
        "path": "/suppliers/{id}",
        "pathParameters": {
            "id": "e85d6c07-748e-46e1-ac51-50fd102aeb20"
        },
        "body": json.dumps({
            "name": "PRUEBA PARA ACTUALIZAR",
            "main_contact": "LEO ASCO",
            "email": "prueba@autorepuestos.com",
            "active": False
        })
    },
    "update_product_partial": {
        "httpMethod": "PUT",
        "path": "/products/{id}",
        "pathParameters": {
            "id": "b03196fd-a140-4781-a529-3862119f8b8c"
        },
        "body": json.dumps({
            "price": 99.99,
            "stock": 100
        })
    },

    "find_product_by_id": {
        "httpMethod": "GET",
        "path": "/products/{id}",
        "pathParameters": {
            "id": "b03196fd-a140-4781-a529-3862119f8b8c"
        }
    },

    "update_customer_partial": {
        "httpMethod": "PUT",
        "path": "/customers/{id}",
        "pathParameters": {
            "id": "136daed3-3b83-4733-9ea2-2f06bea74ff7"
        },
        "body": json.dumps({
            "phone": "0998877665",
            "email": "nuevo.email@example.com"
        })
    },

    "update_customer_email_only": {
        "httpMethod": "PUT",
        "path": "/customers/{id}",
        "pathParameters": {
            "id": "136daed3-3b83-4733-9ea2-2f06bea74ff7"
        },
        "body": json.dumps({
            "email": "actualizado@example.com"
        })
    },
    
    # ============================================
    # CASHBOX (Caja Chica) - Eventos de Prueba
    # ============================================
    
    # 1. Abrir sesión de caja (se hace al inicio del día)
    "open_cashbox": {
        "httpMethod": "POST",
        "path": "/cashboxes/open",
        "body": json.dumps({
            "opening_amount": 100.00,
            "opened_by": "98abe20d-b97d-4b0f-8a50-386a6d75e47b",
            "notes": "Apertura de caja del día de prueba"
        })
    },

    # 2. Obtener sesión actual de caja
    "get_current_session": {
        "httpMethod": "GET",
        "path": "/cashboxes/current-session"
    },

    # 3. Registrar movimiento de caja - INGRESO
    "add_cashbox_income": {
        "httpMethod": "POST",
        "path": "/cashboxes/movement",
        "body": json.dumps({
            "type": "INCOME",
            "amount": 150.00,
            "concept": "Pago en efectivo de cliente",
            "id_user": "98abe20d-b97d-4b0f-8a50-386a6d75e47b"
        })
    },

    # 4. Registrar movimiento de caja - EGRESO
    "add_cashbox_expense": {
        "httpMethod": "POST",
        "path": "/cashboxes/movement",
        "body": json.dumps({
            "type": "EXPENSE",
            "amount": 50.00,
            "concept": "Compra de suministros de oficina",
            "id_user": "98abe20d-b97d-4b0f-8a50-386a6d75e47b"
        })
    },

    # 5. Registrar movimiento de caja - AJUSTE
    "add_cashbox_adjustment": {
        "httpMethod": "POST",
        "path": "/cashboxes/movement",
        "body": json.dumps({
            "type": "ADJUSTMENT",
            "amount": 25.00,
            "concept": "Ajuste por error en conteo anterior",
            "id_user": "98abe20d-b97d-4b0f-8a50-386a6d75e47b"
        })
    },

    # 6. Registrar movimiento en español - INGRESO
    "add_cashbox": {
        "httpMethod": "POST",
        "path": "/cashboxes/movement",
        "body": json.dumps({
            "type": "INGRESO",
            "amount": 200.00,
            "concept": "Venta en efectivo",
            "id_user": "98abe20d-b97d-4b0f-8a50-386a6d75e47b"
        })
    },

    # 7. Obtener movimientos de caja con paginación
    "get_cashbox": {
        "httpMethod": "GET",
        "path": "/cashboxes",
        "queryStringParameters": {"page": "1", "limit": "10", "search": ""}
    },

    # 8. Obtener movimientos de caja filtrados por búsqueda
    "get_cashbox_search": {
        "httpMethod": "GET",
        "path": "/cashboxes",
        "queryStringParameters": {"page": "1", "limit": "10", "search": "efectivo"}
    },

    # 9. Cerrar sesión de caja (se hace al final del día)
    "close_cashbox": {
        "httpMethod": "POST",
        "path": "/cashboxes/close",
        "body": json.dumps({
            "actual_closing": 425.00,
            "closed_by": "98abe20d-b97d-4b0f-8a50-386a6d75e47b",
            "notes": "Cierre de caja del día - Todo correcto"
        })
    },

    # 10. Cerrar caja con diferencia (sobrante)
    "close_cashbox_with_surplus": {
        "httpMethod": "POST",
        "path": "/cashboxes/close",
        "body": json.dumps({
            "actual_closing": 450.00,
            "closed_by": "98abe20d-b97d-4b0f-8a50-386a6d75e47b",
            "notes": "Cierre de caja - Sobrante de $25 encontrado"
        })
    },

    # 11. Cerrar caja con diferencia (faltante)
    "close_cashbox_with_shortage": {
        "httpMethod": "POST",
        "path": "/cashboxes/close",
        "body": json.dumps({
            "actual_closing": 400.00,
            "closed_by": "98abe20d-b97d-4b0f-8a50-386a6d75e47b",
            "notes": "Cierre de caja - Faltante de $25 - Verificar registros"
        })
    },

    # ============================================
    # DASHBOARD - Obtener datos del dashboard
    # ============================================
    "get_dashboard": {
        "httpMethod": "GET",
        "path": "/dashboard"
    },

}
