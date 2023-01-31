# from fastapi import FastAPI,APIRouter,Depends,HTTPException,status
# from passlib.context import CryptContext
# from sqlalchemy.orm import Session
# from ..schemas.auth import Login
# from ..database import get_db
# from ..token import create_access_token
# from ..import models
# # from ..Hashing import hashed
# from passlib.context import CryptContext
# from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm



# router=APIRouter(
#     tags=['Authentication']
# )

# pwd_cxt=CryptContext(schemes=["bcrypt"],deprecated="auto")

# @router.post('/login')
# def login(request:Login,db:Session=Depends(get_db)):
#     user=db.query(models.User).filter(models.User.email==request.username).first()

#     if not user:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#             detail="Invalid Credentials"
#         )
    
#     if not pwd_cxt.verify(request.password,user.password):
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#             detail="Invalid Password"
#         )

#     access_token=create_access_token(
#         data={"sub":user.email}
#     )
    
#     return {"access_token":access_token,"token_type":"bearer"}


# @router.post('/login')
# def login(request:OAuth2PasswordRequestForm=Depends(),db:Session=Depends(get_db)):
#     user=db.query(models.User).filter(models.User.email==request.username).first()

#     if not user:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#             detail="Invalid Credentials"
#         )
    
#     if not pwd_cxt.verify(request.password,user.password):
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#             detail="Invalid Password"
#         )

#     access_token=create_access_token(
#         data={"sub":user.email}
#     )
    
#     return {"access_token":access_token,"token_type":"bearer"}
