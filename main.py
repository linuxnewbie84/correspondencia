import uvicorn
import os
from fastapi import FastAPI
from router import usuarios
from fastapi import Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from model import user, doc
from config.db import engine, Base
from router.usuarios import usr
from router.doc import doct

app = FastAPI()
app.title="Servicio de Correspondencia"
app.version = "1.0"
app.include_router(usr)
app.include_router(doct)
#app.include_router(doc)
template= Jinja2Templates(directory="templates")

user.Base.metadata.create_all(bind = engine) #!Creamos las tablas desde los modelos 
doc.Base.metadata.create_all(bind = engine)#?Creamos la tabla doc

@app.get("/", tags=["Bienvenidos"], response_class=HTMLResponse)
async def home(request:Request):
    return template.TemplateResponse("index.html",{"request":request})