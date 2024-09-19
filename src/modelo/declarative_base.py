from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
#from sqlalchemy.orm import declarative_base

engine = create_engine('sqlite:///aplicacion.sqlite')
Session = sessionmaker(bind=engine)

Base = declarative_base()
session = Session()