"""A module for storing the member model."""

from uuid import UUID

from pydantic import BaseModel


class Member(BaseModel):
    """A class for storing member data."""

    id: UUID
    url: str
