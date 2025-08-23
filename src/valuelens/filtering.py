"""Filtering logic to find mission/values-related paragraphs."""

KEYWORDS_ENG = ["mission", "vision", "values", "purpose", "about us", "who we are"]
KEYWORDS_PL = ["misja", "wizja", "wartości", "cel", "o nas", "kim jesteśmy"]
KEYWORDS = KEYWORDS_ENG + KEYWORDS_PL


def filter_relevant(text: str) -> list[str]:
    """Filter text into relevant paragraphs based on keywords.

    Websites might be in both English and Polish, so it searches for keywords in both languages.

    Args:
        text: Extracted raw text from the website.

    Returns:
        List of relevant paragraphs containing keywords.
    """
    paragraphs = [p.strip() for p in text.split("\n") if len(p.strip()) > 50]
    return [p for p in paragraphs if any(keyword in p.lower() for keyword in KEYWORDS)]
