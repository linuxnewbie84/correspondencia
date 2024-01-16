from fastapi import APIRouter, Request, Form
from schemas.user_schema import UserSchema, Datalogin
from starlette.status import HTTP_201_CREATED,HTTP_200_OK, HTTP_202_ACCEPTED, HTTP_401_UNAUTHORIZED
from model.user import User
from config.db import engine
from fastapi.responses import HTMLResponse, JSONResponse
from sqlalchemy import insert, select
from werkzeug.security import generate_password_hash, check_password_hash
from fastapi.templating import Jinja2Templates
from main import get_db
from sqlalchemy.orm import Session


user = APIRouter()

admintem = Jinja2Templates(directory="templates")

@user.get("/user", tags=["Administración de Usuarios"], response_model=HTMLResponse)
async def admin(request:Request):
    return admintem.TemplateResponse("admin.html",{"request": request})

