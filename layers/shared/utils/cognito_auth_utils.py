import requests
import json
import os
import base64
from typing import Dict, Any, Optional, Tuple
from jose import jwt, JWKError
from jose.utils import base64url_decode

class CognitoAuthUtils:
    """Utilidad para manejar autenticación AWS Cognito y headers relacionados"""
    
    @staticmethod
    def get_auth_headers(token: Optional[str] = None) -> Dict[str, str]:
        """Obtiene headers de autenticación"""
        headers = ResponseUtils.get_cors_headers()
        
        if token:
            headers["Authorization"] = f"Bearer {token}"
        
        return headers
    
    @staticmethod
    def extract_token_from_event(event: Dict[str, Any]) -> Optional[str]:
        """Extrae el token de autorización del evento de Lambda"""
        # Buscar en headers
        headers = event.get("headers", {})
        
        # Buscar Authorization header (case insensitive)
        for header_key, header_value in headers.items():
            if header_key.lower() == "authorization":
                if header_value.startswith("Bearer "):
                    return header_value[7:]  # Remover "Bearer "
        
        return None
    
    @staticmethod
    def get_cognito_public_keys() -> Dict[str, Any]:
        """Obtiene las claves públicas de AWS Cognito para validar tokens"""
        try:
            region = os.getenv("AWS_REGION", "us-east-1")
            user_pool_id = os.getenv("COGNITO_USER_POOL_ID", "us-east-1_XXXXXXXXX")
            
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
            # Obtener header del token sin verificar
            unverified_header = jwt.get_unverified_header(token)
            
            # Obtener claves públicas de Cognito
            jwks = AuthUtils.get_cognito_public_keys()
            if not jwks or "keys" not in jwks:
                return False, {"error": "No se pudieron obtener las claves públicas"}
            
            # Buscar la clave correcta por kid
            kid = unverified_header.get("kid")
            key = None
            
            for jwk in jwks["keys"]:
                if jwk.get("kid") == kid:
                    key = jwk
                    break
            
            if not key:
                return False, {"error": "Clave pública no encontrada"}
            
            # Verificar el token
            region = os.getenv("AWS_REGION", "us-east-1")
            user_pool_id = os.getenv("COGNITO_USER_POOL_ID", "us-east-1_XXXXXXXXX")
            app_client_id = os.getenv("COGNITO_APP_CLIENT_ID", "your-app-client-id")
            
            # Decodificar y validar el token
            payload = jwt.decode(
                token,
                key,
                algorithms=["RS256"],
                audience=app_client_id,
                issuer=f"https://cognito-idp.{region}.amazonaws.com/{user_pool_id}"
            )
            
            return True, payload
            
        except jwt.ExpiredSignatureError:
            return False, {"error": "Token expirado"}
        except jwt.JWTClaimsError:
            return False, {"error": "Claims del token inválidos"}
        except JWKError:
            return False, {"error": "Error de clave JWK"}
        except Exception as e:
            print(f"Error validando token de Cognito: {str(e)}")
            return False, {"error": "Token inválido"}
    
    @staticmethod
    def validate_token(token: str) -> Tuple[bool, Optional[Dict[str, Any]]]:
        """Método principal para validar tokens (detecta automáticamente el tipo)"""
        # Para tokens de Cognito, usar validación específica
        if AuthUtils.is_cognito_token(token):
            return AuthUtils.validate_cognito_token(token)
        else:
            # Fallback para JWT simples (si los usas en algún caso)
            return AuthUtils.validate_simple_jwt(token)
    
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
        """Valida un JWT simple (para casos legacy o desarrollo local)"""
        try:
            secret_key = os.getenv("JWT_SECRET_KEY", "your-secret-key")
            payload = jwt.decode(token, secret_key, algorithms=["HS256"])
            return True, payload
        except jwt.ExpiredSignatureError:
            return False, {"error": "Token expirado"}
        except jwt.JWTError:
            return False, {"error": "Token inválido"}
        except Exception as e:
            return False, {"error": f"Error al validar token: {str(e)}"}
    
    @staticmethod
    def get_cognito_token_with_client_credentials(client_id: str, client_secret: str, scope: str) -> Optional[str]:
        """
        Obtiene un token usando Client Credentials Grant (para servicios)
        Esto es útil para testing o comunicación entre servicios
        """
        try:
            # URL de tu User Pool
            region = os.getenv("AWS_REGION", "us-east-1")
            domain = os.getenv("COGNITO_DOMAIN", "motorcycle-repair-shop-user-pool")
            
            token_url = f"https://{domain}.auth.{region}.amazoncognito.com/oauth2/token"
            
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
                token_data = response.json()
                return token_data.get("access_token")
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
            "user_id": payload.get("sub"),  # Subject (ID único del usuario)
            "username": payload.get("username"),
            "email": payload.get("email"),
            "client_id": payload.get("client_id"),
            "token_use": payload.get("token_use"),  # 'access' o 'id'
            "scope": payload.get("scope", "").split(" ") if payload.get("scope") else [],
            "auth_time": payload.get("auth_time"),
            "iss": payload.get("iss"),  # Issuer
            "exp": payload.get("exp"),  # Expiration time
            "iat": payload.get("iat"),  # Issued at
        }
    
    @staticmethod
    def extract_token_from_event(event: Dict[str, Any]) -> Optional[str]:
        """Extrae el token de autorización de la solicitud HTTP (si lo encuentra)"""
        return event.get("headers", {}).get("Authorization", None)

    @staticmethod
    def extract_user_info_from_event(event: Dict[str, Any]) -> Optional[Dict[str, Any]]:
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
        """Obtiene headers de autenticación con Client Credentials Grant (para servicios)"""
        token = CognitoAuthUtils.get_cognito_token_with_client_credentials(client_id, client_secret, scope)
        return CognitoAuthUtils.get_auth_headers(token)

        return headers