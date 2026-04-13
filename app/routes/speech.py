from fastapi import APIRouter, UploadFile, File, Depends
from sqlalchemy.orm import Session
from app.database.sqlite import get_db
from app.services.whisper_service import transcribe_audio
import shutil
import os

router = APIRouter()

@router.post("/transcribe")
async def transcribe(session_id: int, file: UploadFile = File(...), db: Session = Depends(get_db)):
    # Save file temporarily
    temp_path = f"temp_{file.filename}"
    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # Transcribe
    text = transcribe_audio(temp_path)
    
    # Cleanup
    os.remove(temp_path)
    
    return {"text": text}
