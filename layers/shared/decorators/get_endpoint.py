
from functools import wraps
from utils.response_utils import ResponseUtils

def get_endpoint(entity_name="elementos"):
    def decorator(func):
        @wraps(func)
        def wrapper(event, context):
            try:
                query_params = event.get("queryStringParameters") or {}

                # Extraer valores desde query params
                page = int(query_params.get("page", 1))
                limit = int(query_params.get("limit", 10))
                search = query_params.get("search")
                client_id = query_params.get("client_id")

                # ✅ Si no hay client_id en query, buscar en el token
                if not client_id:
                    user_payload = event.get("user_payload", {})
                    client_id = user_payload.get("client_id")

                if not client_id:
                    return ResponseUtils.bad_request_response("Faltan parámetros requeridos: 'client_id'")

                # Puedes incluir más lógica aquí si necesitas roles o límites
                client_roles = event.get("user_payload", {}).get("scope", []) or []
                max_limit = 100  # o configurable

                # Construir validated_params
                event["validated_params"] = {
                    "page": page,
                    "limit": limit,
                    "search": search,
                    "client_id": client_id,
                    "client_roles": client_roles,
                    "max_limit": max_limit
                }

                return func(event, context)

            except Exception as e:
                print(f"❌ Error en get_endpoint: {str(e)}")
                return ResponseUtils.bad_request_response(f"Parámetros inválidos para obtener {entity_name}")

        return wrapper
    return decorator
