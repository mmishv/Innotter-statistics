from dynamodb.repository import PageStatisticsRepository
from schemas import PageStatistics


class StatisticsService:
    def __init__(self):
        self.__repository = PageStatisticsRepository()

    def get_page_statistics(self, page_uuid: str):
        return self.__repository.get(page_uuid)

    def create_page_record(self, page_uuid: str, owner_uuid: str):
        page = PageStatistics(page_uuid=page_uuid, owner_uuid=owner_uuid)
        return self.__repository.create(page)

    def update_page_record(self, page_uuid, field, delta):
        model_fields = PageStatistics.__annotations__.keys()
        if field not in model_fields:
            raise ValueError("Invalid field name")
        return self.__repository.update(page_uuid, field, delta)

    def delete_page(self, page_uuid: str):
        return self.__repository.delete(page_uuid)
