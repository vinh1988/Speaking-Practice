from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.sqlite import get_db
from app.services.llm_service import evaluate_answer
from app.models.speaking_log import PracticeLog
from app.models.session import Session as SessionModel

import logging
logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/")
def evaluate(session_id: int, question: str, answer: str, question_audio_url: str = None, user_audio_url: str = None, db: Session = Depends(get_db)):
    logger.info(f"API: Evaluating answer for session_id={session_id}")
    
    db_session = db.query(SessionModel).filter(SessionModel.id == session_id).first()
    skill_type = db_session.skill_type if db_session else "Speaking"
    
    feedback_text = evaluate_answer(question, answer, skill_type=skill_type)
    
    # Save to log
    log = PracticeLog(
        session_id=session_id,
        question=question,
        answer=answer,
        feedback=feedback_text,
        question_audio_url=question_audio_url,
        user_audio_url=user_audio_url
    )
    db.add(log)
    db.commit()
    
    return {"feedback": feedback_text}
