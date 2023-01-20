from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from routers import users, books
from auth import login
from webapp.base import api_router as webapp_router
from fastapi.staticfiles import StaticFiles


templates = Jinja2Templates(directory="templates")

def include_router(app):
    app.include_router(users.router)
    app.include_router(books.router)
    app.include_router(login.router)
    app.include_router(webapp_router)


def configure_static(app):
    app.mount("/static",StaticFiles(directory="static"),name="static")


def start_application():
    app=FastAPI()
    include_router(app)
    configure_static(app)
    return app

app= start_application
