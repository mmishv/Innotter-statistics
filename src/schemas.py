from pydantic import BaseModel


class PageStatistics(BaseModel):
    owner_uuid: str
    page_uuid: str
    posts: int = 0
    likes: int = 0
    followers: int = 0
    follow_requests: int = 0


class UserInfo(BaseModel):
    id: str
    is_blocked: bool
