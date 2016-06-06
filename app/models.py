from sqlalchemy import Column, Integer, Float, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Prices(Base):
    __tablename__ = "prices"
    
    id = Column(Integer, primary_key = True)
    date = Column(String, primary_key = True)
    price = Column(Float)