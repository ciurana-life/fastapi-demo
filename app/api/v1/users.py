from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.auth.domain import token_required
from app.dependencies import get_db
from app.schemas import ErrorMessage
from app.users import crud, schemas

router = APIRouter()


@router.post("/", response_model=schemas.User, responses={400: {"model": ErrorMessage}})
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    if crud.get_user_by_email(db, email=user.email):
        raise HTTPException(status_code=400, detail="Email already registered")
    if crud.get_user_by_username(db, username=user.username):
        raise HTTPException(status_code=400, detail="Username already registered")
    return crud.create_user(db=db, user=user)


@router.get("/", response_model=schemas.User)
def read_user(
    username: Annotated[str, Depends(token_required)], db: Session = Depends(get_db)
):
    db_user = crud.get_user_by_username(db, username=username)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.put("/", response_model=schemas.User)
def update_user(
    user: schemas.UserUpdate,
    username: Annotated[str, Depends(token_required)],
    db: Session = Depends(get_db),
):
    db_user = crud.get_user_by_username(db, username=username)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    for var, value in vars(user).items():
        setattr(db_user, var, value) if value else None

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@router.delete("/")
def delete_user(
    username: Annotated[str, Depends(token_required)], db: Session = Depends(get_db)
):
    db_user = crud.get_user_by_username(db, username=username)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(db_user)
    db.commit()
    return {"ok": True}
