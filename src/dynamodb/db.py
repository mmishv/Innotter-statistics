import os

import boto3
from boto3.resources.base import ServiceResource
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())


def initialize_db() -> ServiceResource:
    ddb = boto3.resource(
        "dynamodb",
        endpoint_url=os.environ["ENDPOINT_URL"],
        region_name=os.environ["AWS_DEFAULT_REGION"],
        aws_access_key_id=os.environ["AWS_ACCESS_KEY_ID"],
        aws_secret_access_key=os.environ["AWS_SECRET_ACCESS_KEY"],
    )

    return ddb
