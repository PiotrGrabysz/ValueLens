import pytest

from src.valuelens.filtering import filter_relevant, is_relevant
from src.valuelens.schemas import Paragraph


def test_filter_text_with_keywords_returns_non_empty_list(sample_paragraphs):
    """Should return paragraphs containing mission/values."""
    relevant = filter_relevant(sample_paragraphs)
    assert relevant


def test_filter_text_with_keywords_returns_list_containing_keywords(sample_paragraphs):
    """Should return paragraphs containing mission/values."""
    relevant = filter_relevant(sample_paragraphs)
    assert "mission" in relevant[0].text


def test_filter_text_without_keywords():
    """Should return empty list if no keywords present."""
    text = "This is a generic description with no keywords."
    assert not is_relevant(text)


def test_filter_text_less_than_50_characters():
    """Filter out very short lines, even they contain keywords"""
    text = "We have values"
    assert not is_relevant(text)


@pytest.fixture
def sample_paragraphs() -> list[Paragraph]:
    """Return example extracted text for testing."""
    source = "https://example-corp.com"
    return [
        Paragraph("Welcome to ExampleCorp!", source),
        Paragraph(
            "Our mission is to build a better digital future. We value integrity, innovation, "
            "and collaboration. In 2021, we launched several new products...",
            source,
        ),
    ]
