from fastapi import APIRouter, Request, Form, Depends, HTTPException, Response
from typing import List
from schemas.user_schema import UserSchema, Id_User, CrearUsuario
from starlette.status import (
    HTTP_201_CREATED,
    HTTP_200_OK,
    HTTP_202_ACCEPTED,
    HTTP_401_UNAUTHORIZED,
    HTTP_404_NOT_FOUND,
)
import model
from config.db import engine, Sessionlocal
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from typing import Annotated
from werkzeug.security import check_password_hash, generate_password_hash
import crud
from router import doc


usr = APIRouter()

admintem = Jinja2Templates(directory="templates")


# Acceso a la base de datos
def get_db():
    db = Sessionlocal()
    try:
        yield db  # Generador para iterar los datos de la base
    finally:
        db.close()


db_dependecy = Annotated[Session, Depends(get_db)]  # Necesaria para todas las consultas


#!retonamos la tabla
@usr.get("/admin")
def admin(request: Request, db:db_dependecy):
    todos = db.query(model.user.User).order_by(model.user.User.id.desc())
    return admintem.TemplateResponse("admin.html", {"request": request, "todos":todos})


#!Crear usuarios
@usr.post(
    "/usr/create/",
    tags=["Crear Usuario"],
    status_code=HTTP_201_CREATED,
)
async def Create(
    name: Annotated[str, Form()],
    cargo: Annotated[str, Form()],
    username: Annotated[str, Form()],
    user_password: Annotated[str, Form()],
    db: db_dependecy,
):
    user_password = generate_password_hash(user_password, "pbkdf2:sha256:30", 30)
    new_user = model.user.User(
        name=name, cargo=cargo, username=username, user_password=user_password
    )
    
    db.add(new_user)
    db.commit()
    return JSONResponse(status_code=HTTP_201_CREATED, content="Success")


#!Buscar un usuario por id y mostrar en el formulario
@usr.get("/usr/{user_id}", tags=["busqueda de usuario"], status_code=HTTP_200_OK)
async def buser(user_id:int, db: db_dependecy, request: Request):
    userb = (
        db.query(model.user.User).filter(model.user.User.id == user_id).first()
    )  # Filtramos la busqueda por username

    if userb is None:
        raise admintem.TemplateResponse("404.html", {"request": request})
    return admintem.TemplateResponse("edit.html", {"request": request, "user":userb})


#! Modificar Usuario


@usr.post("/usr/modificar/{id}", tags=["Modificar Usuario"], status_code=HTTP_200_OK)
async def update(id:int,
    name: Annotated[str, Form()],
    cargo: Annotated[str, Form()],
    username: Annotated[str, Form()],
    user_password: Annotated[str, Form()],
    db: db_dependecy, request:Request
):
    user_password = generate_password_hash(user_password, "pbkdf2:sha256:30", 30)
    user_actulizar = (
        db.query(model.user.User)
        .filter(model.user.User.id == id)
        .update(
            {
                "name": name,
                "cargo": cargo,
                "username": username,
                "user_password": user_password,
            }
        )
    )
    db.commit()
    url = usr.url_path_for("admin")
    return RedirectResponse(url=url, status_code=303)


# ? Borrar usuario
@usr.get("/usr/borrar/{id}", tags=["Borrar usuarios"], status_code=HTTP_200_OK)
async def borrar(id:int,db: db_dependecy, request:Request):
    busca = db.query(model.user.User).filter(model.user.User.id == id).first()
    db.delete(busca)
    db.commit()
    url = usr.url_path_for("admin")
    return RedirectResponse(url=url, status_code=303)

# ?Login

@usr.post("/usr/login", tags=["Login"], status_code=HTTP_202_ACCEPTED, response_class=RedirectResponse)
async def login(
    username: Annotated[str, Form()],
    user_password: Annotated[str, Form()],
    db: db_dependecy,
    request: Request,
):  # , db: db_dependecy, request: Request)
    log_s = (
        db.query(model.user.User).filter(model.user.User.username == username).first()
    )

    if log_s != None and username == "admin":
        contra = check_password_hash(log_s.user_password, user_password)
        if contra:
            url = usr.url_path_for("admin")
            return RedirectResponse(url = url, status_code=303)
        else:
            return admintem.TemplateResponse("index.html", {"request": request})
    if log_s != None and username == "DocOlea": 
        contra = check_password_hash(log_s.user_password, user_password)
        if contra:
            return RedirectResponse(url="/doc", status_code=303)
        else:
            return admintem.TemplateResponse("index.html", {"request": request})
    if log_s != None and username == "MFuentes":
        contra = check_password_hash(log_s.user_password, user_password)
        if contra:
            return RedirectResponse(url="/doc", status_code=303)
        else:
            return admintem.TemplateResponse("index.html", {"request": request})
    if log_s != None:
        contra = check_password_hash(log_s.user_password, user_password)
        if contra:
            return RedirectResponse(url="/docnor", status_code=303)
        else:
            return admintem.TemplateResponse("index.html",{"request":request})
