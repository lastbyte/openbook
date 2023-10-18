from typing import List, Optional
from pydantic import BaseModel, Field

class UserSchema(BaseModel):
    id: int = Field(None, alias="id", exclude=True)
    username : str
    email: str
    role: int
    active : bool

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class UserInDB(UserSchema):
    password : str

class ValidateTokenRequest(BaseModel) :
    token : str