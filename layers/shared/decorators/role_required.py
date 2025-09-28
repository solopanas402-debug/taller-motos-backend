from functools import wraps
from utils.response_utils import ResponseUtils
from db.db_client import DBClient

db_client = DBClient.get_client()

def role_required(allowed_roles):
    """
    Decorador para validar que el cliente tenga uno de los roles permitidos.
    Usage: @role_required(["ADMIN", "VENDEDOR"])
    """
    def decorator(func):
        from functools import wraps
        @wraps(func)
        def wrapper(event, context):
            try:
                client_id = event["client_id"]  # El client_id debe estar presente en el evento

                # Consultar roles del cliente desde la tabla client_roles
                query = """
                    SELECT r.role_name 
                    FROM client_roles cr
                    INNER JOIN roles r ON cr.id_role = r.id_role
                    WHERE cr.client_id = %s
                """
                
                with db_client.cursor() as cursor:
                    cursor.execute(query, (client_id,))
                    roles = [row[0] for row in cursor.fetchall()]

                if not roles:
                    return ResponseUtils.forbidden_response("Cliente no encontrado o sin rol asignado")

                # Verificar si el cliente tiene uno de los roles permitidos
                if not any(role in allowed_roles for role in roles):
                    return ResponseUtils.forbidden_response(f"Acceso denegado. Se requiere uno de los roles: {', '.join(allowed_roles)}. Tu rol(es): {', '.join(roles)}")

                # Añadir roles al evento para uso posterior
                event["client_roles"] = roles

                return func(event, context)
            except Exception as e:
                print(f"Error validando rol: {str(e)}")
                return ResponseUtils.internal_server_error_response("Error validando permisos del cliente")

        return wrapper
    return decorator
