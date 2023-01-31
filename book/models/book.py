from sqlalchemy import Column,Integer,String,ForeignKey
from ..database import Base

class Book(Base):
    __tablename__='books'

    id=Column(Integer,primary_key=True,index=True)
    title=Column(String)
    author=Column(String)
    quantity=Column(Integer)

    # user_id=Column(Integer,ForeignKey('user.id'))

    # reader=relationship("User",back_populates="Books")






