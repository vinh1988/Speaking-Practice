import os
import logging
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

def transcribe_audio(audio_path: str):
    logger.info(f"Transcribing audio file: {audio_path}")
    
    if GROQ_API_KEY:
        try:
            from groq import Groq
            client = Groq(api_key=GROQ_API_KEY)
            with open(audio_path, "rb") as file:
                transcription = client.audio.transcriptions.create(
                    file=(os.path.basename(audio_path), file.read()),
                    model="whisper-large-v3",
                    response_format="text",
                )
            logger.info("Transcription complete via Groq.")
            return transcription
        except Exception as e:
            logger.error(f"Groq Whisper Error: {str(e)}")
            return f"Error: Groq Whisper API failed. {str(e)}"
    
    return "Error: Groq API Key not configured. Local models are disabled."
