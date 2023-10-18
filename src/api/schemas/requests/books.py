from typing import List, Optional
from pydantic import BaseModel, Field

class BookCreateRequest(BaseModel):
    name : str = Field(Required=True)
    page_numbers : int = Field(Required=True)
    description : str = Field(Required=False)
    year_published : Optional[int] = None 
    url :  Optional[str] = ''
    authors : List[str] = Field(Required=True)

    class Config : 
        orm_mode = True

class BookUpdateRequest(BookCreateRequest):
    id : Optional[int]

