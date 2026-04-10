from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.sqlite import get_db
from app.services.llm_service import generate_question
from app.models.session import Session as SessionModel

router = APIRouter()

@router.post("/generate")
def get_new_question(session_id: int, image_description: str = None, db: Session = Depends(get_db)):
    db_session = db.query(SessionModel).filter(SessionModel.id == session_id).first()
    if not db_session:
        return {"error": "Session not found"}
    
    question = generate_question(db_session.topic, db_session.context, image_description)
    return {"question": question}
