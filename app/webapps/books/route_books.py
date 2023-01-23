from typing import Optional
from routers.login import get_current_user_from_token
from models import models
from routers.books import create_new_book, list_books, search_book, retreive_book
from dependencies import get_db
from fastapi import APIRouter, Depends, Request, responses, status
from fastapi.security.utils import get_authorization_scheme_param
from fastapi.templating import Jinja2Templates
from schemas import schemas
from sqlalchemy.orm import Session
from webapps.books.forms import BookCreateForm
from jose import jwt
from decouple import config
from utils.utils import get_user_from_email, get_issues_of_user


JWT_SECRET = config("secret")
JWT_ALGORITHM = config("algorithm")



templates = Jinja2Templates(directory="templates")
router = APIRouter(include_in_schema=False)

@router.get("/home")
async def home(request: Request, db: Session = Depends(get_db), msg: str = None):
    books = list_books(db=db)
    token = request.cookies.get("access_token")
    if token is None:
        return templates.TemplateResponse(
        "general_pages/homepage.html", {"request": request, "books": books, "msg": msg}
    )
    else:
        scheme, _, param = token.partition(" ")
        payload = jwt.decode(
            param, JWT_SECRET, JWT_ALGORITHM
        )
        email = payload.get("sub")
        user = get_user_from_email(email,db)
        return templates.TemplateResponse(
        "general_pages/homepage.html", {"request": request, "books": books, "msg": msg, "user":user}
    )
        
    
@router.get("/profile/")
def get_profile(request: Request,db: Session = Depends(get_db)):
    token = request.cookies.get("access_token")
    if token is None:
        print("is none")

    else:
        scheme, _, param = token.partition(" ")
        payload = jwt.decode(
            param, JWT_SECRET, JWT_ALGORITHM
        )
        email = payload.get("sub")
        user = get_user_from_email(email,db)
        issues = get_issues_of_user(email,db)
    return templates.TemplateResponse("components/profile.html", {"request": request, "user":user,"issues":issues})


@router.get("/detail/{id}")
def book_detail(id: int, request: Request, db: Session = Depends(get_db)):
    book = retreive_book(id=id, db=db)
    return templates.TemplateResponse(
        "books/detail.html", {"request": request, "book": book}
    )


@router.get("/post-a-book/")
def create_book(request: Request, db: Session = Depends(get_db)):
    return templates.TemplateResponse("books/create_book.html", {"request": request})


@router.post("/post-a-book/", response_model=schemas.ShowBook)
async def create_book(request: Request, db: Session = Depends(get_db)):
    # current_user: models.User = Depends(get_current_user_from_token)
    form = BookCreateForm(request)
    await form.load_data()
    if form.is_valid():
        try:
            token = request.cookies.get("access_token")
            print("this is token")
            print(token)
            if token is None:
                # print(token)
                print("is none")
                # errors.append("Please login first")
                # return templates.TemplateResponse("login.html", {"request":request})
            else:
                print("else")
                scheme, _, param = token.partition(" ")
                payload = jwt.decode(
                    param, JWT_SECRET, JWT_ALGORITHM
                )
                email = payload.get("sub")
                print(email)

            # token = request.cookies.get("access_token")
            # scheme, param = get_authorization_scheme_param(
            #     token
            # )  # scheme will hold "Bearer" and param will hold actual token value
            book = schemas.Book(**form.__dict__)
            print(book)
            # print(current_user)
            book = create_new_book(book=book, db=db, created_by=email)
        
            return responses.RedirectResponse(
                f"/book-details/{book.id}", status_code=status.HTTP_302_FOUND
            )
        except Exception as e:
            print(e)
            form.__dict__.get("errors").append(
                "You might not be logged in, In case problem persists please contact us."
            )
            return templates.TemplateResponse("books/create_book.html", form.__dict__)
    return templates.TemplateResponse("books/create_book.html", form.__dict__)


@router.get("/delete-book/")
def show_books_to_delete(request: Request, db: Session = Depends(get_db)):
    books = list_books(db=db)
    return templates.TemplateResponse(
        "books/show_books_to_delete.html", {"request": request, "books": books}
    )


@router.get("/search/")
def search(
    request: Request, db: Session = Depends(get_db), query: Optional[str] = None
):
    books = search_book(query, db=db)
    return templates.TemplateResponse(
        "general_pages/homepage.html", {"request": request, "books": books}
    )
