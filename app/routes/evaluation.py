from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.sqlite import get_db
from app.services.llm_service import evaluate_answer
from app.models.speaking_log import SpeakingLog

import logging
logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/")
def evaluate(session_id: int, question: str, answer: str, question_audio_url: str = None, user_audio_url: str = None, db: Session = Depends(get_db)):
    logger.info(f"API: Evaluating answer for session_id={session_id}")
    feedback_text = evaluate_answer(question, answer)
    
    # Save to log
    log = SpeakingLog(
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
