from fastapi import APIRouter,Depends,status,Response,HTTPException
from sqlalchemy.orm import Session
from ..import models
from ..database import get_db
from ..schemas.user import User
from passlib.context import CryptContext
from ..schemas.book import Book,showBook

router=APIRouter(
    tags=['User']
)


pwd_cxt=CryptContext(schemes=["bcrypt"],deprecated="auto")

@router.post('/user')
def create_user(request:User,db:Session=Depends(get_db)):
    hashedPassword=pwd_cxt.hash(request.password)
    new_user=models.User(first_name=request.first_name,last_name=request.last_name,email=request.email,password=hashedPassword)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
    # return request

@router.get('/user')
def all(db: Session=Depends(get_db)):
    users=db.query(models.User).all()
    return users

@router.get('user/{id}')
def get_user(id:int,db:Session=Depends(get_db)):
    user=db.query(models.User).filter(models.User.id==id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with {id} is not availabel"
        )

    return user



# Get the books taken by user
# @router.post('/users/{id}/books/')
# def create_book_for_user(id:int,book:Book,db:Session=Depends(get_db)):
#     db_book=models.Book(**book.dict(),user_id=id)
#     db.add(db_book)
#     db.commit()
#     db.refresh(db_book)
#     return db_book

# @router.post('/users/{u_id}/{b_id}/')
# def create_book_for_user(id:int,book:Book,db:Session=Depends(get_db)):

#     db_book=db.query(models.Book(**book.dict(),user_id=id))
#     db.add(db_book)
#     db.commit()
#     db.refresh(db_book)
#     return db_book


















