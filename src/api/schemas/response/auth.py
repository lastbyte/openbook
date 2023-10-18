from pydantic import BaseModel

class LoginResponse(BaseModel):
    token : str

class ValidateTokenResponse(BaseModel) :
    valid : bool
    message : str

class LogoutResponse(BaseModel) :
    message : str

class CheckLogOutStatusResponse(BaseModel) :
    logged_out : bool
    message : 'str'