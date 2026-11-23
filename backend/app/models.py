from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.sql import func
from .database import Base

class Prediction(Base):
    __tablename__ = "predictions"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String(255), nullable=False)
    category = Column(String(50), nullable=False)
    confidence = Column(Float, nullable=False)
    disposal_advice = Column(String(1000), nullable=False)
    impact_estimate = Column(String(1000), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
