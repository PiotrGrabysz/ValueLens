from src.valuelens.filter_text.text_analyzer import TextAnalyzer
from src.valuelens.schemas import Paragraph


def test_text_analyzer_with_regex():
    analyzer = TextAnalyzer()  # defaults to RegexMatcher
    paragraphs = [
        Paragraph(
            "Our mission is clear and it is all about our customer ...",
            "https://example.com/about-us",
        ),
        Paragraph(
            "CO2 emissions reduction is key to enable sustainable growth ...",
            "https://example.com/about-us",
        ),
    ]
    filtered = analyzer.filter_relevant(paragraphs, ["mission"])
    assert len(filtered) == 1
    assert filtered[0].text.startswith("Our mission is clear")


def test_text_analyzer_excludes_short_text():
    analyzer = TextAnalyzer()  # defaults to RegexMatcher
    paragraphs = [
        Paragraph(
            "Mission",
            "https://example.com/about-us",
        ),
    ]
    filtered = analyzer.filter_relevant(paragraphs, ["mission"])
    assert len(filtered) == 0
