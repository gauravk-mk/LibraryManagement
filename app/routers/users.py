from fastapi import APIRouter, Depends, Body,HTTPException, status
from models import models
from schemas import schemas
from auth.jwt_bearer import JWTBearer
from auth.jwt_handler import signJWT, decodeJWT

from fastapi.security import OAuth2PasswordRequestForm
# from ..auth.login import oauth2_scheme
from auth.login import oauth2_scheme
from sqlalchemy.orm import Session
from dependencies import get_db
from datetime import date, timedelta, datetime
from auth.hashing import Hasher

from jose import jwt
from decouple import config

JWT_SECRET = config("secret")
JWT_ALGORITHM = config("algorithm")
router = APIRouter()


def get_user_from_token(db, token):
    try:
        payload = jwt.decode(token, JWT_SECRET, JWT_ALGORITHM)
        username = payload.get("sub")
        if not username:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate Credentials",
            )
    except:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate Credetials",
        )
    user = db.query(models.User).filter(models.User.email == username).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )
    return user

def create_new_user(user: schemas.UserCreate, db: Session):
    user = models.User(
        name=user.name,
        email=user.email,
        hashed_password=Hasher.get_hash_password(user.password),
        is_active=True,
        created_by=user.email, created_on= datetime.utcnow(), 
        modified_by= user.email, modified_on= datetime.utcnow()
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@router.get("/users/", tags=["users"])
async def get_users(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    return users

@router.post("/users/signup",tags=["users"])
async def create_user(user: schemas.UserCreatedefault, db: Session = Depends(get_db)):
    db_user = models.User(email=user.email, name=user.name, hashed_password = Hasher.get_hash_password(user.password),created_by=user.email, modified_by= user.email)
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
@router.put('/users/issuebook/{id}',tags=["Account-Activity"])
async def issue_Book(acc:schemas.LibraryAccountBase = Body(default=None), db: Session = Depends(get_db),token: str = Depends(oauth2_scheme)):
    return issue_account(db,acc)

@router.delete('/users/returnbook/{id}',tags=["Account-Activity"])
async def return_book(id: int, db: Session = Depends(get_db),token: str = Depends(oauth2_scheme)):
    current_acc = getAccountByIssueId(id,db)
    title = current_acc.book_title
    book= getBookbyTitle(title,db)
    book.quantity = book.quantity+1
    db.delete(current_acc)
    db.commit()
    db.refresh(book)
    return book



def isBookAvailable(title,db):
    book = getBookbyTitle(title,db)
    if not book and book.quantity<1 :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No Book with this id: {id} found")
    else:
        return True


def getUserbyUsername(username, db):
    user = db.query(models.User).filter(models.User.name==username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No User with this ID found")
    else:
        return user
 

def getUserbyId(id, db):
    user = db.query(models.User).filter(models.User.id==id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No User with this ID found")
    else:
        return user

def getBookbyTitle(title,db):
    book = db.query(models.Book).filter(models.Book.title==title).first()
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No Book with this ID found")
    else:
        return book

def getAccountByIssueId(id,db):
    acc = db.query(models.LibraryAccount).filter(models.LibraryAccount.id==id).first()
    if not acc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No Account with this ID found")
    else:
        return acc

# @router.post('/users/acount',tags=["users"])
def issue_account(db, acc):
    curr_book_title = acc.book_title
    curr_user_email = acc.owner_email
    # user = getUserbyEmail(curr_user_email,db)
    curr_date = date.isoformat(date.today())
    last_date = date.isoformat(datetime.now()+ timedelta(days=15))
    new_acc = models.LibraryAccount(
        book_title=curr_book_title, 
        owner_email = curr_user_email,
        date_issued = curr_date,
        valid_till = last_date,
        created_by = curr_user_email,
        modified_by = curr_user_email,
        )    
    curr_book = getBookbyTitle(curr_book_title,db)
    if isBookAvailable(curr_book_title,db):  
        curr_book.quantity = curr_book.quantity-1
    db.add(new_acc)
    db.commit()
    curr_book = getBookbyTitle(curr_book_title,db)

    return {"status": new_acc, 
            "issue_id": new_acc.id,
            "Book Bought": curr_book
    }






    
# @router.get('/users/issuebook/{id}',tags=["users"])
# async def get_book(id: str, db: Session = Depends(get_db)):
#     book = getBookbyId(id,db)
#     if not book and book.quantity ==0 :
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                             detail=f"No Book with this title: {id} found")
#     else:       
#         return {"status" : "success", "note": book}

