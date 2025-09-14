import re
from abc import ABC, abstractmethod
from collections.abc import Iterable

try:
    import spacy
    from langdetect import detect

    HAS_SPACY = True
except ImportError:
    HAS_SPACY = False


class KeywordMatcher(ABC):
    """Abstract base for keyword matchers."""

    @abstractmethod
    def contains(self, text: str, keywords: Iterable[str]) -> bool:
        """Return True if text contains any of the keywords."""
        ...


class RegexMatcher(KeywordMatcher):
    """Simple regex-based keyword matcher."""

    def contains(self, text: str, keywords: Iterable[str]) -> bool:
        for kw in keywords:
            pattern = r"\b" + re.escape(kw.lower()) + r"\b"
            if re.search(pattern, text.lower()):
                return True
        return False


class SpacyMatcher(KeywordMatcher):
    """Lemmatization-aware keyword matcher with spaCy."""

    def __init__(self) -> None:
        if not HAS_SPACY:
            raise RuntimeError(
                "SpacyMatcher requires spaCy and langdetect. "
                "Install with `uv sync --extra spacy`."
            )

        self.nlp_en = spacy.load("en_core_web_sm")
        self.nlp_pl = spacy.load("pl_core_news_sm")

    def contains(self, text: str, keywords: Iterable[str]) -> bool:
        lang = detect(text)
        nlp = self.nlp_en if lang == "en" else self.nlp_pl
        doc = nlp(text)

        lemmas = {token.lemma_.lower() for token in doc}
        for kw in keywords:
            if kw in lemmas:
                return True
        return False
