from fastapi import APIRouter,Depends,status,Response,HTTPException
from sqlalchemy.orm import Session
from ..import models
from ..database import get_db
from ..schemas.user import User
from passlib.context import CryptContext
from ..schemas.book import Book,showBook

router=APIRouter(
    tags=['Library']
)



# Get the books taken by user
@router.post('/users/{id}/books/')
def create_book_for_user(id:int,book:Book,db:Session=Depends(get_db)):
    db_book=models.Book(**book.dict(),user_id=id)
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book

@router.post('/users/{u_id}/{b_id}/')
def create_book_for_user(id:int,book:Book,db:Session=Depends(get_db)):

    db_book=db.query(models.Book(**book.dict(),user_id=id))
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book



