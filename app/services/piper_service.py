import subprocess
import os
import uuid

def text_to_speech(text: str, output_dir: str = "outputs"):
    os.makedirs(output_dir, exist_ok=True)
    filename = f"{uuid.uuid4()}.wav"
    filepath = os.path.join(output_dir, filename)
    
    # Example piper command: echo "hello" | piper --model voice.onnx --output_file out.wav
    # Assuming piper is in the PATH and model is downloaded
    model_path = "models/piper/en_US-lessac-medium.onnx" # Placeholder path
    
    if not os.path.exists(model_path):
        return None, "Piper model not found. Please download it to models/piper/"

    try:
        command = f'echo "{text}" | piper --model {model_path} --output_file {filepath}'
        subprocess.run(command, shell=True, check=True)
        return filepath, None
    except Exception as e:
        return None, str(e)
