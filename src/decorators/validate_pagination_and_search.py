from functools import wraps

def validate_pagination_and_search():
    def decorator(handler):
        @wraps(handler)
        def wrapper(event, context):
            query_params = event.get('queryStringParameters', {}) or {}
            
            try:
                # Validar y convertir parámetros
                page = int(query_params.get('page', 1))
                limit = int(query_params.get('limit', 10))
                search = query_params.get('search', '')

                # Validar rangos
                if page < 1:
                    page = 1
                if limit < 1 or limit > 100:
                    limit = 10

                # Agregar parámetros validados al evento
                event['validated_params'] = {
                    'page': page,
                    'limit': limit,
                    'search': search
                }
                
            except ValueError:
                # Si hay error en la conversión, usar valores por defecto
                event['validated_params'] = {
                    'page': 1,
                    'limit': 10,
                    'search': ''
                }

            return handler(event, context)
        return wrapper
    return decorator
