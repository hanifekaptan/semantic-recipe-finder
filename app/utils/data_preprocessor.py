"""Text preprocessing utilities for search queries."""

import re


def clean_text(text: str) -> str:
    """Clean and normalize text for semantic search.
    
    Applies lowercase conversion, removes digits, punctuation, underscores,
    and normalizes whitespace.
    
    Args:
        text: Raw text to clean
        
    Returns:
        Cleaned text string
    """
    if not text:
        return ""
    t = text.lower()
    t = re.sub(r"\d+", "", t)
    t = re.sub(r"[^\w\s]", "", t)
    t = re.sub(r"_+", "", t)
    t = re.sub(r"\s+", " ", t).strip()
    return t
