from fastapi import APIRouter, Depends, Body
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
    db_user = models.User(email=user.email, hashed_password = user.password)
    db.add(db_user)
    #db.refresh(db_user)
    db.commit()
    return signJWT(db_user.email)

# def check_user(data : get_users):
#     for user in data:
#         if user.email == data.email and user.password == data.password:
#             return True
#         return False

@router.post("/user/login", tags=["users"])
async def user_login(user: schemas.UserCreate = Body(default=None)):
    return signJWT(user.email)
    # if check_user(user):
    #     return signJWT(user.email)
    # else:
    #     return{
    #         "eroor":"Invalid login details"
    #     }