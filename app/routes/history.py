from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.sqlite import get_db
from app.models.speaking_log import PracticeLog
from app.models.session import Session as SessionModel
from typing import List

router = APIRouter()

@router.get("/")
def get_history(db: Session = Depends(get_db)):
    # Join PracticeLog with Session to get topic, level, skill_type, etc.
    results = db.query(
        PracticeLog.id,
        PracticeLog.question,
        PracticeLog.answer,
        PracticeLog.feedback,
        PracticeLog.question_audio_url,
        PracticeLog.user_audio_url,
        PracticeLog.grammar_score,
        PracticeLog.fluency_score,
        PracticeLog.vocab_score,
        PracticeLog.pronunciation_score,
        PracticeLog.task_response_score,
        PracticeLog.cohesion_score,
        PracticeLog.total_correct,
        PracticeLog.total_questions,
        PracticeLog.band_score,
        PracticeLog.created_at.label("log_date"),
        SessionModel.topic,
        SessionModel.level,
        SessionModel.skill_type,
        SessionModel.sub_index
    ).join(SessionModel, PracticeLog.session_id == SessionModel.id).order_by(PracticeLog.created_at.desc()).all()
    
    # Structure the response to include classification info
    history_items = []
    for r in results:
        history_items.append({
            "id": r.id,
            "question": r.question,
            "answer": r.answer,
            "feedback": r.feedback,
            "question_audio_url": r.question_audio_url,
            "user_audio_url": r.user_audio_url,
            "scores": {
                "grammar": r.grammar_score,
                "fluency": r.fluency_score,
                "vocab": r.vocab_score,
                "pronunciation": r.pronunciation_score,
                "task_response": r.task_response_score,
                "cohesion": r.cohesion_score,
                "total_correct": r.total_correct,
                "total_questions": r.total_questions,
                "band_score": r.band_score
            },
            "date": r.log_date.isoformat() if r.log_date else None,
            "topic": r.topic,
            "level": r.level,
            "skill_type": r.skill_type,
            "sub_index": r.sub_index
        })
    
    return history_items

@router.delete("/{log_id}")
def delete_history_item(log_id: int, db: Session = Depends(get_db)):
    db_log = db.query(PracticeLog).filter(PracticeLog.id == log_id).first()
    if not db_log:
        return {"error": "Log not found"}
    db.delete(db_log)
    db.commit()
    return {"message": "Log deleted successfully"}
