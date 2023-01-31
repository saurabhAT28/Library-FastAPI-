from fastapi import APIRouter,Depends,status,Response,HTTPException
from sqlalchemy.orm import Session
from ..import models
from ..database import get_db
from ..schemas.book import Book,showBook
from ..schemas.user import User
from ..schemas.admin import Admin
from ..schemas.issue import IssueCreate
from ..oauth2 import get_current_user
from datetime import date,timedelta,datetime

router=APIRouter(
    tags=['Issue']
)

# current_user:User=Depends(get_current_user)

@router.get('/issue')
def all(db: Session=Depends(get_db)):
    issues=db.query(models.issuedBooks).all()
    return issues

@router.post('/issue',status_code=status.HTTP_201_CREATED)
def add_issue(request: IssueCreate,db: Session=Depends(get_db)):
    new_issue=models.issuedBooks(u_id=request.u_id,b_id=request.b_id,i_date=date.isoformat(date.today()),r_date=date.isoformat(date.today()+timedelta(days=20)))
    
    req_book=db.query(models.Book).filter(new_issue.b_id==models.Book.id).first()

    if(req_book.quantity==0):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with {req_book.title} is not availabel"
        )
    
    req_book.quantity=req_book.quantity-1

    db.commit()
    db.refresh(req_book)


    db.add(new_issue)
    db.commit()
    db.refresh(new_issue)
    return new_issue



@router.put('/issue',status_code=status.HTTP_201_CREATED)
def update_issue(issue_id:int,db: Session=Depends(get_db)):
    issue=db.query(models.issuedBooks).filter(models.issuedBooks.i_id==issue_id).first()
    
    issue.is_given=True
    db.commit()
    db.refresh(issue)
    return issue


@router.delete('/issue')
def delete_issue(issue_id:int,db: Session=Depends(get_db)):
    issue=db.query(models.issuedBooks).filter(models.issuedBooks.i_id==issue_id).first()

    if not issue or issue.is_given==True:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Issue with {issue_id} is not availabel"
        )
    
    req_book=db.query(models.Book).filter(issue.b_id==models.Book.id).first() 

    fine=2*(datetime.strptime(str(issue.r_date),"%Y-%m-%d")-datetime.strptime(date.today(),"%Y-%m-%d")).days

    if(fine<=0):
        return "Fine: Rs.0"
    return f"Fine: Rs.{fine}"



    db.delete(issue)
    db.commit()
    # db.refresh(issue)
    req_book.quantity=req_book.quantity+1
    db.commit()
    db.refresh(req_book)

    # return req_book
    # return 'string'
    # return {"detail": "Issue Deleted Successfully",
    #         "status":"Status 200",
    #         "object": req_book
    #         }


    
    return "Issued Book is Returned"







