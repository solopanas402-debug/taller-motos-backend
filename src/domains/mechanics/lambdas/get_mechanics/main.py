import json
from use_cases.mechanic_use_case import MechanicUseCase
from utils.response_utils import ResponseUtils
from decorators.lambda_decorators import cors_enabled, auth_required
from repositories.mechanic_repository import MechanicRepository
from db.db_client import DBClient

# Inicialización de dependencias
db_client = DBClient.get_client()
repository = MechanicRepository(db_client)
use_case = MechanicUseCase(repository)

@cors_enabled
@cognito_auth_required
@role_required(["ADMIN", "VENDEDOR"])  # Solo estos roles pueden consultar mecánicos
def lambda_handler(event, context):
    print(f'event: {event}')
    print(f'context: {context}')
    
    try:
        # Obtener el client_id del evento (esto proviene del token Cognito)
        client_id = event["client_id"]  # El client_id debe estar presente en el evento
        client_roles = event["client_roles"]  # Roles del cliente (verificados desde la base de datos)
        
        print(f"Cliente autenticado con ID: {client_id} y roles: {client_roles}")

         # Obtener el origen de la solicitud (por ejemplo, de un header CORS)
        origin = event.get("headers", {}).get("Origin", None)  # Obtener el origen dinámico
        headers = ResponseUtils.get_cors_headers(origin)  # Obtener los headers CORS con el origen dinámico
        
        
        # Obtener y validar parámetros de consulta
        params = event.get("queryStringParameters") or {}
        
        # Validar parámetros numéricos
        try:
            page = int(params.get("page", 1))
            limit = int(params.get("limit", 10))
        except ValueError:
            return ResponseUtils.bad_request_response(
                "Los parámetros 'page' y 'limit' deben ser números enteros válidos"
            )
        
        # Validar rangos de paginación
        if page < 1:
            return ResponseUtils.bad_request_response(
                "El parámetro 'page' debe ser mayor o igual a 1"
            )
        
        if limit < 1:
            return ResponseUtils.bad_request_response(
                "El parámetro 'limit' debe ser mayor o igual a 1"
            )
        
        # Límite máximo según el rol
        max_limit = 100 if "ADMIN" in client_roles else 50  # Si es ADMIN, puede ver más resultados
        if limit > max_limit:
            return ResponseUtils.bad_request_response(
                f"El límite máximo para tus roles ({', '.join(client_roles)}) es {max_limit}"
            )
        
        # Validar parámetro de búsqueda
        search = params.get("search")
        if search:
            search = search.strip()
            if len(search) < 1:
                return ResponseUtils.bad_request_response(
                    "El parámetro 'search' debe tener al menos 1 caracteres"
                )
            if len(search) > 100:
                return ResponseUtils.bad_request_response(
                    "El parámetro 'search' no puede tener más de 100 caracteres"
                )
        
        print(f"Consultando mecánicos - Página: {page}, Límite: {limit}, Búsqueda: {search}")
        
        # Ejecutar caso de uso
        result = use_case.get_mechanics(page, limit, search)
        
        # Validar resultado
        if result is None:
            return ResponseUtils.internal_server_error_response(
                "Error interno: el caso de uso retornó None"
            )
        
        # Procesar respuesta vacía
        if isinstance(result, dict) and "data" in result:
            if not result["data"]:
                return ResponseUtils.success_response({
                    **result,
                    "client_roles": client_roles,
                    "message": "No se encontraron mecánicos con los criterios especificados"
                })
        elif isinstance(result, list) and not result:
            return ResponseUtils.success_response({
                "data": [],
                "pagination": {
                    "page": page,
                    "limit": limit,
                    "total": 0,
                    "total_pages": 0
                },
                "client_roles": client_roles,
                "message": "No se encontraron mecánicos"
            })
        
        # Respuesta exitosa
        response_data = result.copy() if isinstance(result, dict) else {"data": result}
        response_data["client_roles"] = client_roles
        response_data["permissions"] = {
            "max_limit": max_limit,
            "is_admin": "ADMIN" in client_roles  # Verifica si el cliente tiene el rol ADMIN
        }
        
        print(f"Consulta exitosa - Encontrados: {len(result.get('data', result)) if isinstance(result, dict) else len(result)} mecánicos")
        return ResponseUtils.success_response(response_data, additional_headers=headers)
        
    except ValueError as ve:
        print(f"Error de validación: {str(ve)}")
        return ResponseUtils.bad_request_response(f"Error en los datos: {str(ve)}")
        
    except PermissionError as pe:
        print(f"Error de permisos: {str(pe)}")
        return ResponseUtils.forbidden_response(f"Sin permisos: {str(pe)}")
        
    except ConnectionError as ce:
        print(f"Error de conexión: {str(ce)}")
        return ResponseUtils.internal_server_error_response(
            "Error de conexión con la base de datos"
        )
        
    except Exception as e:
        print(f"Error inesperado: {str(e)}")
        return ResponseUtils.internal_server_error_response(
            "Ha ocurrido un problema interno al consultar los mecánicos"
        )
