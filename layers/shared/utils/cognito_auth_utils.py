import requests
import json
import os
import base64
from typing import Dict, Any, Optional, Tuple
import jwt  # PyJWT
from jwt import PyJWKClient, ExpiredSignatureError, InvalidTokenError
from utils.response_utils import ResponseUtils


class CognitoAuthUtils:
    """Utilidad para manejar autenticación AWS Cognito y headers relacionados"""
    
    @staticmethod
    def extract_token_from_event(event: Dict[str, Any]) -> Optional[str]:
        """Extrae el token de autorización del evento de Lambda"""
        # Buscar en headers
        headers = event.get("headers", {})
        
        # Buscar Authorization header (case insensitive)
        for header_key, header_value in headers.items():
            if header_key.lower() == "authorization":
                if header_value and header_value.startswith("Bearer "):
                    return header_value[7:]  # Remover "Bearer "
        
        return None
    
    @staticmethod
    def get_cognito_public_keys() -> Dict[str, Any]:
        """Obtiene las claves públicas de AWS Cognito para validar tokens"""
        try:
            region = os.getenv("AWS_REGION", "us-east-1")
            user_pool_id = os.getenv("COGNITO_USER_POOL_ID")
            
            if not user_pool_id:
                raise ValueError("COGNITO_USER_POOL_ID no configurado")
            
            jwks_url = f"https://cognito-idp.{region}.amazonaws.com/{user_pool_id}/.well-known/jwks.json"
            
            response = requests.get(jwks_url, timeout=10)
            response.raise_for_status()
            
            return response.json()
            
        except Exception as e:
            print(f"Error obteniendo claves públicas de Cognito: {str(e)}")
            return {}

    @staticmethod
    def validate_cognito_token(token: str) -> Tuple[bool, Optional[Dict[str, Any]]]:
        """Valida un token de AWS Cognito"""
        try:
            region = os.getenv("AWS_REGION", "us-east-1")
            user_pool_id = os.getenv("COGNITO_USER_POOL_ID")
            app_client_id = os.getenv("COGNITO_APP_CLIENT_ID")

            if not all([user_pool_id, app_client_id]):
                return False, {"error": "Configuración de Cognito incompleta"}

            # URL del JWKS
            jwks_url = f"https://cognito-idp.{region}.amazonaws.com/{user_pool_id}/.well-known/jwks.json"

            # Obtener la clave pública usando PyJWT
            jwk_client = PyJWKClient(jwks_url)
            signing_key = jwk_client.get_signing_key_from_jwt(token)

            # Decodificar el header para determinar el tipo de token
            header = jwt.get_unverified_header(token)
            unverified_payload = jwt.decode(token, options={"verify_signature": False})
            
            # Determinar si es un token de Client Credentials o de usuario
            token_use = unverified_payload.get("token_use")
            client_id = unverified_payload.get("client_id")
            
            if token_use == "access" and client_id and "aud" not in unverified_payload:
                # Token de Client Credentials - no requiere audience
                payload = jwt.decode(
                    token,
                    signing_key.key,
                    algorithms=["RS256"],
                    issuer=f"https://cognito-idp.{region}.amazonaws.com/{user_pool_id}",
                    options={"verify_aud": False}  # ✅ No verificar audience para client credentials
                )
            else:
                # Token de usuario normal - requiere audience
                payload = jwt.decode(
                    token,
                    signing_key.key,
                    algorithms=["RS256"],
                    audience=app_client_id,
                    issuer=f"https://cognito-idp.{region}.amazonaws.com/{user_pool_id}"
                )

            return True, payload

        except ExpiredSignatureError:
            return False, {"error": "Token expirado"}
        except InvalidTokenError as e:
            return False, {"error": f"Token inválido: {str(e)}"}
        except Exception as e:
            print(f"Error validando token: {str(e)}")
            return False, {"error": "Error interno validando token"}
    
    @staticmethod
    def is_cognito_token(token: str) -> bool:
        """Detecta si un token es de AWS Cognito"""
        try:
            header = jwt.get_unverified_header(token)
            # Los tokens de Cognito tienen 'kid' en el header
            return "kid" in header
        except:
            return False
    
    @staticmethod
    def validate_simple_jwt(token: str) -> Tuple[bool, Optional[Dict[str, Any]]]:
        """Valida un JWT simple (para desarrollo local o tokens HS256)"""
        try:
            secret_key = os.getenv("JWT_SECRET_KEY", "your-secret-key")
            payload = jwt.decode(token, secret_key, algorithms=["HS256"])
            return True, payload
        except ExpiredSignatureError:
            return False, {"error": "Token expirado"}
        except InvalidTokenError:
            return False, {"error": "Token inválido"}
        except Exception as e:
            return False, {"error": f"Error al validar token: {str(e)}"}

    @staticmethod
    def validate_token(token: str) -> Tuple[bool, Optional[Dict[str, Any]]]:
        """Método principal para validar tokens (detecta automáticamente el tipo)"""
        if CognitoAuthUtils.is_cognito_token(token):
            return CognitoAuthUtils.validate_cognito_token(token)
        else:
            return CognitoAuthUtils.validate_simple_jwt(token)
    
    @staticmethod
    def get_cognito_token_with_client_credentials(client_id: str, client_secret: str, scope: str) -> Optional[Dict[str, Any]]:
        """
        Obtiene un token usando Client Credentials Grant (para servicios)
        """
        try:
            region = os.getenv("AWS_REGION", "us-east-1")
            domain = os.getenv("COGNITO_DOMAIN", "motorcycle-repair-shop-user-pool")
            
            # Remover https:// si está presente
            if domain.startswith("https://"):
                domain = domain[8:]
            if domain.startswith("http://"):
                domain = domain[7:]
            
            token_url = f"https://{domain}/oauth2/token"
            
            # Crear credenciales en formato Basic Auth
            credentials = base64.b64encode(f"{client_id}:{client_secret}".encode()).decode()
            
            headers = {
                "Content-Type": "application/x-www-form-urlencoded",
                "Authorization": f"Basic {credentials}"
            }
            
            data = {
                "grant_type": "client_credentials",
                "scope": scope
            }
            
            response = requests.post(token_url, headers=headers, data=data, timeout=10)
            
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Error obteniendo token: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            print(f"Error en get_cognito_token_with_client_credentials: {str(e)}")
            return None
    
    @staticmethod
    def extract_user_info_from_token(payload: Dict[str, Any]) -> Dict[str, Any]:
        """Extrae información útil del usuario desde el payload del token de Cognito"""
        return {
            "user_id": payload.get("sub"),
            "username": payload.get("username"),
            "email": payload.get("email"),
            "client_id": payload.get("client_id"),
            "token_use": payload.get("token_use"),
            "scope": payload.get("scope", "").split(" ") if payload.get("scope") else [],
            "auth_time": payload.get("auth_time"),
            "iss": payload.get("iss"),
            "exp": payload.get("exp"),
            "iat": payload.get("iat"),
        }
    
    @staticmethod
    def extract_user_info_from_event(event: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Extrae información del usuario del evento (si fue procesado por decoradores)"""
        return event.get("user_payload", None)

    @staticmethod
    def get_auth_headers(token: Optional[str] = None) -> Dict[str, str]:
        """Obtiene headers de autenticación"""
        headers = ResponseUtils.get_cors_headers()
        
        if token:
            headers["Authorization"] = f"Bearer {token}"
        
        return headers

    @staticmethod
    def get_auth_headers_with_client_credentials(client_id: str, client_secret: str, scope: str) -> Dict[str, str]:
        """Obtiene headers de autenticación con Client Credentials Grant"""
        token_data = CognitoAuthUtils.get_cognito_token_with_client_credentials(client_id, client_secret, scope)
        if token_data and "access_token" in token_data:
            return CognitoAuthUtils.get_auth_headers(token_data["access_token"])
        return ResponseUtils.get_cors_headers()