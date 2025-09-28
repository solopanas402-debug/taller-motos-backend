from functools import wraps
import json
from utils.response_utils import ResponseUtils
from utils.cognito_auth_utils import CognitoAuthUtils

def cors_enabled(func):
    @wraps(func)
    def wrapper(event, context):
        if event.get("httpMethod") == "OPTIONS":
            print("🔧 Manejando petición OPTIONS (CORS preflight)")
            return ResponseUtils.options_response()

        try:
            result = func(event, context)

            if isinstance(result, dict) and "headers" not in result:
                result["headers"] = ResponseUtils.get_cors_headers()
            elif isinstance(result, dict) and result.get("headers"):
                cors_headers = ResponseUtils.get_cors_headers()
                cors_headers.update(result["headers"])
                result["headers"] = cors_headers

            return result

        except Exception as e:
            print(f"❌ Error en cors_enabled wrapper: {str(e)}")
            return ResponseUtils.error_response(
                message="Error interno del servidor",
                status_code=500
            )

    return wrapper


def cognito_auth_required(func):
    @wraps(func)
    def wrapper(event, context):
        print("🔐 Iniciando validación de autenticación Cognito...")
        print(f"📋 Headers recibidos: {json.dumps(event.get('headers', {}), indent=2)}")

        token = CognitoAuthUtils.extract_token_from_event(event)

        if not token:
            print("❌ No se encontró token de autorización")
            return ResponseUtils.unauthorized_response("Token de autorización requerido")

        print(f"🎟️  Token encontrado: {token[:20]}..." if len(token) > 20 else f"🎟️  Token encontrado: {token}")

        is_valid, payload = CognitoAuthUtils.validate_token(token)

        if not is_valid:
            error_message = payload.get("error", "Token inválido") if payload else "Token inválido"
            print(f"❌ Token inválido: {error_message}")
            if payload:
                print(f"📋 Detalles del error: {json.dumps(payload, indent=2)}")
            return ResponseUtils.unauthorized_response(error_message)

        print("✅ Token válido")
        print(f"👤 Payload del token: {json.dumps(payload, indent=2, default=str)}")

        user_info = CognitoAuthUtils.extract_user_info_from_token(payload)
        event["user_payload"] = user_info
        event["raw_token_payload"] = payload

        print(f"👤 Información del usuario extraída: {json.dumps(user_info, indent=2, default=str)}")

        return func(event, context)

    return wrapper


def debug_event(func):
    @wraps(func)
    def wrapper(event, context):
        print("🐛 ===== DEBUG EVENT =====")
        print(f"📋 Evento completo: {json.dumps(event, indent=2, default=str)}")
        print(f"📋 Contexto: {json.dumps({
            'function_name': getattr(context, 'function_name', 'N/A'),
            'function_version': getattr(context, 'function_version', 'N/A'),
            'invoked_function_arn': getattr(context, 'invoked_function_arn', 'N/A'),
            'memory_limit_in_mb': getattr(context, 'memory_limit_in_mb', 'N/A'),
            'remaining_time_in_millis': getattr(context, 'get_remaining_time_in_millis', lambda: 'N/A')()
        }, indent=2)}")
        print("🐛 ========================")

        return func(event, context)

    return wrapper
