from functools import wraps
from utils.response_utils import ResponseUtils
from utils.cognito_auth_utils import CognitoAuthUtils

def cors_enabled(func):
    @wraps(func)
    def wrapper(event, context):
        if event.get("httpMethod") == "OPTIONS":
            return ResponseUtils.options_response()

        try:
            result = func(event, context)
            if isinstance(result, dict):
                if "headers" not in result:
                    result["headers"] = ResponseUtils.get_cors_headers()
                else:
                    result["headers"].update(ResponseUtils.get_cors_headers())
            return result
        except Exception as e:
            return ResponseUtils.error_response(
                message="Error interno del servidor",
                status_code=500
            )
    return wrapper

def cognito_auth_required(func):
    @wraps(func)
    def wrapper(event, context):
        token = CognitoAuthUtils.extract_token_from_event(event)
        if not token:
            return ResponseUtils.unauthorized_response("Token de autorización requerido")

        is_valid, payload = CognitoAuthUtils.validate_token(token)
        if not is_valid:
            return ResponseUtils.unauthorized_response("Token inválido")

        event["user_payload"] = payload
        return func(event, context)
    return wrapper
