from sqlalchemy import Column,Integer,String,ForeignKey,Boolean,DateTime
from sqlalchemy.orm import relationship
from .base_class import Base
from sqlalchemy.sql import func
from datetime import date, timedelta

class Book(Base):
    __tablename__='book'
    __table_args__ = {'extend_existing': True}

    id=Column(Integer,primary_key=True,index=True)
    title=Column(String)
    author=Column(String)
    quantity=Column(Integer)

    admin_id=Column(Integer,ForeignKey('admins.id'))

    adder=relationship("Admin",back_populates="book")

    reader=relationship("issuedBooks",back_populates="book")

class User(Base):
    __tablename__='users'
    __table_args__ = {'extend_existing': True}

    id=Column(Integer,primary_key=True,index=True)
    first_name=Column(String)
    last_name=Column(String)
    email=Column(String,unique=True,index=True)
    password=Column(String)

    # book=relationship('Book',back_populates="reader")


class Admin(Base):
    __tablename__='admins'
    __table_args__ = {'extend_existing': True}

    id=Column(Integer,primary_key=True,index=True)
    first_name=Column(String)
    last_name=Column(String)
    email=Column(String,unique=True,index=True)
    password=Column(String)

    book=relationship('Book',back_populates="adder")


class issuedBooks(Base):
    __tablename__='issuedbooks'
    __table_args__ = {'extend_existing': True}

    issue_id = Column(Integer, primary_key=True, index=True)
    book_id = Column(Integer, ForeignKey("book.id"), index=True)
    r_date = Column(String, index=True)
    return_date = Column(String)

    book=relationship("Book",back_populates="reader")


"""

from sqlalchemy import Boolean, Column, Integer, DateTime, String, ForeignKey
from datetime import date, timedelta
from sqlalchemy.orm import relationship
from .base_class import Base
# from app.database import Base
from sqlalchemy.sql import func

#to add log's column in every table ? 

class User(Base):
    __tablename__="users"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True,index=True)
    email = Column(String, unique=True, index=True)
    name = Column(String)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)



class Book(Base):
    __tablename__ = "books"
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    quantity=Column(Integer)
    # owner_id = Column(Integer, ForeignKey("users.id"))
 
    # owner = relationship("User", back_populates="books")


class LibraryAccount(Base):
    __tablename__ = "accounts"
    acc_id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))
    book_id = Column(Integer, ForeignKey("books.id"))
    date_issued = Column(String)
    valid_till = Column(String)



# class LibraryAdmin(Base):
#     __tablename__="admin"
#     __table_args__ = {'extend_existing': True}

#     id = Column(Integer, primary_key=True,index=True)
#     email = Column(String, unique=True, index=True)
#     name = Column(String)
#     hashed_password = Column(String)







"""


