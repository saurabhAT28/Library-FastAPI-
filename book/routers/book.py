from fastapi import APIRouter,Depends,status,Response,HTTPException
from sqlalchemy.orm import Session
from ..import models
from ..database import get_db
from ..schemas.book import Book,showBook
from ..schemas.user import User
from ..schemas.admin import Admin
from ..oauth2 import get_current_user


router=APIRouter(
    tags=['Book']
)

@router.get('/book')
def all(db: Session=Depends(get_db)):
    books=db.query(models.Book).all()
    return books

@router.post('/book',status_code=status.HTTP_201_CREATED)
def add_book(request: Book,db: Session=Depends(get_db)):
    # cid=models.Admin.id()
    new_book=models.Book(title=request.title,author=request.author,quantity=request.quantity,admin_id=1)
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return new_book

# @router.put('/book/{title}')
# def issue(title,db: Session=Depends(get_db)):
#     books=db.query(models.Book).filter(models.Book.title==title).first()

#     if (not books) or books.quantity==0:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#             detail=f"Book with {title} is not availabel"
#         )
    
#     books.quantity=books.quantity-1
#     db.commit()
#     db.refresh(books)
#     return books



@router.get('/book/{title}')
def get_book_by_title(title,db: Session=Depends(get_db)):
    books=db.query(models.Book).filter(models.Book.title==title).first()

    if not books:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with {title} is not availabel"
        )
    
    return books
















