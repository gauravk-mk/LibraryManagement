from fastapi import FastAPI
import uvicorn
# from .auth.jwt_handler import signJWT
# from .auth.jwt_bearer import JWTBearer
# from fastapi.templating import Jinja2Templates


from app.routers import users, books

app=FastAPI()


# templates = Jinja2Templates(directory="LIB-SYS/templates")

app.include_router(users.router)
app.include_router(books.router)


@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}