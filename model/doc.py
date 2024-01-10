from sqlalchemy import Integer, String, Column, Date
from config.db import  Base

class Doc(Base):
    __tablename__ = 'doc'
    
    id = Column(Integer, primary_key=True, index= True)
    numoficio = Column(String(250), nullable=True)
    proce = Column(String(250), nullable=True)
    asunto = Column(String(250))
    fecha = Column(Date, nullable=True)
    turn = Column(String(250))
    