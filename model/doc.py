from datetime import datetime
from sqlalchemy import Integer, String, Column, Text, Date
from config.db import Base


class Doc(Base):
    __tablename__ = "doc"

    id = Column(Integer, primary_key=True, index=True)
    fecha = Column(Date, nullable=False)
    numoficio = Column(String(250), nullable=False)
    asunto = Column(String(250), nullable=False)
    remitente = Column(String(250), nullable=False)
    turn = Column(String(250), nullable=False)
    resp = Column(String(250), nullable=False)
    femi = Column(Date, nullable=False)
    url = Column(Text, nullable=False)
    urlresp = Column(Text, nullable=False)
