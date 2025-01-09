import ollama
import logging

def classify_prompt(prompt):
    """
    Classify a prompt as 'non-toxic' or 'toxic'.
    """
    logging.info(f"Classifying prompt: {prompt}")
    
    try:
        response = ollama.generate(
            model="Llama3.2",
            prompt=f"""
            You are a content moderation system. Your task is to classify the following prompt as 'safe' or 'malicious'.
            - If the prompt is harmless, respond with 'safe'.
            - If the prompt contains harmful, unethical, or malicious content, respond with 'malicious'.
            Prompt: {prompt}
            Response (one word only): 
            """,
        )
        
        logging.info(f"Classifier raw response: {response}")
        
        result = response["response"].strip().lower()
        logging.info(f"Classification result: {result}")
        
        if result not in ["safe", "malicious"]:
            logging.warning(f"Ambiguous classifier response: {result}. Defaulting to 'non-toxic'.")
            return "non-toxic"
        
        return "non-toxic" if result == "safe" else "toxic"
    except Exception as e:
        logging.error(f"Error classifying prompt: {e}. Defaulting to 'non-toxic'.")
        return "non-toxic"