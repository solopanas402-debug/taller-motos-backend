import json
import boto3
import os
from decorators.lambda_decorators import cors_enabled, cognito_auth_required
from db.db_client import DBClient
from utils.response_utils import ResponseUtils

db_client = DBClient.get_client()

def _get_user_profile(cognito_sub: str):
    """
    Fetch user details from Supabase using their Cognito sub ID.
    Includes role details by joining the 'roles' table.
    """
    try:
        result = (
            db_client
            .table("users")
            .select("id_user, id_role, username, name, surname, email, active, created_at, roles(name)")
            .eq("cognito_sub", cognito_sub)
            .maybe_single()
            .execute()
        )
        return result.data
    except Exception as e:
        print(f"[me] Error querying user profile from DB: {str(e)}")
        return None

@cors_enabled
@cognito_auth_required
def lambda_handler(event, context):
    print("[me] User profile request")

    # Get Cognito sub from the payload attached by cognito_auth_required decorator
    # The decorator usually places payload in event["requestContext"]["authorizer"]["claims"]
    # or sometimes directly in event.get("authed_user_payload") depending on how it's implemented.
    # Looking at cognito_auth_required in lambda_decorators.py:
    # it seems it might be in event.get("authed_user_payload")? Let's check lambda_decorators.py again.
    
    # After checking previous logs, it's often in event.get("authed_user_payload")
    # or we can extract the token directly again to manually get user_info.
    
    auth_payload = event.get("authed_user_payload")
    cognito_sub = auth_payload.get("username") if auth_payload else None
    
    if not cognito_sub:
        # Fallback: Extraction using Cognito identify_user (get_user) if payload not present
        # This is safer but slightly slower
        token = ""
        headers = event.get("headers", {})
        for k, v in headers.items():
            if k.lower() == "authorization":
                token = v.replace("Bearer ", "").strip()
                break
        
        if token:
            try:
                cognito_client = boto3.client("cognito-idp", region_name=os.getenv("AWS_REGION", "us-east-1"))
                user_info = cognito_client.get_user(AccessToken=token)
                cognito_sub = user_info.get("Username")
            except Exception as e:
                print(f"[me] Error manually validating token for profile: {e}")
                return ResponseUtils.unauthorized_response("Session invalid or expired")

    if not cognito_sub:
        return ResponseUtils.unauthorized_response("Authentication required")

    user_data = _get_user_profile(cognito_sub)

    if not user_data:
        return ResponseUtils.forbidden_response("User not found in system")

    # Format user data with full_name
    role_name = ""
    roles_info = user_data.get("roles")
    if isinstance(roles_info, dict):
        role_name = roles_info.get("name", "")
    elif isinstance(roles_info, list) and roles_info:
        role_name = roles_info[0].get("name", "")

    return ResponseUtils.success_response(
        data={
            "user": {
                "id":           user_data.get("id_user"),
                "username":     user_data.get("username"),
                "full_name":    f"{user_data.get('name', '')} {user_data.get('surname', '')}".strip(),
                "email":        user_data.get("email"),
                "role":         role_name,
                "role_id":      user_data.get("id_role"),
                "active":       user_data.get("active"),
                "created_at":   user_data.get("created_at")
            }
        },
        message="User profile retrieved successfully"
    )
