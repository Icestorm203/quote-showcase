from typing import Any

from pydantic import BaseModel


class Quote(BaseModel):
    id: str
    author: str
    text: str

    class Config:
        extra = "allow"
