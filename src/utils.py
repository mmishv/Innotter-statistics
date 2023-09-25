import os

import requests
from fastapi import Header, HTTPException

from schemas import UserInfo
from service import StatisticsService


def is_owner(token: str = Header()):
    validate_jwt_url = os.getenv("VALIDATE_JWT_URL")
    headers = {"token": token}
    user_data = perform_request(validate_jwt_url, "GET", headers)
    user_id = user_data.id

    def inner(page_uuid: str):
        page_owner_id = StatisticsService().get_page_statistics(page_uuid).owner_uuid
        if user_id != page_owner_id:
            raise HTTPException(
                status_code=403, detail="You aren't the owner of this page"
            )

    return inner


def perform_request(url, method, headers=None) -> UserInfo:
    try:
        response = requests.request(method, url, headers=headers)
        if response.status_code == 200:
            return UserInfo(**response.json())
        elif response.status_code == 403:
            raise HTTPException(
                status_code=403,
                detail="You must be an administrator to perform this action",
            )
        else:
            raise HTTPException(
                status_code=401,
                detail="JWT processing decode error: invalid or expired token",
            )
    except requests.exceptions.RequestException:
        raise HTTPException(status_code=503, detail="Service is not available")
