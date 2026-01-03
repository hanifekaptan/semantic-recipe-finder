"""Utility functions for data normalization."""

from typing import List, Any


def normalize_to_list(value: Any) -> List[str]:
    """Convert various input types to a list of strings.
    
    Handles None, lists, strings (with delimiter splitting),
    and other types by converting to string.
    
    Args:
        value: Input value to normalize
        
    Returns:
        List of string values
    """
    if value is None:
        return []
    if isinstance(value, list):
        return [str(x) for x in value]
    if isinstance(value, (str,)):
        if "|" in value:
            return [v.strip() for v in value.split("|") if v.strip()]
        if "," in value:
            return [v.strip() for v in value.split(",") if v.strip()]
        return [value]
    try:
        return [str(value)]
    except Exception:
        return []
