from sqlalchemy import Boolean, String, Integer, Table, Column, Text
from config.db import Base

class User(Base):
    __tablename__= 'user'
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(250), nullable=False)
    cargo = Column(String(250), nullable=False)
    username = Column(String(50), nullable=False)
    user_password =Column(Text, nullable=False)
    

    
    