import json
import os
import time
import uuid

import boto3
import requests
from dotenv import load_dotenv


def main():
    # queue_jwt = "https://sqs.eu-central-1.amazonaws.com/302645174876/JwtTokens"
    # queue_decoded = "https://sqs.eu-central-1.amazonaws.com/302645174876/DecodedTokens"
    correlation_id = str(uuid.uuid4())
    type = "jwt"
    # queue_url = f"https://sqs.eu-central-1.amazonaws.com/302645174876/{correlation_id}"

    # Create SQS client
    sqs = boto3.client(
        "sqs",
        aws_access_key_id=os.getenv("SQS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("SQS_SECRET_ACCESS_KEY"),
    )

    response = sqs.create_queue(
        QueueName=f"{correlation_id}",
        Attributes={
            "ReceiveMessageWaitTimeSeconds": "20",
        },
    )
    print(response)
    queue_url = response["QueueUrl"]
    print(queue_url)

    # List SQS queues
    # aws_access_key_id = os.getenv("SQS_ACCESS_KEY_ID")
    # aws_secret_access_key = os.getenv("SQS_SECRET_ACCESS_KEY")
    # response = sqs.list_queues()

    # Create a SQS queue
    # Get URL for SQS queue //https://eu-central-1.queue.amazonaws.com/302645174876/MyQueue

    jwt_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2NTMzMzE3NjYsInN1YiI6IjM4MjdhYTVmLWFkNzctNDMwMy05ZTYzLWJiZmE4N2E1ZTNiNyJ9.YQ2sLSMJVa-onmYWkAm40z9-Si2Au_XgLZrXOm13DLE"
    payload = {"type": f"{type}", "jwt_token": f"{jwt_token}"}
    response = sqs.send_message(QueueUrl=queue_url, MessageBody=json.dumps(payload))
    # use only in development
    time.sleep(1)
    requests.post(f"http://localhost:8080/api/users/decode-token?queue_id={correlation_id}'")

    print(f"CorrID:{correlation_id}/ waiting for messages...")
    response = sqs.receive_message(
        QueueUrl=queue_url,
        MaxNumberOfMessages=2,
        WaitTimeSeconds=20,
        VisibilityTimeout=20,
    )
    messages = response["Messages"]
    user = {}
    for message in messages:
        print("searching for message...")
        receipt_handle = message["ReceiptHandle"]
        body = json.loads(message["Body"])
        msg_type = body["type"]
        if msg_type == "decoded":
            user = body["user"]
            sqs.delete_message(QueueUrl=queue_url, ReceiptHandle=receipt_handle)
            print(f"MSGtype {type} Message found")
            # print (receipt_handle)
            break
    # print(user)

    # print(response)


if __name__ == "__main__":
    load_dotenv()
    main()
