from fastapi import APIRouter, Depends, Body,HTTPException, status
from ..models import models
from ..schemas import schemas
from ..auth.jwt_bearer import JWTBearer
from ..auth.jwt_handler import signJWT
from sqlalchemy.orm import Session
from app.dependencies import get_db

router = APIRouter()

@router.get("/users/", tags=["users"])
async def get_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = db.query(models.User).offset(skip).limit(limit).all()
    return users

@router.post("/users/signup",tags=["users"])
async def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    #fake_hashed_password = user.password = "notsecure"
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


@router.get('/users/issuebook/{title}',tags=["users"])
async def issue_book(title: str, db: Session = Depends(get_db)):
    book = db.query(models.Book).filter(models.Book.title == title).first()
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No Book with this title: {title} found")
    else:
        return {"status" : "success", "note": book}
        #add book in db of user account remove book from db of book

#post


#for referance
@router.get('/{BookId}')
def get_book(bookId: str, db: Session = Depends(get_db)):
    book = db.query(models.Book).filter(models.Book.id == bookId).first()
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No Book with this id: {id} found")
    else:
        return {"status": "success", "note": book}



