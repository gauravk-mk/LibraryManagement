from fastapi import APIRouter
from webapps.auth import route_login
from webapps.books import route_books
from webapps.users import route_users
from webapps.issued import route_issued

api_router = APIRouter()
api_router.include_router(route_books.router, prefix="", tags=["homepage"])
api_router.include_router(route_users.router, prefix="", tags=["users"])
api_router.include_router(route_login.router, prefix="", tags=["auth"])
api_router.include_router(route_issued.router, prefix="", tags=["issue"])
