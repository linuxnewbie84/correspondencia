import uvicorn
import os
from fastapi import FastAPI
from router import usuarios
from fastapi import Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from model import user, doc
from config.db import Sessionlocal, engine, Base
from router import user, doc


app = FastAPI()
app.title="Servicio de Correspondencia"
app.version = "1.0"
app.include_router(user)
app.include_router(doc)
template= Jinja2Templates(directory="templates")

user.Base.metadata.create_all(bind = engine) #!Creamos las tablas desde los modelos 
doc.Base.metadata.create_all(bind = engine)#?Creamos la tabla doc

def get_db():
    db = Sessionlocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/", tags=["Bienvenidos"], response_class=HTMLResponse)
async def home(request:Request):
    return template.TemplateResponse("index.html",{"request":request})