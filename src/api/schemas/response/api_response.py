from typing import Any, Generic, List
from pydantic import BaseModel
from typing import List, TypeVar

T = TypeVar("T")

# Pydantic schema for Author
class APIResponse(BaseModel, Generic[T]):
    data : T