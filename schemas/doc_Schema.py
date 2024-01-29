from pydantic import BaseModel, Field
from typing import Optional
from datetime import date


class Doc_Schema(BaseModel):
    fecha: date 
    numoficio: str = Field(max_length=50, min_length=10)
    asunto: str = Field(max_length=50)
    remitente: str = Field(max_length=50, min_length=10)
    turn: str = Field(min_length=10, max_length=150)
    resp: str = Field(min_length=10, max_length=50)
    femi: date
    url: str
    urlresp:str

class CrearDoc(Doc_Schema):
    pass

class Id_Doc(Doc_Schema):
    id: int