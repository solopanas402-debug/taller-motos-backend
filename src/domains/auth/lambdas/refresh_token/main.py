import json
import os
import boto3
from botocore.exceptions import ClientError
from decorators.lambda_decorators import cors_enabled
from db.db_client import DBClient
from utils.response_utils import ResponseUtils

db_client = DBClient.get_client()
cognito_client = boto3.client("cognito-idp", region_name=os.getenv("AWS_REGION", "us-east-1"))


def _get_user_from_db(email: str):
    """
    Query Supabase checking if user exists and is active.
    """
    try:
        result = (
            db_client
            .table("users")
            .select("id_user, id_role, username, name, surname, email, active")
            .eq("email", email)
            .maybe_single()
            .execute()
        )
        return result.data
    except Exception as e:
        print(f"[refresh_token] Error querying user in DB: {str(e)}")
        return None


@cors_enabled
def lambda_handler(event, context):
    print(f"[refresh_token] Refresh token attempt")

    try:
        body = json.loads(event.get("body") or "{}")
    except json.JSONDecodeError:
        return ResponseUtils.bad_request_response("The request body is not a valid JSON")

    refresh_token = body.get("refresh_token", "").strip()

    if not refresh_token:
        return ResponseUtils.bad_request_response("The field 'refresh_token' is required")

    user_app_client_id = os.getenv("COGNITO_USER_APP_CLIENT_ID")
    if not user_app_client_id:
        print("[refresh_token] ERROR: COGNITO_USER_APP_CLIENT_ID not configured")
        return ResponseUtils.internal_server_error_response("Server configuration error")

    try:
        cognito_response = cognito_client.initiate_auth(
            AuthFlow="REFRESH_TOKEN_AUTH",
            AuthParameters={
                "REFRESH_TOKEN": refresh_token,
            },
            ClientId=user_app_client_id,
        )
        
        auth_result = cognito_response.get("AuthenticationResult", {})
        new_access_token = auth_result.get("AccessToken")
        expires_in = auth_result.get("ExpiresIn", 3600)
        
        # We need the user data for the standardized response
        user_info = cognito_client.get_user(AccessToken=new_access_token)
        email = next(attr["Value"] for attr in user_info["UserAttributes"] if attr["Name"] == "email")
        user_data = _get_user_from_db(email)
        
        if not user_data:
            return ResponseUtils.forbidden_response("User not found in system")

        return ResponseUtils.success_response(
            data={
                "user": {
                    "id":       user_data.get("id_user"),
                    "username": user_data.get("username"),
                    "name":     user_data.get("name"),
                    "surname":  user_data.get("surname"),
                    "email":    user_data.get("email"),
                    "id_role":  user_data.get("id_role"),
                },
                "tokens": {
                    "access_token": new_access_token,
                    "token_type":   "Bearer",
                    "expires_in":   expires_in,
                }
            },
            message="Token refreshed successfully"
        )

    except ClientError as e:
        error_code = e.response.get("Error", {}).get("Code", "")
        print(f"[refresh_token] Cognito error: {error_code}")

        if error_code in ("NotAuthorizedException", "InvalidParameterException"):
            return ResponseUtils.unauthorized_response("Invalid or expired refresh token")
        if error_code == "TooManyRequestsException":
            return ResponseUtils.too_many_requests_response("Too many requests. Try again later.")

        print(f"[refresh_token] Unexpected Cognito error: {str(e)}")
        return ResponseUtils.internal_server_error_response("Internal server error")
    except Exception as e:
        print(f"[refresh_token] Technical error: {str(e)}")
        return ResponseUtils.internal_server_error_response("Internal server error")
