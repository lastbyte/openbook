from typing import Annotated, List
from fastapi import APIRouter, Depends, Query
from schemas.requests.books import BookCreateRequest, BookUpdateRequest
from schemas.response.books import BookCreateResponse, BookDeleteResponse, BookGetResponse, BookSearchResponse
from schemas.response.api_response import APIResponse
from schemas.book import BookSchema
from db.database import get_db
from sqlalchemy.orm import Session
from service import book as bookService

router = APIRouter()


@router.post("",response_model=APIResponse[BookCreateResponse], tags=["books"])
async def create_book(book: BookCreateRequest, db: Session = Depends(get_db)):
    created_book = bookService.create_book(book, db)
    return APIResponse(data=created_book)


@router.get("", tags=["books"], response_model=APIResponse[BookSearchResponse])
async def get_books(page_no: Annotated[int | None, Query(ge=0)] = None,
                    page_size: Annotated[int | None, Query(gt=0)] = None,
                    sort_key: Annotated[str | None,
                                        Query(max_length=50)] = None,
                    sort_dir: Annotated[str | None, Query()] = None,
                    name: Annotated[str | None, Query(max_length=50)] = None,
                    db: Session = Depends(get_db)):
    options = {"page_no": page_no, "page_size": page_size,
               "sort_key": sort_key, "sort_dir": sort_dir, "name": name}
    book_retrieved = bookService.get_books(db, options)
    return APIResponse(data=book_retrieved)


@router.get("/{book_id}", tags=["books"], response_model=APIResponse[BookGetResponse])
async def get_book_with_id(book_id: int, db: Session = Depends(get_db)):
    book_retrieved = bookService.get_book(book_id, db)
    return APIResponse(data=book_retrieved)


@router.put("/{book_id}", tags=["books"],response_model=APIResponse[BookGetResponse])
async def update_book(book_id: int, book: BookUpdateRequest, db: Session = Depends(get_db)):
    updated_book = bookService.update_book(book_id, book, db)
    return APIResponse(data=updated_book)


@router.delete("/{book_id}", tags=["books"],response_model=APIResponse[BookDeleteResponse])
async def delete_book_with_id(book_id: int, db: Session = Depends(get_db)):
    deleted_book = bookService.delete_book(book_id, db)
    return APIResponse(data=deleted_book)
