from fastapi import APIRouter, Form, HTTPException, Depends, Request
from sqlalchemy.orm import Session
import model
from schemas.doc_Schema import Doc_Schema, Id_Doc, CrearDoc
from starlette.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_404_NOT_FOUND, HTTP_202_ACCEPTED
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from config.db import engine, Base, Sessionlocal
from fastapi.templating import Jinja2Templates
from typing import Annotated
import crud

doct = APIRouter()
doctem = Jinja2Templates(directory="templates")

def get_db():
    db = Sessionlocal()
    try:
        yield db #Generador para iterar los datos de la base
    finally:
        db.close()

db_dependecy  = Annotated[Session, Depends(get_db)]

@doct.get("/doc", tags=["Bienvenida"], status_code=HTTP_200_OK)
async def doc(request:Request, db:db_dependecy):
    docs = db.query(model.doc.Doc).order_by(model.doc.Doc.id.desc())
    return doctem.TemplateResponse("docs.html", {"request":request})


@doct.post("/doc/crear", tags=["Crear Documento"], status_code=HTTP_201_CREATED, response_model=Id_Doc)
async def created(doc:CrearDoc, db:db_dependecy):
    return crud.crearD(db=db, doc=doc)

@doct.get("/doc/bfecha", tags=["Busca por Fecha"], status_code=HTTP_200_OK)
async def bfecha(fechadoc:str, db: db_dependecy):
    bf = db.query(model.doc.Doc).filter(model.doc.Doc.fecha == fechadoc).all()
    if bf is None:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="No existe el documento")
    return bf

@doct.get("/doc/boficio", tags=["Busqueda Oficio"], status_code=HTTP_200_OK)
async def boficio(nofi:str, db:db_dependecy):
    bo = db.query(model.doc.Doc).filter(model.doc.Doc.numoficio == nofi).first()
    if bo is None:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="No existe el documento")
    return bo
@doct.put("/doc/actualizar", tags=["Actualizar Documento"], status_code=HTTP_202_ACCEPTED)
async def acdoc(num_oficio:str,doc_ac:Doc_Schema, db:db_dependecy):
    docact=db.query(model.doc.Doc).filter(model.doc.Doc.numoficio == num_oficio).update({"numoficio":doc_ac.numoficio,"asunto":doc_ac.asunto, "remitente":doc_ac.remitente, "turn":doc_ac.turn, "resp":doc_ac.resp, "femi":doc_ac.femi, "url":doc_ac.url})
    if docact is None:
        raise HTTPException(HTTP_404_NOT_FOUND, detail="Documento no encontrado")
    return docact
