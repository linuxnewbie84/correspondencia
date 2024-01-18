from pydantic import BaseModel, Field
from typing import Optional


class Doc_Schema(BaseModel):
    id: Optional[int] = None
    fecha:str = Field(min_lenght=10,max_length=10)
    numoficio:str = Field(max_length=50, min_length=10)
    asunto:str = Field(max_length=50)
    remitente: str = Field(max_length=50, min_length=10)
    turn:str= Field(min_length=10, max_length=150)
    resp:str =Field(min_length=10, max_length=50)
    femi:str= Field(min_length=10, max_length=10) 
    url:str
