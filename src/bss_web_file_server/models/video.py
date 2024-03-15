from uuid import UUID
from pydantic import BaseModel


class Video(BaseModel):
    id: UUID
    urls: list[str]
