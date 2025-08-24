import pytest

from src.valuelens.filtering import filter_relevant


def test_filter_text_with_keywords_returns_non_empty_list(sample_text):
    """Should return paragraphs containing mission/values."""
    relevant = filter_relevant(sample_text)
    assert relevant


def test_filter_text_with_keywords_returns_list_containing_keywords(sample_text):
    """Should return paragraphs containing mission/values."""
    relevant = filter_relevant(sample_text)
    assert "mission" in relevant[0]


def test_filter_text_without_keywords():
    """Should return empty list if no keywords present."""
    text = "This is a generic description with no keywords."
    relevant = filter_relevant(text)
    assert relevant == []


def test_filter_text_less_than_50_characters():
    """Filter out very short lines, even they contain keywords"""
    text = (
        "We have values\n"
        "This is a much longer line but it doesn't contain any matching keywords."
    )
    assert not filter_relevant(text)


@pytest.fixture
def sample_text() -> str:
    """Return example extracted text for testing."""
    return (
        "Welcome to ExampleCorp!\n"
        "Our mission is to build a better digital future. We value integrity, innovation, and collaboration."
        "In 2021, we launched several new products..."
    )
