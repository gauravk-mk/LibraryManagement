from ...routers.users import create_user
from ...dependencies import get_db
from fastapi import APIRouter, Depends, Request, responses, status
from fastapi.templating import Jinja2Templates
from ...schemas.schemas import UserCreate
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from ...webapp.users.forms import UserCreateForm

router = APIRouter(include_in_schema=False)
templates = Jinja2Templates(directory="app/templates")


@router.get("/register")
def register(request: Request):
    return templates.TemplateResponse(
        "auth/register.html", {"request": request}
    )


@router.post("/register")
async def register(request: Request, db: Session = Depends(get_db)):
    form = UserCreateForm(request)
    await form.load_data()
    if await form.is_valid():
        user = UserCreate(
            name=form.username, email=form.email, password=form.password
        )
        try:
            user = create_user(user=user, db=db)
            return responses.RedirectResponse(
                "/?msg=Successfully-Registered", status_code=status.HTTP_302_FOUND
            )  # default is post request, to use get request added status code 302
        except IntegrityError:
            form.__dict__.get("errors").append("Duplicate username or email")
            return templates.TemplateResponse("users/register.html", form.__dict__)
    return templates.TemplateResponse("users/register.html", form.__dict__)
