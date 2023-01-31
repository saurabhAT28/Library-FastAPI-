from typing import List
from fastapi import FastAPI,Depends,status,Response,HTTPException
from . import models
# from . import schemas.user import User
from sqlalchemy.orm import Session
from .database import engine,SessionLocal,get_db
from .schemas.book import Book,showBook
from .schemas.user import User
from passlib.context import CryptContext
from .routers import book,user,library,authentication,admin,issue
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles


# Imports from webapps
from .webapps import books as web_books
from .webapps import users as web_users
from .webapps import auth as web_auth


templates=Jinja2Templates(directory="book/templates")

# def configure_static(book):
#     book.mount("/book/static",
#     StaticFiles(directory="book/static"),
#     name="static"
#     )

app=FastAPI()

app.mount("/static",StaticFiles(directory="book/static"),name="static")
models.Base.metadata.create_all(engine)

app.include_router(book.router)
app.include_router(user.router)
app.include_router(library.router)
# app.include_router(authentication.router)
app.include_router(admin.router)
app.include_router(issue.router)

# Web apps Routers
app.include_router(web_books.router)
app.include_router(web_users.router)
app.include_router(web_auth.router)












