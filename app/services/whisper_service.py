from faster_whisper import WhisperModel
import os
import logging

logger = logging.getLogger(__name__)

# Initialize model (can be loaded once)
model_size = "base"
# In a real app, you might want to load this globally or on demand
model = None

def get_model():
    global model
    if model is None:
        logger.info(f"Loading Whisper model '{model_size}' on CPU...")
        # Use CPU for this architecture
        model = WhisperModel(model_size, device="cpu", compute_type="int8")
        logger.info("Whisper model loaded successfully.")
    return model

def transcribe_audio(audio_path: str):
    logger.info(f"Transcribing audio file: {audio_path}")
    whisper_model = get_model()
    segments, info = whisper_model.transcribe(audio_path, beam_size=5)
    
    text = ""
    for segment in segments:
        text += segment.text + " "
    
    result = text.strip()
    logger.info(f"Transcription complete: {result[:50]}...")
    return result
