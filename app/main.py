from fastapi import FastAPI
import logging
from app.database.sqlite import engine, Base
from app.models import session, speaking_log
from app.routes import session as session_router
from app.routes import speech as speech_router
from app.routes import image as image_router
from app.routes import question as question_router
from app.routes import evaluation as evaluation_router

from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Multimodal AI Speaking Coach")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ensure outputs directory exists
os.makedirs("outputs", exist_ok=True)
app.mount("/outputs", StaticFiles(directory="outputs"), name="outputs")

# Include routers
app.include_router(session_router.router, prefix="/session", tags=["Session"])
app.include_router(speech_router.router, prefix="/audio", tags=["Audio"])
app.include_router(image_router.router, prefix="/image", tags=["Image"])
app.include_router(question_router.router, prefix="/question", tags=["Question"])
app.include_router(evaluation_router.router, prefix="/evaluate", tags=["Evaluation"])

@app.get("/")
async def root():
    return {"message": "Welcome to the Speaking Coach API"}
