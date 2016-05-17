import os.path

from flask import url_for
from sqlalchemy import Column, Integer, String, Sequence, ForeignKey
from sqlalchemy.orm import relationship

from tuneful import app
from .database import Base, engine

class Tikcers(Base):
    # Stores tickers of stocks to include in DB using Google Finance format
    __tablename__ = "tickers"

    id = Column(Integer, primary_key=True)
    ticker = Column(String(128))