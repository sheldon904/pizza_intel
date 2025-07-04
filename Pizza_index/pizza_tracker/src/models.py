# pizza_tracker/src/models.py

from sqlalchemy import Column, Integer, String, DateTime, Float
from .database import Base

class ScrapeData(Base):
    __tablename__ = "scrape_data"

    id = Column(Integer, primary_key=True, index=True)
    place = Column(String, index=True)
    url = Column(String)
    scrape_time = Column(DateTime)
    day_of_week = Column(String)
    hour_of_day = Column(Integer)
    popularity_percent_normal = Column(Float)
    popularity_percent_current = Column(Float, nullable=True)
