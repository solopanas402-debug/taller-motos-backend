from utils.response_utils import ResponseUtils

def lambda_handler(event, context):
    """
    Lambda para manejar peticiones OPTIONS (preflight CORS)
    No requiere autenticación
    """
    return ResponseUtils.options_response()