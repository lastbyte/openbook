from typing import Annotated
from fastapi import APIRouter, Depends, Query
from schemas.requests.authors import AuthorCreateRequest, AuthorUpdateRequest
from schemas.response.author import AuthorCreateResponse
from schemas.response.api_response import APIResponse
from db.database import get_db
from sqlalchemy.orm import Session
from schemas.author import AuthorSchema

from service import author as authorService

router = APIRouter()


@router.post("", response_model=APIResponse[AuthorCreateResponse], tags=["authors"])
def create_author(author: AuthorCreateRequest, db: Session = Depends(get_db)):
    created_author = authorService.create_author(author, db)
    return APIResponse(data=created_author)


@router.get("", response_model=APIResponse, tags=["authors"])
def get_authors(page_no: Annotated[int | None, Query(ge=0)] = None,
                page_size: Annotated[int | None, Query(gt=0)] = None,
                sort_key: Annotated[str | None, Query(max_length=50)] = None,
                sort_dir: Annotated[str | None, Query()] = None,
                name: Annotated[str | None, Query(max_length=50)] = None,
                db: Session = Depends(get_db)):
    options = {"page_no": page_no, "page_size": page_size,
               "sort_key": sort_key, "sort_dir": sort_dir, "name": name}
    retrieved_autoors = authorService.get_authors(options, db)
    return APIResponse(data=retrieved_autoors)


@router.get("/{author_id}", tags=["authors"])
async def get_author_with_id(author_id: int, db: Session = Depends(get_db)):
    retrieved_autoors = authorService.get_author_with_id(author_id, db)
    return APIResponse(data=retrieved_autoors)


@router.put("/{author_id}", response_model=APIResponse, tags=["authors"])
def update_author(author_id: int, author: AuthorUpdateRequest, db: Session = Depends(get_db)):
    updated_author = authorService.update_author(author_id, author, db)
    return APIResponse(data=updated_author)


@router.delete("/{author_id}", response_model=APIResponse, tags=["authors"])
def delete_author(author_id: int, db: Session = Depends(get_db)):
    deleted_author = authorService.delete_author(author_id, db)
    return APIResponse(data=deleted_author)
