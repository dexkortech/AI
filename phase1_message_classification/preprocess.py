import re

def clean_text(text: str) -> str:
    """Removes special characters, extra spaces, and converts to lowercase."""
    text = re.sub(r"[^a-zA-Z0-9@?.!,']", " ", text)  # Keep necessary symbols
    text = re.sub(r"\s+", " ", text).strip()  # Remove extra spaces
    return text.lower()
