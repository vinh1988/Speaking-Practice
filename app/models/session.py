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
    skill_type = Column(String, default="Speaking") # Speaking, Writing, Listening, Reading
    sub_index = Column(String, nullable=True) # Part 1, Task 1, Section 1, etc.
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
