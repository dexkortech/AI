import re
from .config import bedrock_client
from botocore.exceptions import ClientError
from .preprocess import clean_text
import json
from dotenv import load_dotenv
import os

# load environment variables
load_dotenv()

def is_question(message: str) -> bool:
    """Detects if the message is a question."""
    question_words = ["who", "what", "when", "where", "why", "how", "can", "does", "is", "are", "do"]
    return any(message.lower().startswith(word) for word in question_words) or message.strip().endswith("?")

def contains_mention(message: str, bot_name: str = "@bot") -> bool:
    """Checks if the bot is mentioned in the message."""
    return bot_name.lower() in message.lower()

def keyword_match(message: str) -> bool:
    """Checks if the message contains predefined AI-relevant keywords."""
    keywords = ["help", "define", "weather", "support", "assist"]
    return any(keyword in message.lower() for keyword in keywords)

def rule_based_classification(message: str) -> bool:
    """Applies rule-based logic to determine if AI should respond."""
    return is_question(message) or contains_mention(message) or keyword_match(message)

def classify_with_llm(message: str) -> bool:
    # Construct the LLM prompt
    prompt = f"""<s>[INST] <<SYS>>
    You are an AI assistant that determines whether a message in a group chat requires an AI response. 
    Follow these strict rules:

    1. If the message contains a direct **question** (e.g., starts with "Who", "What", "When", "How", "Why", "Can you"), return "yes - direct question".
    2. If the message **mentions** the chatbot explicitly (e.g., "@bot help"), return "yes - chatbot mentioned".
    3. If the message contains **keywords** like "help", "define", "weather", "support", or "assist", return "yes - relevant keyword detected".
    4. If the message **requests a definition or explanation** (e.g., "Tell me the definition of X" or "Explain X"), return "yes - definition request".
    5. If the message **asks for general information or an enquiry**, return "yes - general enquiry".
    6. If the message is **casual conversation** or **small talk** (e.g., "Hey, how's it going?"), return "no - small talk detected".
    7. If the message is a **statement** (not a question and not relevant to AI), return "no - general statement".
    8. If the message is **ambiguous** and you are unsure, return "no - uncertain classification".

    Message: "{message}" 
    Should AI respond? [/INST]"""


    # Create request body
    body = json.dumps({
            "prompt": prompt,
            "max_tokens": 1,
            "temperature": 0.3
    })
    
    try:
        response = bedrock_client.invoke_model(body=body, modelId=os.getenv("CLASSIFICATION_MODEL_ID"))
        response_body = json.loads(response.get("body").read())

        generated_text = response_body.get("outputs", "")[0]["text"].strip().lower()

        # Return True if the LLM confirms an AI response is needed
        return generated_text == "yes"

    except Exception as err:
        print(f"Error invoking model: {err}")
        return False  

def hybrid_classification(message: str) -> bool:
    """Uses rule-based logic first, then falls back to LLM if uncertain."""
    message = clean_text(message)  # Preprocess message
    if rule_based_classification(message):
        return True
    return classify_with_llm(message)
