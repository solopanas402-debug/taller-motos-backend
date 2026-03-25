import os
import sys
import json
from flask import Flask, request, jsonify
from functools import wraps
from dotenv import load_dotenv
from auth_service import AuthService, token_required
from lambda_wrapper import ejecutar_lambda

# Cargar variables de entorno
load_dotenv()

app = Flask(__name__)


def create_lambda_event(method, path, query_params=None, body=None, path_params=None, user=None):
    """Convierte una request de Flask a evento Lambda"""
    event = {
        "httpMethod": method,
        "path": path,
        "queryStringParameters": query_params or {},
        "body": json.dumps(body) if body else None,
        "pathParameters": path_params or {},
        "headers": dict(request.headers),
        "requestContext": {
            "authorizer": {
                "claims": {
                    "sub": user.get("user_id") if user else "anonymous",
                    "email": user.get("email") if user else "anonymous@example.com"
                }
            }
        }
    }
    return event


def parse_lambda_response(response):
    """Parsea la respuesta de una lambda"""
    status_code = response.get("statusCode", 200)
    body = response.get("body", "{}")
    
    if isinstance(body, str):
        try:
            body = json.loads(body)
        except json.JSONDecodeError:
            body = {"message": body}
    
    return jsonify(body), status_code


# ==================== AUTH ENDPOINTS ====================

@app.route("/auth/register", methods=["POST"])
def register():
    """Registrar nuevo usuario"""
    try:
        data = request.get_json()
        
        if not data.get("email") or not data.get("password"):
            return jsonify({"error": "Email y contraseña requeridos"}), 400
        
        result = AuthService.register_user(
            email=data["email"],
            password=data["password"],
            name=data.get("name")
        )
        
        status = result.pop("status")
        return jsonify(result), status
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/auth/login", methods=["POST"])
def login():
    """Login y obtener tokens"""
    try:
        data = request.get_json()
        
        if not data.get("email") or not data.get("password"):
            return jsonify({"error": "Email y contraseña requeridos"}), 400
        
        result = AuthService.login_user(
            email=data["email"],
            password=data["password"]
        )
        
        status = result.pop("status")
        return jsonify(result), status
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/auth/refresh", methods=["POST"])
def refresh():
    """Obtener nuevo access token usando refresh token"""
    try:
        data = request.get_json()
        
        if not data.get("refresh_token"):
            return jsonify({"error": "Refresh token requerido"}), 400
        
        result = AuthService.refresh_access_token(data["refresh_token"])
        
        status = result.pop("status")
        return jsonify(result), status
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/auth/logout", methods=["POST"])
@token_required
def logout():
    """Logout e invalidar refresh token"""
    try:
        data = request.get_json()
        
        if not data.get("refresh_token"):
            return jsonify({"error": "Refresh token requerido"}), 400
        
        result = AuthService.logout_user(data["refresh_token"])
        
        status = result.pop("status")
        return jsonify(result), status
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/auth/me", methods=["GET"])
@token_required
def get_current_user():
    """Obtener información del usuario actual"""
    return jsonify({
        "user_id": request.user["user_id"],
        "email": request.user["email"]
    }), 200


# ==================== CUSTOMERS ====================

@app.route("/customers", methods=["GET"])
@token_required
def get_customers():
    """Obtener clientes"""
    try:
        event = create_lambda_event(
            "GET", "/customers",
            query_params=dict(request.args),
            user=request.user
        )
        response = ejecutar_lambda("customers", "get_customers", event, None)
        return parse_lambda_response(response)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/customers/<id>", methods=["GET"])
@token_required
def get_customer_by_id(id):
    """Obtener cliente por ID"""
    try:
        event = create_lambda_event(
            "GET", f"/customers/{id}",
            path_params={"id": id},
            user=request.user
        )
        response = ejecutar_lambda("customers", "get_customer_by_id", event, None)
        return parse_lambda_response(response)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/customers", methods=["POST"])
@token_required
def add_customer():
    """Crear cliente"""
    try:
        data = request.get_json()
        event = create_lambda_event(
            "POST", "/customers",
            body=data,
            user=request.user
        )
        response = ejecutar_lambda("customers", "add_customer", event, None)
        return parse_lambda_response(response)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/customers/<id>", methods=["PUT", "PATCH"])
@token_required
def update_customer(id):
    """Actualizar cliente"""
    try:
        data = request.get_json()
        event = create_lambda_event(
            "PUT", f"/customers/{id}",
            body=data,
            path_params={"id": id},
            user=request.user
        )
        response = ejecutar_lambda("customers", "update_customer", event, None)
        return parse_lambda_response(response)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/customers/<id>", methods=["DELETE"])
@token_required
def delete_customer(id):
    """Eliminar cliente"""
    try:
        event = create_lambda_event(
            "DELETE", f"/customers/{id}",
            path_params={"id": id},
            user=request.user
        )
        response = ejecutar_lambda("customers", "delete_customer", event, None)
        return parse_lambda_response(response)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ==================== PRODUCTS ====================

@app.route("/products", methods=["GET"])
@token_required
def get_products():
    """Obtener productos"""
    try:
        event = create_lambda_event(
            "GET", "/products",
            query_params=dict(request.args),
            user=request.user
        )
        response = ejecutar_lambda("products", "get_products", event, None)
        return parse_lambda_response(response)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/products/<id>", methods=["GET"])
@token_required
def get_product_by_id(id):
    """Obtener producto por ID"""
    try:
        event = create_lambda_event(
            "GET", f"/products/{id}",
            path_params={"id": id},
            user=request.user
        )
        response = ejecutar_lambda("products", "get_product_by_id", event, None)
        return parse_lambda_response(response)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/products", methods=["POST"])
@token_required
def add_product():
    """Crear producto"""
    try:
        data = request.get_json()
        event = create_lambda_event(
            "POST", "/products",
            body=data,
            user=request.user
        )
        response = ejecutar_lambda("products", "add_product", event, None)
        return parse_lambda_response(response)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/products/<id>", methods=["PUT", "PATCH"])
@token_required
def update_product(id):
    """Actualizar producto"""
    try:
        data = request.get_json()
        event = create_lambda_event(
            "PUT", f"/products/{id}",
            body=data,
            path_params={"id": id},
            user=request.user
        )
        response = ejecutar_lambda("products", "update_product", event, None)
        return parse_lambda_response(response)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/products/<id>", methods=["DELETE"])
@token_required
def delete_product(id):
    """Eliminar producto"""
    try:
        event = create_lambda_event(
            "DELETE", f"/products/{id}",
            path_params={"id": id},
            user=request.user
        )
        response = ejecutar_lambda("products", "delete_product", event, None)
        return parse_lambda_response(response)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ==================== REPAIRS ====================

@app.route("/repairs", methods=["GET"])
@token_required
def get_repairs():
    """Obtener reparaciones"""
    try:
        event = create_lambda_event(
            "GET", "/repairs",
            query_params=dict(request.args),
            user=request.user
        )
        response = ejecutar_lambda("repairs", "get_repairs", event, None)
        return parse_lambda_response(response)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/repairs/<id>", methods=["GET"])
@token_required
def get_repair_by_id(id):
    """Obtener reparación por ID"""
    try:
        event = create_lambda_event(
            "GET", f"/repairs/{id}",
            path_params={"id": id},
            user=request.user
        )
        response = ejecutar_lambda("repairs", "get_repair_by_id", event, None)
        return parse_lambda_response(response)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/repairs", methods=["POST"])
@token_required
def add_repair():
    """Crear reparación"""
    try:
        data = request.get_json()
        event = create_lambda_event(
            "POST", "/repairs",
            body=data,
            user=request.user
        )
        response = ejecutar_lambda("repairs", "add_repair", event, None)
        return parse_lambda_response(response)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/repairs/<id>", methods=["PUT", "PATCH"])
@token_required
def update_repair(id):
    """Actualizar reparación"""
    try:
        data = request.get_json()
        event = create_lambda_event(
            "PUT", f"/repairs/{id}",
            body=data,
            path_params={"id": id},
            user=request.user
        )
        response = ejecutar_lambda("repairs", "update_repair", event, None)
        return parse_lambda_response(response)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/repairs/<id>", methods=["DELETE"])
@token_required
def delete_repair(id):
    """Eliminar reparación"""
    try:
        event = create_lambda_event(
            "DELETE", f"/repairs/{id}",
            path_params={"id": id},
            user=request.user
        )
        response = ejecutar_lambda("repairs", "delete_repair", event, None)
        return parse_lambda_response(response)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ==================== MECHANICS ====================

@app.route("/mechanics", methods=["GET"])
@token_required
def get_mechanics():
    """Obtener mecánicos"""
    try:
        event = create_lambda_event(
            "GET", "/mechanics",
            query_params=dict(request.args),
            user=request.user
        )
        response = ejecutar_lambda("mechanics", "get_mechanics", event, None)
        return parse_lambda_response(response)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/mechanics/<id>", methods=["GET"])
@token_required
def get_mechanic_by_id(id):
    """Obtener mecánico por ID"""
    try:
        event = create_lambda_event(
            "GET", f"/mechanics/{id}",
            path_params={"id": id},
            user=request.user
        )
        response = ejecutar_lambda("mechanics", "get_mechanic_by_id", event, None)
        return parse_lambda_response(response)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/mechanics", methods=["POST"])
@token_required
def add_mechanic():
    """Crear mecánico"""
    try:
        data = request.get_json()
        event = create_lambda_event(
            "POST", "/mechanics",
            body=data,
            user=request.user
        )
        response = ejecutar_lambda("mechanics", "add_mechanic", event, None)
        return parse_lambda_response(response)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/mechanics/<id>", methods=["PUT", "PATCH"])
@token_required
def update_mechanic(id):
    """Actualizar mecánico"""
    try:
        data = request.get_json()
        event = create_lambda_event(
            "PUT", f"/mechanics/{id}",
            body=data,
            path_params={"id": id},
            user=request.user
        )
        response = ejecutar_lambda("mechanics", "update_mechanic", event, None)
        return parse_lambda_response(response)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/mechanics/<id>", methods=["DELETE"])
@token_required
def delete_mechanic(id):
    """Eliminar mecánico"""
    try:
        event = create_lambda_event(
            "DELETE", f"/mechanics/{id}",
            path_params={"id": id},
            user=request.user
        )
        response = ejecutar_lambda("mechanics", "delete_mechanic", event, None)
        return parse_lambda_response(response)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ==================== SUPPLIERS ====================

@app.route("/suppliers", methods=["GET"])
@token_required
def get_suppliers():
    """Obtener proveedores"""
    try:
        event = create_lambda_event(
            "GET", "/suppliers",
            query_params=dict(request.args),
            user=request.user
        )
        response = ejecutar_lambda("suppliers", "get_suppliers", event, None)
        return parse_lambda_response(response)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/suppliers/<id>", methods=["GET"])
@token_required
def get_supplier_by_id(id):
    """Obtener proveedor por ID"""
    try:
        event = create_lambda_event(
            "GET", f"/suppliers/{id}",
            path_params={"id": id},
            user=request.user
        )
        response = ejecutar_lambda("suppliers", "get_supplier_by_id", event, None)
        return parse_lambda_response(response)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/suppliers", methods=["POST"])
@token_required
def add_supplier():
    """Crear proveedor"""
    try:
        data = request.get_json()
        event = create_lambda_event(
            "POST", "/suppliers",
            body=data,
            user=request.user
        )
        response = ejecutar_lambda("suppliers", "add_supplier", event, None)
        return parse_lambda_response(response)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/suppliers/<id>", methods=["PUT", "PATCH"])
@token_required
def update_supplier(id):
    """Actualizar proveedor"""
    try:
        data = request.get_json()
        event = create_lambda_event(
            "PUT", f"/suppliers/{id}",
            body=data,
            path_params={"id": id},
            user=request.user
        )
        response = ejecutar_lambda("suppliers", "update_supplier", event, None)
        return parse_lambda_response(response)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/suppliers/<id>", methods=["DELETE"])
@token_required
def delete_supplier(id):
    """Eliminar proveedor"""
    try:
        event = create_lambda_event(
            "DELETE", f"/suppliers/{id}",
            path_params={"id": id},
            user=request.user
        )
        response = ejecutar_lambda("suppliers", "delete_supplier", event, None)
        return parse_lambda_response(response)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ==================== SALES ====================

@app.route("/sales", methods=["GET"])
@token_required
def get_sales():
    """Obtener ventas"""
    try:
        event = create_lambda_event(
            "GET", "/sales",
            query_params=dict(request.args),
            user=request.user
        )
        response = ejecutar_lambda("sales", "get_sales", event, None)
        return parse_lambda_response(response)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/sales/<id>", methods=["GET"])
@token_required
def get_sale_by_id(id):
    """Obtener venta por ID"""
    try:
        event = create_lambda_event(
            "GET", f"/sales/{id}",
            path_params={"id": id},
            user=request.user
        )
        response = ejecutar_lambda("sales", "get_sale_by_id", event, None)
        return parse_lambda_response(response)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/sales", methods=["POST"])
@token_required
def add_sale():
    """Crear venta"""
    try:
        data = request.get_json()
        event = create_lambda_event(
            "POST", "/sales",
            body=data,
            user=request.user
        )
        response = ejecutar_lambda("sales", "add_sale", event, None)
        return parse_lambda_response(response)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/sales/<id>", methods=["PUT", "PATCH"])
@token_required
def update_sale(id):
    """Actualizar venta"""
    try:
        data = request.get_json()
        event = create_lambda_event(
            "PUT", f"/sales/{id}",
            body=data,
            path_params={"id": id},
            user=request.user
        )
        response = ejecutar_lambda("sales", "update_sale", event, None)
        return parse_lambda_response(response)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/sales/<id>", methods=["DELETE"])
@token_required
def delete_sale(id):
    """Eliminar venta"""
    try:
        event = create_lambda_event(
            "DELETE", f"/sales/{id}",
            path_params={"id": id},
            user=request.user
        )
        response = ejecutar_lambda("sales", "delete_sale", event, None)
        return parse_lambda_response(response)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/sales/payment-methods", methods=["GET"])
@token_required
def get_payment_methods():
    """Obtener métodos de pago"""
    try:
        event = create_lambda_event(
            "GET", "/sales/payment-methods",
            user=request.user
        )
        response = ejecutar_lambda("sales", "get_payment_methods", event, None)
        return parse_lambda_response(response)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ==================== CATEGORIES ====================

@app.route("/categories", methods=["GET"])
@token_required
def get_categories():
    """Obtener categorías"""
    try:
        event = create_lambda_event(
            "GET", "/categories",
            query_params=dict(request.args),
            user=request.user
        )
        response = ejecutar_lambda("products", "get_categories", event, None)
        return parse_lambda_response(response)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ==================== BRANDS ====================

@app.route("/brands", methods=["GET"])
@token_required
def get_brands():
    """Obtener marcas"""
    try:
        event = create_lambda_event(
            "GET", "/brands",
            query_params=dict(request.args),
            user=request.user
        )
        response = ejecutar_lambda("products", "get_brands", event, None)
        return parse_lambda_response(response)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ==================== CASHBOXES ====================

@app.route("/cashboxes", methods=["GET"])
@token_required
def get_cashbox():
    """Obtener cajas"""
    try:
        event = create_lambda_event(
            "GET", "/cashboxes",
            query_params=dict(request.args),
            user=request.user
        )
        response = ejecutar_lambda("cashboxes", "get_cashbox", event, None)
        return parse_lambda_response(response)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/cashboxes", methods=["POST"])
@token_required
def add_cashbox():
    """Crear caja"""
    try:
        data = request.get_json()
        event = create_lambda_event(
            "POST", "/cashboxes",
            body=data,
            user=request.user
        )
        response = ejecutar_lambda("cashboxes", "add_cashbox", event, None)
        return parse_lambda_response(response)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/cashboxes/current-session", methods=["GET"])
@token_required
def get_current_session():
    """Obtener sesión actual de caja"""
    try:
        event = create_lambda_event(
            "GET", "/cashboxes/current-session",
            user=request.user
        )
        response = ejecutar_lambda("cashboxes", "get_current_session", event, None)
        return parse_lambda_response(response)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/cashboxes/open", methods=["POST"])
@token_required
def open_cashbox():
    """Abrir caja"""
    try:
        data = request.get_json()
        event = create_lambda_event(
            "POST", "/cashboxes/open",
            body=data,
            user=request.user
        )
        response = ejecutar_lambda("cashboxes", "open_cashbox", event, None)
        return parse_lambda_response(response)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/cashboxes/close", methods=["POST"])
@token_required
def close_cashbox():
    """Cerrar caja"""
    try:
        data = request.get_json()
        event = create_lambda_event(
            "POST", "/cashboxes/close",
            body=data,
            user=request.user
        )
        response = ejecutar_lambda("cashboxes", "close_cashbox", event, None)
        return parse_lambda_response(response)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ==================== HEALTH CHECK ====================

@app.route("/health", methods=["GET"])
def health():
    """Health check"""
    return jsonify({"status": "ok"}), 200


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port, debug=False)
