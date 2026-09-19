from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

import models
from database import get_db
from schemas import UserCreate, UserResponse, UserUpdate

app = FastAPI()

@app.post('/user', response_model=UserResponse)
async def create_user(payLoad: UserCreate, database: Session = Depends(get_db)):
    new_user = models.User(**payLoad.model_dump())

    database.add(new_user)
    database.commit()

    return new_user

@app.get('/users', response_model=list[UserResponse])
def get_users(database: Session = Depends(get_db), skip: int = 0, limit: int = 10):
    return database.scalars(select(models.User).offset(skip).limit(limit)).all()

@app.patch('/user/{user_id}', response_model=UserResponse)
def update_user(user_id: int, payLoad: UserUpdate, database: Session = Depends(get_db)):
    user = database.get(models.User, user_id)

    update_data = payLoad.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(user, key, value)

    database.commit()
    database.refresh(user)

    return user


@app.delete('/user/{user_id}')
def delete_user(user_id: int, database: Session = Depends(get_db)):
    user = database.get(models.User, user_id)

    database.delete(user)
    database.commit()
