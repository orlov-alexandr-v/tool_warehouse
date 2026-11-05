# routers/users.py
from fastapi import Depends, HTTPException, APIRouter, status
from typing import List
from sqlalchemy.orm import Session

import schemas
import database
import crud

router = APIRouter()

@router.post("/", response_model=schemas.User)
def create_new_user(user: schemas.UserCreat, db: Session = Depends(database.get_db)):
    return crud.create_user(db=db, user=user)

@router.get("/", response_model=List[schemas.ReadUser])
def read_users(db: Session = Depends(database.get_db)):
    users = crud.get_users(db)
    return users # Возвращаем пустой список [], если пользователей нет

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, db: Session = Depends(database.get_db)):
    success = crud.delete_user(db, user_id)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return None
