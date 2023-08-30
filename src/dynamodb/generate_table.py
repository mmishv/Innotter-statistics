from botocore.exceptions import ClientError

from dynamodb.db import initialize_db


def generate_table(ddb):
    ddb.create_table(
        TableName="PageStatistics",
        AttributeDefinitions=[{"AttributeName": "page_uuid", "AttributeType": "S"}],
        KeySchema=[{"AttributeName": "page_uuid", "KeyType": "HASH"}],
        ProvisionedThroughput={"ReadCapacityUnits": 5, "WriteCapacityUnits": 5},
    )


db = initialize_db()

try:
    generate_table(db)
except ClientError as e:
    if e.response["Error"]["Code"] == "ResourceInUseException":
        print("Table already exists!")
    else:
        print("Error creating table:", e)
