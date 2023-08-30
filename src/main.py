from fastapi import Depends, FastAPI

from schemas import PageStatistics
from service import StatisticsService
from utils import is_owner

app = FastAPI()

statistics_service = StatisticsService()


@app.get("/statistics/{page_uuid}/", response_model=PageStatistics)
def statistics(page_uuid: str, authorized=Depends(is_owner)):
    return statistics_service.get_page_statistics(page_uuid)
