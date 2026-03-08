import json
import re
import boto3
from botocore.exceptions import ClientError
from decorators.lambda_decorators import cors_enabled
from utils.response_utils import ResponseUtils
from db.db_client import DBClient
import os

from utils.cognito_auth_utils import CognitoAuthUtils

db_client = DBClient.get_client()
cognito_client = boto3.client("cognito-idp", region_name=os.getenv("AWS_REGION", "us-east-1"))

EMAIL_REGEX = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")

# ── Helpers ─────────────────────────────────────────────────────────────────────

def _validate_email(email: str) -> bool:
    return bool(EMAIL_REGEX.match(email))

def _validate_password(password: str) -> tuple:
    if len(password) < 8:
        return False, "Password must have at least 8 characters"
    if not re.search(r"[A-Z]", password):
        return False, "Password must contain at least one uppercase letter"
    if not re.search(r"[a-z]", password):
        return False, "Password must contain at least one lowercase letter"
    if not re.search(r"\d", password):
        return False, "Password must contain at least one number"
    return True, ""

def _resolve_role_id(role_name: str):
    """ Looks up id_role by name in 'roles' table. """
    try:
        result = db_client.table("roles").select("id_role").ilike("name", role_name).limit(1).execute()
        return result.data[0] if result.data else None
    except Exception as e:
        print(f"[register] Error resolving role '{role_name}': {str(e)}")
        raise

def _email_exists_in_db(email: str) -> bool:
    """ Checks if email exists in users table. """
    try:
        result = db_client.table("users").select("id_user").eq("email", email).limit(1).execute()
        return len(result.data) > 0 if result.data else False
    except Exception as e:
        print(f"[register] Error checking email: {str(e)}")
        raise

def _is_admin(cognito_sub: str) -> bool:
    """ Checks if a user has the admin role in Supabase. """
    try:
        result = (
            db_client
            .table("users")
            .select("roles(name)")
            .eq("cognito_sub", cognito_sub)
            .maybe_single()
            .execute()
        )
        if result and result.data:
            role_data = result.data.get("roles")
            # If roles is a list (multiple roles per user), handle accordingly.
            # Usually Supabase might return a dict for single relation.
            role_name = ""
            if isinstance(role_data, list) and role_data:
                role_name = role_data[0].get("name", "")
            elif isinstance(role_data, dict):
                role_name = role_data.get("name", "")
            
            return role_name.lower() == "admin"
        return False
    except Exception as e:
        print(f"[register] Error checking admin status for {cognito_sub}: {str(e)}")
        return False

# ── Handler ──────────────────────────────────────────────────────────────────────

@cors_enabled
def lambda_handler(event, context):
    print("[register] New registration attempt (Admin required)")

    # ── Paso 1: Verificar token del admin ─────────────────────────────────────
    access_token = CognitoAuthUtils.extract_token_from_event(event)
    if not access_token:
        return ResponseUtils.unauthorized_response("Authorization token is required")

    try:
        user_info = cognito_client.get_user(AccessToken=access_token)
        admin_sub = user_info["Username"]  # Or lookup in Attributes for 'sub'
        # user_info['Username'] usually contains the sub if using AccessToken
    except ClientError as e:
        print(f"[register] Token validation failed: {str(e)}")
        return ResponseUtils.unauthorized_response("Invalid or expired token")

    # ── Paso 2: Verificar que quien registra es admin ──────────────────────────
    if not _is_admin(admin_sub):
        print(f"[register] Access denied: User {admin_sub} is not an admin")
        return ResponseUtils.forbidden_response("You do not have permission to register new users")

    # ── Paso 3: Registrar el nuevo usuario ─────────────────────────────────────
    try:
        body = json.loads(event.get("body") or "{}")
    except json.JSONDecodeError:
        return ResponseUtils.bad_request_response("The request body is not a valid JSON")

    email    = (body.get("email")    or "").strip().lower()
    password = (body.get("password") or "").strip()
    username = (body.get("username") or "").strip()
    name     = (body.get("name")     or "").strip()
    surname  = (body.get("surname")  or "").strip()
    role     = (body.get("role")     or "").strip()

    if not email or not password or not username or not role:
        return ResponseUtils.bad_request_response("Missing required fields")

    if not _validate_email(email):
        return ResponseUtils.bad_request_response("Invalid email format")
    
    valid_pwd, pwd_msg = _validate_password(password)
    if not valid_pwd:
        return ResponseUtils.bad_request_response(pwd_msg)

    user_pool_id = os.getenv("COGNITO_USER_POOL_ID")
    
    try:
        # Resolver Rol para el nuevo usuario
        role_data = _resolve_role_id(role)
        if not role_data:
            return ResponseUtils.bad_request_response(f"The role '{role}' does not exist")
        
        id_role = role_data["id_role"]

        if _email_exists_in_db(email):
            return ResponseUtils.conflict_response(f"The email '{email}' is already registered")

        print(f"[register] Creating in Cognito: {email}")
        try:
            response = cognito_client.admin_create_user(
                UserPoolId=user_pool_id,
                Username=email,
                MessageAction="SUPPRESS",
                UserAttributes=[
                    {"Name": "email", "Value": email},
                    {"Name": "email_verified", "Value": "true"},
                ],
            )
            
            cognito_sub = next(attr["Value"] for attr in response["User"]["Attributes"] if attr["Name"] == "sub")

            cognito_client.admin_set_user_password(
                UserPoolId=user_pool_id,
                Username=email,
                Password=password,
                Permanent=True,
            )
        except ClientError as e:
            error_code = e.response.get("Error", {}).get("Code", "")
            if error_code == "UsernameExistsException":
                return ResponseUtils.bad_request_response("User already exists")
            if error_code == "InvalidPasswordException":
                return ResponseUtils.bad_request_response("Password does not meet requirements")
            print(f"[register] Cognito error: {str(e)}")
            return ResponseUtils.bad_request_response("Error during registration process")

        print(f"[register] Inserting into Supabase...")
        try:
            user_record = (
                db_client
                .table("users")
                .insert({
                    "cognito_sub": cognito_sub,
                    "id_role":     id_role,
                    "username":    username,
                    "password":    "COGNITO_MANAGED",
                    "name":        name,
                    "surname":     surname,
                    "email":       email,
                    "active":      True,
                })
                .execute()
            )
            
            user_data = user_record.data[0] if user_record and getattr(user_record, "data", None) else {}
            
            return ResponseUtils.created_response(
                data={
                    "user": {
                        "id":         user_data.get("id_user"),
                        "username":   user_data.get("username"),
                        "full_name":  f"{user_data.get('name', '')} {user_data.get('surname', '')}".strip(),
                        "email":      user_data.get("email"),
                        "role_id":    user_data.get("id_role"),
                        "active":     user_data.get("active"),
                        "created_at": user_data.get("created_at")
                    }
                },
                message="User registered successfully"
            )

        except Exception as supabase_error:
            print(f"[register] Error inserting into Supabase: {supabase_error}")
            try:
                cognito_client.admin_delete_user(
                    UserPoolId=user_pool_id,
                    Username=email,
                )
            except Exception as rollback_err:
                print(f"[register] ERROR Cognito rollback: {rollback_err}")
            
            return ResponseUtils.internal_server_error_response("Internal server error")

    except Exception as e:
        print(f"[register] Technical error: {str(e)}")
        return ResponseUtils.internal_server_error_response("Internal server error")
