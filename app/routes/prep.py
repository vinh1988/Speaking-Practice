from fastapi import APIRouter
from app.services.llm_service import generate_prep_sheet

router = APIRouter()

@router.get("/generate")
def get_prep_sheet(topic: str, skill_type: str = "Speaking"):
    content = generate_prep_sheet(topic, skill_type)
    return {"content": content}
