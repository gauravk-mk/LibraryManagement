from fastapi import APIRouter, Depends, Body,HTTPException, status
from ..models import models
from ..schemas import schemas
from ..auth.jwt_bearer import JWTBearer
from ..auth.jwt_handler import signJWT
from sqlalchemy.orm import Session
from app.dependencies import get_db
from datetime import date, timedelta


router = APIRouter()


@router.get("/users/", tags=["users"])
async def get_users(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    return users

@router.post("/users/signup",tags=["users"])
async def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = models.User(email=user.email, name=user.name, hashed_password = user.password)
    db.add(db_user)
    db.commit()
    return signJWT(db_user.email)


@router.post("/user/login", tags=["users"])
async def user_login(db: Session = Depends(get_db),user: schemas.UserLoginSchema = Body(default=None)):
    if (db.query(models.User).filter(models.User.email == user.email).first()) and (db.query(models.User).filter(models.User.hashed_password == user.password).first()):
        return signJWT(user.email)
    else:
        return{
            "error":"Invalid Credential!"
        }

#to issue a book from books database
@router.put('/users/issuebook/{id}',tags=["Account-Activity"],dependencies=[Depends(JWTBearer())])
async def issue_Book(acc:schemas.LibraryAccountBase = Body(default=None), db: Session = Depends(get_db)):
    return issue_account(db,acc)

@router.delete('/users/returnbook/{id}',tags=["Account-Activity"],dependencies=[Depends(JWTBearer())])
async def return_book(id: int, db: Session = Depends(get_db)):
    current_acc = getAccountByIssueId(id,db)
    book_id = current_acc.book_id
    book= getBookbyId(book_id,db)
    book.quantity = book.quantity+1
    db.delete(current_acc)
    db.commit()
    db.refresh(book)
    return book



def isBookAvailable(id,db):
    book = getBookbyId(id,db)
    if not book and book.quantity<1 :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No Book with this id: {id} found")
    else:
        return True
        

def getUserbyId(id, db):
    user = db.query(models.User).filter(models.User.id==id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No User with this ID found")
    else:
        return user

def getBookbyId(id,db):
    book = db.query(models.Book).filter(models.Book.id==id).first()
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No Book with this ID found")
    else:
        return book

def getAccountByIssueId(id,db):
    acc = db.query(models.LibraryAccount).filter(models.LibraryAccount.acc_id==id).first()
    if not acc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No Account with this ID found")
    else:
        return acc

# @router.post('/users/acount',tags=["users"])
def issue_account(db, acc):
    currBookId = acc.book_id
    new_acc = models.LibraryAccount(
        book_id=currBookId, 
        owner_id = acc.owner_id,
        )
    
    curr_book = getBookbyId(currBookId,db)
    if isBookAvailable(currBookId,db):  
        curr_book.quantity = curr_book.quantity-1
    db.add(new_acc)
    db.commit()
    curr_book = getBookbyId(currBookId,db)
    return {"status": curr_book, 
            "issue_id": new_acc.acc_id
    }






    
# @router.get('/users/issuebook/{id}',tags=["users"])
# async def get_book(id: str, db: Session = Depends(get_db)):
#     book = getBookbyId(id,db)
#     if not book and book.quantity ==0 :
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                             detail=f"No Book with this title: {id} found")
#     else:       
#         return {"status" : "success", "note": book}

