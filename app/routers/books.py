from fastapi import APIRouter, Depends, HTTPException, HTTPException, status,Response
from auth.jwt_bearer import JWTBearer
from models import models
from schemas import schemas
from sqlalchemy.orm import Session
from dependencies import get_db
from .users import get_user_from_token
from auth.login import oauth2_scheme

router = APIRouter(
    prefix="/books",
    tags=["books"],
    responses={404: {"description": "Not found"}},
)

@router.get("/books/", tags=["books"])
async def get_books(db: Session = Depends(get_db)):
    books = db.query(models.Book).all()
    return books

@router.post('/', tags=["books"])
def addbook(payload:schemas.Book, db: Session=Depends(get_db),token: str = Depends(oauth2_scheme)):
    user = get_user_from_token(db, token)
    new_book = models.Book(title=payload.title, 
                            description=payload.description, 
                            quantity=payload.quantity, 
                            created_by = user.email,
                            modified_by = user.email
                            )
    
    
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return{"status":"success","book":new_book}

@router.get('/{BookId}')
def get_book(bookId: str, db: Session = Depends(get_db)):
    book = db.query(models.Book).filter(models.Book.id == bookId).first()
    if not book:
        raise HTTPException(status_code=status.HTTP_404555_NOT_FOUND,
                            detail=f"No Book with this id: {id} found")
    return {"status": "success", "note": book}

