import json
from db.db_client import DBClient
from repositories.sale_repository import SaleRepository
from use_cases.sale_use_case import SaleUseCase

# Imports del sistema centralizado
from decorators.lambda_decorators import cors_enabled, cognito_auth_required
from utils.response_utils import ResponseUtils

# Inicialización de dependencias
db_client = DBClient.get_client()
repository = SaleRepository(db_client)
use_case = SaleUseCase(repository)


@cors_enabled
@cognito_auth_required  # Requiere autenticación con Cognito
def lambda_handler(event, context):
    print(f"event: {event}")
    print(f"context: {context}")
    
    try:
        # Obtener información del usuario autenticado
        user_info = event["user_payload"]
        user_id = user_info["user_id"]
        scopes = user_info["scope"]
        
        print(f"Usuario autenticado: {user_id}")
        print(f"Scopes disponibles: {scopes}")
        
        # Verificar que tenga permisos para leer ventas
        required_scope = "motorcycerepairshop-api/read"
        if required_scope not in scopes:
            return ResponseUtils.forbidden_response(
                f"Se requiere el scope: {required_scope}"
            )
        
        # Obtener parámetros de consulta
        params = event.get("queryStringParameters") or {}
        
        # Validar parámetros numéricos
        try:
            page = int(params.get("page", 1))
            limit = int(params.get("limit", 10))
        except ValueError:
            return ResponseUtils.bad_request_response(
                "Los parámetros 'page' y 'limit' deben ser números enteros"
            )
        
        # Validar rangos
        if page < 1:
            return ResponseUtils.bad_request_response("El parámetro 'page' debe ser mayor a 0")
        
        if limit < 1 or limit > 100:
            return ResponseUtils.bad_request_response(
                "El parámetro 'limit' debe estar entre 1 y 100"
            )
        
        search = params.get("search")
        
        # Ejecutar caso de uso
        result = use_case.get_sales(page, limit, search)
        
        # Verificar si se encontraron resultados
        if not result or (isinstance(result, dict) and not result.get("data")):
            return ResponseUtils.success_response({
                "data": [],
                "pagination": {
                    "page": page,
                    "limit": limit,
                    "total": 0,
                    "total_pages": 0
                },
                "message": "No se encontraron ventas"
            })
        
        # Respuesta exitosa
        return ResponseUtils.success_response(result)
        
    except ValueError as e:
        # Error de validación de datos
        return ResponseUtils.bad_request_response(f"Error en los datos: {str(e)}")
        
    except PermissionError as e:
        # Error de permisos
        return ResponseUtils.forbidden_response(f"Sin permisos: {str(e)}")
        
    except FileNotFoundError as e:
        # Recurso no encontrado
        return ResponseUtils.not_found_response(f"Recurso no encontrado: {str(e)}")
        
    except ConnectionError as e:
        # Error de conexión a base de datos
        print(f"Error de conexión: {str(e)}")
        return ResponseUtils.internal_server_error_response(
            "Error de conexión con la base de datos"
        )
        
    except Exception as e:
        # Error genérico
        print(f"Error inesperado: {str(e)}")
        return ResponseUtils.internal_server_error_response(
            "Ha ocurrido un problema al consultar las ventas"
        )


# ============== VERSIÓN ALTERNATIVA SIN AUTENTICACIÓN ==============
# Si quieres que sea un endpoint público, usa esta versión:

@cors_enabled  # Solo CORS, sin autenticación
def lambda_handler_public(event, context):
    """Versión pública sin autenticación requerida"""
    print(f"event: {event}")
    print(f"context: {context}")
    
    try:
        # Obtener parámetros de consulta
        params = event.get("queryStringParameters") or {}
        
        # Validar parámetros numéricos
        try:
            page = int(params.get("page", 1))
            limit = int(params.get("limit", 10))
        except ValueError:
            return ResponseUtils.bad_request_response(
                "Los parámetros 'page' y 'limit' deben ser números enteros"
            )
        
        # Validar rangos
        if page < 1:
            return ResponseUtils.bad_request_response("El parámetro 'page' debe ser mayor a 0")
        
        if limit < 1 or limit > 100:
            return ResponseUtils.bad_request_response(
                "El parámetro 'limit' debe estar entre 1 y 100"
            )
        
        search = params.get("search")
        
        # Ejecutar caso de uso
        result = use_case.get_sales(page, limit, search)
        
        # Respuesta exitosa
        return ResponseUtils.success_response(result)
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return ResponseUtils.internal_server_error_response(
            "Ha ocurrido un problema al consultar las ventas"
        )


# ============== VERSIÓN CON CONTROL GRANULAR DE PERMISOS ==============
# Si quieres diferentes niveles de acceso según el scope:

@cors_enabled
@cognito_auth_required
def lambda_handler_with_role_control(event, context):
    """Versión con control granular de permisos"""
    try:
        user_info = event["user_payload"]
        user_id = user_info["user_id"]
        scopes = user_info["scope"]
        client_id = user_info["client_id"]
        
        # Obtener parámetros
        params = event.get("queryStringParameters") or {}
        page = int(params.get("page", 1))
        limit = int(params.get("limit", 10))
        search = params.get("search")
        
        # Control de permisos granular
        if "motorcycerepairshop-api/admin" in scopes:
            # Admin puede ver todas las ventas
            result = use_case.get_sales(page, limit, search)
            
        elif "motorcycerepairshop-api/read" in scopes:
            # Usuario normal solo puede ver sus propias ventas
            result = use_case.get_sales_by_user(user_id, page, limit, search)
            
        else:
            return ResponseUtils.forbidden_response(
                "No tienes permisos para consultar ventas"
            )
        
        return ResponseUtils.success_response(result)
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return ResponseUtils.internal_server_error_response()