from sqlalchemy import Integer, String, Column, Text
from config.db import Base


class Doc(Base):
    __tablename__ = "doc"

    id = Column(Integer, primary_key=True, index=True)
    fecha = Column(String(250), nullable=False)
    numoficio = Column(String(250), nullable=False)
    asunto = Column(String(250), nullable=False)
    remitente = Column(String(250), nullable=False)
    turn = Column(String(250), nullable=False)
    resp = Column(String(250), nullable=False)
    femi = Column(String(250), nullable=False)
    url = Column(Text)
