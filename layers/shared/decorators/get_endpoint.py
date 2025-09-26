from functools import wraps
from decorators.pagination_validation import validate_pagination_and_search
from decorators.standard_get_response import standard_get_response

def get_endpoint(entity_name="elementos", max_limit_admin=100, max_limit_other=50):
    """
    Decorador combinado para endpoints GET que incluye:
    - Validación de paginación y búsqueda
    - Manejo estándar de respuestas
    
    Args:
        entity_name (str): Nombre de la entidad para mensajes
        max_limit_admin (int): Límite máximo para usuarios ADMIN
        max_limit_other (int): Límite máximo para otros roles
    """
    def decorator(func):
        # Aplicar ambos decoradores
        decorated_func = validate_pagination_and_search(max_limit_admin, max_limit_other)(func)
        decorated_func = standard_get_response(entity_name)(decorated_func)
        
        return decorated_func
    return decorator
