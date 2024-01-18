from pydantic import BaseModel, Field
from typing import Optional
from werkzeug.security import generate_password_hash, check_password_hash


class UserSchema(BaseModel):
    id: Optional[int] = None
    name: str = Field(
        min_length=8,
        max_length=250,
    )
    cargo: str = Field(min_length=8, max_length=250)
    username: str = Field(min_length=8, max_length=50)
    user_password:str
#*Función para hasshear el password
    def set_password(self,password):
        self.user_password = generate_password_hash(password,"pbkdf2:sha256:30", 30)


class Datalogin(BaseModel):
    username: str = Field(min_length=8, max_length=50)
    password: str = Field(min_length=8, max_length=50)
