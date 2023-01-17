from fastapi import APIRouter, Depends, Body
from ..models import models
from ..schemas import schemas
from ..auth.jwt_bearer import JWTBearer
from ..auth.jwt_handler import signJWT
from sqlalchemy.orm import Session
from app.dependencies import get_db

router = APIRouter()

@router.get("/admin/", tags=["admin"])
async def get_admin(db: Session = Depends(get_db)):
    admin = db.query(models.LibraryAdmin).all()
    return admin

@router.post("/admin/signup",tags=["admin"])
async def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    #fake_hashed_password = user.password = "notsecure"
    db_user = models.LibraryAdmin(email=user.email, name=user.name, hashed_password = user.password)
    db.add(db_user)
    db.commit()
    return signJWT(db_user.email)


@router.post("/admin/login", tags=["admin"])
async def user_login(db: Session = Depends(get_db),user: schemas.UserLoginSchema = Body(default=None)):
    if (db.query(models.LibraryAdmin).filter(models.LibraryAdmin.email == user.email).first()) and (db.query(models.LibraryAdmin).filter(models.LibraryAdmin.hashed_password == user.password).first()):
        return signJWT(user.email)
    else:
        return{
            "error":"Invalid Credential!"
        }

    