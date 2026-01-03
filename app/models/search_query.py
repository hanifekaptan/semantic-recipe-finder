"""Model for incoming search requests."""

from pydantic import BaseModel
from typing import Optional


class SearchQuery(BaseModel):
    query: str
