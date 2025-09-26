from functools import wraps
from utils.response_utils import ResponseUtils

def validate_pagination_and_search(max_limit_admin=100, max_limit_other=50):
    """
    Decorador para validar parámetros de paginación y búsqueda en endpoints GET
    
    Args:
        max_limit_admin (int): Límite máximo para usuarios ADMIN
        max_limit_other (int): Límite máximo para otros roles
    """
    def decorator(func):
        @wraps(func)
        def wrapper(event, context):
            try:
                # Obtener el client_id y roles del evento
                client_id = event["client_id"]
                client_roles = event["client_roles"]
                
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
                max_limit = max_limit_admin if "ADMIN" in client_roles else max_limit_other
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
                
                # Agregar parámetros validados al evento para que la función los use
                event["validated_params"] = {
                    "page": page,
                    "limit": limit,
                    "search": search,
                    "max_limit": max_limit,
                    "client_roles": client_roles
                }
                
                print(f"Parámetros validados - Página: {page}, Límite: {limit}, Búsqueda: {search}")
                
                # Llamar a la función original
                return func(event, context)
                
            except KeyError as ke:
                print(f"Error de clave faltante: {str(ke)}")
                return ResponseUtils.bad_request_response(f"Faltan parámetros requeridos: {str(ke)}")
                
            except Exception as e:
                print(f"Error en validación: {str(e)}")
                return ResponseUtils.internal_server_error_response(f"Error en validación: {str(e)}")
        
        return wrapper
    return decorator
