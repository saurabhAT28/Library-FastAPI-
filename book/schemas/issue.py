from pydantic import BaseModel


class IssueCreate(BaseModel):
    u_id:int
    b_id:int


class IssueBook(IssueCreate):
    u_id:int
    b_id:int

    class Config():
        orm_mode=True