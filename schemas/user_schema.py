from pydantic import BaseModel, Field
from typing import Optional

class UserSchema(BaseModel):
    id:Optional[int] = None
    name:str = Field(min_length=8, max_length=250,)
    cargo:str = Field(min_length=8, max_length=250)
    username:str=Field(min_length=8, max_length=50)
    password:str = Field(min_length=8, max_length=50)
    
class Datalogin(BaseModel):
    username:str = Field(min_length=8, max_length=50)
    password:str = Field(min_length=8, max_length=50)