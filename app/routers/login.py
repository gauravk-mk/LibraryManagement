from fastapi import APIRouter, Depends, Body,HTTPException, status, Response
from models import models
from schemas import schemas
from typing import Optional
from fastapi.security import OAuth2PasswordRequestForm
from auth.login import oauth2_scheme
from sqlalchemy.orm import Session
from dependencies import get_db
from datetime import date, timedelta, datetime
from auth.hashing import Hasher
from auth.utils import OAuth2PasswordBearerWithCookie
from jose import jwt
from decouple import config

JWT_SECRET = config("secret")
JWT_ALGORITHM = config("algorithm")

router = APIRouter()

def get_user(email, db):
    user = db.query(models.User).filter(models.User.email == email).first()
    return user


def authenticate_user(username: str, password: str, db: Session = Depends(get_db)):
    user = get_user(email=username, db=db)
    print(user)
    if not user:
        return False
    if not Hasher.verify_password(password, user.hashed_password):
        return False
    return user

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=30
        )
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, JWT_SECRET, algorithm=JWT_ALGORITHM
    )
    return encoded_jwt


@router.post("/token", response_model=schemas.Token)
def login_for_access_token(
    response: Response,
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    user = authenticate_user(form_data.username, form_data.password, db)
    # print(user.username)
    # print(user.email)
    print("----")
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    print(access_token)
    print("---acc token--")
    response.set_cookie(
        key="access_token", value=f"Bearer {access_token}"
    )
    
    return access_token

oauth2_scheme = OAuth2PasswordBearerWithCookie(tokenUrl="/login/token")


def get_current_user_from_token(token, db):
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