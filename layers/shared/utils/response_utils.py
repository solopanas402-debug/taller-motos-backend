import json
from typing import Dict, Any, Optional

class ResponseUtils:
    """Utilidad para manejar respuestas estandarizadas con headers CORS"""
    
    @staticmethod
    def get_cors_headers(origin: Optional[str] = None) -> Dict[str, str]:
        """Obtiene los headers CORS básicos"""



        return {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Headers": "Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token,X-Requested-With,x-tenant-id",
            "Access-Control-Allow-Methods": "GET,POST,PUT,DELETE,OPTIONS,PATCH",
            "Content-Type": "application/json"
        }
    
    @staticmethod
    def success_response(data: Any, status_code: int = 200, message: str = "Operation successful", additional_headers: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        """Crea una respuesta de éxito con el formato estándar: status, statusCode, message, data"""
        headers = ResponseUtils.get_cors_headers()
        
        if additional_headers:
            headers.update(additional_headers)
        
        response_body = {
            "status": "success",
            "statusCode": status_code,
            "message": message,
            "data": data
        }
        
        return {
            "statusCode": status_code,
            "headers": headers,
            "body": json.dumps(response_body, ensure_ascii=False, default=str)
        }
    
    @staticmethod
    def error_response(message: str, status_code: int = 500, additional_headers: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        """Crea una respuesta de error con el formato estándar: status, statusCode, message, data"""
        headers = ResponseUtils.get_cors_headers()
        
        if additional_headers:
            headers.update(additional_headers)
        
        error_data = {
            "status": "error",
            "statusCode": status_code,
            "message": message,
            "data": None
        }
        
        return {
            "statusCode": status_code,
            "headers": headers,
            "body": json.dumps(error_data, ensure_ascii=False, default=str)
        }
    
    @staticmethod
    def options_response() -> Dict[str, Any]:
        """Respuesta para peticiones OPTIONS (preflight CORS)"""
        return {
            "statusCode": 200,
            "headers": ResponseUtils.get_cors_headers(),
            "body": ""
        }
    
    @staticmethod
    def not_found_response(message: str = "Resource not found", additional_headers: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        """Crea una respuesta 404 Not Found"""
        return ResponseUtils.error_response(message, 404, additional_headers)
    
    @staticmethod
    def conflict_response(message: str = "Conflict in request", additional_headers: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        """Crea una respuesta 409 Conflict"""
        return ResponseUtils.error_response(message, 409, additional_headers)
    
    @staticmethod
    def bad_request_response(message: str = "Bad request", additional_headers: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        """Crea una respuesta 400 Bad Request"""
        return ResponseUtils.error_response(message, 400, additional_headers)
    
    @staticmethod
    def unauthorized_response(message: str = "Unauthorized", additional_headers: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        """Crea una respuesta 401 Unauthorized"""
        return ResponseUtils.error_response(message, 401, additional_headers)
    
    @staticmethod
    def forbidden_response(message: str = "Forbidden access", additional_headers: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        """Crea una respuesta 403 Forbidden"""
        return ResponseUtils.error_response(message, 403, additional_headers)
    
    @staticmethod
    def unprocessable_entity_response(message: str = "Unprocessable entity", additional_headers: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        """Crea una respuesta 422 Unprocessable Entity"""
        return ResponseUtils.error_response(message, 422, additional_headers)
    
    @staticmethod
    def internal_server_error_response(message: str = "Internal server error", additional_headers: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        """Crea una respuesta 500 Internal Server Error"""
        return ResponseUtils.error_response(message, 500, additional_headers)
    
    @staticmethod
    def created_response(data: Any, message: str = "Resource created successfully", additional_headers: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        """Crea una respuesta 201 Created"""
        return ResponseUtils.success_response(data=data, status_code=201, message=message, additional_headers=additional_headers)
    
    @staticmethod
    def no_content_response(additional_headers: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        """Crea una respuesta 204 No Content"""
        headers = ResponseUtils.get_cors_headers()
        
        if additional_headers:
            headers.update(additional_headers)
        
        return {
            "statusCode": 204,
            "headers": headers,
            "body": ""
        }
    
    @staticmethod
    def too_many_requests_response(message: str = "Too many requests", additional_headers: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        """Crea una respuesta 429 Too Many Requests"""
        return ResponseUtils.error_response(message, 429, additional_headers)