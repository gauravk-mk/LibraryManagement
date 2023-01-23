from models import models
from schemas import schemas
from sqlalchemy.orm import Session
from routers.books import retreive_book, search_book
from datetime import datetime
from fastapi import APIRouter, Depends, Body,HTTPException, status


def create_new_issue(issue: schemas.ShowLibraryAcoount, db: Session, created_by: str):
    issue_object = models.LibraryAccount(**issue.dict(), created_by = created_by)

    books = search_book(issue.book_title, db)
    for book in books:
        book_id = book.id

        book = retreive_book(book_id, db)
        if book.quantity >= 0:
            book.quantity -= 1

            book.modified_by = created_by

            db.add(issue_object)
            db.commit()
            db.refresh(issue_object)

            return issue_object
        
def get_user_from_email(email, db:Session):
    user = db.query(models.User).filter(models.User.email == email).first()
    return user


def list_issues(db: Session):
    issues = db.query(models.LibraryAccount).all()
    return issues

def retreive_issue(id: int, db: Session):
    item = db.query(models.LibraryAccount).filter(models.LibraryAccount.id == id).first()
    return item


def update_issue_by_id(id: int, issue: schemas.UpdateAccount, db: Session, created_by: str):
    existing_issue = db.query(models.LibraryAccount).filter(models.LibraryAccount.id == id)
    if not existing_issue.first():
        return 0

    books = search_book(issue.book, db)
    for book in books:
        book_id = book.id

        book_ = retreive_book(book_id, db)
        if book_.quantity >= 0:
            book_.quantity += 1

            book.modified_by = created_by

            issue.__dict__.update(
                actual_return_date = datetime.now().date(),
                modified_by=created_by
            )  # update dictionary with new key value of owner_id
            
            existing_issue.update(issue.__dict__)
            db.commit()
            return 1
        
def get_book_from_id(id, db:Session):
    book = db.query(models.Book).filter(models.Book.id == id).first()
    return book

def get_book_from_title(title,db):
    book = db.query(models.Book).filter(models.Book.title==title).first()
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No Book with this ID found")
    else:
        return book


def is_book_available(title,db):
    book = get_book_from_title(title,db)
    if not book and book.quantity<1 :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No Book: {title} found or Not enough books")
    else:
        return True

def get_issues_of_user(email,db):
    issues=[]
    issues = db.query(models.LibraryAccount).filter(models.LibraryAccount.owner_email==email).all()
    # print(issues)
    return issues

def get_issue_by_id(id,db):
    issue=db.query(models.LibraryAccount).filter(models.LibraryAccount.id==id).first()
    return issue