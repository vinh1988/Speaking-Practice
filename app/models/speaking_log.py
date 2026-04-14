from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from app.database.sqlite import Base
import datetime

class PracticeLog(Base):
    __tablename__ = "speaking_logs" # Keeping name for compatibility, but it acts as a general PracticeLog now

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("sessions.id"))
    question = Column(String)
    answer = Column(String, nullable=True)
    
    # Speaking specific
    user_audio_url = Column(String, nullable=True)
    fluency_score = Column(Float, nullable=True)
    pronunciation_score = Column(Float, nullable=True)
    
    # Generic / Writing / Speaking
    grammar_score = Column(Float, nullable=True)
    vocab_score = Column(Float, nullable=True)
    
    # Writing specific
    task_response_score = Column(Float, nullable=True)
    cohesion_score = Column(Float, nullable=True)
    
    # Listening / Reading specific
    total_correct = Column(Integer, nullable=True)
    total_questions = Column(Integer, nullable=True)
    band_score = Column(Float, nullable=True)
    
    feedback = Column(String, nullable=True)
    question_audio_url = Column(String, nullable=True)
    next_question = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
