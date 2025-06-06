from sqlalchemy import Column, String, Integer, Text, ForeignKey, DateTime, Float
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime


class User(Base):
    __tablename__="users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)

    predictions= relationship("PredictionLog",back_populates="user" )

    # ✅ Prediction logs table
class PredictionLog(Base):
    __tablename__ = "prediction_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    input_data = Column(Text, nullable=False)       # Store raw input as JSON string
    prediction_result = Column(String, nullable=False)
    #confidence = Column(Float, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="predictions")

