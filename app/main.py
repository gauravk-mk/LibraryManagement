from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
import uvicorn
from fastapi.templating import Jinja2Templates
from app.routers import users, books, admin
from app.webapp.base import api_router as webapp_router
from fastapi.staticfiles import StaticFiles


templates = Jinja2Templates(directory="lib-sys/templates")

def include_router(app):
    app.include_router(users.router)
    app.include_router(books.router)
    app.include_router(admin.router)
    app.include_router(webapp_router)

def configure_static(app):
    app.mount("/static",StaticFiles(directory="lib-sys/Static"),name="static")


def start_application():
    app=FastAPI()
    include_router(app)
    # configure_static(app)
    return app

app= start_application
