from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///sales.sql', echo = True)
Base = declarative_base()

class Customers(Base):
   __tablename__ = 'customers'
   id = Column(Integer, primary_key=True)
   name = Column(String)
   address = Column(String)
   email = Column(String)


   def __init__(self, name, email, address):
   		self.name = name 
   def __repr__(self):
   		return f"{self.name}"

Base.metadata.create_all(engine)