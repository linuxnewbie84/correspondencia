from fastapi import APIRouter, Request, Form,  Depends, HTTPException, status
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
from typing import Annotated


user = APIRouter()

admintem = Jinja2Templates(directory="templates")

db_dependecy = Annotated[Session,Depends(get_db)]

@user.get("/user", tags=["Administración de Usuarios"], response_class= HTTP_200_OK)
async def admin(request:Request):
    return admintem.TemplateResponse("admin.html",{"request": request})

@user.post("/user", tags=["Crear Usuario"], response_class=HTTP_201_CREATED)

