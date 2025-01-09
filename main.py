import yaml
import logging
from utils.sanitizer import sanitize_input
from utils.classifier import classify_prompt
from utils.validator import validate_prompt

with open("settings.yml", "r") as file:
    settings = yaml.safe_load(file)

logging_config = settings.get("logging", {})
logging.basicConfig(
    level=logging_config.get("log_level", "INFO").upper(),
    filename=logging_config.get("log_file", "prompt_guard.log"),
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

def log_message(message, level="INFO"):
    """
    Log a message to the log file.
    """
    if settings["features"].get("logging", False):
        logging.log(getattr(logging, level.upper()), message)

def process_prompt(prompt):
    """
    Process a user prompt: sanitize, classify, validate, and generate a response.
    """
    if settings["features"].get("input_sanitization", False):
        prompt = sanitize_input(prompt)
        log_message(f"Sanitized prompt: {prompt}")

    if settings["features"].get("prompt_classification", False):
        classification_result = classify_prompt(prompt)
        log_message(f"Classification result: {classification_result}")

    if settings["features"].get("personality_alignment_check", False) or settings["features"].get("ethical_compliance_check", False):
        is_valid, message = validate_prompt(prompt, settings)
        if not is_valid:
            log_message(f"Blocked prompt: {message}", level="WARNING")
            return f"Blocked: {message}"

    response = "This is a safe response."
    log_message(f"Generated response: {response}")

    if settings["features"].get("response_validation", False):
        is_valid, message = validate_prompt(response, settings)
        if not is_valid:
            log_message(f"Blocked response: {message}", level="WARNING")
            return f"Blocked: {message}"

    return response

def main():
    """
    Main function to interactively validate prompts.
    """
    logging.info("AI Prompt Guard System started.")

    while True:
        prompt = input("Enter a prompt (or type 'exit' to quit): ").strip()

        if prompt.lower() == "exit":
            logging.info("Exiting AI Prompt Guard System.")
            break

        response = process_prompt(prompt)

        print(response)

if __name__ == "__main__":
    main()