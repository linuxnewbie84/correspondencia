from fastapi import APIRouter, Request
from schemas.user_schema import UserSchema, Datalogin
from starlette.status import HTTP_201_CREATED,HTTP_200_OK, HTTP_202_ACCEPTED, HTTP_401_UNAUTHORIZED
from model.user import User
from config.db import engine
from fastapi.responses import HTMLResponse, JSONResponse
from sqlalchemy import insert, select
from werkzeug.security import generate_password_hash, check_password_hash