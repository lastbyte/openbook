from typing import Any, Generator
from fastapi import Depends, FastAPI, HTTPException, Request, status
from fastapi.responses import JSONResponse
from db.book import Book
from schemas.response.api_response import APIResponse
from router import book, user, auth, author, healthcheck
from db.database import get_db, initialize_sql
from service import auth as authService
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware import Middleware
from sqlalchemy.orm import Session


# create a FastAPI app
app = FastAPI()

# define the routes
app.include_router(book.router, prefix='/api/books')
app.include_router(author.router, prefix='/api/authors')
app.include_router(auth.router, prefix='/api/auth')
app.include_router(user.router, prefix='/api/users')
app.include_router(healthcheck.router, prefix='/api/health-check')


excluded = ["/api/auth/login", "/api/auth/token/validate",
            "/api/auth/logout", "/api/auth/current-user"]

dbSession: Session = get_db().__next__()

# type: ignore
@app.middleware("http")
async def authorization(request: Request, call_next):
    if request.url.path not in excluded and not request.url.path.startswith('/api'):
        token = request.headers.get("Authorization")
        if token is None or not token.startswith("Bearer "):
            return JSONResponse(status_code=401, content={"message": "un-authorized user"})

        token = token.split("Bearer ")[-1].strip()
        is_valid = authService.validate_token(token, dbSession)
        if is_valid == False:
            return JSONResponse(status_code=401, content={"message": "un-authorized user"})
        response = await call_next(request)
        return response

    response = await call_next(request)
    return response

app.add_middleware(CORSMiddleware, allow_origins=['*'], allow_methods=['*'],
                   allow_headers=['*'],
                   allow_credentials=False)

initialize_sql()
# uncomment the line to generate dummy data
# import db.dummy_data;
