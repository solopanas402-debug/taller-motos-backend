import json
import boto3
import os
import re
from botocore.exceptions import ClientError
from decorators.lambda_decorators import cors_enabled, cognito_auth_required
from utils.response_utils import ResponseUtils

cognito_client = boto3.client("cognito-idp", region_name=os.getenv("AWS_REGION", "us-east-1"))

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

@cors_enabled
@cognito_auth_required
def lambda_handler(event, context):
    print("[change_password] Attempting to change password")

    # Get token from headers (cognito_auth_required should have validated basic format)
    headers = event.get("headers", {})
    auth_header = ""
    for key, value in headers.items():
        if key.lower() == "authorization":
            auth_header = value
            break

    access_token = auth_header.replace("Bearer ", "").strip() if auth_header else ""

    if not access_token:
        # Should not happen with cognito_auth_required, but for safety:
        return ResponseUtils.unauthorized_response("Authentication token not found")

    try:
        body = json.loads(event.get("body") or "{}")
    except json.JSONDecodeError:
        return ResponseUtils.bad_request_response("The request body is not a valid JSON")

    previous_password = (body.get("old_password") or "").strip()
    proposed_password = (body.get("new_password") or "").strip()

    if not previous_password or not proposed_password:
        return ResponseUtils.bad_request_response("Missing required fields: old_password, new_password")

    valid_pwd, pwd_msg = _validate_password(proposed_password)
    if not valid_pwd:
        return ResponseUtils.bad_request_response(pwd_msg)

    try:
        # Change password in Cognito with Access Token
        cognito_client.change_password(
            PreviousPassword=previous_password,
            ProposedPassword=proposed_password,
            AccessToken=access_token
        )
        
        return ResponseUtils.success_response(
            data=None,
            message="Password changed successfully"
        )

    except ClientError as e:
        error_code = e.response.get("Error", {}).get("Code", "")
        print(f"[change_password] Cognito error: {error_code}")
        
        if error_code == "NotAuthorizedException":
            return ResponseUtils.unauthorized_response("Incorrect previous password")
        if error_code == "InvalidPasswordException":
            return ResponseUtils.bad_request_response("New password does not meet security requirements")
        if error_code in ("LimitExceededException", "TooManyRequestsException"):
            return ResponseUtils.too_many_requests_response("Too many attempts. Please try again later.")
            
        print(f"[change_password] Technical error: {str(e)}")
        return ResponseUtils.internal_server_error_response("Internal server error")
    except Exception as e:
        print(f"[change_password] Unexpected technical error: {str(e)}")
        return ResponseUtils.internal_server_error_response("Internal server error")
