from botocore.exceptions import ClientError

from dynamodb.db import initialize_db
from schemas import PageStatistics


class PageStatisticsRepository:
    TABLE_NAME = "PageStatistics"

    def __init__(self):
        db = initialize_db()
        self.table = db.Table(self.TABLE_NAME)

    def get_all(self) -> list[PageStatistics]:
        response = self.table.scan()
        return response.get("Items", [])

    def get(self, page_uuid: str) -> PageStatistics:
        try:
            response = self.table.get_item(Key={"page_uuid": page_uuid})["Item"]
            return PageStatistics(**response)
        except ClientError as e:
            raise ValueError(e.response["Error"]["Message"])

    def create(self, page: PageStatistics):
        self.table.put_item(Item=page.model_dump())

    def update(self, page_uuid: str, field: str, delta: int):
        self.table.update_item(
            Key={"page_uuid": page_uuid},
            UpdateExpression=f"SET {field} = {field} + :delta",
            ExpressionAttributeValues={":delta": delta},
        )

    def delete(self, page_uuid: str):
        self.table.delete_item(Key={"page_uuid": page_uuid})
