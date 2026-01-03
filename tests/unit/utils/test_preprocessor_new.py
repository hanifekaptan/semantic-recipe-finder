"""Unit tests for text preprocessing utilities."""

import pytest
from app.utils.data_preprocessor import clean_text


def test_clean_text_basic():
    """Should lowercase and normalize whitespace."""
    assert clean_text(" Hello  WORLD ") == "hello world"


def test_clean_text_removes_digits():
    """Should remove all digits."""
    assert clean_text("recipe123 with 456 ingredients") == "recipe with ingredients"


def test_clean_text_removes_punctuation():
    """Should remove punctuation marks."""
    assert clean_text("Hello, World! How's it going?") == "hello world hows it going"


def test_clean_text_removes_underscores():
    """Should remove underscores."""
    assert clean_text("snake_case_variable") == "snakecasevariable"


def test_clean_text_normalizes_whitespace():
    """Should normalize multiple spaces to single space."""
    assert clean_text("too    many     spaces") == "too many spaces"


def test_clean_text_empty_string():
    """Empty string should return empty string."""
    assert clean_text("") == ""


def test_clean_text_none():
    """None input should return empty string."""
    assert clean_text(None) == ""


def test_clean_text_only_punctuation():
    """String with only punctuation should return empty string."""
    assert clean_text("!!??,.;") == ""


def test_clean_text_only_digits():
    """String with only digits should return empty string."""
    assert clean_text("123456") == ""


def test_clean_text_mixed_content():
    """Should handle mixed content correctly."""
    text = "Recipe #42: Pasta-Carbonara (with 5 ingredients)!"
    expected = "recipe pastacarbonara with ingredients"
    assert clean_text(text) == expected


def test_clean_text_unicode_characters():
    """Should handle unicode characters."""
    result = clean_text("café naïve")
    assert "caf" in result or "cafe" in result
