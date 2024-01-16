from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

urlddatabase= 'mysql+pymysql://root:sandbeto@localhost:3306/correspondencia'
engine = create_engine(urlddatabase, echo=True)

Sessionlocal= sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()   