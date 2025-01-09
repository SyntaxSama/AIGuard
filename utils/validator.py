import logging
from utils.classifier import classify_prompt

def load_manipulation_rules():
    """
    Load manipulation rules from the `manipulation_rules.txt` file.
    """
    try:
        with open("manipulation_rules.txt", "r") as file:
            return [line.strip() for line in file if line.strip()]
    except FileNotFoundError:
        logging.warning("manipulation_rules.txt not found. No rules loaded.")
        return []

def check_manipulation(prompt):
    """
    Check if the prompt contains any manipulation attempts.
    """
    if not prompt.strip():
        return False

    manipulation_rules = load_manipulation_rules()
    for rule in manipulation_rules:
        if rule.lower() in prompt.lower():
            logging.info(f"Manipulation rule triggered: {rule}")
            return True
    return False

def validate_prompt(prompt, settings):
    """
    Validate the prompt based on manipulation rules and classification.
    """
    if not prompt.strip():
        logging.info("Empty prompt detected. Marked as safe.")
        return True, "Prompt is safe."

    if settings.get("features", {}).get("personality_alignment_check", False):
        if check_manipulation(prompt):
            if settings.get("security", {}).get("block_manipulation_attempts", False):
                logging.warning("Manipulation attempt detected.")
                return False, "Manipulation attempt detected."

    if settings.get("features", {}).get("ethical_compliance_check", False):
        classification = classify_prompt(prompt)
        logging.info(f"Classification result: {classification}")
        if classification == "toxic":
            if settings.get("security", {}).get("block_malicious_prompts", False):
                logging.warning("Malicious prompt detected.")
                return False, "Malicious prompt detected."

    logging.info("Prompt is safe.")
    return True, "Prompt is safe."