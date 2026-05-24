import os
import logging
from PIL import Image
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

def describe_image(image_path: str):
    if GOOGLE_API_KEY:
        try:
            import google.generativeai as genai
            genai.configure(api_key=GOOGLE_API_KEY)
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            img = Image.open(image_path)
            response = model.generate_content([
                "Describe this image for an IELTS speaking task. Provide a clear and detailed description.",
                img
            ])
            return response.text
        except Exception as e:
            logger.error(f"Gemini Vision Error: {str(e)}")
    
    return "Error: Gemini Vision API not configured or failed. Local models are disabled."
