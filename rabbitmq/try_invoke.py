import json
import os

import boto3
from dotenv import load_dotenv

# str(check_current_active_superuser(get_current_user(token)))


def main():
    client = boto3.client(
        "lambda",
        aws_access_key_id=os.getenv("LAMBDA_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("LAMBDA_SECRET_ACCESS_KEY"),
    )

    payload = {
        "resource": "/api/maps/",
        "path": "/api/maps/",
        "httpMethod": "GET",
        "requestContext": {
            "resourcePath": "/prod/api/maps/",
            "httpMethod": "GET",
            "path": "/Prod/",
            "protocol": "HTTP/1.1",
            "stage": "Prod",
        },
        "body": "null",
        "isBase64Encoded": "false",
    }
    response = client.invoke(FunctionName="vidpit-authentication", InvocationType="Event", Payload=json.dumps(payload))

    print(response)
    print(os.getenv("LAMBDA_ACCESS_KEY_ID"))
    print(os.getenv("LAMBDA_SECRET_ACCESS_KEY"))


if __name__ == "__main__":
    load_dotenv()
    main()
