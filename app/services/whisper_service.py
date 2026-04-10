from faster_whisper import WhisperModel
import os

# Initialize model (can be loaded once)
model_size = "base"
# In a real app, you might want to load this globally or on demand
model = None

def get_model():
    global model
    if model is None:
        # Use CPU for this architecture
        model = WhisperModel(model_size, device="cpu", compute_type="int8")
    return model

def transcribe_audio(audio_path: str):
    whisper_model = get_model()
    segments, info = whisper_model.transcribe(audio_path, beam_size=5)
    
    text = ""
    for segment in segments:
        text += segment.text + " "
    
    return text.strip()
