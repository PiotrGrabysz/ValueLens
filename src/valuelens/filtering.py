"""Filtering logic to find mission/values-related paragraphs."""

from src.valuelens.schemas import Paragraph

KEYWORDS_ENG = {"mission", "vision", "values", "purpose", "about us", "who we are"}
KEYWORDS_PL = {"misja", "wizja", "wartości", "cel", "o nas", "kim jesteśmy"}
KEYWORDS = KEYWORDS_ENG.union(KEYWORDS_PL)


def filter_relevant(paragraphs: list[Paragraph]) -> list[Paragraph]:
    """Filter text into relevant paragraphs based on keywords.

    Websites might be in both English and Polish, so it searches for keywords in both languages.

    Args:
        paragraphs: Extracted raw text from the website.

    Returns:
        List of relevant paragraphs containing keywords.
    """
    return [p for p in paragraphs if is_relevant(p.text)]


def is_relevant(text: str) -> bool:
    return contains_keyword(text) and len(text.strip()) > 50


def contains_keyword(text: str) -> bool:
    return any(keyword in text.lower() for keyword in KEYWORDS)
