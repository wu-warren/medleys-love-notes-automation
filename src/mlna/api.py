"""Defines the APIs for interacting with medleys-love-notes-automation."""

from fastapi import FastAPI, APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

__all__ = ("rest_api",)

rest_api = FastAPI()
templates = Jinja2Templates(directory="src/mlna/data/templates")


@rest_api.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


api_v1_router = APIRouter(prefix="/api/v1")


@api_v1_router.get("/status")
def status():
    return {"ok": True, "message": "API is healthy"}


rest_api.include_router(api_v1_router)
