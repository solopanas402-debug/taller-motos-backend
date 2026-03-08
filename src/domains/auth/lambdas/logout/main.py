import boto3
from botocore.exceptions import ClientError
from decorators.lambda_decorators import cors_enabled, cognito_auth_required
from utils.response_utils import ResponseUtils
import os

cognito_client = boto3.client("cognito-idp", region_name=os.getenv("AWS_REGION", "us-east-1"))


@cors_enabled
@cognito_auth_required
def lambda_handler(event, context):
    print(f"[logout] Logout attempt")

    headers = event.get("headers", {})
    auth_header = ""
    for key, value in headers.items():
        if key.lower() == "authorization":
            auth_header = value
            break

    access_token = auth_header.replace("Bearer ", "").strip() if auth_header else ""

    if not access_token:
        return ResponseUtils.unauthorized_response("Authentication token not found")

    try:
        cognito_client.global_sign_out(AccessToken=access_token)
        print(f"[logout] GlobalSignOut successful")
    except ClientError as e:
        error_code = e.response.get("Error", {}).get("Code", "")
        print(f"[logout] Cognito error: {error_code}")

        if error_code == "NotAuthorizedException":
            # Token already expired or invalidated — consider it successful logout
            return ResponseUtils.success_response(data=None, message="Logged out successfully")

        print(f"[logout] Unexpected Cognito error: {str(e)}")
        return ResponseUtils.internal_server_error_response("Internal server error")

    return ResponseUtils.success_response(data=None, message="Logged out successfully")
