from functools import wraps
from utils.response_utils import ResponseUtils
from utils.auth_utils import AuthUtils

def cors_enabled(func):
    """Decorator que añade automáticamente soporte CORS a una lambda"""
    @wraps(func)
    def wrapper(event, context):
        # Manejar peticiones OPTIONS automáticamente
        if event.get("httpMethod") == "OPTIONS":
            return ResponseUtils.options_response()
        
        try:
            result = func(event, context)
            
            # Si la función no devuelve headers, añadirlos
            if isinstance(result, dict) and "headers" not in result:
                result["headers"] = ResponseUtils.get_cors_headers()
            elif isinstance(result, dict) and result.get("headers"):
                # Merge con headers CORS
                cors_headers = ResponseUtils.get_cors_headers()
                cors_headers.update(result["headers"])
                result["headers"] = cors_headers
                
            return result
            
        except Exception as e:
            return ResponseUtils.error_response(
                message="Error interno del servidor",
                status_code=500
            )
    
    return wrapper

def auth_required(func):
    """Decorator que requiere autenticación AWS Cognito para acceder a la lambda"""
    @wraps(func)
    def wrapper(event, context):
        # Extraer token
        token = AuthUtils.extract_token_from_event(event)
        
        if not token:
            return ResponseUtils.unauthorized_response("Token de autorización requerido")
        
        # Validar token de Cognito
        is_valid, payload = AuthUtils.validate_token(token)
        
        if not is_valid:
            error_message = payload.get("error", "Token inválido") if payload else "Token inválido"
            return ResponseUtils.unauthorized_response(error_message)
        
        # Extraer información del usuario y añadirla al evento
        user_info = AuthUtils.extract_user_info_from_token(payload)
        event["user_payload"] = user_info
        event["raw_token_payload"] = payload  # Por si necesitas el payload completo
        
        return func(event, context)
    
    return wrapper