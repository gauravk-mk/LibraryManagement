from routers.login import get_current_user_from_token
from models import models
from utils.utils import create_new_issue, list_issues,retreive_issue
from dependencies import get_db
from fastapi import APIRouter, Depends, Request, responses, status
from fastapi.security.utils import get_authorization_scheme_param
from fastapi.templating import Jinja2Templates
from schemas import schemas
from sqlalchemy.orm import Session
from webapps.issued.forms import IssuedCreateForm
from jose import jwt
from decouple import config
from utils.utils import get_book_from_id, get_book_from_title,is_book_available,get_issue_by_id
from datetime import date, timedelta, datetime


JWT_SECRET = config("secret")
JWT_ALGORITHM = config("algorithm")

templates = Jinja2Templates(directory="templates")
router = APIRouter(include_in_schema=False)


@router.get("/home")
async def home(request: Request, db: Session = Depends(get_db), msg: str = None):
    issued = list_issues(db=db)
    return templates.TemplateResponse(
        "general_pages/homepage.html", {"request": request, "issued": issued, "msg": msg}
    )

@router.get("/issue-details/{id}")
def issue_detail(id: int, request: Request, db: Session = Depends(get_db)):
    issue = retreive_issue(id=id, db=db)
    return templates.TemplateResponse(
        "issued/issued_detail.html", {"request": request, "issue": issue}
    )


@router.get("/post-a-issue/")
def create_issued(request: Request, db: Session = Depends(get_db)):
    return templates.TemplateResponse("issued/create_issue.html", {"request": request})


@router.post("/post-a-issue/")
async def create_issued(request: Request, db: Session = Depends(get_db)):
    form = IssuedCreateForm(request)
    await form.load_data()
    print(form.book_title)
    if form.is_valid():
        try:
            token = request.cookies.get("access_token")
            print("token-")
            print(token)
            scheme, _, param = token.partition(" ")
            payload = jwt.decode(
                param, JWT_SECRET, JWT_ALGORITHM
            )
            email = payload.get("sub")
            print(email)
            if form.owner_email == email:
                print("is is if")
                issue = schemas.LibraryAcoount(**form.__dict__)
                print(issue)
                issue = create_new_issue(issue=issue, db=db, created_by=email)
                print(issue.id)
                return responses.RedirectResponse(
                    f"/issue-details/{issue.id}", status_code=status.HTTP_302_FOUND
                )
                
            form.__dict__.get("errors").append(
                "Please enter your email id"
            )
        except Exception as e:
            print(e)
            form.__dict__.get("errors").append(
                "User not logged in or Insufficient book quantity, please check back again later"
            )
            return templates.TemplateResponse("issued/create_issue.html", form.__dict__)
    return templates.TemplateResponse("issued/create_issue.html", form.__dict__)



@router.get("/post-a-issue-button/{id}")
async def create_issue_button(id:int,request: Request, db: Session = Depends(get_db)):
        token = request.cookies.get("access_token")
        print("token-")
        print(token)
        scheme, _, param = token.partition(" ")
        payload = jwt.decode(
            param, JWT_SECRET, JWT_ALGORITHM
        )
        email = payload.get("sub")
        book= get_book_from_id(id,db)
        issue = models.LibraryAccount( owner_email = email, book_title=book.title,
            date_issued = date.isoformat(date.today()),
            valid_till = date.isoformat(datetime.now()+ timedelta(days=15)),
            created_by = email,
            modified_by = email
        )
        print(issue)
        if is_book_available(book.title,db):  
            book.quantity = book.quantity-1
        db.add(issue)
        db.commit()
        return responses.RedirectResponse(
            f"/issue-details/{issue.id}", status_code=status.HTTP_302_FOUND
        )
            
@router.get("/return-a-book/{id}")
async def delete_issue(id:int,request: Request, db: Session = Depends(get_db)):
    current_issue = get_issue_by_id(id,db)
    current_book=get_book_from_title(current_issue.book_title,db)
    current_book.quantity=current_book.quantity+1
    db.delete(current_issue)
    db.commit()
    # db.refresh(current_book)
    return responses.RedirectResponse(
        "/profile/", status_code=status.HTTP_302_FOUND
    )



@router.get("/lib_history/")
def show_issues_to_update(request: Request, db: Session = Depends(get_db),):
    issued = list_issues(db=db)
    return templates.TemplateResponse(
        "issued/show_issues_to_update.html", {"request": request, "issued": issued}
    )
