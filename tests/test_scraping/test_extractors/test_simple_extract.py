from unittest.mock import patch

import pytest

from src.valuelens.scraping.extractors.simple_extract import extract_text


def test_extract_text_successful_response():
    """Should return extracted text when HTML is available."""
    with patch(
        "src.valuelens.scraping.extractors.simple_extract.fetch_html",
        return_value="<html><body><p>Our mission is innovation.</p></body></html>",
    ):
        result = extract_text("https://fake-url.com")

    assert result == ["Our mission is innovation."]


def test_extract_text_no_html():
    """Should return None if fetch_html returns None."""
    with patch("src.valuelens.scraping.extractors.simple_extract.fetch_html", return_value=None):
        result = extract_text("https://fake-url.com")

    assert result is None


@pytest.mark.skip("Integration test – requires internet connection")
def test_extract_text_real_site():
    """Optional integration test against a real site."""
    result = extract_text("https://www.openai.com/about")
    assert result is None or "OpenAI" in "\n".join(result)
