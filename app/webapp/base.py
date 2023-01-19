from fastapi import APIRouter
# from .books import route_books
from .users import route_users
from .auth import route_login

api_router = APIRouter(include_in_schema=False)

# api_router.include_router route_books.router, tags=["homepage"])
api_router.include_router(route_users.router, tags=["users"])
api_router.include_router(route_login.router, tags=["Auth"])

