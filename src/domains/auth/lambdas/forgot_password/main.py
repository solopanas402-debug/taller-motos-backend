import json
import boto3
import os
from botocore.exceptions import ClientError
from decorators.lambda_decorators import cors_enabled
from utils.response_utils import ResponseUtils

cognito_client = boto3.client("cognito-idp", region_name=os.getenv("AWS_REGION", "us-east-1"))

@cors_enabled
def lambda_handler(event, context):
    print("[forgot_password] Password reset request")

    try:
        body = json.loads(event.get("body") or "{}")
    except json.JSONDecodeError:
        return ResponseUtils.bad_request_response("The request body is not a valid JSON")

    email = (body.get("email") or "").strip().lower()

    if not email:
        return ResponseUtils.bad_request_response("The 'email' field is required")

    user_app_client_id = os.getenv("COGNITO_USER_APP_CLIENT_ID")
    
    try:
        # Request password reset code from Cognito
        cognito_client.forgot_password(
            ClientId=user_app_client_id,
            Username=email
        )
        
        return ResponseUtils.success_response(
            data=None,
            message="Verification code sent to your email"
        )

    except ClientError as e:
        error_code = e.response.get("Error", {}).get("Code", "")
        print(f"[forgot_password] Cognito error: {error_code}")
        
        # We return success even if user not found to avoid account harvesting
        if error_code == "UserNotFoundException":
            return ResponseUtils.success_response(
                data=None,
                message="Verification code sent to your email"
            )
            
        if error_code == "InvalidParameterException":
            return ResponseUtils.bad_request_response("Invalid input parameters")
            
        print(f"[forgot_password] Technical error: {str(e)}")
        return ResponseUtils.internal_server_error_response("Internal server error")
    except Exception as e:
        print(f"[forgot_password] Unexpected error: {str(e)}")
        return ResponseUtils.internal_server_error_response("Internal server error")
