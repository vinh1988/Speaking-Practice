from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.sqlite import get_db
from app.models.speaking_log import SpeakingLog
from app.models.session import Session as SessionModel
from typing import List

router = APIRouter()

@router.get("/")
def get_history(db: Session = Depends(get_db)):
    # Join SpeakingLog with Session to get topic, level, etc.
    results = db.query(
        SpeakingLog.id,
        SpeakingLog.question,
        SpeakingLog.answer,
        SpeakingLog.feedback,
        SpeakingLog.question_audio_url,
        SpeakingLog.user_audio_url,
        SpeakingLog.created_at.label("log_date"),
        SessionModel.topic,
        SessionModel.level
    ).join(SessionModel, SpeakingLog.session_id == SessionModel.id).order_by(SpeakingLog.created_at.desc()).all()
    
    return [
        {
            "id": r.id,
            "question": r.question,
            "answer": r.answer,
            "feedback": r.feedback,
            "question_audio_url": r.question_audio_url,
            "user_audio_url": r.user_audio_url,
            "date": r.log_date.isoformat() if r.log_date else None,
            "topic": r.topic,
            "level": r.level
        } for r in results
    ]

@router.delete("/{log_id}")
def delete_history_item(log_id: int, db: Session = Depends(get_db)):
    db_log = db.query(SpeakingLog).filter(SpeakingLog.id == log_id).first()
    if not db_log:
        return {"error": "Log not found"}
    db.delete(db_log)
    db.commit()
    return {"message": "Log deleted successfully"}
