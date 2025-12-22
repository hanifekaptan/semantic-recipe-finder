"""Input model for search requests.

Defines the shape of the JSON body accepted by the `/search` endpoint.
"""

from pydantic import BaseModel


class SearchQuery(BaseModel):
    """Search payload containing the user query string."""
    query: str
