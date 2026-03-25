import os
import sys
import json
from flask import Flask, request, jsonify
from functools import wraps
import requests
from auth_service import AuthService, token_required

# Agregar paths para importar las lambdas
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'layers/shared'))

app = Flask(__name__)

# Importar todas las lambdas
try:
    from domains.customers.lambdas.get_customers.main import lambda_handler as get_customers_handler
    from domains.customers.lambdas.get_customer_by_id.main import lambda_handler as get_customer_by_id_handler
    from domains.customers.lambdas.add_customer.main import lambda_handler as add_customer_handler
    from domains.customers.lambdas.update_customer.main import lambda_handler as update_customer_handler
    from domains.customers.lambdas.delete_customer.main import lambda_handler as delete_customer_handler

    from domains.repairs.lambdas.get_repairs.main import lambda_handler as get_repairs_handler
    from domains.repairs.lambdas.get_repair_by_id.main import lambda_handler as get_repair_by_id_handler
    from domains.repairs.lambdas.add_repair.main import lambda_handler as add_repair_handler
    from domains.repairs.lambdas.update_repair.main import lambda_handler as update_repair_handler
    from domains.repairs.lambdas.delete_repair.main import lambda_handler as delete_repair_handler

    from domains.mechanics.lambdas.get_mechanics.main import lambda_handler as get_mechanics_handler
    from domains.mechanics.lambdas.get_mechanic_by_id.main import lambda_handler as get_mechanic_by_id_handler
    from domains.mechanics.lambdas.add_mechanic.main import lambda_handler as add_mechanic_handler
    from domains.mechanics.lambdas.update_mechanic.main import lambda_handler as update_mechanic_handler
    from domains.mechanics.lambdas.delete_mechanic.main import lambda_handler as delete_mechanic_handler

    from domains.products.lambdas.get_products.main import lambda_handler as get_products_handler
    from domains.products.lambdas.get_product_by_id.main import lambda_handler as get_product_by_id_handler
    from domains.products.lambdas.add_product.main import lambda_handler as add_product_handler
    from domains.products.lambdas.update_product.main import lambda_handler as update_product_handler
    from domains.products.lambdas.delete_product.main import lambda_handler as delete_product_handler

    from domains.cashboxes.lambdas.get_cashbox.main import lambda_handler as get_cashbox_handler
    from domains.cashboxes.lambdas.add_cashbox.main import lambda_handler as add_cashbox_handler
    from domains.cashboxes.lambdas.close_cashbox.main import lambda_handler as close_cashbox_handler
    from domains.cashboxes.lambdas.get_current_session.main import lambda_handler as get_current_session_handler

    from domains.brands.lambdas.get_brands.main import lambda_handler as get_brands_handler

    from domains.bulk_products.lambdas.add_products.main import lambda_handler as add_products_bulk_handler
    
    LAMBDAS_LOADED = True
except ImportError as e:
    print(f"⚠️ Advertencia: No se pudieron cargar todas las lambdas: {e}")
    print("ℹ️ Los endpoints de autenticación funcionarán normalmente")
    LAMBDAS_LOADED = False


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


def lambda_route(lambda_handler_func, require_auth=True):
    """Decorador para ejecutar una lambda y retornar su respuesta"""
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            try:
                # Verificar autenticación si es requerida
                if require_auth:
                    token = None
                    if "Authorization" in request.headers:
                        auth_header = request.headers["Authorization"]
                        try:
                            token = auth_header.split(" ")[1]
                        except IndexError:
                            return jsonify({"error": "Token inválido"}), 401
                    
                    if not token:
                        return jsonify({"error": "Token requerido"}), 401
                    
                    payload = AuthService.verify_token(token)
                    if not payload or payload.get("type") != "access":
                        return jsonify({"error": "Token inválido o expirado"}), 401
                    
                    user = payload
                else:
                    user = None
                
                # Obtener parámetros
                path_params = kwargs if kwargs else None
                query_params = request.args.to_dict() if request.args else None
                body = request.get_json() if request.is_json else None
                
                # Crear evento Lambda
                event = create_lambda_event(
                    request.method,
                    request.path,
                    query_params,
                    body,
                    path_params,
                    user
                )
                
                # Ejecutar lambda
                response = lambda_handler_func(event, None)
                
                # Parsear respuesta
                status_code = response.get("statusCode", 200)
                response_body = response.get("body", "{}")
                
                if isinstance(response_body, str):
                    response_body = json.loads(response_body)
                
                return jsonify(response_body), status_code
                
            except Exception as e:
                print(f"Error: {str(e)}")
                return jsonify({"error": str(e)}), 500
        
        return wrapper
    return decorator


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

# ==================== CUSTOMERS ====================

@app.route("/customers", methods=["GET"])
@token_required
def get_customers():
    """Obtener clientes"""
    try:
        url = f"{os.environ.get('DB_URL')}/rest/v1/customers"
        headers = {
            "apikey": os.environ.get("DB_KEY"),
            "Authorization": f"Bearer {os.environ.get('DB_KEY')}",
        }
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code < 400:
            return jsonify(response.json()), 200
        return jsonify({"error": "Error al obtener clientes"}), response.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/customers/<id>", methods=["GET"])
@token_required
def get_customer_by_id(id):
    """Obtener cliente por ID"""
    try:
        url = f"{os.environ.get('DB_URL')}/rest/v1/customers?id_customer=eq.{id}"
        headers = {
            "apikey": os.environ.get("DB_KEY"),
            "Authorization": f"Bearer {os.environ.get('DB_KEY')}",
        }
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code < 400:
            data = response.json()
            return jsonify(data[0] if data else {}), 200
        return jsonify({"error": "Cliente no encontrado"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/customers", methods=["POST"])
@token_required
def add_customer():
    """Crear cliente"""
    try:
        data = request.get_json()
        url = f"{os.environ.get('DB_URL')}/rest/v1/customers"
        headers = {
            "apikey": os.environ.get("DB_KEY"),
            "Authorization": f"Bearer {os.environ.get('DB_KEY')}",
            "Content-Type": "application/json",
            "Prefer": "return=representation"
        }
        response = requests.post(url, json=data, headers=headers, timeout=10)
        if response.status_code < 400:
            return jsonify(response.json()), 201
        return jsonify({"error": "Error al crear cliente"}), response.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/customers/<id>", methods=["PUT"])
@token_required
def update_customer(id):
    """Actualizar cliente"""
    try:
        data = request.get_json()
        url = f"{os.environ.get('DB_URL')}/rest/v1/customers?id_customer=eq.{id}"
        headers = {
            "apikey": os.environ.get("DB_KEY"),
            "Authorization": f"Bearer {os.environ.get('DB_KEY')}",
            "Content-Type": "application/json",
            "Prefer": "return=representation"
        }
        response = requests.patch(url, json=data, headers=headers, timeout=10)
        if response.status_code < 400:
            return jsonify(response.json()), 200
        return jsonify({"error": "Error al actualizar cliente"}), response.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/customers/<id>", methods=["DELETE"])
@token_required
def delete_customer(id):
    """Eliminar cliente"""
    try:
        url = f"{os.environ.get('DB_URL')}/rest/v1/customers?id_customer=eq.{id}"
        headers = {
            "apikey": os.environ.get("DB_KEY"),
            "Authorization": f"Bearer {os.environ.get('DB_KEY')}",
        }
        response = requests.delete(url, headers=headers, timeout=10)
        if response.status_code < 400:
            return jsonify({"message": "Cliente eliminado"}), 200
        return jsonify({"error": "Error al eliminar cliente"}), response.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ==================== PRODUCTS ====================

@app.route("/products", methods=["GET"])
@token_required
def get_products():
    """Obtener productos"""
    try:
        url = f"{os.environ.get('DB_URL')}/rest/v1/products"
        headers = {
            "apikey": os.environ.get("DB_KEY"),
            "Authorization": f"Bearer {os.environ.get('DB_KEY')}",
        }
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code < 400:
            return jsonify(response.json()), 200
        return jsonify({"error": "Error al obtener productos"}), response.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/products/<id>", methods=["GET"])
@token_required
def get_product_by_id(id):
    """Obtener producto por ID"""
    try:
        url = f"{os.environ.get('DB_URL')}/rest/v1/products?id_product=eq.{id}"
        headers = {
            "apikey": os.environ.get("DB_KEY"),
            "Authorization": f"Bearer {os.environ.get('DB_KEY')}",
        }
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code < 400:
            data = response.json()
            return jsonify(data[0] if data else {}), 200
        return jsonify({"error": "Producto no encontrado"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/products", methods=["POST"])
@token_required
def add_product():
    """Crear producto"""
    try:
        data = request.get_json()
        url = f"{os.environ.get('DB_URL')}/rest/v1/products"
        headers = {
            "apikey": os.environ.get("DB_KEY"),
            "Authorization": f"Bearer {os.environ.get('DB_KEY')}",
            "Content-Type": "application/json",
            "Prefer": "return=representation"
        }
        response = requests.post(url, json=data, headers=headers, timeout=10)
        if response.status_code < 400:
            return jsonify(response.json()), 201
        return jsonify({"error": "Error al crear producto"}), response.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ==================== REPAIRS ====================

@app.route("/repairs", methods=["GET"])
@token_required
def get_repairs():
    """Obtener reparaciones"""
    try:
        url = f"{os.environ.get('DB_URL')}/rest/v1/repairs"
        headers = {
            "apikey": os.environ.get("DB_KEY"),
            "Authorization": f"Bearer {os.environ.get('DB_KEY')}",
        }
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code < 400:
            return jsonify(response.json()), 200
        return jsonify({"error": "Error al obtener reparaciones"}), response.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/repairs/<id>", methods=["GET"])
@token_required
def get_repair_by_id(id):
    """Obtener reparación por ID"""
    try:
        url = f"{os.environ.get('DB_URL')}/rest/v1/repairs?id_repair=eq.{id}"
        headers = {
            "apikey": os.environ.get("DB_KEY"),
            "Authorization": f"Bearer {os.environ.get('DB_KEY')}",
        }
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code < 400:
            data = response.json()
            return jsonify(data[0] if data else {}), 200
        return jsonify({"error": "Reparación no encontrada"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ==================== MECHANICS ====================

@app.route("/mechanics", methods=["GET"])
@token_required
def get_mechanics():
    """Obtener mecánicos"""
    try:
        url = f"{os.environ.get('DB_URL')}/rest/v1/mechanics"
        headers = {
            "apikey": os.environ.get("DB_KEY"),
            "Authorization": f"Bearer {os.environ.get('DB_KEY')}",
        }
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code < 400:
            return jsonify(response.json()), 200
        return jsonify({"error": "Error al obtener mecánicos"}), response.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/mechanics/<id>", methods=["GET"])
@token_required
def get_mechanic_by_id(id):
    """Obtener mecánico por ID"""
    try:
        url = f"{os.environ.get('DB_URL')}/rest/v1/mechanics?id_mechanic=eq.{id}"
        headers = {
            "apikey": os.environ.get("DB_KEY"),
            "Authorization": f"Bearer {os.environ.get('DB_KEY')}",
        }
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code < 400:
            data = response.json()
            return jsonify(data[0] if data else {}), 200
        return jsonify({"error": "Mecánico no encontrado"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ==================== CASHBOXES ====================

@app.route("/cashboxes", methods=["GET"])
@token_required
def get_cashbox():
    """Obtener cajas"""
    try:
        url = f"{os.environ.get('DB_URL')}/rest/v1/cashbox"
        headers = {
            "apikey": os.environ.get("DB_KEY"),
            "Authorization": f"Bearer {os.environ.get('DB_KEY')}",
        }
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code < 400:
            return jsonify(response.json()), 200
        return jsonify({"error": "Error al obtener cajas"}), response.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ==================== BRANDS ====================

@app.route("/brands", methods=["GET"])
@token_required
def get_brands():
    """Obtener marcas"""
    try:
        url = f"{os.environ.get('DB_URL')}/rest/v1/brands"
        headers = {
            "apikey": os.environ.get("DB_KEY"),
            "Authorization": f"Bearer {os.environ.get('DB_KEY')}",
        }
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code < 400:
            return jsonify(response.json()), 200
        return jsonify({"error": "Error al obtener marcas"}), response.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ==================== HEALTH CHECK ====================

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"}), 200


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
