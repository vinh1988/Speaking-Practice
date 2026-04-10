from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.sqlite import get_db
from app.services.llm_service import generate_question
from app.services.piper_service import text_to_speech
from app.models.session import Session as SessionModel

router = APIRouter()

@router.post("/generate")
def get_new_question(session_id: int, image_description: str = None, db: Session = Depends(get_db)):
    db_session = db.query(SessionModel).filter(SessionModel.id == session_id).first()
    if not db_session:
        return {"error": "Session not found"}
    
    question = generate_question(db_session.topic, db_session.context, image_description)
    
    # Generate TTS
    audio_file, error = text_to_speech(question)
    audio_url = f"/outputs/{audio_file}" if audio_file else None
    
    return {
        "question": question,
        "audio_url": audio_url,
        "tts_error": error
    }
