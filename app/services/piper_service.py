import os
import uuid
import logging
import asyncio
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

# No config needed for strictly cloud

def text_to_speech(text: str, output_dir: str = "outputs"):
    os.makedirs(output_dir, exist_ok=True)
    filename = f"q_{uuid.uuid4().hex[:8]}.wav"
    filepath = os.path.join(output_dir, filename)
    
    logger.info(f"Generating TTS for: {text[:50]}...")
    
    try:
        import edge_tts
        
        async def generate_edge_tts():
            communicate = edge_tts.Communicate(text, "en-US-AndrewNeural")
            await communicate.save(filepath)
        
        # Use asyncio to run the tts
        asyncio.run(generate_edge_tts())
        
        logger.info(f"Edge-TTS generated successfully at {filepath}")
        return filename, None
    except Exception as e:
        logger.error(f"Edge-TTS Error: {str(e)}")
        return None, f"Error: Edge-TTS failed. Local models are disabled. {str(e)}"
