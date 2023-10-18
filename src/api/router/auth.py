from ast import Dict
from typing import Annotated, Optional
from cachetools import LRUCache
from fastapi import APIRouter, Depends, HTTPException, status
import jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm
from schemas.response.auth import LoginResponse
from db.database import SessionLocal, get_db
from schemas.response.api_response import APIResponse
from schemas.auth import UserSchema, ValidateTokenRequest
from service import auth as authService
from sqlalchemy.orm import Session

from db.user import User

# Define secret key and algorithm for JWT (JSON Web Tokens)
SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


# Initialize password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Define the OAuth2PasswordBearer for token extraction
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

# Initialize a token blacklist cache (LRU Cache)
token_blacklist_cache = LRUCache(
    maxsize=1000, getsizeof=lambda x: len(x))  # type: ignore

router = APIRouter()


def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


@router.post('/token/validate/', response_model=bool, tags=["auth"])
def validate_token(tokenRequest: ValidateTokenRequest,db: Session = Depends(get_db)):
    if tokenRequest.token is not None : 
        token = tokenRequest.token.split("Bearer ")[-1].strip()
        return authService.get_current_user(token, db) is not None
    return False


@router.post('/login', tags=["auth"], response_model=LoginResponse, )
async def login(data: OAuth2PasswordRequestForm=Depends(),db: Session = Depends(get_db)):
    print(data);
    return await authService.login_for_access_token(data, db)

@router.post('/current-user', tags=["auth"] )
async def get_current_active_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    db : Session = Depends(get_db) 
):
    return {"user" : authService.get_current_user(token,db)};


@router.post("/logout")
def logout(token: Optional[str] = Depends(oauth2_scheme)):
    if token : 
        return authService.logout_user(token)
    return {"success" : False}


@router.get("/check-logout-status")
def check_logout_status(token: Optional[str] = Depends(oauth2_scheme)):
    return authService.check_logout_status(token)
