from typing import Any
from fastapi import APIRouter, HTTPException
from sqlalchemy import text
from schemas.requests.authors import AuthorCreateRequest, AuthorUpdateRequest
from schemas.response.author import AuthorSearchResponse
from db.author import Author
from sqlalchemy.orm import Session, joinedload
from schemas.author import AuthorSchema

router = APIRouter()


def create_author(author: AuthorCreateRequest, db: Session):
    db_author = Author(name=author.name, age=author.age, description=author.description)
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author


async def get_author_with_id(author_id: int, db: Session):
    db_author = db.query(Author).filter(Author.id == author_id).first()
    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return db_author


def get_authors(options: Any, db: Session):
    # collect all the required parameters from the options
    sort_key,sort_dir,name,offset,rows = convert_search_params(options)

    # prepare the query
    db_authors = db.query(Author).options(joinedload(Author.books))
    db_authors = db_authors if name is None else db_authors.where(
        Author.name.ilike('%'+text(name).text+'%'))
    db_authors = db_authors.order_by(Author.name)
    db_authors_count = db_authors.count()
    if offset is not None and rows is not None : 
        db_authors = db_authors.limit(offset+rows).all()
    else : 
        db_authors = db_authors.all();
    # return the results
    return AuthorSearchResponse(total_count=db_authors_count, authors=[AuthorSchema.from_orm(author) for author in db_authors])


def update_author(author_id: int, author: AuthorUpdateRequest, db: Session):
    db_author = db.query(Author).filter(Author.id == author_id).first()
    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")

    for key, value in author.dict().items():
        setattr(db_author, key, value)

    db.commit()
    db.refresh(db_author)
    return db_author


def delete_author(author_id: int, db: Session):
    db_author = db.query(Author).filter(Author.id == author_id).first()
    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")

    db.delete(db_author)
    db.commit()
    return db_author

def convert_search_params(options: Any):
    page_no = 1 if options.get('page_no') is None else int(
        options.get('page_no').__str__())
    page_size = None if options.get(
        'page_no') is None else int(options.get('page_size').__str__())
    sort_key = "name" if options.get(
        'sort_key') is None else options.get('sort_key')
    sort_dir = "asc" if options.get(
        'sort_dir') is None else options.get('sort_dir')
    name = options.get('name')
    offset = None if page_size is None else (page_no - 1) * page_size
    rows = page_size

    return [sort_key,sort_dir,name,offset,rows]
