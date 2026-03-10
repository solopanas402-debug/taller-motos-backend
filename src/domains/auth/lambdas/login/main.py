import json
import boto3
from botocore.exceptions import ClientError
from decorators.lambda_decorators import cors_enabled
from utils.response_utils import ResponseUtils
from db.db_client import DBClient
import os

db_client = DBClient.get_client()

cognito_client = boto3.client("cognito-idp", region_name=os.getenv("AWS_REGION", "us-east-1"))


def _get_user_from_db(email: str):
    """
    Consulta Supabase verificando que el usuario exista y esté activo.
    """
    try:
        result = (
            db_client
            .table("users")
            .select("id_user, id_role, username, name, surname, email, active, roles(name)")
            .eq("email", email)
            .maybe_single()
            .execute()
        )
        return result.data
    except Exception as e:
        print(f"[login] Error consultando usuario en DB: {str(e)}")
        return None


@cors_enabled
def lambda_handler(event, context):
    print(f"[login] event: {event}")

    try:
        body = json.loads(event.get("body") or "{}")
    except json.JSONDecodeError:
        return ResponseUtils.bad_request_response("The request body is not a valid JSON")

    email    = (body.get("email")    or "").strip().lower()
    password = (body.get("password") or "").strip()

    if not email or not password:
        return ResponseUtils.bad_request_response("Email and password are required")

    user_app_client_id = os.getenv("COGNITO_USER_APP_CLIENT_ID")
    if not user_app_client_id:
        print("[login] ERROR: COGNITO_USER_APP_CLIENT_ID not configured")
        return ResponseUtils.internal_server_error_response("Server configuration error")

    try:
        cognito_response = cognito_client.initiate_auth(
            AuthFlow="USER_PASSWORD_AUTH",
            AuthParameters={
                "USERNAME": email,
                "PASSWORD": password,
            },
            ClientId=user_app_client_id,
        )
    except ClientError as e:
        error_code = e.response.get("Error", {}).get("Code", "")
        print(f"[login] Cognito error: {error_code}")

        if error_code in ("NotAuthorizedException", "UserNotFoundException"):
            return ResponseUtils.unauthorized_response("Invalid credentials")
        if error_code == "UserNotConfirmedException":
            return ResponseUtils.unauthorized_response("The account has not been verified. Check your email.")
        if error_code == "PasswordResetRequiredException":
            return ResponseUtils.unauthorized_response("You must reset your password before logging in")
        if error_code == "TooManyRequestsException":
            return ResponseUtils.too_many_requests_response("Too many login attempts. Try again later.")

        print(f"[login] Unexpected Cognito error: {str(e)}")
        return ResponseUtils.internal_server_error_response("Internal server error")

    auth_result = cognito_response.get("AuthenticationResult", {})
    user_data = _get_user_from_db(email)

    if user_data is None:
        print(f"[login] User authenticated in Cognito but not found in DB: {email}")
        return ResponseUtils.forbidden_response("Your account is not registered in the system.")

    if not user_data.get("active", True):
        print(f"[login] Disabled user attempting login: {email}")
        return ResponseUtils.forbidden_response("Your account is disabled. Contact the administrator.")

    # Extract role name
    role_name = ""
    roles_info = user_data.get("roles")
    if isinstance(roles_info, dict):
        role_name = roles_info.get("name", "")
    elif isinstance(roles_info, list) and roles_info:
        role_name = roles_info[0].get("name", "")

    # Format specified: user first, then tokens
    return ResponseUtils.success_response(
        data={
            "user": {
                "id":       user_data.get("id_user"),
                "username": user_data.get("username"),
                "name":     user_data.get("name"),
                "surname":  user_data.get("surname"),
                "email":    user_data.get("email"),
                "role":     role_name,
                "id_role":  user_data.get("id_role"),
            },
            "tokens": {
                "access_token":  auth_result.get("AccessToken"),
                "refresh_token": auth_result.get("RefreshToken"),
                "token_type":    "Bearer",
                "expires_in":    auth_result.get("ExpiresIn", 3600),
            }
        },
        message="Login successful"
    )
