

from pydantic import BaseModel
from typing import Optional

#basemodel type validation, parsing, and serialization for my API data

class validationgist(BaseModel):
        id: str
        description: Optional[str] = None
        url: str


