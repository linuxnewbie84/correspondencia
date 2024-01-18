from fastapi import APIRouter, Request, Form, Depends, HTTPException, Response
from schemas.user_schema import UserSchema, Datalogin
from starlette.status import (
    HTTP_201_CREATED,
    HTTP_200_OK,
    HTTP_202_ACCEPTED,
    HTTP_401_UNAUTHORIZED,
    HTTP_404_NOT_FOUND,
)
import model
from config.db import engine, Sessionlocal
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from typing import Annotated
from werkzeug.security import generate_password_hash, check_password_hash


usr = APIRouter()

admintem = Jinja2Templates(directory="templates")

#Acceso a la base de datos
def get_db():
    db = Sessionlocal()
    try:
        yield db #Generador para iterar los datos de la base
    finally:
        db.close()


db_dependecy = Annotated[Session, Depends(get_db)]  # Necesaria para todas las consultas


#!Bienvenida
@usr.get(
    "/user",
    tags=["Administración de Usuarios"],
    status_code=HTTP_200_OK,
    response_class=HTMLResponse,
)
async def admin(request: Request):
    return admintem.TemplateResponse("admin.html", {"request": request})


#!Crear usuarios
@usr.post(
    "/user",
    tags=["Crear Usuario"],
    status_code=HTTP_201_CREATED,
)
async def Create(user_data: UserSchema, db: db_dependecy):
    user_data.set_password(user_data.user_password) #Hasheamos el password antes de guardar
    new_user = model.user.User(**user_data.model_dump()) #Creamos un directorio
    db.add(new_user)#Agregamos a la base en la tabla usuarios
    db.commit()
    return Response(status_code=HTTP_201_CREATED)


#!Buscar un usuario por username
@usr.get("/user/buser", tags=["busqueda de usuario"], status_code=HTTP_200_OK)
async def buser(user_name: str, db: db_dependecy):
    userb = db.query(model.user.User).filter(model.user.User.username == user_name).first() #Filtramos la busqueda por username
    
    if userb is None:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND, detail="Usuario no encontrado"
        )
    return userb


#! Mostrar usuarios
@usr.get("/user/todos", tags=["Mostrar usuarios"], status_code=HTTP_200_OK)
async def mostrar(db: db_dependecy):
    todos = db.query(model.user.User).all()
    if todos is None:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND, detail="No hay Usuarios que mostrar"
        )
    return todos


#! Modificar Usuario


@usr.put("/user/modificar", tags=["Modificar Usuario"], status_code=HTTP_200_OK)
async def update(user_name: str, datos_actualizar: UserSchema, db: db_dependecy):
    datos_actualizar.set_password(datos_actualizar.user_password)
    act = db.query(model.user.User).filter(model.user.User.username ==user_name).update({"name":datos_actualizar.name, "cargo":datos_actualizar.cargo, "user_password":datos_actualizar.user_password})

    if act is None:
        raise HTTPException(HTTP_404_NOT_FOUND, detail="No hay usuario por actualizar")
    db.commit()


# ? Borrar usuario
@usr.delete("/usr/borrar", tags=["Borrar usuarios"], status_code=HTTP_200_OK)
async def borrar(user_name: str, db: db_dependecy):
    busca = (
        db.query(model.user.User).filter(model.user.User.username == user_name).first()
    )
    if busca is None:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND, detail="No Existe el usuario"
        )
    db.delete(busca)
    db.commit()
    return Response(status_code=HTTP_200_OK)
