from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

urlddatabase= 'mysql+pymysql://root:sandbeto@localhost:3306/corre'
engine = create_engine(urlddatabase, echo=True)

sesionlocal= sessionmaker(autocommit=False, autoflush=False, blind=engine)

Base = declarative_base()