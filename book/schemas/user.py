from pydantic import BaseModel

class UserBase(BaseModel):
    first_name:str
    last_name:str
    email:str
    class Config():
        orm_mode=True


class User(UserBase):
    password:str
    class Config():
        orm_mode=True


# class showUser(UserBase):
#     class Config():
#         orm_mode=True













    