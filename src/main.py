from fastapi import Depends, FastAPI
from starlette.middleware.cors import CORSMiddleware

from schemas import PageStatistics
from service import StatisticsService
from utils import is_owner

app = FastAPI()

statistics_service = StatisticsService()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/statistics/{page_uuid}/", response_model=PageStatistics)
def statistics(page_uuid: str, authorized=Depends(is_owner)):
    return statistics_service.get_page_statistics(page_uuid)
