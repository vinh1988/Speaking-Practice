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
    prompt = f"""
    You are an IELTS {skill_type} examiner. The topic is '{topic}' and the context is '{context}'.
    {'This is for ' + sub_index if sub_index else ''}
    {'The user uploaded an image described as: ' + image_description if image_description else ''}
    
    TASK:
    1. Generate a natural IELTS-style {skill_type} question.
    2. Provide a "Knowledge Bank" (Preparation guide) in BOTH English and Vietnamese.
    
    FORMAT YOUR RESPONSE EXACTLY LIKE THIS:
    
    ### QUESTION
    [The question text here]

    ### KNOWLEDGE BANK (Preparation)
    #### 🏷️ Vocabulary & Idioms (Từ vựng & Thành ngữ)
    * **English Term** (IPA) - Vietnamese Meanings
    * ... (Provide 3 key terms)

    #### 🏗️ Useful Phrases (Cấu trúc hữu ích)
    * **Phrase** - Vietnamese Context/Meaning
    * ... (Provide 2 phrases)

    #### 💡 5W1H Planning (Gợi ý ý tưởng)
    * **Who/What**: [English advice] - [Vietnamese advice]
    * **Where/When**: [English advice] - [Vietnamese advice]
    * **Why/How**: [English advice] - [Vietnamese advice]
    """
    
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
    You are an IELTS tutor. Create a high-quality BILINGUAL (English and Vietnamese) Preparation Sheet for:
    Topic: '{topic}'
    Skill: '{skill_type}'
    
    Structure:
    1. 🏷️ TOP-TIER VOCABULARY: 5 advanced words/collocations with Vietnamese meanings and IPA.
    2. 🏗️ USEFUL STRUCTURES: 3 complex models with Vietnamese translations/explanations.
    3. 📝 SCENARIO-BASED EXAMPLES: 2 short paragraphs in English with brief Vietnamese summaries.
    4. 💡 5W1H ADVICE: Planning tips in both languages.
    
    Format using Markdown.
    """
    return query_phi3(prompt)
