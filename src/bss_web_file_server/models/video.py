"""A module for storing the video model."""

from typing import Annotated
from uuid import UUID

from annotated_types import Len
from pydantic import BaseModel


class Video(BaseModel):
    """A class for storing video data."""

    id: UUID
    urls: Annotated[list[str], Len(min_length=1)]
