import regex as re
import unicodedata
import string
from typing import List

# precompute translator and regex patterns for performance
_TRANSLATOR = str.maketrans('', '', string.punctuation.replace('.', ''))  # keep dots
_PAT_ALPHA_DIGIT = re.compile(r'(?<=[A-Za-z])(?=\d)')
_PAT_DIGIT_ALPHA = re.compile(r'(?<=\d)(?=[A-Za-z])')
_PAT_SPACES = re.compile(r'\s+')


def to_lower(text: str) -> str:
    """
    Converts the input text to lowercase.

    Args:
        text (str): Input string.
    Returns:
        str: Lowercased string. Returns an empty string if input is not str.
    """
    return text.lower() if isinstance(text, str) else ""

def normalize_unicode(text: str) -> str:
    """
    Normalizes unicode characters in the input text using NFKD normalization
    and removes accents (diacritics).

    Args:
        text (str): Input string.
    Returns:
        str: Normalized string without accents. Returns an empty string if input is not str.
    """
    if not isinstance(text, str):
        return ""
    text = unicodedata.normalize('NFKD', text)
    text = ''.join(c for c in text if unicodedata.category(c) != 'Mn')
    return text

def remove_punctuation(text: str) -> str:
    """
    Removes punctuation and special characters from the input text, but keeps spaces between words and numbers.

    Args:
        text (str): Input string.
    Returns:
        str: String without punctuation. Returns an empty string if input is not str.
    """
    if not isinstance(text, str):
        return ""

    # remove punctuation except dots (kept for decimals and abbreviations)
    text = text.translate(_TRANSLATOR)

    # ensure separation between letters and digits (e.g. 'Egg2' -> 'Egg 2')
    text = _PAT_ALPHA_DIGIT.sub(' ', text)
    text = _PAT_DIGIT_ALPHA.sub(' ', text)

    return text

def remove_extra_spaces(text: str) -> str:
    """
    Collapses multiple spaces into a single space and trims leading/trailing spaces.

    Args:
        text (str): Input string.
    Returns:
        str: Cleaned string with single spaces. Returns an empty string if input is not str.
    """
    return _PAT_SPACES.sub(' ', text).strip() if isinstance(text, str) else ""

def clean_text(text: str) -> str:
    """
    Applies a standard text preprocessing pipeline to user input:
        - Converts to lowercase
        - Normalizes unicode characters
        - Removes punctuation and special characters
        - Collapses multiple spaces

    Args:
        text (str): Raw user input string.
    Returns:
        str: Cleaned and standardized string.
    """
    text = to_lower(text)
    text = normalize_unicode(text)
    text = remove_punctuation(text)
    text = remove_extra_spaces(text)
    return text
