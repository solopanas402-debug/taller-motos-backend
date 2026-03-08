import json
import boto3
import os
import re
from botocore.exceptions import ClientError
from decorators.lambda_decorators import cors_enabled
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
def lambda_handler(event, context):
    print("[reset_password] Confirming password reset")

    try:
        body = json.loads(event.get("body") or "{}")
    except json.JSONDecodeError:
        return ResponseUtils.bad_request_response("The request body is not a valid JSON")

    email = (body.get("email") or "").strip().lower()
    code = (body.get("code") or "").strip()
    new_password = (body.get("new_password") or "").strip()

    if not email or not code or not new_password:
        return ResponseUtils.bad_request_response("Missing required fields: email, code, new_password")

    valid_pwd, pwd_msg = _validate_password(new_password)
    if not valid_pwd:
        return ResponseUtils.bad_request_response(pwd_msg)

    user_app_client_id = os.getenv("COGNITO_USER_APP_CLIENT_ID")
    
    try:
        # Confirm password reset with Cognito using the verification code
        cognito_client.confirm_forgot_password(
            ClientId=user_app_client_id,
            Username=email,
            ConfirmationCode=code,
            Password=new_password
        )
        
        return ResponseUtils.success_response(
            data=None,
            message="Your password has been reset successfully"
        )

    except ClientError as e:
        error_code = e.response.get("Error", {}).get("Code", "")
        print(f"[reset_password] Cognito error: {error_code}")
        
        if error_code == "CodeMismatchException":
            return ResponseUtils.bad_request_response("Invalid verification code")
        if error_code == "ExpiredCodeException":
            return ResponseUtils.bad_request_response("Verification code has expired. Request a new one.")
        if error_code == "InvalidPasswordException":
            return ResponseUtils.bad_request_response("Password does not meet security requirements")
        if error_code == "UserNotFoundException":
            # Although user might not exist, we avoid specific error to prevent account discovery
            return ResponseUtils.bad_request_response("Error confirming password reset")
            
        print(f"[reset_password] Unexpected error: {str(e)}")
        return ResponseUtils.internal_server_error_response("Internal server error")
    except Exception as e:
        print(f"[reset_password] Technical error: {str(e)}")
        return ResponseUtils.internal_server_error_response("Internal server error")
