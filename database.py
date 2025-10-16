from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, String, Integer, DateTime
from datetime import datetime

Base = declarative_base()

class IbgeData(Base):
    __tablename__ = 'ibge_dados'

    id = Column(Integer, primary_key=True, autoincrement=True)
    country = Column(String(10), nullable=False)
    year = Column(Integer, nullable=False)
    population = Column(Integer, nullable=False)
    timestamp = Column(DateTime, default=datetime.now)


