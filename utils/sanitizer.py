import re

def sanitize_input(prompt):
    prompt = re.sub(r"[^\w\s]", "", prompt)
    return prompt.strip()