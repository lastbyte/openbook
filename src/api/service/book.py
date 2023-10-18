
from multiprocessing import dummy
from typing import Any, Dict
from fastapi import HTTPException
from pydantic import conset
from sqlalchemy import text
from db.author import Author
from schemas.requests.books import BookCreateRequest, BookUpdateRequest
from schemas.response.books import BookCreateResponse, BookDeleteResponse, BookGetResponse, BookSearchResponse, BookUpdateResponse
from db.book import Book
from schemas.book import BookSchema
from sqlalchemy.orm import joinedload, Session


def create_book(book: BookCreateRequest, db: Session):

    db_book = Book(name=book.name, description=book.description, page_numbers=book.page_numbers);
    authors = db.query(Author).where(Author.id.in_(book.authors)).all();
    if  authors is None or len(authors) != len(book.authors) :
        raise HTTPException(status_code=422 , detail="Unprocessable entity")
    db_book.authors = authors
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return BookCreateResponse(success=True, book=db_book)


def get_book(book_id: int, db: Session):
    db_book = db.query(Book).options(joinedload(Book.authors)
                                     ).filter(Book.id == book_id).first()
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return BookGetResponse(book=db_book)


def get_books(db: Session, options: Dict):
    # collect all the required parameters from the options
    sort_key, sort_dir, name, offset, rows = convert_search_params(options)

    # prepare the query
    db_books = db.query(Book).options(joinedload(Book.authors))
    db_books = db_books if name is None else db_books.where(
        Book.name.ilike("%"+text(name).text+"%"))
    db_books = db_books.order_by(Book.name)
    db_books_count = db_books.count()
    if offset is not None and rows is not None :
        db_books = db_books.limit(offset+rows).all()
    else :
        db_books = db_books.all() 

    # return the results
    return BookSearchResponse(total_count=db_books_count, books=[BookSchema.from_orm(book) for book in db_books])


def update_book(book_id: int, book: BookUpdateRequest, db: Session):
    print({"bookId": book_id, "book": book})
    db_book = db.query(Book).options(joinedload(Book.authors)
                                     ).filter(Book.id == book_id).first()
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")

    dummy_book = Book(name=book.name, description=book.description, page_numbers=book.page_numbers, year_published=book.year_published, url=book.url)

    db_book.name=dummy_book.name
    db_book.description=dummy_book.description
    db_book.page_numbers=dummy_book.page_numbers
    db_book.year_published=dummy_book.year_published
    db_book.url=dummy_book.url
    
    authors = db.query(Author).where(Author.id.in_(book.authors)).all();
    if  authors is None or len(authors) != len(book.authors) :
        raise HTTPException(status_code=422 , detail="Unprocessable entity")
    
    db_book.authors =authors;
    db.commit()
    db.refresh(db_book)
    return BookUpdateResponse(success=True, book=BookSchema.from_orm(db_book))


def delete_book(book_id: int, db: Session):
    db_book = db.query(Book).options(joinedload(Book.authors)
                                     ).filter(Book.id == book_id).first()
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")

    db.delete(db_book)
    db.commit()
    return BookDeleteResponse(success=True, book=BookSchema.from_orm(db_book))


def convert_search_params(options: Any):
    page_no = 1 if options.get('page_no') is None else int(
        options.get('page_no').__str__())
    page_size = -1 if options.get(
        'page_no') is None else int(options.get('page_size').__str__())
    sort_key = "name" if options.get(
        'sort_key') is None else options.get('sort_key')
    sort_dir = "asc" if options.get(
        'sort_dir') is None else options.get('sort_dir')
    name = options.get('name')
    offset = (page_no - 1) * page_size
    rows = page_size

    return [sort_key, sort_dir, name, offset, rows]
