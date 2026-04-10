from fastapi import APIRouter, UploadFile, File, Depends
from sqlalchemy.orm import Session
from app.database.sqlite import get_db
from app.services.blip_service import describe_image
import shutil
import os

router = APIRouter()

@router.post("/describe")
async def describe(session_id: int, file: UploadFile = File(...), db: Session = Depends(get_db)):
    # Save image
    upload_dir = "uploads"
    os.makedirs(upload_dir, exist_ok=True)
    file_path = os.path.join(upload_dir, file.filename)
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # Generate description
    description = describe_image(file_path)
    
    return {"description": description, "image_path": file_path}
