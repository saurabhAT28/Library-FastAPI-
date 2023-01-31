from sqlalchemy import Column,Integer,String,ForeignKey
import database 
from sqlalchemy.orm import relationship


class User(database.Base):
    __tablename__='users'

    id=Column(Integer,primary_key=True,index=True)
    first_name=Column(String)
    last_name=Column(String)
    email=Column(String)
    password=Column(String)

    # books=relationship("Book",back_populates="reader")