from typing import List, Optional
from pydantic import BaseModel

class BookSchema(BaseModel):
    id: int
    name: str   
    page_numbers: int
    year_published : Optional[int]
    description : Optional[str]
    url : Optional[str]
    authors : List

    class Config : 
        orm_mode = True