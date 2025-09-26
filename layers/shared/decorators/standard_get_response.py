from functools import wraps
from utils.response_utils import ResponseUtils

def standard_get_response(entity_name="elementos"):
    """
    Decorador para manejar respuestas estándar en endpoints GET
    
    Args:
        entity_name (str): Nombre de la entidad para mensajes (ej: "clientes", "productos", "ventas")
    """
    def decorator(func):
        @wraps(func)
        def wrapper(event, context):
            try:
                # Obtener parámetros validados del evento
                validated_params = event.get("validated_params", {})
                client_roles = validated_params.get("client_roles", [])
                max_limit = validated_params.get("max_limit", 50)
                
                # Obtener el origen de la solicitud para CORS
                origin = event.get("headers", {}).get("Origin", None)
                headers = ResponseUtils.get_cors_headers(origin)
                
                # Ejecutar la función original
                result = func(event, context)
                
                # Si la función ya retornó una respuesta HTTP, devolverla tal como está
                if isinstance(result, dict) and "statusCode" in result:
                    return result
                
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
                            "message": f"No se encontraron {entity_name} con los criterios especificados"
                        }, additional_headers=headers)
                elif isinstance(result, list) and not result:
                    page = validated_params.get("page", 1)
                    limit = validated_params.get("limit", 10)
                    return ResponseUtils.success_response({
                        "data": [],
                        "pagination": {
                            "page": page,
                            "limit": limit,
                            "total": 0,
                            "total_pages": 0
                        },
                        "client_roles": client_roles,
                        "message": f"No se encontraron {entity_name}"
                    }, additional_headers=headers)
                
                # Respuesta exitosa
                response_data = result.copy() if isinstance(result, dict) else {"data": result}
                response_data["client_roles"] = client_roles
                response_data["permissions"] = {
                    "max_limit": max_limit,
                    "is_admin": "ADMIN" in client_roles
                }
                
                print(f"Consulta exitosa - Encontrados: {len(result.get('data', result)) if isinstance(result, dict) else len(result)} {entity_name}")
                return ResponseUtils.success_response(response_data, additional_headers=headers)
                
            except Exception as e:
                print(f"Error en respuesta estándar: {str(e)}")
                return ResponseUtils.internal_server_error_response(
                    f"Ha ocurrido un problema interno al consultar los {entity_name}"
                )
        
        return wrapper
    return decorator
