import requests
import json
import logging

logger = logging.getLogger(__name__)

OLLAMA_URL = "http://localhost:11434/api/generate"

def query_phi3(prompt: str):
    logger.info(f"Querying Phi-3 with prompt: {prompt[:100]}...")
    payload = {
        "model": "phi3",
        "prompt": prompt,
        "stream": False
    }
    
    try:
        response = requests.post(OLLAMA_URL, json=payload, timeout=600)
        response.raise_for_status()
        result = response.json().get("response", "")
        logger.info(f"Received response from Phi-3: {result[:100]}...")
        return result
    except Exception as e:
        logger.error(f"Error connecting to Ollama: {str(e)}")
        return f"Error connecting to Ollama: {str(e)}"

def generate_question(topic: str, context: str, skill_type: str = "Speaking", sub_index: str = None, image_description: str = None):
    prompt = f"You are an IELTS {skill_type} examiner. The topic is '{topic}' and the context is '{context}'."
    if sub_index:
        prompt += f" This is for {sub_index}."
    if image_description:
        prompt += f" The user uploaded an image described as: '{image_description}'."
    
    if skill_type == "Speaking":
        prompt += "\nGenerate one natural IELTS-style speaking question for the user."
    elif skill_type == "Writing":
        prompt += f"\nGenerate an IELTS Writing {sub_index if sub_index else 'Task'} prompt for the user."
    elif skill_type == "Reading":
        prompt += f"\nGenerate a short IELTS-style Reading passage and one multiple choice question based on it."
    elif skill_type == "Listening":
        prompt += f"\nGenerate a short dialogue transcript and one question about what was said."
    
    return query_phi3(prompt)

def evaluate_answer(question: str, user_answer: str, skill_type: str = "Speaking"):
    prompt = f"""
    SYSTEM: You are a MINIMALIST IELTS examiner. Your goal is to be EXTREMELY BRIEF and concise.
    
    Question: {question}
    User Answer: {user_answer}
    
    INSTRUCTIONS:
    1. Provide a ONE-SENTENCE metaphor.
    2. Provide 3 SHORT bullet points for Core Ideas.
    3. Provide ONE SINGLE PARAGRAPH sample answer.
    4. CRITICAL: The sample answer MUST BE UNDER 80 WORDS. IF YOU WRITE MORE, YOU FAIL.
    
    FORMAT:
    ### 🌈 Metaphor
    [One sentence]
    
    ### 💡 Core Ideas
    * [Idea 1]
    * [Idea 2]
    * [Idea 3]
    
    ### 🌟 Concise Sample (Band 9)
    [Exactly 50-80 words. One paragraph only.]
    """
    return query_phi3(prompt)
