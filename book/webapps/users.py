from fastapi import APIRouter, Request, Depends, responses, status
from fastapi.templating import Jinja2Templates
from ..import models
from ..schemas.book import Book,showBook
from sqlalchemy.orm import Session
from ..database import get_db
from jose import jwt
from ..schemas.user import User
from passlib.context import CryptContext
from sqlalchemy.exc import IntegrityError

templates=Jinja2Templates(directory="book/templates")
router = APIRouter(include_in_schema=False)


@router.get("/register")
def registration(request: Request):
    return templates.TemplateResponse("user_register.html", {"request": request})


@router.post("/register")
async def registration(request: Request, db: Session = Depends(get_db)):
    form = await request.form()
    first_name = form.get("first_name")
    last_name = form.get("last_name")
    email = form.get("email")
    password = form.get("password")

    # print(first_name)
    # print(last_name)
    # print(email)
    # print(password)



    errors = []
    if not password or len(password) < 8:
        errors.append("Password should be greater than 8 chars")
        return templates.TemplateResponse(
            "user_register.html", {"request": request, "errors": errors}
        )
    
    pwd_cxt=CryptContext(schemes=["bcrypt"],deprecated="auto")
    hashedPassword=pwd_cxt.hash(password)

    user = models.User(first_name=first_name,last_name=last_name,email=email,password=hashedPassword)
    
    if len(errors) > 0:
        return templates.TemplateResponse(
            "user_register.html", {"request": request, "errors": errors}
        )
    try:
        db.add(user)
        db.commit()
        db.refresh(user)
        return responses.RedirectResponse(
            "/login?msg=successfully registered", status_code=status.HTTP_302_FOUND
        )
    except IntegrityError:
        errors.append("Email already registered")
        return templates.TemplateResponse(
            "user_register.html", {"request": request, "errors": errors}
        )


