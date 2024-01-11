import uvicorn
import os
from fastapi import FastAPI, Depends, HTTPException, status
from router import usuarios
from fastapi import Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

app = FastAPI()
app.title("Servicio de Correspondencia")

template= Jinja2Templates(directory="templates")

@app.get("/", tags=["Bienvenidos"], response_class=HTMLResponse)
async def home(request:Request):
    return template.TemplateResponse("index.html",{"request":request})