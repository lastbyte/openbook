from typing import List
from pydantic import BaseModel

from schemas.author import AuthorSchema

class AuthorCreateResponse(BaseModel):
    success : bool
    author : AuthorSchema| None

class AuthorGetResponse(BaseModel):
    author : AuthorSchema| None

class AuthorUpdateResponse(BaseModel):
    success : bool
    author : AuthorSchema | None

class AuthorDeleteResponse(BaseModel):
    success : bool
    author : AuthorSchema| None

class AuthorSearchResponse(BaseModel):
    total_count : int
    authors : List[AuthorSchema]

