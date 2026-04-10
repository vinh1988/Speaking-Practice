from sqlalchemy import Column, Integer, String, DateTime
from app.database.sqlite import Base
import datetime

class Session(Base):
    __tablename__ = "sessions"

    id = Column(Integer, primary_key=True, index=True)
    topic = Column(String)
    context = Column(String)
    image_path = Column(String, nullable=True)
    level = Column(String, default="Intermediate")
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
