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
    You are an expert IELTS examiner. Analyze the student's response and provide constructive feedback to help them expand their imagination and vocabulary using the 5W1H framework.
    
    Question: {question}
    User Answer: {user_answer}
    
    INSTRUCTIONS:
    1. 🧠 Expansion Strategy (5W1H): Suggest specific details the student could add involving Who, What, When, Where, Why, and How to make their story more vivid.
    2. 🌟 Model Answer (Band 7): Provide a natural, clear response targeting IELTS Band 7. It should be realistic, using good grammar and vocabulary without being overly complex. Aim for 80-120 words.
    3. 💎 Vocabulary Boost: Identify 3-5 useful collocations or phrases from your model answer.

    FORMAT:
    ### 🧠 Expansion Strategy (5W1H)
    * **Who & What**: [Guidance]
    * **When & Where**: [Guidance]
    * **Why & How**: [Guidance on emotions and process]
    
    ### 🌟 Model Band 7 Answer
    [Write the model answer here]
    
    ### 💎 Vocabulary Boost
    * **[Term]**: [Brief explanation]
    """
    return query_phi3(prompt)
def generate_prep_sheet(topic: str, skill_type: str = "Speaking"):
    prompt = f"""
    You are an IELTS tutor. Create a high-quality Preparation Sheet for the topic: '{topic}' and skill: '{skill_type}'.
    
    The goal is to help a student get familiar with the topic and boost their fluency before they start a practice session.
    
    Structure your response carefully:
    1. 🏷️ TOP-TIER VOCABULARY: 5 advanced words/collocations with meanings and IPA (for speaking).
    2. 🏗️ USEFUL STRUCTURES: 3 complex grammatical structures or sentence starters relevant to the topic.
    3. 📝 SCENARIO-BASED EXAMPLES: Provide 2 short example paragraphs applying the above vocabulary and structures.
    4. 💡 EXPERT TIPS: One critical tip for this specific skill and topic.
    
    Format using Markdown and clear headers.
    """
    return query_phi3(prompt)
