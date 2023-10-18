from typing import List
from pydantic import BaseModel

from api.schemas.auth import UserSchema

class UserCreateResponse(BaseModel):
    success : bool
    user : UserSchema| None

class UserGetResponse(BaseModel):
    user : UserSchema| None

class UserUpdateResponse(BaseModel):
    success : bool
    user : UserSchema | None

class UserDeleteResponse(BaseModel):
    success : bool
    user : UserSchema| None

class UserSearchResponse(BaseModel):
    total_count : int
    users : List[UserSchema]

