from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from app.database.sqlite import Base
import datetime

class SpeakingLog(Base):
    __tablename__ = "speaking_logs"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("sessions.id"))
    question = Column(String)
    answer = Column(String, nullable=True)
    grammar_score = Column(Float, nullable=True)
    fluency_score = Column(Float, nullable=True)
    vocab_score = Column(Float, nullable=True)
    pronunciation_score = Column(Float, nullable=True)
    feedback = Column(String, nullable=True)
    next_question = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
