from typing import List
from pydantic import BaseModel

from schemas.book import BookSchema

class BookCreateResponse(BaseModel):
    success : bool
    book : BookSchema| None

    class Config : 
        orm_mode = True

class BookGetResponse(BaseModel):
    book : BookSchema| None

class BookUpdateResponse(BaseModel):
    success : bool
    book : BookSchema | None

class BookDeleteResponse(BaseModel):
    success : bool
    book : BookSchema| None

class BookSearchResponse(BaseModel):
    total_count : int
    books : List[BookSchema]

