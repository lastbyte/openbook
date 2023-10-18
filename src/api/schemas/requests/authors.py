from typing import List, Optional
from click import Option
from pydantic import BaseModel, Field, Required


class AuthorCreateRequest(BaseModel):
    name: str = Field(Required=True)
    age: Optional[int] = None
    description: Optional[str] = None

    class Config:
        orm_mode = True


class AuthorUpdateRequest(AuthorCreateRequest):
    id: int
