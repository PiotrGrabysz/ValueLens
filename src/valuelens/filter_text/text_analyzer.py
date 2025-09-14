from collections.abc import Iterable

from src.valuelens.schemas import Paragraph

from .matchers import KeywordMatcher, RegexMatcher

KEYWORDS_ENG = {"mission", "vision", "values", "value", "purpose"}
KEYWORDS_PL = {"misja", "wizja", "wartość", "cel"}
KEYWORDS = KEYWORDS_ENG.union(KEYWORDS_PL)


class TextAnalyzer:
    """Runs keyword-based analysis using a pluggable matcher."""

    def __init__(self, matcher: KeywordMatcher | None = None) -> None:
        self.matcher = matcher or RegexMatcher()

    def filter_relevant(
        self, paragraphs: list[Paragraph], keywords: Iterable[str] | None = None
    ) -> list[Paragraph]:
        """Return only paragraphs that match the given keywords."""
        if keywords is None:
            keywords = KEYWORDS
        return [p for p in paragraphs if self.is_relevant(p.text, keywords)]

    def is_relevant(self, text: str, keywords: Iterable[str]) -> bool:
        return self.matcher.contains(text, keywords) and len(text.strip()) > 50
