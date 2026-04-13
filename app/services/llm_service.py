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

def generate_question(topic: str, context: str, image_description: str = None):
    prompt = f"You are an IELTS speaking coach. The topic is '{topic}' and the context is '{context}'."
    if image_description:
        prompt += f" The user uploaded an image described as: '{image_description}'."
    
    prompt += "\nGenerate one natural IELTS-style speaking question for the user."
    
    return query_phi3(prompt)

def evaluate_answer(question: str, user_answer: str):
    prompt = f"""
    You are an expert IELTS examiner. 
    Question: {question}
    User Answer: {user_answer}
    
    Tasks:
    1. Evaluate the answer for Grammar, Fluency, and Vocabulary (Scores 1-9).
    2. Provide detailed feedback on strengths and weaknesses.
    3. PROPOSE A STANDARD HIGH-SCORING SAMPLE ANSWER (Band 8 or 9) that captures the user's original intent but uses much better vocabulary, varied grammatical structures, and vivid descriptions to guide the student.

    Format your response EXACTLY like this:
    Grammar: [score]
    Fluency: [score]
    Vocabulary: [score]
    
    Feedback: [Your analysis]
    
    ---
    ### 🌟 Improved Sample Answer (Band 8-9):
    [Provide the high-quality sample version of the user's answer here]
    """
    return query_phi3(prompt)
