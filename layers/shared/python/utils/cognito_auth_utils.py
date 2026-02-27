import os
from typing import Dict, Any, Optional, Tuple
import jwt
from jwt import PyJWKClient, ExpiredSignatureError, InvalidTokenError
from utils.response_utils import ResponseUtils


class CognitoAuthUtils:
    """Utilidad básica para autenticación AWS Cognito"""
    
    @staticmethod
    def extract_token_from_event(event: Dict[str, Any]) -> Optional[str]:
        """Extrae el token de autorización del evento de Lambda"""
        headers = event.get("headers", {})
        for header_key, header_value in headers.items():
            if header_key.lower() == "authorization":
                if header_value and header_value.startswith("Bearer "):
                    return header_value[7:]
        return None

    @staticmethod
    def validate_token(token: str) -> Tuple[bool, Optional[Dict[str, Any]]]:
        """Validación simple de token Cognito"""
        try:
            region = os.getenv("AWS_REGION", "us-east-1")
            user_pool_id = os.getenv("COGNITO_USER_POOL_ID")
            
            if not user_pool_id:
                return False, None

            jwks_url = f"https://cognito-idp.{region}.amazonaws.com/{user_pool_id}/.well-known/jwks.json"
            jwk_client = PyJWKClient(jwks_url)
            signing_key = jwk_client.get_signing_key_from_jwt(token)

            return True, jwt.decode(
                token,
                signing_key.key,
                algorithms=["RS256"],
                options={"verify_aud": False},
                issuer=f"https://cognito-idp.{region}.amazonaws.com/{user_pool_id}"
            )

        except (ExpiredSignatureError, InvalidTokenError, Exception):
            return False, None

    @staticmethod
    def get_auth_headers() -> Dict[str, str]:
        """Headers CORS básicos"""
        return ResponseUtils.get_cors_headers()