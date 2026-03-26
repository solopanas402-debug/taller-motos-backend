from functools import wraps
from utils.response_utils import ResponseUtils

def validate_pagination_and_search(max_limit: int = 100):
    """
    Decorador para endpoints públicos GET con parámetros:
    - page: int (>=1)
    - limit: int (>=1)
    - search: str (opcional, 1-100 caracteres)
    """
    def decorator(func):
        @wraps(func)
        def wrapper(event, context):
            try:
                query_params = event.get("queryStringParameters")
                
                # Si queryStringParameters es None o vacío, usar diccionario vacío
                if not query_params:
                    query_params = {}

                # Obtener valores con defaults
                page_str = query_params.get("page", "1")
                limit_str = query_params.get("limit", "10")
                
                try:
                    page = int(page_str)
                    limit = int(limit_str)
                except (ValueError, TypeError):
                    return ResponseUtils.bad_request_response(
                        "Los parámetros 'page' y 'limit' deben ser números enteros válidos"
                    )

                if page < 1:
                    return ResponseUtils.bad_request_response(
                        "El parámetro 'page' debe ser mayor o igual a 1"
                    )
                
                if limit < 1:
                    return ResponseUtils.bad_request_response(
                        "El parámetro 'limit' debe ser mayor o igual a 1"
                    )
                
                if limit > max_limit:
                    limit = max_limit

                search = query_params.get("search", "").strip() if query_params.get("search") else None
                if search:
                    if len(search) > 100:
                        return ResponseUtils.bad_request_response(
                            "El parámetro 'search' no puede tener más de 100 caracteres"
                        )

                event["validated_params"] = {
                    "page": page,
                    "limit": limit,
                    "search": search
                }

                return func(event, context)

            except Exception as e:
                print(f"Error en validate_pagination_and_search: {str(e)}")
                import traceback
                traceback.print_exc()
                return ResponseUtils.bad_request_response(f"Error validando parámetros: {str(e)}")
        
        return wrapper
    return decorator