from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.sqlite import get_db
from app.services.llm_service import generate_question
from app.services.piper_service import text_to_speech
from app.models.session import Session as SessionModel

import logging
logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/generate")
def get_new_question(session_id: int, image_description: str = None, db: Session = Depends(get_db)):
    logger.info(f"API: Generating question for session_id={session_id}")
    db_session = db.query(SessionModel).filter(SessionModel.id == session_id).first()
    if not db_session:
        return {"error": "Session not found"}
    
    raw_response = generate_question(db_session.topic, db_session.context, db_session.skill_type, db_session.sub_index, image_description)
    
    # Parse the response
    question = raw_response
    prep_data = ""
    
    if "### QUESTION" in raw_response and "### KNOWLEDGE BANK" in raw_response:
        parts = raw_response.split("### KNOWLEDGE BANK")
        prep_data = parts[1].strip()
        question = parts[0].replace("### QUESTION", "").strip()
    
    # Generate TTS only for the question text
    audio_file, error = text_to_speech(question)
    audio_url = f"/outputs/{audio_file}" if audio_file else None
    
    return {
        "question": question,
        "prep_data": prep_data,
        "audio_url": audio_url,
        "tts_error": error
    }
