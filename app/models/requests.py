from pydantic import BaseModel
from pydantic import Field
from pydantic import HttpUrl
from pydantic import ConfigDict


class CatalogSourceRequest(BaseModel):
    url: HttpUrl


class QuoteImport(BaseModel):
    id: str
    author: str
    text: str

    model_config = ConfigDict(
        extra="allow"
    )


class ImportRequest(BaseModel):
    quotes: list[QuoteImport]


class QuoteUpdateRequest(BaseModel):
    author: str = Field(
        min_length=1,
        max_length=200
    )

    text: str = Field(
        min_length=1,
        max_length=16384
    )