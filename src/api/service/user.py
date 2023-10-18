
from typing import Any, Dict
from fastapi import HTTPException
from sqlalchemy import text
from db.user import USER_ROLE, User
from db.user import User
from schemas.auth import UserSchema
from sqlalchemy.orm import joinedload, Session


def create_user(user: UserSchema, db: Session):
    db_user = db.add(User(**user.dict()))
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user(user_id: str, db: Session):
    db_user = db.query(User).options(joinedload(User.authors)
                                     ).filter(User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


def get_users(options: Dict, db: Session):
    # collect all the required parameters from the options
    sort_key, sort_dir, name, offset, rows = convert_search_params(options)

    # prepare the query
    db_users = db.query(User).options(joinedload(User.authors))
    db_users = db_users if name is None else db_users.where(
        User.name.like(text('%' + name + '%')))
    db_users = db_users.order_by(text(' {0} asc'.format(
        sort_key))) if sort_dir == 'asc' else db_users.order_by(text(' {0} desc'.format(sort_key)))
    db_users = db_users.limit(limit=rows).offset(offset=offset)

    # return the results
    return db_users.all()


def get_user_by_name(username: str,db: Session):
    db_user = db.query(User).where(User.username == username).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user;

def update_user(user_id: str, user: UserSchema, db: Session):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    for key, value in user.dict().items():
        setattr(db_user, key, value)

    db.commit()
    db.refresh(db_user)
    return db_user

def toggle_active(user_id: str, active: bool, db: Session):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    db.query(User).filter(User.id == user_id).update({User.active : active})
    db.commit()
    db.refresh(db_user)
    return db_user

def change_role(user_id: str, user_role: USER_ROLE, db: Session):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    db.query(User).filter(User.id == user_id).update({User.role : user_role})

    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user(user_id: str, db: Session):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(db_user)
    db.commit()
    return db_user


def convert_search_params(options: Any):
    page_no = 1 if options.get('page_no') is None else int(
        options.get('page_no').__str__())
    page_size = 20 if options.get(
        'page_no') is None else int(options.get('page_size').__str__())
    sort_key = "name" if options.get(
        'sort_key') is None else options.get('sort_key')
    sort_dir = "asc" if options.get(
        'sort_dir') is None else options.get('sort_dir')
    name = options.get('name')
    offset = (page_no - 1) * page_size
    rows = page_size

    return [sort_key, sort_dir, name, offset, rows]
