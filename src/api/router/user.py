from typing import Annotated
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from db.user import USER_ROLE, User
from schemas.auth import UserSchema
from schemas.response.api_response import APIResponse
from db.database import get_db
from service import user as userService

router = APIRouter()


@router.get('/', response_model=UserSchema, tags=["users"])
def create_user(user: UserSchema, db: Session = Depends(get_db)):
    db_user = db.add(User(**user.dict()))
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@router.get('/', response_model=UserSchema, tags=["users"])
def get_users(page_no: Annotated[int | None, Query(ge=0)] = None,
              page_size: Annotated[int | None, Query(gt=0)] = None,
              sort_key: Annotated[str | None, Query(max_length=50)] = None,
              sort_dir: Annotated[str | None, Query()] = None,
              name: Annotated[str | None, Query(max_length=50)] = None,
              db: Session = Depends(get_db)):
    options = {"page_no": page_no, "page_size": page_size,
               "sort_key": sort_key, "sort_dir": sort_dir, "name": name}
    users_retrieved = userService.get_users(options, db)
    return APIResponse(data=users_retrieved)


@router.post('/{user_id}', response_model=UserSchema, tags=["users"])
def get_user_by_id(user_id: str, db: Session = Depends(get_db)):
    users_retrieved = userService.get_user(user_id, db)
    return APIResponse(data=users_retrieved)


@router.put('/{user_id}', response_model=UserSchema, tags=["users"])
def update_user(user_id: str, user: UserSchema, db: Session = Depends(get_db)):
    users_retrieved = userService.update_user(user_id, user, db)
    return APIResponse(data=users_retrieved)


@router.patch('/update-role/{user_id}/{user_role}', response_model=UserSchema, tags=["users"])
def change_user_role(user_id: str, user_role: USER_ROLE, db: Session = Depends(get_db)):
    users_retrieved = userService.change_role(user_id, user_role, db)
    return APIResponse(data=users_retrieved)


@router.patch('/deactivate/{user_id}', response_model=UserSchema, tags=["users"])
def deactivate_user(user_id: str, db: Session = Depends(get_db)):
    users_updated = userService.toggle_active(user_id, False,db)
    return APIResponse(data=users_updated)


@router.patch('/activate/{user_id}', response_model=UserSchema, tags=["users"])
def activate_user(user_id: str, db: Session = Depends(get_db)):
    users_updated = userService.toggle_active(user_id, True,db)
    return APIResponse(data=users_updated)


@router.delete('/{user_id}', response_model=UserSchema, tags=["users"])
def delete_user(user_id: str,  db: Session = Depends(get_db)):
    user_deleted = userService.delete_user(user_id, db)
    return APIResponse(data=user_deleted)
