from transformers import BlipProcessor, BlipForConditionalGeneration
from PIL import Image
import torch

# Load model
processor = None
model = None

def get_model():
    global processor, model
    if model is None:
        processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
        model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")
    return processor, model

def describe_image(image_path: str):
    proc, mdl = get_model()
    raw_image = Image.open(image_path).convert('RGB')

    # Unconditional image captioning
    inputs = proc(raw_image, return_tensors="pt")
    out = mdl.generate(**inputs)
    description = proc.decode(out[0], skip_special_tokens=True)
    
    return description
