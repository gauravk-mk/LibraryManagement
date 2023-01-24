from fastapi import APIRouter, Depends, HTTPException, Request, status, responses
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from webapps.auth.forms import LoginForm
from routers.login import login_for_access_token
from dependencies import get_db



templates = Jinja2Templates(directory="templates")
router = APIRouter(include_in_schema=False)


@router.get("/login/")
def login(request: Request):
    return templates.TemplateResponse("auth/login.html", {"request": request})


@router.post("/login/")
async def login(request: Request, db: Session = Depends(get_db)):
    form = LoginForm(request)
    await form.load_data()
    if await form.is_valid():
        try:
            form.__dict__.update(msg="Login Successful :)")
            response = templates.TemplateResponse("auth/login.html", form.__dict__)
            access_token= login_for_access_token(response=response, form_data=form, db=db)
            # return responses.RedirectResponse(
            #     "/home?msg=Successfully-Logged In", status_code=status.HTTP_302_FOUND
            # )
            response.set_cookie(key="access_token", value=f"Bearer {access_token}", httponly=True) 
            return response
        except HTTPException:
            form.__dict__.update(msg="")
            form.__dict__.get("errors").append("Incorrect Email or Password")
            return templates.TemplateResponse("auth/login.html", form.__dict__)
    return templates.TemplateResponse("auth/login.html", form.__dict__)


@router.get("/logout/")
def login(request: Request):
    token = request.cookies.get("access_token")
    errors=[]
    if token is None:
        errors.append("please login")
        return templates.TemplateResponse("auth/login.html",{"request":request, "errors":errors})
    else:
        msg="You have been Logged Out!"
        response= templates.TemplateResponse("auth/login.html",{"request":request, "errors":errors, "msg":msg})
        response.delete_cookie("access_token")

    return response
