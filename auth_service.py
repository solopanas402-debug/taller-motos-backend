import os
import jwt
import json
import requests
from datetime import datetime, timedelta
from functools import wraps
from flask import request, jsonify

# Configuración
JWT_SECRET = os.environ.get("JWT_SECRET", "motorcycle-repair-shop-jwt-secret-key-2024")
JWT_ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 15
REFRESH_TOKEN_EXPIRE_DAYS = 7

# Supabase
SUPABASE_URL = os.environ.get("DB_URL", "https://toklwbqrgqsgaovzleev.supabase.co")
SUPABASE_KEY = os.environ.get("DB_KEY", "sb_publishable_9ToFd0mY6_QhXaGecuwxQA_ixnC9hQ0")


class AuthService:
    """Servicio de autenticación con JWT y Refresh Tokens"""
    
    @staticmethod
    def _make_supabase_request(method, table, data=None, filters=None):
        """Hace requests a Supabase REST API"""
        try:
            url = f"{SUPABASE_URL}/rest/v1/{table}"
            headers = {
                "apikey": SUPABASE_KEY,
                "Authorization": f"Bearer {SUPABASE_KEY}",
                "Content-Type": "application/json",
                "Prefer": "return=representation"
            }
            
            if method == "GET":
                if filters:
                    query_parts = []
                    for key, value in filters.items():
                        query_parts.append(f"{key}=eq.{value}")
                    url += "?" + "&".join(query_parts)
                response = requests.get(url, headers=headers, timeout=10)
            elif method == "POST":
                response = requests.post(url, json=data, headers=headers, timeout=10)
            elif method == "DELETE":
                if filters:
                    query_parts = []
                    for key, value in filters.items():
                        query_parts.append(f"{key}=eq.{value}")
                    url += "?" + "&".join(query_parts)
                response = requests.delete(url, headers=headers, timeout=10)
            else:
                return None
            
            if response.status_code < 400:
                return response.json() if response.text else []
            else:
                print(f"Error Supabase: {response.status_code} - {response.text}")
                return None
        except Exception as e:
            print(f"Error en request Supabase: {e}")
            return None
    
    @staticmethod
    def create_access_token(user_id: str, email: str) -> str:
        """Crea un token de acceso (corta duración)"""
        payload = {
            "user_id": user_id,
            "email": email,
            "type": "access",
            "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
            "iat": datetime.utcnow()
        }
        return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    
    @staticmethod
    def create_refresh_token(user_id: str) -> str:
        """Crea un refresh token (larga duración)"""
        payload = {
            "user_id": user_id,
            "type": "refresh",
            "exp": datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS),
            "iat": datetime.utcnow()
        }
        return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    
    @staticmethod
    def verify_token(token: str) -> dict:
        """Verifica y decodifica un token"""
        try:
            payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
            return payload
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None
    
    @staticmethod
    def register_user(email: str, password: str, name: str = None, username: str = None) -> dict:
        """Registra un nuevo usuario en Supabase"""
        try:
            # Verificar si el usuario ya existe por email
            users = AuthService._make_supabase_request("GET", "users", filters={"email": email})
            
            if users and len(users) > 0:
                return {"error": "El usuario ya existe", "status": 400}
            
            # Verificar si el username ya existe
            if username:
                users = AuthService._make_supabase_request("GET", "users", filters={"username": username})
                if users and len(users) > 0:
                    return {"error": "El username ya existe", "status": 400}
            
            # Obtener un rol por defecto
            roles = AuthService._make_supabase_request("GET", "roles")
            if not roles or len(roles) == 0:
                return {"error": "No hay roles disponibles", "status": 500}
            
            default_role_id = roles[0]["id_role"]
            
            # Crear usuario
            user_data = {
                "email": email,
                "password": password,
                "username": username or email.split("@")[0],
                "name": name or email.split("@")[0],
                "surname": "User",
                "id_role": default_role_id,
                "active": True
            }
            
            response = AuthService._make_supabase_request("POST", "users", data=user_data)
            
            if response and len(response) > 0:
                user = response[0]
                return {
                    "user_id": user["id_user"],
                    "email": user["email"],
                    "username": user["username"],
                    "name": user["name"],
                    "status": 201
                }
            
            return {"error": "Error al crear usuario", "status": 500}
            
        except Exception as e:
            return {"error": str(e), "status": 500}
    
    @staticmethod
    def login_user(email: str, password: str) -> dict:
        """Autentica un usuario y retorna tokens"""
        try:
            # Buscar usuario por email
            users = AuthService._make_supabase_request("GET", "users", filters={"email": email})
            
            if not users or len(users) == 0:
                return {"error": "Usuario o contraseña incorrectos", "status": 401}
            
            user = users[0]
            
            # Verificar que el usuario esté activo
            if not user.get("active", False):
                return {"error": "Usuario inactivo", "status": 401}
            
            # Verificar contraseña
            if user["password"] != password:
                return {"error": "Usuario o contraseña incorrectos", "status": 401}
            
            # Generar tokens
            access_token = AuthService.create_access_token(user["id_user"], user["email"])
            refresh_token = AuthService.create_refresh_token(user["id_user"])
            
            # Guardar refresh token en BD (opcional)
            try:
                AuthService._make_supabase_request("POST", "refresh_tokens", data={
                    "user_id": user["id_user"],
                    "token": refresh_token,
                    "expires_at": (datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)).isoformat()
                })
            except Exception as e:
                print(f"Advertencia: No se pudo guardar refresh token: {e}")
                pass
            
            return {
                "access_token": access_token,
                "refresh_token": refresh_token,
                "user": {
                    "id": user["id_user"],
                    "email": user["email"],
                    "username": user["username"],
                    "name": user["name"]
                },
                "status": 200
            }
            
        except Exception as e:
            return {"error": str(e), "status": 500}
    
    @staticmethod
    def refresh_access_token(refresh_token: str) -> dict:
        """Genera un nuevo access token usando el refresh token"""
        try:
            # Verificar refresh token
            payload = AuthService.verify_token(refresh_token)
            
            if not payload or payload.get("type") != "refresh":
                return {"error": "Refresh token inválido", "status": 401}
            
            user_id = payload["user_id"]
            
            # Obtener datos del usuario
            users = AuthService._make_supabase_request("GET", "users", filters={"id_user": user_id})
            
            if not users or len(users) == 0:
                return {"error": "Usuario no encontrado", "status": 404}
            
            user = users[0]
            
            # Generar nuevo access token
            new_access_token = AuthService.create_access_token(user["id_user"], user["email"])
            
            return {
                "access_token": new_access_token,
                "status": 200
            }
            
        except Exception as e:
            return {"error": str(e), "status": 500}
    
    @staticmethod
    def logout_user(refresh_token: str) -> dict:
        """Invalida el refresh token"""
        try:
            try:
                AuthService._make_supabase_request("DELETE", "refresh_tokens", filters={"token": refresh_token})
            except Exception as e:
                print(f"Advertencia: No se pudo eliminar refresh token: {e}")
                pass
            return {"message": "Logout exitoso", "status": 200}
        except Exception as e:
            return {"error": str(e), "status": 500}


def token_required(f):
    """Decorador para proteger rutas que requieren token"""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        
        # Obtener token del header
        if "Authorization" in request.headers:
            auth_header = request.headers["Authorization"]
            try:
                token = auth_header.split(" ")[1]
            except IndexError:
                return jsonify({"error": "Token inválido"}), 401
        
        if not token:
            return jsonify({"error": "Token requerido"}), 401
        
        # Verificar token
        payload = AuthService.verify_token(token)
        
        if not payload or payload.get("type") != "access":
            return jsonify({"error": "Token inválido o expirado"}), 401
        
        # Pasar información del usuario a la ruta
        request.user = payload
        
        return f(*args, **kwargs)
    
    return decorated
