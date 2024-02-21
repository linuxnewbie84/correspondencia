from fastapi import APIRouter, Form, HTTPException, Depends, Request
from sqlalchemy.orm import Session
import model
from schemas.doc_Schema import Doc_Schema, Id_Doc, CrearDoc
from starlette.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_404_NOT_FOUND, HTTP_202_ACCEPTED
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from config.db import engine, Base, Sessionlocal
from fastapi.templating import Jinja2Templates
from typing import Annotated
from datetime import date
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
    documents = db.query(model.doc.Doc).order_by(model.doc.Doc.id.desc())
    return doctem.TemplateResponse("docs.html", {"request":request, "documents":documents})

@doct.get("/docnor", tags=["Documentos Turnados"], status_code=200)
async def tunados(request:Request, db:db_dependecy):
    turnados= db.query(model.doc.Doc).order_by(model.doc.Doc.id. desc())
    return doctem.TemplateResponse("turn.html",{"request":request, "turnados":turnados})

#! Crear Documento


@doct.post("/doc/create/", tags=["Crear Documento"], status_code=HTTP_201_CREATED)
async def creadoc(
    fecha: Annotated[date, Form()],
    numoficio: Annotated[str, Form()],
    asunto: Annotated[str, Form()],
    remitente: Annotated[str, Form()],
    turn: Annotated[str, Form()],
    resp: Annotated[str, Form()],
    femi: Annotated[date, Form()],
    url: Annotated[str, Form()],
    urlresp: Annotated[str, Form()],
    db: db_dependecy,
):
    new_doc = model.doc.Doc(fecha = fecha, numoficio = numoficio, 
                             asunto = asunto, remitente = remitente, turn=turn, 
                             resp=resp, femi=femi, url=url, urlresp=urlresp)
    db.add(new_doc)
    db.commit()
    return JSONResponse(status_code=HTTP_201_CREATED, content="Success")


# ? Buscar por id para devolver a formulario


@doct.get("/doc/{doc_id}", tags=["Buscar id"], response_class=HTTP_200_OK)
async def docid(doc_id:int, db:db_dependecy, request:Request):
    search = db.query(model.doc.Doc).filter(model.doc.Doc.id == doc_id).first()
    if search:
        return doctem.TemplateResponse(
            "editdoc.html", {"request": request, "search": search}
        )
@doct.post("/doc/update/{doc_id}", tags=["Modificar Documento"], response_class=HTTP_202_ACCEPTED)
async def modificar(
    doc_id: int,
    db: db_dependecy,
    fecha: Annotated[date, Form()],
    numoficio: Annotated[str, Form()],
    asunto: Annotated[str, Form()],
    remitente: Annotated[str, Form()],
    turn:Annotated[str, Form()],
    resp:Annotated[str,Form()],
    femi:Annotated[date, Form()],
    url:Annotated[str, Form()],
    urlresp:Annotated[str, Form()],
    request: Request,
):
    doc_act = db.query(model.doc.Doc).filter(model.doc.Doc.id == doc_id).update({
        "fecha" : fecha, 
        "numoficio" : numoficio,
        "asunto" :asunto, 
        "remitente" : remitente,
        "turn": turn,
        "resp": resp,
        "femi": femi,
        "url": url,
        "urlresp":urlresp
    })
    if doc_act:
        db.commit()
        path = doct.url_path_for("doc")
        return RedirectResponse(url = path, status_code=303)

#?Borrar Documentos    

@doct.get("/doc/borrar/{id_doc}", tags=["Borrar Documento"], status_code=HTTP_200_OK)
async def borrar(id_doc:int, db:db_dependecy, request:Request):
    buscar = db.query(model.doc.Doc).filter(model.doc.Doc.id == id_doc).first()
    db.delete(buscar)
    db.commit()
    url= doct.url_path_for("doc")
    return RedirectResponse(url = url, status_code=303)