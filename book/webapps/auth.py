from fastapi import APIRouter, Request, Depends, Response, status
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

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30




@router.get("/login")
def login(request: Request,msg:str=None):
    return templates.TemplateResponse("login.html", {"request": request,"msg":msg})


@router.post("/login")
async def login(response: Response, request: Request, db: Session = Depends(get_db)):
    form = await request.form()
    email = form.get("email")
    password = form.get("password")
    
    print(email)
    # print(password)

    errors = []
    pwd_cxt=CryptContext(schemes=["bcrypt"],deprecated="auto")
    if not email:
        errors.append("Please Enter valid Email")
    if not password:
        errors.append("Password enter password")
    if len(errors) > 0:
        return templates.TemplateResponse(
            "login.html", {"request": request, "errors": errors}
        )
    
    try:
        user=db.query(models.User).filter(models.User.email==email).first()
        if user is None:
            errors.append("Email does not exists")
            return templates.TemplateResponse(
                "login.html", {"request": request, "errors": errors}
            )
        else:
            if pwd_cxt.verify(password, user.password):
                data = {"sub": email}
                jwt_token = jwt.encode(
                    data, SECRET_KEY, algorithm=ALGORITHM
                )
                # if we redirect response in below way, it will not set the cookie
                # return responses.RedirectResponse("/?msg=Login Successfull", status_code=status.HTTP_302_FOUND)
                msg = "Login Successful"
                response = templates.TemplateResponse(
                    "login.html", {"request": request, "msg": msg}
                )
                response.set_cookie(
                    key="access_token", value=f"Bearer {jwt_token}", httponly=True
                )
                return response

            else:
                errors.append("Invalid Password")
                return templates.TemplateResponse(
                    "login.html", {"request": request, "errors": errors}
                )
    except:
        errors.append("Something Wrong while authentication or storing tokens!")
        return templates.TemplateResponse(
            "login.html", {"request": request, "errors": errors}
        )