from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.sqlite import get_db
from app.models.session import Session as SessionModel
from pydantic import BaseModel
from typing import Optional

router = APIRouter()

class SessionCreate(BaseModel):
    topic: str
    context: str
    level: Optional[str] = "Intermediate"
    skill_type: Optional[str] = "Speaking"
    sub_index: Optional[str] = None

@router.post("/")
def create_session(session_data: SessionCreate, db: Session = Depends(get_db)):
    db_session = SessionModel(
        topic=session_data.topic,
        context=session_data.context,
        level=session_data.level,
        skill_type=session_data.skill_type,
        sub_index=session_data.sub_index
    )
    db.add(db_session)
    db.commit()
    db.refresh(db_session)
    return db_session

@router.get("/{session_id}")
def get_session(session_id: int, db: Session = Depends(get_db)):
    db_session = db.query(SessionModel).filter(SessionModel.id == session_id).first()
    if not db_session:
        raise HTTPException(status_code=404, detail="Session not found")
    return db_session
