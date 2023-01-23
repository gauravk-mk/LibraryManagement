from routers.users import create_new_user
from dependencies import get_db
from fastapi import APIRouter, Depends, Request, responses, status
from fastapi.templating import Jinja2Templates
from schemas import schemas
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from webapps.users.forms import UserCreateForm
from datetime import date, timedelta, datetime



templates = Jinja2Templates(directory="templates")
router = APIRouter(include_in_schema=False)


@router.get("/register/")
def register(request: Request):
    return templates.TemplateResponse("auth/register.html", {"request": request})


@router.post("/register/")
async def register(request: Request, db: Session = Depends(get_db)):
    form = UserCreateForm(request)
    await form.load_data()
    if await form.is_valid():
        user = schemas.UserCreate(
            name=form.username, email=form.email, password=form.password,
            created_by=form.email, created_on= datetime.utcnow(), 
            modified_by= form.email, modified_on= datetime.utcnow()
        )
        try:
            user = create_new_user(user=user, db=db)
            return responses.RedirectResponse(
                "/login?msg=Successfully-Registered", status_code=status.HTTP_302_FOUND
            )  # default is post request, to use get request added status code 302
        except IntegrityError:
            form.__dict__.get("errors").append("Duplicate username or email")
            return templates.TemplateResponse("users/register.html", form.__dict__)
    return templates.TemplateResponse("users/register.html", form.__dict__)
