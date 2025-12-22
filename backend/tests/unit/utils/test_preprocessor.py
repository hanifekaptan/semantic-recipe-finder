from app.utils.data_preprocessor import clean_text

def test_clean_text_basic():
    s = "  Hello, WORLD!!\n"
    out = clean_text(s)
    assert "hello" in out
    assert "world" in out
    assert "\n" not in out

def test_clean_empty():
    assert clean_text("") == ""
    assert clean_text(None) == ""
