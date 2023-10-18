from typing import List, Optional
from pydantic import BaseModel, Field

# Pydantic schema for Author
class AuthorSchema(BaseModel):
    id: int
    name: str
    age : Optional[int]
    description : Optional[str]
    books : List

    class Config :
        orm_mode = True

