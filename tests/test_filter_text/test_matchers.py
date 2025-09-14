import pytest

from src.valuelens.filter_text.matchers import (
    HAS_SPACY,
    RegexMatcher,
    SpacyMatcher,
)


class TestRegexMatcher:
    def test_simple_match(self):
        matcher = RegexMatcher()
        assert matcher.contains("Our mission is clear", ["mission"])

    def test_doesnt_catch_sub_words(self):
        matcher = RegexMatcher()
        assert not matcher.contains("Reducing emissions is key", ["mission"])

    def test_case_insensitivity(self):
        matcher = RegexMatcher()
        assert matcher.contains("Our Mission is clear", ["mission"])


@pytest.mark.skipif(
    not HAS_SPACY,  # checks if spaCy models loaded
    reason="Spacy models not installed. Install with `uv sync --extra spacy`",
)
class TestSpaCyMatcher:
    @pytest.fixture()
    def matcher(self):
        return SpacyMatcher()

    def test_simple_match(self, matcher):
        assert matcher.contains("Our mission is growth", ["mission"])

    def test_doesnt_catch_sub_words(self, matcher):
        assert not matcher.contains("CO2 emissions reduction", ["mission"])

    def test_works_with_polish_lang(self, matcher):
        assert matcher.contains("Nasza misją są innowacja i rozwój", ["misja"])
        assert not matcher.contains("emisja CO2 jest problemem", ["misja"])
