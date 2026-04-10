import subprocess
import os
import uuid
import logging

logger = logging.getLogger(__name__)

def text_to_speech(text: str, output_dir: str = "outputs"):
    os.makedirs(output_dir, exist_ok=True)
    filename = f"q_{uuid.uuid4().hex[:8]}.wav"
    filepath = os.path.join(output_dir, filename)
    
    logger.info(f"Generating TTS for: {text[:50]}...")
    
    # Path to piper model - adjust this to where user downloads models
    model_path = "models/piper/en_US-lessac-medium.onnx"
    
    if not os.path.exists(model_path):
        logger.warning(f"Piper model not found at {model_path}. Skipping TTS generation.")
        return None, f"Piper model not found. Please download it to {model_path}"

    try:
        # Get absolute path to piper in venv
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        piper_bin = os.path.join(base_dir, "venv/bin/piper")
        
        logger.info(f"Running Piper command ({piper_bin}) for file: {filepath}")
        
        # Proper way to pipe in python
        process = subprocess.Popen(
            [piper_bin, '--model', model_path, '--output_file', filepath],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        stdout, stderr = process.communicate(input=text)
        
        if process.returncode != 0:
            logger.error(f"Piper Error: {stderr}")
            return None, stderr
            
        logger.info(f"TTS generated successfully at {filepath}")
        return filename, None
    except Exception as e:
        logger.error(f"Exception in Piper service: {str(e)}")
        return None, str(e)
