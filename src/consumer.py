import json
import os

from dotenv import find_dotenv, load_dotenv
from pika import BlockingConnection, URLParameters

from service import StatisticsService

load_dotenv(find_dotenv())

statistics_service = StatisticsService()

queue = "statistics_queue"
connection = BlockingConnection(URLParameters(os.environ.get("RABBITMQ_URL")))

channel = connection.channel()
channel.queue_declare(queue=queue)


def callback(channel, method, properties, body) -> None:
    data = json.loads(body)
    event_type = data.get("event")
    if event_type == "page_create":
        page_uuid = data.get("page_uuid")
        owner_uuid = data.get("owner_uuid")
        statistics_service.create_page_record(page_uuid, owner_uuid)

    elif event_type == "page_delete":
        page_uuid = data.get("page_uuid")
        statistics_service.delete_page(page_uuid)

    elif event_type == "page_update":
        page_uuid = data.get("page_uuid")
        field = data.get("field")
        delta = int(data.get("delta"))
        statistics_service.update_page_record(page_uuid, field, delta)


channel.basic_consume(queue=queue, on_message_callback=callback, auto_ack=True)
channel.start_consuming()
