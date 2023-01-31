from fastapi import APIRouter,Depends,status,Response,HTTPException
from sqlalchemy.orm import Session
from ..import models
from ..database import get_db
from ..schemas.admin import Admin

from passlib.context import CryptContext


router=APIRouter(
    tags=['Admin']
)


pwd_cxt=CryptContext(schemes=["bcrypt"],deprecated="auto")

@router.post('/admin')
def create_admin(request:Admin,db:Session=Depends(get_db)):
    hashedPassword=pwd_cxt.hash(request.password)
    new_admin=models.Admin(first_name=request.first_name,last_name=request.last_name,email=request.email,password=hashedPassword)
    db.add(new_admin)
    db.commit()
    db.refresh(new_admin)
    return new_admin


@router.get('/admin')
def all(db: Session=Depends(get_db)):
    admins=db.query(models.Admin).all()
    return admins



# @router.post('/book',status_code=status.HTTP_201_CREATED)
# def add_book(request: Book,db: Session=Depends(get_db)):
#     new_book=models.Book(title=request.title,author=request.author,quantity=request.quantity,user_id=1)
#     db.add(new_book)
#     db.commit()
#     db.refresh(new_book)
#     return new_book

# @router.put('/book/{title}')
# def issue(title,db: Session=Depends(get_db)):
#     books=db.query(models.Book).filter(models.Book.title==title).first()

#     if not books:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#             detail=f"Book with {title} is not availabel"
#         )
    
#     books.quantity=books.quantity-100
#     db.commit()
#     db.refresh(books)
#     return books



