import requests
import json

OLLAMA_URL = "http://localhost:11434/api/generate"

def query_phi3(prompt: str):
    payload = {
        "model": "phi3",
        "prompt": prompt,
        "stream": False
    }
    
    try:
        response = requests.post(OLLAMA_URL, json=payload)
        response.raise_for_status()
        return response.json().get("response", "")
    except Exception as e:
        return f"Error connecting to Ollama: {str(e)}"

def generate_question(topic: str, context: str, image_description: str = None):
    prompt = f"You are an IELTS speaking coach. The topic is '{topic}' and the context is '{context}'."
    if image_description:
        prompt += f" The user uploaded an image described as: '{image_description}'."
    
    prompt += "\nGenerate one natural IELTS-style speaking question for the user."
    
    return query_phi3(prompt)

def evaluate_answer(question: str, user_answer: str):
    prompt = f"""
    You are an IELTS examiner. 
    Question: {question}
    User Answer: {user_answer}
    
    Evaluate the answer based on:
    1. Grammar (1-9)
    2. Fluency (1-9)
    3. Vocabulary (1-9)
    
    Provide scores and a brief feedback with corrections. 
    Format:
    Grammar: [score]
    Fluency: [score]
    Vocabulary: [score]
    Feedback: [text]
    """
    return query_phi3(prompt)
