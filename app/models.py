from sqlalchemy import Column, Integer, Float, DateTime
from sqlalchemy.sql import func
from .database import Base

class Roll(Base):
    __tablename__ = "rolls"

    id = Column(Integer, primary_key=True, index=True)
    length = Column(Float, nullable=False)
    weight = Column(Float, nullable=False)
    date_added = Column(DateTime(timezone=True), server_default=func.now())
    date_removed = Column(DateTime(timezone=True), nullable=True)
