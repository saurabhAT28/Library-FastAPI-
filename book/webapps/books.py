from fastapi import APIRouter, Request, Depends, responses, status,HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from ..import models
from ..schemas.book import Book,showBook
from sqlalchemy.orm import Session
from sqlalchemy import and_
from ..database import get_db
from jose import jwt
from typing import Optional
from datetime import datetime, time, timedelta, date
# from config import settings



# BASE_DIR=Path(__file__).resolve().parent

# from fastapi.staticfiles import StaticFiles

templates=Jinja2Templates(directory="book/templates")
router = APIRouter(include_in_schema=False)

# def configure_static(book):
#     book.mount("../book/static",
#     StaticFiles(directory="frontend"),
#     name="static"
#     )

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

max_issue = 3

@router.get('/books/autocomplete')
def autocomplete(term:Optional[str],db: Session = Depends(get_db)):
    books=db.query(models.Book).filter(models.Book.title.contains(term)).all()
    suggestions=[]
    for b in books:
        suggestions.append(b.title)
    return suggestions

@router.get("/")
def item_home(request: Request,db: Session=Depends(get_db),msg:str=None):
    books=db.query(models.Book).all()
    token = request.cookies.get("access_token")
    errors=[]
    if token is None:
        errors.append("Please login first")
        return templates.TemplateResponse("login.html", {"request":request, "errors":errors})
    scheme, _, param = token.partition(" ")
    payload = jwt.decode(
        param, SECRET_KEY, ALGORITHM
    )
    email = payload.get("sub")

    user=db.query(models.User).filter(models.User.email==email).first()
    return templates.TemplateResponse(
        "item_homepage.html", {"request": request,"books":books,"msg":msg,"user":user}
    )


@router.get("/add_book")
def add_book(request: Request):
    return templates.TemplateResponse("add_book.html", {"request": request})


@router.post("/add_book")
async def create_an_item(request: Request, db: Session = Depends(get_db)):
    form = await request.form()
    title = form.get("title")
    author = form.get("author")
    quantity = form.get("quantity")

    # print(title)
    # print(author)
    # print(quantity)


    errors = []
    if not title:
        errors.append("Please enter title")
    if not author:
        errors.append("Please enter author")
    if not quantity:
        errors.append("Please enter quantity")
    if len(errors) > 0:
        return templates.TemplateResponse(
            "add_book.html", {"request": request, "errors": errors}
        )
    try:
        token = request.cookies.get("access_token")
        if not token:
            errors.append("Kindly Authenticate first by login")
            return templates.TemplateResponse(
                "add_book.html", {"request": request, "errors": errors}
            )
        scheme, _, param = token.partition(" ")
        # print(scheme)
        # print(param)
        payload = jwt.decode(param,SECRET_KEY, algorithms=ALGORITHM)
        email = payload.get("sub")
        if email is None:
            errors.append("Kindly login first, you are not authenticated")
            return templates.TemplateResponse(
                "add_book.html", {"request": request, "errors": errors}
            )
        else:
            user = db.query(models.User).filter(models.User.email == email).first()
            if user is None:
                errors.append("You are not authenticated, Kindly Login")
                return templates.TemplateResponse(
                    "add_book.html", {"request": request, "errors": errors}
                )
            else:
                book = models.Book(
                    title=title,
                    author=author,
                    quantity=quantity,
                    admin_id=user.id,
                    created_by=user.email
                )
                db.add(book)
                db.commit()
                db.refresh(book)
                # print(book.id)
                return responses.RedirectResponse(
                    f"/", status_code=status.HTTP_302_FOUND
                )
    except Exception as e:
        errors.append("Something is wrong !")
        # print(e)
        return templates.TemplateResponse(
            "add_book.html", {"request": request, "errors": errors}
        )

@router.get("/search")
def search_books(request: Request, query: Optional[str], db: Session = Depends(get_db)):
    search = db.query(models.Book).filter(models.Book.title.contains(query)).all()
    return templates.TemplateResponse(
        "item_homepage.html", {"request": request, "books": search}
    )


@router.get("/issue-book/{book_id}")
def issue_book(request: Request, book_id:int, db:Session=Depends(get_db)):
    token = request.cookies.get("access_token")
    errors=[]
    if token is None:
        errors.append("Please login first")
        return templates.TemplateResponse("login.html", {"request":request, "errors":errors})
    else:
        scheme, _, param = token.partition(" ")
        payload = jwt.decode(
            param, SECRET_KEY, ALGORITHM
        )
        email = payload.get("sub")
         
        book = db.query(models.Book).filter(models.Book.id==book_id).first()

        books_issued = db.query(models.issuedBooks).filter(and_(models.issuedBooks.created_by==email, models.issuedBooks.return_date.is_(None))).all()

        if(len(books_issued)==max_issue):
            errors.append("You can't issue more than 3 books")
            return templates.TemplateResponse("item_detail.html", {"request":request, "book": book, "errors":errors})
        else:
            last_date=date.isoformat(date.today() + timedelta(days=7))

            issue = models.issuedBooks(book_id=book_id,r_date=last_date, created_by=email)

            book.quantity = book.quantity - 1
            
            db.add(issue)
            db.commit()
            db.refresh(book)
            db.refresh(issue)

            return templates.TemplateResponse(
                "item_detail.html", {"request":request, "book":book, "errors":errors}
            )





@router.get("/detail/{id}")
def book_detail(request: Request, id: int, db: Session = Depends(get_db)):
    book = db.query(models.Book).filter(models.Book.id == id).first()
    
    avl=False
    if(book.quantity > 0):
        avl=True
    
    return templates.TemplateResponse(
        "item_detail.html", {"request": request, "book": book,"avl":avl}
    )


@router.get("/return_book/{issue_id}", response_class=HTMLResponse)
def return_book(request: Request, issue_id:int, db:Session=Depends(get_db)):
    issue = db.query(models.issuedBooks).filter(models.issuedBooks.issue_id==issue_id).first()

    issue.return_date = date.isoformat(date.today())
    
    book = db.query(models.Book).filter(models.Book.id==issue.book_id).first()

    book.quantity = book.quantity + 1

    db.commit()
    db.refresh(book)

    # print(issue.created_by)

    user = db.query(models.User).filter(models.User.email==issue.created_by).first()

    late = (datetime.strptime(issue.return_date, "%Y-%m-%d")-datetime.strptime(issue.r_date, "%Y-%m-%d")).days

    # print(user)

    count = db.query(models.issuedBooks).filter(and_(models.issuedBooks.created_by==user.email, models.issuedBooks.return_date.is_(None))).all()

    # books = db.query(models.issuedBooks).filter(models.Book.created_by==issue.created_by).all()

    fees=0
    if(late>0):
        fees = late*5
        return templates.TemplateResponse("profile.html", {"request":request, "issue_id":issue.issue_id, "user":user, "fees":fees, "books":count, "length":len(count)})
    
    return templates.TemplateResponse("profile.html", {"request":request, "issue_id":issue.issue_id,"fees":fees, "user":user, "books":count, "length":len(count)})


@router.get("/profile/{user_id}", response_class=HTMLResponse)
def user_profile(request: Request, user_id:int, db:Session=Depends(get_db)):
    # print("token")
    token = request.cookies.get("access_token")
    errors=[]
    if token is None:
        errors.append("Please login first")
        return templates.TemplateResponse("login.html", {"request":request, "errors":errors})
    else:
        scheme, _, param = token.partition(" ")
        payload = jwt.decode(
            param, SECRET_KEY, ALGORITHM
        )
        email = payload.get("sub")

        user=db.query(models.User).filter(models.User.email==email).first()

        i_books = db.query(models.issuedBooks).filter(and_(models.issuedBooks.created_by==email, models.issuedBooks.return_date.is_(None))).all()

        # print(user.email)

    return templates.TemplateResponse("profile.html", {"request":request, "books":i_books, "length":len(i_books), "errors":errors, "user":user})














