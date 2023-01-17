from fastapi import APIRouter, Depends, Body,HTTPException, status
from ..models import models
from ..schemas import schemas
from ..auth.jwt_bearer import JWTBearer
from ..auth.jwt_handler import signJWT
from sqlalchemy.orm import Session
from app.dependencies import get_db


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
@router.put('/users/issuebook/{id}',tags=["users"])
async def issue_bookToAcc(acc:schemas.LibraryAccountBase = Body(default=None), db: Session = Depends(get_db)):
    return issue_account(db,acc)

def isBookAvailable(id,db):
    book = getBookbyId(id,db)
    if not book and book.quantity<1 :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No Book with this id: {id} found")
    else:
        return True
        

@router.put('/users/returnbook/{id}',tags=["users"])
async def return_book(id: int, db: Session = Depends(get_db)):
    book= getBookbyId(id,db)

    
@router.get('/users/issuebook/{id}',tags=["users"])
async def get_book(id: str, db: Session = Depends(get_db)):
    book = getBookbyId(id,db)
    if not book and book.quantity ==0 :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No Book with this title: {id} found")
    else:       
        return {"status" : "success", "note": book}

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


# @router.post('/users/acount',tags=["users"])
def issue_account(db, acc):
    currBookId = acc.book_id
    new_acc = models.LibraryAccount(
        book_id=currBookId, 
        owner_id = acc.owner_id
        )
    curr_book = getBookbyId(currBookId,db)
    if isBookAvailable(currBookId,db):  
        curr_book.quantity = curr_book.quantity-1
    db.add(new_acc)
    db.commit()
    return {"status": curr_book}





