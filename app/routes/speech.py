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
    # Determine extension based on content type
    ext = ".wav"
    if "webm" in file.content_type:
        ext = ".webm"
    elif "ogg" in file.content_type:
        ext = ".ogg"
    elif "mpeg" in file.content_type:
        ext = ".mp3"
        
    output_filename = f"user_ans_{session_id}_{file_id}{ext}"
    output_path = os.path.join("outputs", output_filename)
    
    with open(output_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # Transcribe using the saved file
    text = transcribe_audio(output_path)
    
    return {
        "text": text, 
        "user_audio_url": f"/outputs/{output_filename}"
    }
