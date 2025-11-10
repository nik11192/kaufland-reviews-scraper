import re

def clean_text(text: str) -> str:
    """Normalize whitespace and strip unwanted characters."""
    if not text:
        return ""
    text = re.sub(r"\s+", " ", text)
    return text.strip()