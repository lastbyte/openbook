import json
from typing import Any, Dict
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from response.baseRespone import Response
from response.baseRespone import Response
from fastapi.encoders import jsonable_encoder


router = APIRouter()

@router.get('',tags=["health"])
def health_check() :
    return  {"message" : "Library is running"};