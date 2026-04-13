from fastapi import APIRouter, UploadFile, File, Depends
from sqlalchemy.orm import Session
from app.database.sqlite import get_db
from app.services.whisper_service import transcribe_audio
import shutil
import os

router = APIRouter()

import uuid

@router.post("/transcribe")
async def transcribe(session_id: int, file: UploadFile = File(...), db: Session = Depends(get_db)):
    # Save file permanently in outputs for history
    file_id = str(uuid.uuid4())[:8]
    output_filename = f"user_ans_{session_id}_{file_id}.wav"
    output_path = os.path.join("outputs", output_filename)
    
    with open(output_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # Transcribe using the saved file
    text = transcribe_audio(output_path)
    
    return {
        "text": text, 
        "user_audio_url": f"/outputs/{output_filename}"
    }
